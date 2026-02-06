FROM node:22-bookworm

# Install Bun (required for build scripts)
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

RUN corepack enable

WORKDIR /app

ARG OPENCLAW_DOCKER_APT_PACKAGES=""
RUN if [ -n "$OPENCLAW_DOCKER_APT_PACKAGES" ]; then \
      apt-get update && \
      DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends $OPENCLAW_DOCKER_APT_PACKAGES && \
      apt-get clean && \
      rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*; \
    fi

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY ui/package.json ./ui/package.json
COPY patches ./patches
COPY scripts ./scripts

RUN pnpm install --frozen-lockfile

COPY openclaw.json ./openclaw.json
COPY . .
RUN OPENCLAW_A2UI_SKIP_MISSING=1 pnpm build
# Force pnpm for UI build (Bun may fail on ARM/Synology architectures)
ENV OPENCLAW_PREFER_PNPM=1
RUN pnpm ui:build

ENV NODE_ENV=production

# Allow non-root user to write temp files during runtime/tests.
RUN chown -R node:node /app

# Create .openclaw directory, copy config and workspace files
RUN mkdir -p /home/node/.openclaw/workspace && \
    cp /app/openclaw.json /home/node/.openclaw/openclaw.json && \
    if [ -d /app/workspace ]; then cp -r /app/workspace/* /home/node/.openclaw/workspace/; fi && \
    chown -R node:node /home/node/.openclaw

# Pre-create /data for Railway persistent volume mount
RUN mkdir -p /data && chown -R node:node /data

# Install gosu for secure user switching at runtime
RUN apt-get update && apt-get install -y --no-install-recommends gosu && \
    rm -rf /var/lib/apt/lists/*

# Start gateway: fix volume permissions then switch to node user
# Railway mounts volumes as root after container build, so we fix perms at runtime
CMD ["sh", "-c", "chown -R node:node /data 2>/dev/null; exec gosu node node dist/index.js gateway --allow-unconfigured --bind lan"]



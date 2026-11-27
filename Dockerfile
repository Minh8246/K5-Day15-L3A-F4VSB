FROM node:22-bookworm-slim AS build
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /app/web
COPY web/package.json web/package-lock.json ./
RUN npm ci
COPY web/app/ ./app/
COPY web/lib/ ./lib/
COPY web/next.config.mjs ./
RUN npm run build && npm prune --omit=dev

FROM node:22-bookworm-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates python3 \
    && rm -rf /var/lib/apt/lists/*
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app/web
COPY --from=build /app/web/node_modules/ ./node_modules/
COPY --from=build --chown=node:node /app/web/.next/ ./.next/
COPY --chmod=644 web/package.json web/next.config.mjs web/analyze_sms.py ./
COPY --chmod=u=rwX,go=rX codebase/ /app/codebase/
COPY --chmod=u=rwX,go=rX data/ /app/data/
USER node
EXPOSE 8080
CMD ["node", "node_modules/next/dist/bin/next", "start", "--hostname", "0.0.0.0", "--port", "8080"]

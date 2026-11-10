# syntax=docker/dockerfile:1

# ---- deps: installs packages from the lock file -----------------------------
FROM node:22-slim AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# ---- dev: code is mounted from the host, Vite reloads on change -------------
FROM deps AS dev
CMD ["npm", "run", "dev"]

# ---- build: type check, tests and the static files --------------------------
FROM deps AS build
COPY . .
RUN npm run typecheck && npm test && npm run build

# ---- production: nginx serves the files and forwards /api ------------------
FROM nginxinc/nginx-unprivileged:1.29-alpine AS production
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080

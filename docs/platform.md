# Backing Platform — Postiz

`postiz-agent` is a **client** of a [Postiz](https://postiz.com/) instance. You can
point it at the managed service, or deploy a self-hosted instance with the recipe
below to serve as the target of `POSTIZ_URL`. For production topologies, follow the
upstream [Postiz documentation](https://docs.postiz.com/).

!!! note "Backing-system recipe"
    Each connector in the ecosystem follows the same convention — a
    `docs/platform.md` recipe for the system it integrates with, accompanied by a
    sample Compose stack that mirrors [`services/`](https://github.com/Knuckles-Team).
    Systems offered only as a managed service have no local recipe.

## Single-node deployment (Compose)

Postiz publishes the `ghcr.io/gitroomhq/postiz-app` image and requires Postgres and
Redis. The following stack runs one Postiz instance with its data services:

```yaml
# docker/postiz-platform.compose.yml
services:
  postiz:
    image: ghcr.io/gitroomhq/postiz-app@sha256:<digest>
    container_name: postiz
    restart: unless-stopped
    environment:
      MAIN_URL: "http://postiz.example.invalid"            # your local DNS or IP
      FRONTEND_URL: "http://postiz.example.invalid"
      NEXT_PUBLIC_BACKEND_URL: "http://postiz.example.invalid/api"
      JWT_SECRET: "${POSTIZ_JWT_SECRET}"   # provide a unique random string via the environment
      DATABASE_URL: "postgresql://postiz-user:postiz-password@postiz-postgres:5432/postiz-db-local"
      REDIS_URL: "redis://postiz-redis:6379"
      BACKEND_INTERNAL_URL: "http://localhost:3000"
      IS_GENERAL: "true"
      STORAGE_PROVIDER: "local"
      UPLOAD_DIRECTORY: "/uploads"
      NEXT_PUBLIC_UPLOAD_DIRECTORY: "/uploads"
    ports:
      - "5000:5000"
    volumes:
      - postiz-config:/config/
      - postiz-uploads:/uploads/
    depends_on:
      - postiz-postgres
      - postiz-redis

  postiz-postgres:
    image: postgres:17-alpine
    container_name: postiz-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postiz-user
      POSTGRES_PASSWORD: postiz-password
      POSTGRES_DB: postiz-db-local
    volumes:
      - postiz-postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postiz-user -d postiz-db-local"]
      interval: 10s
      timeout: 3s
      retries: 3

  postiz-redis:
    image: redis@sha256:<digest>
    container_name: postiz-redis
    restart: unless-stopped
    volumes:
      - postiz-redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

volumes:
  postiz-config:
  postiz-uploads:
  postiz-postgres-data:
  postiz-redis-data:
```

```bash
docker compose -f docker/postiz-platform.compose.yml up -d

# Postiz UI is then available on port 5000; create an account and an API token
```

Generate an API token from the Postiz settings, then point the connector at the
instance.

## Connect postiz-agent

```bash
export POSTIZ_URL=http://postiz.example.invalid/public/v1     # instance API base
export POSTIZ_TOKEN=<runtime-secret>                 # token from the Postiz UI
export TLS_PROFILE=private-pki
export TLS_PROFILES_REF=secret://runtime/tls-profiles

postiz-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

## Combined deployment

A combined stack places Postiz and the MCP server on one Docker network, so the
connector reaches Postiz by container name:

```yaml
# docker/stack.compose.yml
services:
  postiz:
    image: ghcr.io/gitroomhq/postiz-app@sha256:<digest>
    ports: ["5000:5000"]
    environment:
      DATABASE_URL: "postgresql://postiz-user:postiz-password@postiz-postgres:5432/postiz-db-local"
      REDIS_URL: "redis://postiz-redis:6379"
      IS_GENERAL: "true"
    depends_on: [postiz-postgres, postiz-redis]

  postiz-postgres:
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: postiz-user
      POSTGRES_PASSWORD: postiz-password
      POSTGRES_DB: postiz-db-local

  postiz-redis:
    image: redis@sha256:<digest>

  postiz-agent-mcp:
    image: example/postiz-agent@sha256:<digest>
    depends_on: [postiz]
    environment:
      - POSTIZ_URL=http://postiz:5000/public/v1
      - POSTIZ_TOKEN=${POSTIZ_TOKEN:?required}
      - TRANSPORT=streamable-http
      - HOST=0.0.0.0
      - PORT=8000
    ports: ["8000:8000"]
```

```bash
docker compose -f docker/stack.compose.yml up -d
```

Once the instance is reachable, the [MCP tools and `PostizApi`](usage.md) operate
against your channels, posts, uploads, and analytics.

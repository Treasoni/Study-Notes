---
url: "https://raw.githubusercontent.com/misskey-dev/misskey/develop/.config/docker_example.env"
scraped_at: 2026-09-15T12:30:21+00:00
---


```
# misskey settings
# MISSKEY_URL=https://example.tld/

# db settings
POSTGRES_PASSWORD=example-misskey-pass
# DATABASE_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_USER=example-misskey-user
# DATABASE_USER=${POSTGRES_USER}
POSTGRES_DB=misskey
# DATABASE_DB=${POSTGRES_DB}
DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"

```


# Sanitized fixture: note-update-patch

Stable, non-sensitive input profile for the note-updater request group.

```yaml
note_path: docker/README.md
stale_sections:
  - 安装步骤
  - 版本对比
new_sources:
  - fixtures/note-update-patch.md
scope: local-patch-only
```

Representative of a single-note partial update. No real user data.

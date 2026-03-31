# MEMORY.md

## OpenClaw browser automation baseline

- On this Ubuntu machine, the stable browser-control path is **Chromium + remote CDP + OpenClaw browser profile `user`**, not `existing-session` auto-attach.
- Reliable restart sequence:
  1. `openclaw gateway start` (or restart)
  2. `/snap/bin/chromium --user-data-dir=/home/hag/snap/chromium/common/chromium --remote-debugging-port=9222`
  3. Verify with `openclaw browser status` and `openclaw browser tabs`
- OpenClaw browser config should point `browser.profiles.user.cdpUrl` to `http://127.0.0.1:9222`.

## Xiaohongshu automation lesson

- Small Red Book detail pages are unstable if treated as simple static links.
- The durable approach is:
  - parse result-page DOM,
  - prefer `/search_result/<id>?...` wrapper links,
  - fall back to `/explore/<id>`,
  - validate detail-page success using title/author/body/comments,
  - record failures by type instead of pretending success.
- For note extraction, DOM/evaluate is more reliable than snapshot alone.

## GitHub repo + auth baseline

- Private GitHub repo created for OpenClaw config/workspace: `openclaw-next-level` under `HuangR0ngHa0`.
- Git remote now uses SSH: `git@github.com:HuangR0ngHa0/openclaw-next-level.git`.
- SSH auth to GitHub is working on this machine.

## Repo hygiene rule

- Keep tracked template files in git:
  - `IDENTITY.template.md`
  - `USER.template.md`
  - `TOOLS.template.md`
- Keep local real files out of git:
  - `IDENTITY.md`
  - `USER.md`
  - `TOOLS.md`
- `.openclaw/` should stay ignored.

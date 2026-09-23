#!/usr/bin/env bash
# Lane B #300 — capture what a CLEAN Claude Code CLI sends at boot, with no model call.
# A local HTTP server stands in for the API, records the first /v1/messages body, answers 400.
# env -i strips every cloud-session variable, so this is the plain CLI (API-key mode: no claude.ai
# login, so no synced skills, no Artifact tool, no claude.ai connectors). Run in the cloud container.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; W="$(mktemp -d)"; PORT=18779
mkdir -p "$W/out" "$W/cfg" "$W/home" "$W/proj"; (cd "$W/proj" && git init -q .)
python3 "$HERE/capsrv.py" $PORT "$W/out" & SRV=$!; sleep 1
( cd "$W/proj" && env -i PATH=/opt/node22/bin:/usr/local/bin:/usr/bin:/bin HOME="$W/home" CLAUDE_CONFIG_DIR="$W/cfg" \
  ANTHROPIC_BASE_URL=http://127.0.0.1:$PORT ANTHROPIC_API_KEY=sk-ant-dummy-capture NO_PROXY=127.0.0.1,localhost TERM=xterm \
  timeout 90 claude -p "hi" --output-format json < /dev/null > /dev/null 2>&1 )
kill $SRV 2>/dev/null
claude --version; python3 "$HERE/anal.py" "$(ls "$W"/out/req-*.json | head -1)"

#!/usr/bin/env bash
# GitHub の main ブランチを定期的に確認し、更新があればデプロイする（プル型デプロイ）。
# サーバ側から GitHub へ外向きに接続するだけなので、受信ポートの開放は不要。
# discord-bot-update.timer から定期実行される。
set -euo pipefail

APP_DIR="${APP_DIR:-/opt/discord-bot}"
BRANCH="${BRANCH:-main}"
SERVICE="${SERVICE:-discord-bot.service}"
PY="$APP_DIR/.venv/bin/python"

cd "$APP_DIR"

git fetch --quiet origin "$BRANCH"
LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse "origin/$BRANCH")"
if [ "$LOCAL" = "$REMOTE" ]; then
    exit 0
fi
echo "更新を検出: ${LOCAL:0:7} -> ${REMOTE:0:7}"

rollback() {
    echo "デプロイに失敗したため ${LOCAL:0:7} に戻します: $1" >&2
    git reset --quiet --hard "$LOCAL"
    "$PY" -m pip install --quiet -r requirements.txt || true
    exit 1
}

# 早送りできない（サーバ側で直接コードを変更している等）場合は何もしない
git merge --quiet --ff-only "origin/$BRANCH" || { echo "fast-forward できません。手動で確認してください。" >&2; exit 1; }

if ! git diff --quiet "$LOCAL" "$REMOTE" -- requirements.txt; then
    echo "requirements.txt が変更されたため依存関係を更新します"
    "$PY" -m pip install --quiet -r requirements.txt || rollback "pip install"
fi

# 構文エラーのあるコードで再起動しないよう、事前にコンパイル確認する
"$PY" -m py_compile bot.py cogs/*.py util/*.py database/__init__.py || rollback "構文チェック"

systemctl restart "$SERVICE"
sleep 10
systemctl is-active --quiet "$SERVICE" || {
    git reset --quiet --hard "$LOCAL"
    systemctl restart "$SERVICE"
    echo "再起動後に停止したため ${LOCAL:0:7} に戻しました" >&2
    exit 1
}
echo "デプロイ完了: ${REMOTE:0:7}"

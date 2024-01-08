#!/usr/bin/env sh
set -e

if [ "$1" = 'python' ] || [ "$1" = 'python3' ] || [ "$1" = 'uvicorn' ]; then
  chown -R app:app /usr/src/app/files
  exec gosu app "$@"
fi

exec "$@"

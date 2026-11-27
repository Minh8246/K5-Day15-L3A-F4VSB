#!/usr/bin/env bash
set -euo pipefail
umask 077

repository=https://github.com/Minh8246/K5-Day15-L3A-F4VSB.git
ci_runs=https://api.github.com/repos/Minh8246/K5-Day15-L3A-F4VSB/actions/workflows/ci.yml/runs
branch=refs/heads/deloy
project="$HOME/f4vsb"
source_git="$project/source.git"
failed="$project/failed-release"

cd "$project"
exec 9>"$project/deploy.lock"
flock -n 9 || exit 0

previous="$(readlink -e current)"
ref="$(git ls-remote --exit-code "$repository" "$branch")"
commit="${ref%%$'\t'*}"
[[ "$commit" =~ ^[0-9a-f]{40}$ ]]

if [[ "$previous" == "$project/releases/$commit" ]] || [[ -f "$failed" && "$(cat "$failed")" == "$commit" ]]; then
  exit 0
fi

if ! curl -fsS --max-time 10 "$ci_runs?branch=deloy&head_sha=$commit&event=push&status=success&per_page=1" \
  | python3 -c 'import json, sys; sys.exit(not json.load(sys.stdin)["workflow_runs"])'; then
  echo "Waiting for CI to pass on $commit."
  exit 0
fi

if [[ ! -d "$source_git" ]]; then
  git init --bare --quiet "$source_git"
fi
git --git-dir="$source_git" fetch --no-tags --depth=1 "$repository" "$branch"
if [[ "$(git --git-dir="$source_git" rev-parse FETCH_HEAD)" != "$commit" ]]; then
  echo "Branch moved during fetch. The next check will deploy the new commit."
  exit 0
fi

compose() {
  local directory="$1" image="$2"
  shift 2
  F4VSB_IMAGE="$image" docker --context rootless compose \
    --project-name f4vsb --project-directory "$directory" "$@"
}

previous_image="$(docker --context rootless inspect --format '{{.Config.Image}}' f4vsb-app-1)"
release="$project/releases/$commit"
image="f4vsb-app:$commit"
mkdir -p "$release"
git --git-dir="$source_git" archive "$commit" .dockerignore Dockerfile compose.yaml web codebase data \
  | tar -x -C "$release"
ln -sfn "$project/.env.deploy" "$release/.env.deploy"
ln -sfn "$project/.env.tunnel" "$release/.env.tunnel"

echo "Building $commit"
if ! compose "$release" "$image" build app; then
  printf '%s\n' "$commit" > "$failed"
  exit 1
fi

if compose "$release" "$image" up -d --no-deps --no-build --wait --wait-timeout 90 app \
  && ln -sfn "$release" "$project/current"; then
  echo "Deployed $commit"
else
  printf '%s\n' "$commit" > "$failed"
  echo "Release failed. Restoring $previous_image." >&2
  compose "$previous" "$previous_image" up -d --no-deps --no-build --wait --wait-timeout 90 app
  exit 1
fi

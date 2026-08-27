#!/usr/bin/env bash
set -euo pipefail

base_url="${1:-https://docs.braidkit.io}"
base_url="${base_url%/}"
page_file="$(mktemp)"
headers_file="$(mktemp)"
trap 'rm -f "$page_file" "$headers_file"' EXIT

curl --fail --silent --show-error --location \
  --max-time 20 --output "$page_file" "$base_url/"
grep --fixed-strings --quiet "Documentation is coming soon" "$page_file"

curl --fail --silent --show-error --head \
  --max-time 20 --output "$headers_file" "$base_url/"
tr -d '\r' < "$headers_file" | grep --ignore-case --quiet \
  '^x-robots-tag:.*noindex'

for path in robots.txt sitemap.xml llms.txt llms-full.txt; do
  curl --fail --silent --show-error --location \
    --max-time 20 --output /dev/null "$base_url/$path"
done

legacy_status="$(curl --silent --show-error --output /dev/null \
  --max-time 20 --write-out '%{http_code}' "$base_url/protocol/overview/")"
test "$legacy_status" = "404"

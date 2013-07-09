#!/bin/bash -u
pastebin=""
upload() {
    curl -i -s --form data="$@" -k "$pastebin" | grep '^Location' | awk '{print $2}'
}

[[ -z "$@" ]] && data=$(pbpaste)
url=$(upload "${data-}$@")
if [[ -n "$url" ]]; then
    [[ -n "$@" ]] || echo -n "$url" | pbcopy
    echo "$url"
fi

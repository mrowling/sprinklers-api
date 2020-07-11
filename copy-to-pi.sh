#!/usr/bin/env bash
SRC="$(pwd)"
DST="pi@10.0.0.15:/home/pi/Code"

rsync -ah \
    --exclude-from="$(git -C $SRC ls-files --exclude-standard -oi --directory > .git/ignores.tmp && echo .git/ignores.tmp)" \
    $SRC \
    $DST 

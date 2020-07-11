#!/usr/bin/env bash
rsync -azP --exclude '.git' --exclude-from='.gitignore' "$(pwd)" pi@10.0.0.15:/home/pi/Code/sdhc-sprinklers-api

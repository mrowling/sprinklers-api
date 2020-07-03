#!/usr/bin/env bash
cp systemd/system/sdhc-sprinklers-api.service /etc/systemd/system/sdhc-sprinklers-api.service
systemctl start sdhc-sprinklers-api
systemctl enable sdhc-sprinklers-api

#!/bin/bash

cd "$(dirname "$0")"

sudo cp ./*.service /etc/systemd/system/
sudo systemctl daemon-reload

sudo systemctl enable librespot.service
sudo systemctl enable soundsnear-rfid.service
sudo systemctl enable soundsnear-server.service

sudo systemctl restart soundsnear-server.service

sudo systemctl status soundsnear-server.service
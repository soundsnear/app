#! /bin/sh

sudo apt update

Sudo apt-get libc6 \
systemd \
libasound2 \
alsa-utils \
libpulse0 \
init-system-helpers 

# initial install
sudo apt-get -y install curl && curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

# CONFIGURE
# https://github.com/dtcooper/raspotify/wiki/Basic-Setup-Guide#run-asound-conf-wizard


# make things easier to con    
sudo apt update && sudo apt install -y --no-install-recommends libasound2-plugins

# configure output
sudo apt update && sudo apt install -y asound-conf-wizard
# Run asound-conf-wizard
sudo awiz

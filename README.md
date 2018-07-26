# Chessbots

## Intro

Prepare raspberry pi 3:

```bash
cp .env.dist .env
vi .env # insert wifi ssid and password

./scripts/prepare_pi_disk_on_osx.sh
# and follow instructions
```

Place SD Card in raspberry pi 3 and wait until device is accessable in wlan

Then run this (replace ip address, but keep the comma, it tricks ansible in thinking, we are passing as list of hosts instead of a hostsfile)

```bash
ansible-playbook ansible/prototype.yml -i 192.168.178.30 -u pi -k
# password: raspberry
```

Then login into raspberry pi 3 and initialize/startup the project

```bash
# replace ip address
ssh pi@192.168.178.30
cd /opt/chessbots/
yarn install
sudo node webserver.js
```

Then open the IP address in the browser and click buttons.

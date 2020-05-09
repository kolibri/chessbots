include .env
export

BOT_UPLOAD_DEVICE=/dev/ttyUSB0
PI_SD_CARD_DEVIDE=/dev/mmcblk0
RASPBIAN_IMG_PATH=./raspbian_lite_latest.img
RASPBIAN_ZIP_PATH=./raspbian_lite_latest.zip
RASPBIAN_DOWNLOAD_URL="https://downloads.raspberrypi.org/raspbian_lite_latest"



bot-compile:
	arduino-cli compile --fqbn esp8266:esp8266:generic src/bot

bot-upload:
	arduino-cli upload -p $(BOT_UPLOAD_DEVICE) --fqbn esp8266:esp8266:generic src/bot

bot-screen:
	screen $(BOT_UPLOAD_DEVICE) 9600

bot-install: bot-compile bot-upload bot-screen

bot-setup:
	rm -rf .arduino15
	arduino-cli core update-index
	arduino-cli core install esp8266:esp8266
	arduino-cli lib install MFRC522


download-raspian:
	curl -L -o $(RASPBIAN_ZIP_PATH) $(RASPBIAN_DOWNLOAD_URL)
	unzip -p $(RASPBIAN_ZIP_PATH) \*.img | cat > $(RASPBIAN_IMG_PATH)

server-setup-pi:
	IMAGE_PATH=$(RASPBIAN_IMG_PATH) \
	TARGET_DEVICE=$(PI_SD_CARD_DEVIDE) \
	./src/server/setup_pi.sh 

server-provision:
	ansible-playbook -u pi -i $(SERVER_IP), src/server/provision.yml

server-deploy:
	
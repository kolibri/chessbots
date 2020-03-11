BOT_UPLOAD_DEVICE=/dev/ttyUSB1

compile:
	arduino-cli compile --fqbn esp8266:esp8266:generic src/bot

upload:
	arduino-cli upload -p $(BOT_UPLOAD_DEVICE) --fqbn esp8266:esp8266:generic src/bot

setup:
	rm -rf .arduino15
	arduino-cli core update-index
	arduino-cli core install esp8266:esp8266
	arduino-cli lib install MFRC522

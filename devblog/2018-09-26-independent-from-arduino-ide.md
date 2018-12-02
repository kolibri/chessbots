# (Almost) independent from arduino ide

A lot happend!

We git a new case, build from lego: 

![lego bot](./images/legobot.png "Lego bot")

Also the code of the bot evolved a lot. It now takes sequences as JSON via a HTTP request.
The basic concept for reaction on the nfc tags also exists.

and it took a huge step to get free from the arduino ide. We currently only need to `mv /arduino15/packages ./src/bot/packages`, rest is automated, except the comitted `QueueArray` lib from arduino website.


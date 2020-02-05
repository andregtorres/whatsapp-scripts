# whatsapp-scripts
Scripts for statistics on exported WhatsApp chats

To export a chat from whatapp select send chat by email on the android app.

## Get whatsapp data
In a chat, on the phone, press `Export chat > Without media`.
Transfer to PC and remove the first 3 lines:
> sed -i 1,3d file.txt

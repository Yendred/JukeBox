# change to home folder
cd ~

#update
sudo apt -y update

# Install SSH Server
sudo apt -y install openssh-server

# Install USB Auto Mount
sudo apt -y install usbmount
# May need to edit    /etc/usbmount/usbmount.conf
#   ls -l /dev/disk/by-uuid/
#       1C87-CC63

# create folder to mount the USB (Music) drive to
#   sudo mkdir -p /mnt/usb1
#give it the appropiate permissions
#   sudo chown -R pi:pi /mnt/usb1

# Edit /etc/fstab
# https://www.shellhacks.com/raspberry-pi-mount-usb-drive-automatically/
#   Get UUID and FileSystem Type
#       lsblk -fp
#           NAME             FSTYPE LABEL  UUID                                 FSAVAIL FSUSE% MOUNTPOINT
#           /dev/sda
#           └─/dev/sda1      exfat  Music  1C87-CC63                              56.6G    53% /mnt/USBMusic
#
#
#   sudo blkid
#       /dev/sda1: LABEL="Music" UUID="1C87-CC63" TYPE="exfat" PARTUUID="44e444a8-01"


#   UUID=1C87-CC63 /mnt/USBMusic exfat defaults,auto,users,rw,nofail 0 0

# open the firewall to allow SSH
sudo ufw allow ssh

# Check the status of the SSH Server
#sudo systemctl status ssh

# Install GIT
sudo apt -y install wget, git
git config --global user.email "henry.thompson@gmail.com"
git config --global user.name "henry Thompson"

# alsa-base:
# alsa-utils:
# pulseaudio:
sudo apt -y install alsa-base alsa-utils pulseaudio

# ffmpeg:
# mpd:
# mpc:
# sudo apt -y install ffmpeg mpd mpc zip
sudo apt -y install ffmpeg mpd mpc

# create folder for logs
sudo mkdir /var/log/musiccards
sudo chown pi:pi musiccards/


# Install youtube-dl
sudo wget https://yt-dl.org/latest/youtube-dl -O /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl

sudo apt -y install python3 python3-pip

# Install youtube-dl python module
sudo -H pip3 install --upgrade youtube-dl
sudo -H pip3 install --upgrade python-mpd2
sudo -H pip3 install --upgrade evdev

sudo apt -y autoremove
sudo apt -y clean

# on some systems the user is not in the input group, let's make sure they are
# This is needed if the user wants to use the RFID input device
sudo usermod -a -G input $USER
sudo usermod -a -G sudo $USER

# cd $HOME/src/music-cards/src
# sudo cp musiccards.service /etc/systemd/system/musiccards.service
# sudo chmod 644 /etc/systemd/system/musiccards.service
# sudo systemctl daemon-reload
# sudo systemctl start musiccards.service
# sudo systemctl enable musiccards.service

# Could not get bluetooth working
# # Turn on BlueTooth
# # unmask the Bluetooth service
# sudo systemctl unmask bluetooth
# sudo systemctl enable bluetooth
# # the bluetooth module was not loading so you need to figure that out, but manually you can type
# sudo modprobe btusb
# # Start the Bluetooth service
# sudo systemctl start bluetooth

# #install Bluetooth command line tools, you should reboot after installing these
# sudo apt install bluez
# sudo apt install pi-bluetooth
# sudo apt install pulseaudio-module-bluetooth
# pulseaudio -k
# pulseaudio --start

# # add user to the bluetooth users group
# sudo usermod -a -G bluetooth $USER

# # interactive mode
# sudo bluetoothctl << EOF
# power on
# agent on
# default-agent
# pair D8:37:3B:63:1B:30
# trust D8:37:3B:63:1B:30
# connect D8:37:3B:63:1B:30
# EOF

# sudo bluetoothctl << EOF
# connect D8:37:3B:63:1B:30
# EOF



# # sudo bluetoothctl
# # If you dont get a result from show you have an issue
# # --> show
# #  https://www.youtube.com/watch?v=lHwvoFLbAkM
# #  https://forums.raspberrypi.com/viewtopic.php?t=242281
# #  https://forums.raspberrypi.com/viewtopic.php?t=207025
# #  https://raspberrypi.stackexchange.com/questions/50109/bluetooth-device-list
# #  https://forums.raspberrypi.com/viewtopic.php?t=240492
# #
# # --> default-agent
# # --> scan on
# # bluetooth ID for Dad's JBL Flip 5 -->  D8:37:3B:63:1B:30
# # --> pair D8:37:3B:63:1B:30

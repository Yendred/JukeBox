# change to home folder
cd ~

#update
sudo apt -y update

# Install GIT
sudo apt -y install git
#git config --global user.email "My Email Address"
#git config --global user.name "My Name"

mkdir ~/src
cd ~/src
git clone https://github.com/Yendred/JukeBox.git

# create directory for logs
sudo mkdir /var/log/jukebox
sudo chown pi:pi /var/log/jukebox

# alsa-base:
# alsa-utils:
# pulseaudio:
sudo apt -y install alsa-base alsa-utils
# sudo apt -y install ffmpeg
sudo apt -y install mpd mpc
sudo apt -y purge pulseaudio

# install python 3 and pip
sudo apt -y install python3 python3-pip

# install exfat, this is the USB Drive format
sudo apt install -y exfat-fuse

sudo apt -y autoremove
sudo apt -y clean

# edit /etc/mpd.conf and make the folowing changes
# comment out this line
#       bind_to_address         "localhost"
#
# uncomment this line
#       bind_to_address         "/run/mpd/socket"
# sed -i -e 's/#bind_to_address "/run/mpd/socket"/bind_to_address "/run/mpd/socket"/' /etc/mpd.conf
#
# uncomment this line and change replace "hardware" with "software"
#       mixer_type              "hardware"      # optional
#
# uncomment this line and change replace "no" with "yes"
#       volume_normalization    "no"



cat /proc/asound/cards
# if the output of the above command does not show the speakers as the
# default or 0 device we will need to edit /usr/share/alsa/alsa.conf and change the following
# find the following lines and change the number to the device as shown in 'cat /proc/asound/cards'
#   defaults.pcm.card 1
#   defaults.ctl.card 1
# I dont like this solution, if the devices switch places we will no longer have a working sound device


# Install python modules
# sudo -H pip3 install --upgrade python-mpd2
# sudo -H pip3 install --upgrade evdev
/usr/bin/python3 -m pip install --user --upgrade python-mpd2 evdev jsonpath-ng black

# /usr/bin/env python3 -m pip freeze > requirements.txt
# /usr/bin/env python3 -m pip install -r requirements.txt

# https://www.shellhacks.com/raspberry-pi-mount-usb-drive-automatically/
# create mount point for USB Drive
sudo mkdir /mnt/USBMusic

# run 'lsblk -fp'  to determine where the USB Drive is mounted, on this run it is located at /dev/sda1
sudo mount -t exfat /dev/sda1 /mnt/USBMusic

# run 'blkid' to determine the UUID, on this run it is '1C87-CC63'
#/dev/sda1: LABEL="Music" UUID="1C87-CC63" BLOCK_SIZE="512" TYPE="exfat" PARTUUID="44e444a8-01"

# add the following to /etc/fstab
# Remember to change the UUID and mount location with what was determined above '/mnt/USBMusic'
#   UUID=1C87-CC63 /mnt/USBMusic exfat defaults,auto,users,rw,nofail 0 0



# on some systems the user is not in the input group, let's make sure they are
# This is needed if the user wants to use the RFID input device
sudo usermod -a -G input $USER
sudo usermod -a -G sudo $USER

cd ~/src/JukeBox/src
sudo cp /home/pi/src/JukeBox/src/jukebox.service /etc/systemd/system/jukebox.service
sudo chmod 644 /etc/systemd/system/jukebox.service
sudo systemctl daemon-reload
sudo systemctl enable jukebox.service
sudo systemctl start jukebox.service

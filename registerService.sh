src='/home/pi/src/JukeBox/src'
dest='/etc/systemd/system'

cd $src
sudo cp $src/jukebox.service $dest/jukebox.service
sudo chmod 644 $dest/jukebox.service
sudo systemctl daemon-reload
sudo systemctl enable jukebox.service
sudo systemctl start jukebox.service

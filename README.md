# Music Cards

Click the image below to see a video of it being used

[![RFID Jukebox with Google Home](https://img.youtube.com/vi/AvCseOQidSw/0.jpg)](https://www.youtube.com/watch?v=AvCseOQidSw)

## Requires

### software:

- python evdev. To install:

```bash
wget http://dl.piwall.co.uk/python-evdev_0.4.1-1_armhf.deb

dpkg -i python-evdev_0.4.1-1_armhf.deb
```

- python mpd-2. To install

```bash
pip install python-mpd2
```

### hardware:

- [Raspberry Pi Zero (Don't forget micro sd card and power supply)](http://www.microcenter.com/product/486575/Zero_W)
- [USB OTG Hub](https://www.amazon.com/gp/product/B01HYJLZH6/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1)
- [RFID 125Khz Reader](https://www.amazon.com/gp/product/B018C8C162/ref=oh_aui_detailpage_o03_s01?ie=UTF8&psc=1)
- [125Khz Cards](https://www.amazon.com/gp/product/B01MQY5Y7U/ref=ox_sc_act_title_1?smid=A1GYMVIZIMSYWM&psc=1)
- [RFID Card Inkjet Tray to print in your printer (Note this is the model needed for my Canon MX922 Printer)](https://www.amazon.com/gp/product/B00P25H0BA/ref=oh_aui_detailpage_o03_s01?ie=UTF8&psc=1)

Please note that Raspberry Pi Zero is insufficient to run both the Home Assistant and Music Cards concurrently. I recommend you use a Raspberry Pi 3 if you intend to run both at the same time.

## Steps to Configure and/or Run once if you dont want Music Cards to AutoStart

1. Run `python config.py` to select the reader from the inputs
2. Run `python add_card.py` to scan cards and enter your Google Play Music Playlist Name
3. Run `python box.py` to start the application and verify that it is reading your cards and csv list properly

## Install Service to AutoStart

- Change directory to music-cards/

```bash
cd music-cards/
```

- Copy the musiccards.service file to systemd

```bash
sudo cp musiccards.service /etc/systemd/system/musiccards.service
```

- Reload the Daemon

```bash
sudo systemctl daemon-reload
```

- Start the musiccards.service

```bash
sudo systemctl start musiccards.service
```

- Check if musiccards.service is running

```bash
sudo systemctl status musiccards.service
```

## HomeAssistant Setup for Google Music

1. Place the files under homeassistant_files in the config directory of your [Homeassistant](https://www.home-assistant.io/) machine.
2. You will need to create custom_components/switch directory in your config directory and place [`gmusic.py`](https://github.com/mf-social/Home-Assistant/blob/master/custom_components/switch/gmusic.py) in there.
3. Follow [this forum post](https://community.home-assistant.io/t/google-music-in-ha/10976) to install gmusicapi, find your device id, and set up the component.

##Code
Sub ProcessCards()
EnumerateFilesAndFolders
End Sub

Sub EnumerateFilesAndFolders( _
Optional FolderPath As String = "e:\sorted\", _
Optional index As Integer = 1, _
Optional MaxDepth As Long = -1, _
Optional CurrentDepth As Long = 0)

    processCard = True

    'Set the file name to a variable
    Set FSO = CreateObject("Scripting.FileSystemObject")

    'Check the folder exists
    If FSO.FolderExists(FolderPath) Then
        Dim oFolder As Object
        Set oFolder = FSO.GetFolder(FolderPath)

        'Enumerate the subfolders
        Dim oSubFolder As Object
        For Each oSubFolder In oFolder.SubFolders
            'Debug.Print Space$((CurrentDepth + 1)) & oSubFolder.Name
            If CurrentDepth < MaxDepth Or MaxDepth = -1 Then
                'Recursively call EnumerateFilesAndFolders
                EnumerateFilesAndFolders oSubFolder.path, index, MaxDepth, CurrentDepth + 1
            End If
        Next oSubFolder

        'Enumerate the files
        Dim oFile As Object
        If (oFolder.Files.Count >= 10) Then
            For Each oFile In oFolder.Files
                If (oFile.Name = "Folder.jpg") Then

                    AlbumName = Split(oFile.path, "\")(3)
                    ArtistName = Split(oFile.path, "\")(2)
                    AlbumImage = oFile.path

                    If (processCard = vbTrue) Then
                        Selection.Font.Bold = False
                        Selection.Font.Name = "SF Pro Regular"
                        Selection.Font.Size = 9
                        Selection.InlineShapes.AddPicture fileName:=AlbumImage, LinkToFile:=False, SaveWithDocument:=True
                        Selection.TypeParagraph
                        Selection.TypeParagraph
                        Selection.Font.Size = 14
                        Selection.TypeText Text:=AlbumName
                        Selection.Font.Size = 9
                        Selection.TypeParagraph
                        If (Len(AlbumName) <= 20) Then Selection.TypeParagraph
                        Selection.Font.Size = 11
                        Selection.TypeText Text:=ArtistName

                        Selection.Move Unit:=wdCell, Count:=1
                        If index Mod 5 <> 0 Then
                            Selection.Move Unit:=wdCell, Count:=1
                        Else
                            Selection.MoveRight Unit:=wdCharacter  ', Count:=3
                            Selection.InsertRows 1
                        End If
                    End If

                    Debug.Print Space$((CurrentDepth + 1)) & ArtistName & "/" & AlbumName & " (" & oFolder.Files.Count & "|" & index & ")"
                    index = index + 1

                End If
            Next oFile
        End If
    End If

End Sub

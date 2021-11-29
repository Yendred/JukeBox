#!/usr/bin/python3
import os.path
from pathlib import Path
import sys
import getpass

from evdev import InputDevice, list_devices

devices = [InputDevice(fn) for fn in list_devices()]

if len(devices) == 0:
    print(
        f"Could not find a RFID device, make sure it is plugged in.\nIf it is plugged in you may need to be added to the 'input' group (sudo usermod -a -G input {getpass.getuser()})"
    )
    sys.exit(0)

while True:
    try:
        i = 0
        print("Choose the reader from list?")
        for dev in devices:
            print(f"{i} : {dev.name}")
            i += 1

        dev_id = int(input("Device Number: "))

        devicePath = Path(os.path.dirname(os.path.realpath(__file__)))
        devicePath = Path.joinpath(devicePath.parent.absolute(), "deviceName.txt")

        with open(devicePath, "w") as f:
            f.write(devices[dev_id].name)

        break

    except Exception as ex:
        print(f"{ex}\n")

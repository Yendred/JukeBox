#!/usr/bin/python3
# from csv import reader, DictReader
import logging, csv, json, sys
from pathlib import Path
from os.path import os
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse


class BuildConfig:
    def __init__(self):  # , filepath, logger):
        pass

    def createInitialJSON(self) -> dict:
        data = {}
        data["Settings"] = {
            "initialVolume": 20,
            "logFile": "/var/log/musiccards/music-cards.log",
            "musicRoot": "/mnt/USBMusic/Sorted/",
        }
        data["Cards"] = []
        data["Cards"].append(
            {
                "ID": "0002933058",
                "Name": "Reboot Pi",
                "Type": "system",
                "URI": "system://pi/reboot",
                # "Active": True,
            },
        )
        data["Cards"].append(
            {
                "ID": "0002933057",
                "Name": "Shutdown Pi",
                "Type": "system",
                "URI": "system://pi/shutdown",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002915921",
                "Name": "Quit",
                "Type": "system",
                "URI": "system://pi/quit",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002933292",
                "Name": "Volume Up",
                "Type": "setting",
                "URI": "setting://volume/up/10",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002933291",
                "Name": "Volume Down",
                "Type": "setting",
                "URI": "setting://volume/down/10",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002933270",
                "Name": "Pause",
                "Type": "action",
                "URI": "action://pause",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002933269",
                "Name": "Play",
                "Type": "action",
                "URI": "action://play",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002929617",
                "Name": "Stop",
                "Type": "action",
                "URI": "action://stop",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002929612",
                "Name": "Next",
                "Type": "action",
                "URI": "action://next",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002973948",
                "Name": "Skip Forward",
                "Type": "action",
                "URI": "action://skip/forward/15",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002973939",
                "Name": "Skip Backward",
                "Type": "action",
                "URI": "action://skip/backward/15",
                # "Active": True,
            }
        )
        data["Cards"].append(
            {
                "ID": "0002915856",
                "Name": "Previous",
                "Type": "action",
                "URI": "action://previous",
                # "Active": True,
            }
        )
        return data

    def saveJSON(self, data: dict):

        jsonString = json.dumps(data, indent=4, ensure_ascii=True)
        with open("data.json", "w") as jsonFile:
            jsonFile.write(jsonString)

        # jsonFile = open("data.json", "w")
        # jsonFile.write(jsonString)
        # jsonFile.close()

    def readMusic(self, data: dict, musicPath: str) -> dict:
        if not Path(musicPath).exists():
            return data

        index = 1
        rootPath = os.path.dirname(musicPath)
        for root, d_names, f_names in os.walk(rootPath):
            if len(d_names) == 0:
                print(root)
                splitPath = root.split("/")
                # {"ID": "0002973800", "Name": "Mother's Milk", "Type": "album", "URI": "file:///mnt/USBMusic/Sorted/Red Hot Chili Peppers/Mother's Milk", "Active": true},
                # match splitPath[-1]:
                #     case "":
                #         id = ""
                #     case "":
                #         id = ""
                #     case "":
                #         id = ""
                #     case _:
                #         id = (str(index)).zfill(10)

                id = (str(index)).zfill(10)

                data["Cards"].append(
                    {
                        "ID": id,
                        "Name": f"{splitPath[-2]} - {splitPath[-1]}",
                        "Type": "album",
                        "URI": f"{(root.replace(rootPath.rstrip('/'), '')).lstrip('/')}"
                        # "Active": True,
                    }
                )
                index = index + 1

        return data

    def setUpLogging(self, logfile):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)5s] %(name)s::%(funcName)s - %(message)s",
            handlers=[
                # logging.FileHandler("/var/log/musiccards/music-cards.log"), # , when="D", backupCount=5
                logging.StreamHandler(),
                logging.handlers.TimedRotatingFileHandler(
                    logfile, when="D", backupCount=5
                ),
            ],
        )

        self.logger = logging.getLogger(self.__class__.__name__)


if __name__ == "__main__":
    # try:
    app = BuildConfig()
    # app.getLogger().info(f"Starting Program!!")
    path = "/mnt/USBMusic/Sorted/"

    dict = app.createInitialJSON()
    dict = app.readMusic(dict, path)
    app.saveJSON(dict)

# except SystemExit as se:
#     # logging.getLogger(__name__).info(f"Exiting: {se}")
#     pass
# except Exception as ex:
#     # logging.getLogger(__name__).error(
#     #     f"global: Unhandled Exception Exiting.... {ex}"
#     # )
#     sys.exit(100)
# finally:
# logging.getLogger(__name__).info(f"Exiting Program!!")

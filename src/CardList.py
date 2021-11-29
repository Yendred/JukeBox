# from csv import reader, DictReader
import logging, csv, json
from os.path import os
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse

# from itertools import dropwhile


class CardList:
    def __init__(self, filepath):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cardListPath = filepath
        self.cardList = None  # self.readList()

    def getPlaylist(self, card):
        try:
            # if not self.cardList:
            self.cardList = self.readPlaylist()

            jsonpath_expr = parse("$[?(@.ID==" + card + ")]")
            results = jsonpath_expr.find(self.cardList)

            if len(results) == 1:
                album = results[0].value

                if "album" in album["Type"]:
                    # probably should be a little defensive here, but if the data is bad we have bigger issues
                    album["URI"] = f"{self.readSetting('musicRoot')}{album['URI']}"

                self.logger.debug(
                    f"Found -- ID:{album['ID']}, Name:{album['Name']}, URI:{album['URI']}"
                )
                return album

        except Exception as e:
            self.logger.error(f"Unknown Exception: {e}")

        return None

    def readPlaylist(self):
        if self.logger:
            self.logger.debug(f"starting " + __name__)
        try:
            cardList = None

            # with open('/home/pi/src/music-cards/src/cardList.json', "r", encoding="utf-8") as jsonfile:
            with open(self.cardListPath, "r", encoding="utf-8") as jsonfile:
                cardJson = json.load(jsonfile)

            if cardJson != None:
                cardList = cardJson["Cards"]

            return cardList

        except Exception as e:
            if self.logger:
                self.logger.error(f"Unknown Exception: {e}")
            return None

    def readSetting(self, setting):
        if self.logger:
            self.logger.debug(f"starting " + __name__)
        try:
            readSetting = None

            # with open('/home/pi/src/music-cards/src/cardList.json', "r", encoding="utf-8") as jsonfile:
            with open(self.cardListPath, "r", encoding="utf-8") as jsonfile:
                cardJson = json.load(jsonfile)

            if cardJson != None:
                cardList = cardJson["Settings"]
                readSetting = cardList.get(setting)

            return readSetting

        except Exception as e:
            if self.logger:
                self.logger.error(f"Unknown Exception: {e}")
            return None

    # Function to convert a CSV to JSON
    # Takes the file paths as arguments
    def convertCsvToJson(self):
        # create a dictionary
        # data = {}
        data = []

        # Open a csv reader called DictReader
        with open(self.cardListPath_csv, encoding="utf-8") as csvf:
            csvReader = csv.DictReader(csvf)

            # Convert each row into a dictionary
            # and add it to data
            for rows in csvReader:

                # Assuming a column named 'No' to
                # be the primary album
                # album = rows["ID"]
                # data[album] = rows

                data.append(rows)

        # Open a json writer, and use the json.dumps()
        # function to dump data
        with open(self.cardListPath, "w", encoding="utf-8") as jsonf:
            jsonf.write(json.dumps(data, indent=4))

    def exportJSON(self):
        with open(self.cardListFileName, "w") as write_file:
            json.dump(self.cardList, write_file, indent=4, sort_keys=True)

#!/usr/bin/python3
# from __future__ import unicode_literals
# import hashlib
# import os
# import random
import re

# import subprocess
import sys
import time
import logging
import time
from pathlib import Path
from os import listdir, walk, system
from os import path
from os.path import isfile
from os.path import join
from os.path import dirname
from os.path import realpath
from mpd import MPDClient

from CardList import CardList
from Reader import Reader

# ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
# MEDIA_PATH = os.path.join(Path.home(), "media")  # ~/media
# TRACK_DIR_PATH = os.path.join(MEDIA_PATH, "tracks")  # ~/media/tracks
# MUSIC_DIR_PATH = os.path.join(MEDIA_PATH, "music")  # ~/media/music
# TMP_PATH = os.path.join(MEDIA_PATH, "tmp")  # ~/media/tmp
# CACHE_PATH = os.path.join(MEDIA_PATH, "cache")  # ~/media/cache
# MUSIC_DIR_MAX_MEGABYTES = 500
# START_VOLUME = 30


def setUpLogging(logfile):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)5s] %(name)s::%(funcName)s - %(message)s",
        handlers=[
            logging.FileHandler(
                "/var/log/musiccards/music-cards.log"
            ),  # , when="D", backupCount=5
            logging.StreamHandler(),
            # logging.handlers.TimedRotatingFileHandler(logfile, when="D", backupCount=5),
        ],
    )
    logging.getLogger("mpd.base").setLevel(logging.WARNING)


class JukeBox:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.initializeMPDClient = False
        cardListPath = Path.joinpath(Path(dirname(realpath(__file__))), "cardList.json")
        self.cardList = CardList(cardListPath)
        self.reader = Reader()

        self.logger.info("Starting")
        pass

    def connectMPD(self):
        try:
            self.logger.debug("Setting up MPD server Connection")
            client = MPDClient()  # create client object
            client.timeout = (
                200  # network timeout in seconds (floats allowed), default: None
            )
            client.idletimeout = None
            client.connect("/run/mpd/socket", 6600)

            if not self.initializeMPDClient:
                self.logger.debug("Setting up MPD server Connection")
                self.initializeMPDClient = True
                initialVolume = self.cardList.readSetting("initialVolume")
                client.setvol(initialVolume)
                client.clear()
                client.repeat(0)
                client.random(0)
                client.crossfade(2)

            return client
        except:
            self.logger.exception("Could not connect to MPD server")

    def ClearAndPlay(self, client, cardData):
        try:
            cardID = cardData["ID"]
            cardName = cardData["Name"]
            cardType = cardData["Type"]
            cardURI = cardData["URI"]

            if cardType == "album":
                client.stop()
                client.clear()

                for root, directories, files in walk(cardURI, topdown=False):
                    for name in files:
                        filePath = join(root, name)
                        if isfile(filePath) and (not name.endswith(".jpg")):
                            client.add(filePath)
                            self.logger.info(f"Adding Song [{filePath}]")

                client.play()

            elif cardType == "youtube":
                # do nothing for now
                pass

            elif cardType == "url":
                client.stop()
                client.clear()

                self.logger.info(f"Adding {cardName}, URL [{cardURI}]")
                client.add(cardURI)
                client.play()

            else:
                print(f"Don't know what to do here with URI '{cardURI}'")
                return

        except Exception as e:
            self.logger.warning(f"Could not play '{cardData}'")
            self.logger.warning(f"ClearAndPlay: Unknown Exception (Ignorring): {e}")

    def initializeMDP_OLD(self):
        """
        We want to make sure that the MPD server is responding

        Paremeters:
        None

        Returns:
        Instance of the MPC Client

        """
        try:
            connectTry = 1
            client = None
            while not client and connectTry <= 5:
                client = self.connectMPD()
                # print(type(client))
                # print(client.mpd_version)  # print the MPD version

                if not client:
                    time.sleep(2)
                else:
                    initialVolume = self.cardList.readSetting("initialVolume")

                    client.setvol(initialVolume)
                    client.clear()
                    # client.add("file:///home/pi/ready.mp3")

                    client.repeat(0)
                    client.random(0)

                    client.crossfade(2)
                    # client.play()
                    #  time.sleep(2)
                connectTry = connectTry + 1

            if client == None or connectTry > 5:
                sys.exit("Failed to create a connection to the MPD server, Exiting!!!")

        except Exception as e:
            print(f"initializeMDP: Unknown Exception (Ignoring): {e}")
            raise

        return client

    def printStatus(self, client=None):
        localClientInstance = False
        try:
            if not client:
                client = self.connectMPD()
                localClientInstance = True

            clientStatus = client.status()
            # print(f"Status: {clientStatus}")
            for key in clientStatus:
                try:
                    self.logger.info(
                        f"status\t{key.ljust(14,' ')} --> {clientStatus[key]}"
                    )
                except:
                    pass

            fileFullPathsong = client.fileFullPathsong()
            # print(f"Status: {clientStatus}")
            for key in fileFullPathsong:
                try:
                    self.logger.info(
                        f"song\t{key.ljust(14,' ')} --> {fileFullPathsong[key]}"
                    )
                except:
                    pass
        except:  # Exception as e:
            # We should not care about this exception, continue
            # print(f"printStatus: unknown exception: {e}")
            pass

        finally:
            if localClientInstance and client:
                client.close()
                client.disconnect()

    def ProcessCard2(self, client, cardData, sameAsPreviousCard):
        try:
            # print(f"Card Data found : '{cardData}'")
            # cardID = cardData[0]
            cardName = cardData[1]
            cardURI = cardData[2]

            if "system://" in cardURI:
                # print(f"System card found.\t{cardURI}")

                if "reboot" in cardURI:
                    # print(f"Rebooting Pi: {cardURI}")
                    system("sudo shutdown -r now")
                elif "shutdown" in cardURI:
                    # print(f"Shutting down PI: {cardURI}")
                    system("sudo shutdown -P now")
                else:
                    print(f"Unknown System Card: {cardURI}")

            elif "setting://" in cardURI:
                # print(f"Settings card found.\t{cardURI}")

                if "setting://volume" in cardURI:
                    try:
                        # print(f"Volume card found.\t{cardURI}")

                        volume = 0
                        direction = "down"

                        splitURI = cardURI.split("/")
                        if len(splitURI) >= 2:
                            volume = int(splitURI[len(splitURI) - 1])
                            direction = splitURI[len(splitURI) - 2]

                        fileFullPathVolume = int(client.status().get("volume"))

                        if not fileFullPathVolume:
                            fileFullPathVolume = self.cardList.readSetting(
                                "initialVolume"
                            )

                        # round to nearest multiple of 5
                        fileFullPathVolume = 5 * round(fileFullPathVolume / 5)

                        # print(f"fileFullPath Volume : \t{fileFullPathVolume}")
                        if fileFullPathVolume:
                            if "up" == direction:
                                newVolume = fileFullPathVolume + volume
                            else:
                                newVolume = fileFullPathVolume - volume

                            if newVolume < 0 or newVolume > 100:
                                newVolume = 0
                            if newVolume > 100:
                                newVolume = 100

                            # print(f"New Volume : \t{newVolume}")
                            client.setvol(newVolume)
                            fileFullPathVolume = client.status().get("volume")
                            # print(f"New Volume : \t{ fileFullPathVolume }")
                        else:
                            print(
                                "Could not determine the fileFullPath Volume, keeping fileFullPath volume"
                            )

                    except Exception as e:
                        print(f"Failed to set volume: {e}")
                        pass
                    finally:
                        pass

            elif "action://" in cardURI:
                try:
                    # print(f"Play card found.\t{cardURI}")
                    # 0002933270,Pause,action,action://action/pause
                    # 0002933269,Play,action,action://action/play
                    # 0002929617,Stop,action,action://action/stop
                    # 0002929612,Next,action,action://action/next
                    # 0002915856,Previous,action,action://action/previous

                    fileFullPathVolume = client.status().get("volume")
                    # print(f"State:'{client.status().get('state')}'")
                    if "action://action/pause" == cardURI:
                        # print("Pausing")
                        client.pause()
                    elif "action://action/play" == cardURI:
                        # print("Playing")
                        client.play()
                    elif "action://action/stop" == cardURI:
                        # print("Stopping")
                        client.stop()
                    elif "action://action/next" == cardURI:
                        # TODO: need to address playlists
                        client.next()
                    elif "action://action/previous" == cardURI:
                        # TODO: need to address playlists
                        client.previous()
                    # print(f"State:'{client.status().get('state')}'")

                except:
                    print(f"Failed to set playable action")
                    pass
                finally:
                    pass

            #  This must be "file://" or "https://"  TODO: We should check
            else:
                fileFullPathSong = client.fileFullPathsong()
                if (
                    fileFullPathSong
                    and fileFullPathSong.get("file") in cardURI
                    and sameAsPreviousCard
                ):
                    # internet based streams do not populate the name propert
                    # immediately, so we will shove something in here until it is popilated
                    if fileFullPathSong and fileFullPathSong.get("name") is None:
                        fileFullPathSong["name"] = cardName

                    print(f"\tSame card: '{fileFullPathSong.get('name')}'")
                    if client.status().get("state") == "play":
                        print("\tPausing the music")
                        client.pause()
                    else:
                        print("\tResuming the music")
                        client.play()
                else:
                    # print("Playing a new song")
                    self.ClearAndPlay(client, cardData)
                    return True

        except Exception as e:
            # We should not care about this exception, continue
            print(f"ProcessCard: unknown exception: {e}")
            raise

        return False

    def processCard(self, card: str) -> None:
        if card == "":
            # This probably will never happen, but lets check anyway
            self.logger.warning(f"Card returned invalid data: '{card}'")
        else:
            # find the data represented by the card
            cardData = self.cardList.getPlaylist(card)
            if cardData == None:
                self.logger.info(
                    f"Card not found, this card '{card}' can be used for adding additional music.  Skipping..."
                )
            else:
                self.logger.info(f"Found Card: {cardData}")

                cardID = cardData["ID"]
                cardName = cardData["Name"]
                cardType = cardData["Type"]
                cardURI = cardData["URI"]

                # The card is valid and we found data in the DB for this card, awesome!
                client = self.connectMPD()

                if cardType == "system":
                    if "system://pi/reboot" == cardURI:
                        system("sudo shutdown -r now")
                    elif "system://pi/shutdown" in cardURI:
                        system("sudo shutdown -P now")
                    else:
                        print(f"Unknown System Card: {cardURI}")

                elif cardType == "setting":
                    if "setting://volume/up" in cardURI:
                        try:
                            splitURI = cardURI.split("/")
                            volumeIncrease = int(splitURI[-1])
                            actualVolume = int(client.status().get("volume"))
                            if not actualVolume:
                                actualVolume = self.cardList.readSetting(
                                    "initialVolume"
                                )

                            # round to nearest multiple of 5
                            newVolume = 5 * round((actualVolume + volumeIncrease) / 5)

                            if newVolume < 100:
                                client.setvol(newVolume)

                        except Exception as e:
                            self.logger.exception(f"Failed to turn down volume: {e}")

                    elif "setting://volume/down" in cardURI:
                        try:
                            splitURI = cardURI.split("/")
                            volumeIncrease = int(splitURI[-1])
                            actualVolume = int(client.status().get("volume"))
                            if not actualVolume:
                                actualVolume = self.cardList.readSetting(
                                    "initialVolume"
                                )

                            # round to nearest multiple of 5
                            newVolume = 5 * round((actualVolume - volumeIncrease) / 5)

                            if newVolume > 0:
                                client.setvol(newVolume)

                        except Exception as e:
                            self.logger.exception(f"Failed to turn down volume: {e}")

                elif cardType == "action":
                    try:
                        if "action://pause" == cardURI:
                            client.pause()
                        elif "action://play" == cardURI:
                            client.play()
                        elif "action://stop" == cardURI:
                            client.stop()
                        elif "action://next" == cardURI:
                            client.next()
                        elif "action://previous" == cardURI:
                            client.previous()
                        elif "action://skip/backward" in cardURI:
                            # BUG: This does not see to work
                            splitURI = cardURI.split("/")
                            skipAmount = int(splitURI[-1])
                            client.seekcur(skipAmount * -1)
                        elif "action://skip/forward" in cardURI:
                            splitURI = cardURI.split("/")
                            skipAmount = int(splitURI[-1])
                            client.seekcur(skipAmount)
                        else:
                            self.logger.warning(
                                "Could not determine the fileFullPath Action for card {cardID}, skipping"
                            )
                    except Exception as e:
                        self.logger.exception(
                            f"Failed to execute Action {cardName}, skipping : {e}"
                        )

                elif cardType == "url":
                    self.ClearAndPlay(client, cardData)

                elif cardType == "youtube":
                    self.ClearAndPlay(client, cardData)

                elif cardType == "album":
                    self.ClearAndPlay(client, cardData)

                if client:
                    client.close()
                    client.disconnect()
                    client = None

    def main(self, card: str = None) -> None:
        while True:
            try:
                if card is None:
                    print("Ready: place a card on top of the reader")
                    card = self.reader.readCard()

                self.processCard(card)

                card = None
            except Exception as ex:
                self.logger.exception(f"Unhandled Exception, Ignoring.... {ex}")
                pass

    def main2(self):
        reader = Reader()
        cardList = CardList()

        before_card = None

        # make sure the MPD Server is responding
        client = self.initializeMDP()

        cardData = "empty"
        while True:
            try:
                card = ""

                print("Ready: place a card on top of the reader")
                # print(f"\tBefore_card:'{before_card}'")

                card = reader.readCard()
                # print(f"Card read: '{card}'")

                if card == "":
                    # This probably will never happen, but lets check anyway
                    print(f"Card returned invalid data: '{card}'")
                else:
                    # find the data represented by the card
                    cardData = cardList.getPlaylist(card)
                    # if cardData:
                    #     print(f"Found Card Data: {cardData}")

                    if cardData == "":
                        print(f"Card was not found in the Database: '{card}'")
                        print(
                            f"This card '{card}' can be used for adding additional music.  Skipping..."
                        )
                    else:
                        # The card is valid and we found data in the DB for this card, awesome!
                        client = self.connectMPD()

                        # returns false if the card is not a song (System/Setting/Action), otherwise true
                        if self.ProcessCard(client, cardData, card == before_card):
                            before_card = card
                            card = ""

                            fileFullPathSong = cardData[1]
                            if client.fileFullPathsong().get("name"):
                                fileFullPathSong = client.fileFullPathsong().get("name")

                        print(
                            f"\tClient Status:\tPlaying:'{fileFullPathSong}'\tVolume:'{client.status().get('volume')}'\tState:'{client.status().get('state')}'\n"
                        )

                        client.close()
                        client.disconnect()
                        client = None
            except KeyboardInterrupt:
                sys.exit(0)

            except Exception as e:
                print(f"main: Unknown Exception: {e}")
                time.sleep(2)
                pass

            finally:
                # self.printStatus(None)
                pass


if __name__ == "__main__":
    try:
        setUpLogging(None)
        logger = logging.getLogger(__name__)
        logger.debug("-- Starting")
        app = JukeBox()
        app.printStatus(None)
        if False:
            # this really needs to be moved to a test framework and implemented there
            cards = [
                # "0000000440"  # Youtube
                "0002911458"  #   "WHRV"
                # "0002933291",  #   "Volume Down"
                # "0002933291",  #   "Volume Down"
                # "0002933292",  #   "Volume Up"
                # "0002933292",  #   "Volume Up"
                # "0004139483",  #   "Nirvana - MTV Unplugged in New York"
                # "0002933291",  #   "Volume Down"
                # "0002933291",  #   "Volume Down"
                # "0002933292",  #   "Volume Up"
                # "0002933270",  #   "Pause"
                # "0002933269",  #   "Play"
                # "0002929612",  #   "Next"
                # "0002929612",  #   "Next"
                # "0002973948",  #   "Skip Forward"
                # "0002973948",  #   "Skip Forward"
                # "0002929617",  #   "Stop"
                # "0000051813",  #   "Killers"
                # "0002929612",  #   "Next"
                # "0002929612",  #   "Next"
                # "0002933291",  #   "Volume Down"
                # "0002929617",  #   "Stop"
            ]
            for card in cards:
                app.processCard(card)
                time.sleep(2)

            client = app.connectMPD()
            logger.info(client.status())
            client.disconnect()
            client = None
            sys.exit(0)

        app.main()
    except SystemExit as se:
        logger.exception(f"global: Unhandled System Exit Exception, Exiting.... {se}")
    except Exception as ex:
        logger.exception(f"global: Unhandled Exception, Exiting.... {ex}")
        sys.exit(100)
    finally:
        logger.debug("-- Exiting")

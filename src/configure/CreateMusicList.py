#!/usr/bin/python3
# from __future__ import unicode_literals
import os, csv

# from os import listdir
# from os.path import isfile, join


class MusicFiles:
    def __init__(self):
        pass

    def Main(self):
        ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
        MUSIC_ROOT = "/mnt/sorted/"

        file1 = open(os.path.join(ROOT_PATH, "album.csv"), "w")

        for subdir, dirs, files in os.walk(MUSIC_ROOT):
            if len(dirs) == 0:  # and len(files) > 5:
                Artist = subdir.replace(MUSIC_ROOT, "").split("/")[0]
                Album = subdir.replace(MUSIC_ROOT, "").split("/")[1]

                # if "_" in Album:
                print(f"{Artist} - {Album} - ({len(files)})")
                file1.write(f'"{Artist}","{Album}",,"{len(files)}"\n')
            # for file in files:
            #     print(os.path.join(subdir, file))

        file1.close()


if __name__ == "__main__":
    app = MusicFiles()
    app.Main()

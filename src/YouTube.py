from pathlib import Path
import youtube_dl
import os, subprocess

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
MEDIA_PATH = os.path.join(Path.home(), "media")  # ~/media
TRACK_DIR_PATH = os.path.join(MEDIA_PATH, "tracks")  # ~/media/tracks
MUSIC_DIR_PATH = os.path.join(MEDIA_PATH, "music")  # ~/media/music
TMP_PATH = os.path.join(MEDIA_PATH, "tmp")  # ~/media/tmp
CACHE_PATH = os.path.join(MEDIA_PATH, "cache")  # ~/media/cache
MUSIC_DIR_MAX_MEGABYTES = 500
START_VOLUME = 30


class YouTube:
    def __init__(self):
        for filePath in [
            MEDIA_PATH,
            TRACK_DIR_PATH,
            MUSIC_DIR_PATH,
            TMP_PATH,
            CACHE_PATH,
        ]:
            try:
                if not Path(filePath).exists():
                    print(f"Creating {filePath}")
                    Path(filePath).mkdir(mode=0o755, parents=True)

            except:  # Exception as e:
                print(f"Failed to create {filePath}")
                pass

            finally:
                pass

    def GetMusicDirSizeMegabytes(self):
        output = 0
        try:
            rawOutput = subprocess.run(["du", "-m", MUSIC_DIR_PATH], capture_output=True)

            output = rawOutput.stdout.decode("ascii").split("\t")[0].strip()
            # print(f"GetMusicDirSizeMegabytes: output: '{output}'")
            return int(output)

        except:
            print(f"Returning 0, Could not determine the folder size of '{output}'")
            return 0
        finally:
            pass

    def GetAbsoluteFilepath(self, trackNameDecoded):
        return os.path.join(MUSIC_DIR_PATH, trackNameDecoded)

    def GetOldestTrackFilePath(self):
        try:
            output = ""
            p1 = subprocess.Popen(("ls", "-t", MUSIC_DIR_PATH), stdout=subprocess.PIPE)
            p2 = subprocess.Popen(("tail", "-1"), stdin=p1.stdout, stdout=subprocess.PIPE, encoding="utf-8",)

            p1.stdout.close()
            rawOutput = p2.communicate()
            p2.stdout.close()

            output = rawOutput[0].strip()
            # ..stdout.decode("ascii")  # .split("\t")[0].strip())

            if output == "":
                return ""
        except:
            print("EXCEPTION:  Could not find oldest track")
            return ""
        finally:
            pass

        return self.GetAbsoluteFilepath(output)

    def PruneOldTracks(self, maxTotalMegabytes):
        # Never delete more than this many files, even if we're still
        # not below the max megabyte limit.
        deleteCountMax = 3

        # As long as the music library is too large, delete the oldest track.
        deleteCount = 0

        try:
            while self.GetMusicDirSizeMegabytes() > maxTotalMegabytes:
                oldestFilePath = self.GetOldestTrackFilePath()
                if not os.path.exists(oldestFilePath):
                    break

                os.unlink(oldestFilePath)
                deleteCount = deleteCount + 1
                if deleteCount >= deleteCountMax:
                    break

        except Exception as e:
            print(f"PruneOldTracks: Unknown Exception: {e}")
            pass
        finally:
            pass

        return deleteCount

    def ClearAndPlay(self, client, musicData):
        try:
            # lets git rid of tracks that have been sitting around for awhile
            self.PruneOldTracks(MUSIC_DIR_MAX_MEGABYTES)
        except:
            pass
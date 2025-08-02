import sys
import os


if __name__ == "__main__":
    from sh import mise

    cmd = [str(mise), ["mise", *sys.argv[1:]]]
    os.execv(*cmd)

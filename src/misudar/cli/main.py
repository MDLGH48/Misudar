import sys
import os

def run():
    from sh import mise
    cmd = [str(mise), ["mise", *sys.argv[1:]]]
    os.execv(*cmd)


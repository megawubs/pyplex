from interface import pyPlex
import sys

args = sys.argv
plex = pyPlex(args)
plex.start()
plex.run()
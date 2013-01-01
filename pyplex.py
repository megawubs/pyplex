from pyplex.interface import pyPlex
import sys
from pprint import pprint


if __name__ == "__main__":
	args = sys.argv
	plex = pyPlex(args)
	plex.start()
	plex.run()
import urllib2, re, xml.etree.cElementTree as et
from urllib import urlencode
from urlparse import urlparse
import uuid, hmac, hashlib, base64, time

from pprint import pprint

from server import Server
from ..pyplexlogger.logger import pyPlexLogger

class PlexMedia:
    def __init__(self, mediaurl, serverSceme):
        self.l = pyPlexLogger("PlexMedia").logger
        self.media_url = mediaurl
        server = serverSceme.split(':')
        self.server = Server(server[0], server[1])
        self.media = self.server.getMedia(mediaurl)

    def setPlayed(self):
        try:
            f = urllib2.urlopen(self.playedURL)
        except urllib2.HTTPError:
            print "Failed to update plex that item was played: %s" % setPlayPos
            pass

    def updatePosition(self, posMilli):
        #TODO: make setPlayPos a function
        try:
            f = urllib2.urlopen((self.updateURL % (posMilli)))
        except urllib2.HTTPError:
            print "Failed to update plex play time, url: %s" % setPlayPos
            pass
        
        

class PlexInterface:

    def __init__(self):
        pass


    def getMedia(self, mediaurl, serverSceme):
        return PlexMedia(mediaurl, serverSceme)

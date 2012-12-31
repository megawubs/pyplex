from ..interfaces.plexInterface import PlexInterface
from ..interfaces.server import Server
from ..pyomx.pyomxplayer import OMXPlayer

from urlparse import urlparse
from ..pyplexlogger.logger import pyPlexLogger

from pprint import pprint
class xbmcCommands:
    def __init__(self, omxArgs, server):
        self.l = pyPlexLogger("xbmcCommands").logger
        self.l.info('Initated xbmcCommands')
        self.media = None
        self.plex = server
        self.omx = None
        self.omxArgs = omxArgs
        self.shutDown = False

    def PlayMedia(self, fullpath, tag, unknown1, unknown2, unknown3):
        self.l.info("playing media!")
        # Serach for media based on tag
        self.media = self.plex.getMedia(tag) #Media now contains all kind of information about the file
        # media.transcodeURL is currentley not working
        if(self.omx):
            self.Stop()

        self.omx = OMXPlayer(self.media.transcodeURL, args=self.omxArgs, start_playback=True)

    def Pause(self, message):
        if(self.omx):
            self.omx.set_speed(1)
            self.omx.toggle_pause()

    def Play(self, message):
        if(self.omx):
            ret = self.omx.set_speed(1)
            if(ret == 0):
                self.omx.toggle_pause()

    def Stop(self, message=""):
        if(self.omx):
            self.omx.stop()
            self.omx = None

    def stopPyplex(self, message = None):
        self.shutDown = True

    def SkipNext(self, message = None):
        if(self.omx):
            self.omx.increase_speed()

    def SkipPrevious(self, message = None):
        if(self.omx):
            self.omx.decrease_speed()

    def StepForward(self, message = None):
        if(self.omx):
            self.omx.increase_speed()

    def StepBack(self, message = None):
        if(self.omx):
            self.omx.decrease_speed()

    def BigStepForward(self, message = None):
        if(self.omx):
            self.omx.jump_fwd_600()

    def BigStepBack(self, message = None):
        if(self.omx):
            self.omx.jump_rev_600()

    def getMilliseconds(self,s):
        hours, minutes, seconds = (["0", "0"] + ("%s" % s).split(":"))[-3:]
        hours = int(hours)
        minutes = int(minutes)
        seconds = float(seconds)
        miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
        return miliseconds

    def getPosMilli(self):
        return self.getMilliseconds(self.omx.position)
    
    def setPlayed(self):
        self.plex.execute(self.media.updateURL)

    def isFinished(self):
        if(self.omx):
            finished = self.omx.finished
        else:
            finished = True
        return finished
    
    def isRunning(self):
        if(self.omx):
            return True
        return False

    def updatePosition(self):
        try:
            if self.isFinished():
                if (self.getPosMilli() > (self.media.duration * .95)):
                    self.plex.execute(self.media.scrobbleURL % self.media.key)
                self.Stop()
            else:
                self.plex.execute(self.media.updateURL % (self.media.key, self.getPosMilli()))
        except Exception, e:
            print e

# test = xbmcCommands('')
# test.PlayMedia('http://192.168.1.201:32400/library/onDeck', '/library/metadata/1713', '+', ' ', ' ')
# self.stopPyplex()
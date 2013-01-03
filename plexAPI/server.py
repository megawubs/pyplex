from library import Library
from client import Client
from media import Media
from pyplexlogger.logger import pyPlexLogger
import base64

import urllib2
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import XML

class Server(object):
    transcodeURL = '/video/:/transcode/segmented/start.m3u8?'
    transcode_private = base64.b64decode('k3U6GLkZOoNIoSgjDshPErvqMIFdE0xMTx8kgsrhnC0=')
    transcode_public = 'KQMIY6GATPC63AIMC4R2'

    def __init__(self, address, port=32400):
        self.l = pyPlexLogger('PlexAPI').logger
        # TODO: clean up address, remove http:// etc
        
        # remove slash at end of address
        if address[-1] == '/':
            address = address[:-1]
        self.address = address
        self.port = int(port)

        
        
    def execute(self, path):
        self.l.info("execute %s" % path)
        if path[0] == '/':
            path = path[1:]
            
        # open url
        try: 
            urllib2.urlopen("http://%s:%d/%s" % (self.address, self.port, path)) 
        except urllib2.URLError, e:
            self.l.error("Reading %s failed. %s" % (path, e))

        
    def query(self, path):
        self.l.info("Query %s" % path)
        if path[0] == '/':
            path = path[1:]
            
        # open url and get raw xml data
        try:
            response = urllib2.urlopen("http://%s:%d/%s" % (self.address, self.port, path))
        except urllib2.URLError, e:
            self.l.error("Reading %s failed. %s" % (path, e))
        
        # create element from xml data
        xmldata = response.read()
        self.l.info("Got response: %s" % xmldata)
        element = XML(xmldata)
        return element
    
    
    def __str__(self):
        return "<Server: %s:%d/>" % (self.address, self.port) 
    
    def __repr__(self):
        return "<Server: %s:%d/>" % (self.address, self.port) 
    
    def getMedia(self, mediaPath):
        result = self.query(mediaPath)
        media = Media(result, self)
        return media.getMediaObject()
    
    @property
    def library(self):
        elem = self.query("/library")
        return Library(self)
    
    @property
    def clients(self):
        elem = self.query("/clients")
        clist = [Client(e, self) for e in elem]
        return clist

    @property
    def servers(self):
        elem = self.query("/servers")
        


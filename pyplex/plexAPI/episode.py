from info import Info
from pprint import pprint

class Episode(object):
    
    def __init__(self, element, server):
        self.server = server
        self.element = element
        self.type = "episode"
        info = Info(self, server).info
        for k in info:
            setattr(self.__class__, k,  info[k])
        # self.transcodeBaseURL = parsed_path.scheme + "://" + parsed_path.netloc
        # self.transcodeURL = '/video/:/transcode/segmented/start.m3u8?'
        
        # parsed_path = urlparse(mediaurl)
        # self.fileURL = parsed_path.scheme + "://" + parsed_path.netloc + self.partTag.attrib['key']
        

    def __str__(self):
        return "<Episode: %s (%d)>" % (self.title, self.index)
        
    def __repr__(self):
        return "<Episode: %s (%d)>" % (self.title, self.index)

    
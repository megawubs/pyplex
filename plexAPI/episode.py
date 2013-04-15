from info import Info
from pprint import pprint

class Episode(object):
    
    def __init__(self, element, server):
        self.server = server
        self.element = element
        self.type = "episode"
        # Get infor of object
        info = Info(self, server).info
        # Add value of info[k] to property named as the value of k  
        for k in info:
            setattr(self, k,  info[k])
        

    def __str__(self):
        return "<Episode: %s (%d)>" % (self.title, self.index)
        
    def __repr__(self):
        return "<Episode: %s (%d)>" % (self.title, self.index)

    

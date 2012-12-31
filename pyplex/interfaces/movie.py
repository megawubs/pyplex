from info import Info

class Movie(object):
    
    def __init__(self, element, server):
        self.server = server
        self.element = element
        # browse element and extract some information
        self.type = 'movie'
        info = Info(self, server).info
        for k in info:
            setattr(self.__class__, k,  info[k])

        if not hasattr(self.__class__, 'year'):
            self.year = 0
    
    def __str__(self):
        return "<Movie: %s (%s)>" % (self.title, self.year)
    
    def __repr__(self):
        return "<Movie: %s (%d)>" % (self.title, self.year)
    
    

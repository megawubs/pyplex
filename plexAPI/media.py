from episode import Episode
from movie import Movie
from show import Show
from season import Season

class Media(object):
	"""Test class for media object"""
	def __init__(self, element, server):
		self.element = element
		self.server = server
		tags = ['Video', 'Directory']
		
		#get video
		for tag in tags:
			tag = element.find("./%s" % tag)
			if tag != None:
				self.type = tag.attrib['type']
				self.tag = tag
				break

	def getMediaObject(self):
		media = False
		if self.type == "episode":
			media = Episode(self.tag, self.server)
		elif self.type == "movie":
			media = Movie(self.tag, self.server)
		elif self.type == "show":
			media = Show(self.tag, self.server)
		elif self.type == "season":
			media = Season(self.tag, self.server)
		return media
		
from episode import Episode
from movie import Movie

class Media(object):
	"""Test class for media object"""
	def __init__(self, element, server):
		self.element = element
		self.server = server
		
		#get video
		self.video = element.find('./Video')
		self.type = self.video.attrib['type']


	def getMediaObject(self):
		if self.type == "episode":
			media = Episode(self.video, self.server)
		elif self.type == "movie":
			media = Movie(self.video, self.server)
		if media:
			return media
		else:
			return False
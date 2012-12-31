import uuid, hmac, hashlib, base64, time
from urllib import urlencode
from urlparse import urlparse

class Info(object):
	"""Get info of media"""
	def __init__(self, media, server):
		self.str = '<Info Object Type: %s, Title: %s>'
		element = media.element
		mediaElement = element.find('.Media')

		key = element.attrib['key']
		self.media = media
		self.server = server
		self.serverAddr = 'http://%s:%d' % (server.address, server.port)
		self.info = {}

		self.info['key'] =  key
		self.info['ratingKey'] = element.attrib['ratingKey']
		self.info['type'] = media.type
		self.info['title'] = element.attrib['title']
		self.info['summary'] = element.attrib['summary']

		if 'index' in element.attrib:
			self.info['index'] = int(element.attrib['index'])
		if 'year' in element.attrib:
			self.year = int(element.attrib['year'])

		self.info['duration'] = int(mediaElement.attrib['duration'])
		self.info['viewed'] = ('viewCount' in element.attrib) and (element.attrib['viewCount'] == '1')
		self.info['offset'] = int(element.attrib['viewOffset']) if 'viewOffset' in element.attrib else 0
		self.info['file'] = element.find('.Media/Part').attrib['file']
		
		self.info['video_codec'] = mediaElement.attrib['videoCodec']
		self.info['audio_codec'] = mediaElement.attrib['audioCodec']
		self.info['width'] = mediaElement.attrib['width']
		self.info['height'] = mediaElement.attrib['height']
		
		self.info['updateURL'] =  "progress?key=%s&identifier=com.plexapp.plugins.library&time=%s&state=playing"
	 	self.info['scrobbleURL'] = "scrobble?key=%s&identifier=com.plexapp.plugins.library"
	 	self.info['transcodeURL'] = self.getTranscodeURL()

	 	self.info['fileURL'] = "%s%s" % (self.serverAddr, element.find('.Media/Part').attrib['key'])

	 	self.info['setPlayed'] = getattr(self, setPlayed)
	 	self.info['updatePosition'] = getattr(self, updatePosition)
	def getTranscodeURL(self, extension='mkv', format='matroska', videoCodec='libx264', audioCodec=None, continuePlay=False, continueTime=None, videoWidth='1280', videoHeight='720', videoBitrate=None):
		if(videoWidth > self.info['width']):
			videoWidth = self.info['width']

		if(videoHeight > self.info['height']):
			videoHeight = self.info['height']

		self.session = uuid.uuid4()

		args = dict()
		args['offset'] = 0
		args['3g'] = 0
		args['subtitleSize'] = 125
		args['secondsPerSegment'] = 10
		args['ratingKey'] = self.info['ratingKey']
		args['key'] =  self.info['key']
		args["identifier"] = "com.plexapp.plugins.library"
		args["quality"] = 7
		args["url"] = self.info['file']
		transcodeURL = self.server.transcodeURL
		transcodeURL += urlencode(args)
		atime = int(time.time())
		message = transcodeURL + "@%d" % atime
		sig = base64.b64encode(hmac.new(self.server.transcode_private, msg=message, digestmod=hashlib.sha256).digest())
		plexAccess = dict()
		plexAccess['X-Plex-Access-Key'] = self.server.transcode_public
		plexAccess['X-Plex-Access-Time'] = atime
		plexAccess['X-Plex-Access-Code'] = sig
		plexAccess['X-Plex-Client-Capabilities'] = 'protocols=http-live-streaming,http-mp4-streaming,http-mp4-video,http-mp4-video-720p,http-streaming-video,http-streaming-video-720p;videoDecoders=h264{profile:high&resolution:1080&level:41};audioDecoders=aac,mp3,ac3,dts'
		transcodeURL = transcodeURL + "&" + urlencode(plexAccess)
		return "%s%s" % (self.serverAddr, transcodeURL)


	def setPlayed(self):
		try:
			f = urllib2.urlopen(self.playedURL)
		except urllib2.HTTPError:
			print "Failed to update plex that item was played: %s" % setPlayPos
			pass

	def updatePosition(self, posMilli):
		try:
			f = urllib2.urlopen((self.updateURL % (posMilli)))
		except urllib2.HTTPError:
			print "Failed to update plex play time, url: %s" % setPlayPos
			pass

	def __str__(self):
		return self.str % (self.info['type'], self.info['title'])

	def __repr__(self):
		return self.str % (self.info['type'], self.info['title'])
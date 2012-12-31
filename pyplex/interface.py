from commands.xbmc import xbmcCommands
from gui.image import image
import platform
from listeners.udplistener import udplistener
from listeners.httplistener import httplistener
from service.zeroconf import ZeroconfService
import Queue, sys
from pprint import pprint
from pyplexlogger.logger import pyPlexLogger
# from interfaces.plexInterface import plexInterface
# from interfaces.plexInterface
# from listners.httplistner import
class pyPlex():
	"""Wrapper class for pyPlex"""
	def __init__(self, arg):
		self.l = pyPlexLogger('pyplex').logger
		self.l.info('Pyplex initaited')
		self.omxCommand = self.getArg(arg)
		self.hostname = platform.uname()[1]

	def start(self):
		"""Setting up listners and all other stuff"""
		print "Setting up listeners, please wait..."
		self.l.info("Setting up listeners")
		global service
		global queue
		global parsed_path
		global media_key
		global duration
		self.service = ZeroconfService(name=self.hostname + " PyPlex", port=3000, text=["machineIdentifier=" + self.hostname,"version=2.0"])
		self.service.publish()
		self.duration = 0
		self.xbmcCmmd = xbmcCommands(self.omxCommand)
		self.media_key = None
		self.parsed_path = None
		self.queue = Queue.Queue()
		self.udp = udplistener(self.queue)
		self.udp.start()
		self.http = httplistener(self.queue)
		self.http.start()
		# __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
		# f = open(os.path.join(__location__, 'image/logo.png'));
		# image = image(f)
		#image.set()
		
	def run(self):
		"""The heart of pyPlex (can you hear it pounding...?)"""
		self.l.info("Running pyplex")
		try:
			while True:
				if(self.xbmcCmmd.isRunning()):
					self.xbmcCmmd.updatePosition()
				command = self.parseCommand()
				if command:
					func, args = command
					print(func)
					func(*args)
					if(self.xbmcCmmd.shutDown == True):
						self.stop()
						break
		except Exception, e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno) 
			print "Caught exception"
			message = 'There went something wrong in %s'
			if(self.xbmcCmmd):
				print message % 'xbmc'
				print e
				self.xbmcCmmd.Stop("")
				self.stop()
				return 0
			if(udp):
				print message % 'udp'
				print e
				self.udp.stop()
				self.udp.join()
			if(http):
				print message % 'http'
				print e
				self.http.stop()
				self.http.join()
			raise

	def getArg(self, arg):
		if len(arg) > 1: 
			if arg[1] == "hdmi":
				self.omxCommand = '-o hdmi'
				print "Audo output over HDMI"
				self.l.info("Audo output over HDMI")
		else:
			self.omxCommand = ''
			print "Audio output over 3,5mm jack"

	def parseCommand(self):
		try:
			command, args = self.queue.get(True, 2)
			print "Got command: %s, args: %s" %(command, args)
			if not hasattr(self.xbmcCmmd, command):
				print "Command %s not implemented yet" % command
			else:
				func = getattr(self.xbmcCmmd, command)
				return [func, args]
		except Queue.Empty:
			pass

	def stop(self):
		self.xbmcCmmd.Stop("")
		self.udp.stop()
		self.http.stop()
		self.service.unpublish()

	def keepRunning(self):
		if(self.xbmcCmmd.shutDown == True):
			
			print "Shutting down"
			return False
		else:
			print "Keep running!"
			return True

		

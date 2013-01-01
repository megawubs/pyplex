from commands.xbmc import xbmcCommands
from gui.image import image
import platform, Queue, sys
from listeners.udplistener import udplistener
from listeners.httplistener import httplistener
from service.zeroconf import ZeroconfService, AvahiLookUp
from pprint import pprint
from pyplexlogger.logger import pyPlexLogger

class pyPlex():
	"""Wrapper class for pyPlex"""
	def __init__(self, arg):
		self.l = pyPlexLogger('PyPlex').logger
		self.l.info("Starting up...")
		self.omxCommand = self.getArg(arg)
		self.hostname = platform.uname()[1]
		self.server = AvahiLookUp("_plexmediasvr._tcp").servers[0]
		# TODO stop script if no server is found
		


	def start(self):
		"""Setting up listners and all other stuff"""
		self.l.info("Setting up listeners")
		self.service = ZeroconfService(name=self.hostname + " PyPlex", port=3000, text=["machineIdentifier=" + self.hostname,"version=2.0"])
		self.service.publish()
		self.duration = 0
		self.queue = Queue.Queue()
		self.xbmcCmmd = xbmcCommands(self.omxCommand, self.server)
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
		self.l.info("Running PyPlex")
		try:
			while True:
				# check if xmbc is running
				if(self.xbmcCmmd.isRunning()):
					# update position
					self.xbmcCmmd.updatePosition()
				# get the command from the listneners
				command = self.parseCommand()
				if command:
					# read the command and args
					func, args = command
					# excecute the command
					func(*args)
					# check if pyplex has to stop
					if(self.xbmcCmmd.shutDown == True):
						self.stop()
						break
		except Exception, e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			self.l.error("Caught exception")
			self.l.error(exc_type, fname, exc_tb.tb_lineno) 
			message = 'There went something wrong in %s'
			if(self.xbmcCmmd):
				self.l.error(message % 'xbmc')
				self.l.error(e) 
				self.xbmcCmmd.Stop("")
				self.stop()
				return 0
			if(udp):
				self.l.error(message % 'udp')
				self.l.error(e)
				self.udp.stop()
				self.udp.join()
			if(http):
				self.l.error(message % 'http')
				self.l.error(e)
				self.http.stop()
				self.http.join()
			raise

	def getArg(self, arg):
		if len(arg) > 1: 
			if arg[1] == "hdmi":
				self.omxCommand = '-o hdmi'
				self.l.info("Audo output over HDMI")
		else:
			self.omxCommand = ''
			self.l.info("Audio output over 3,5mm jack")

	def parseCommand(self):
		"""Get commands from the queue"""
		try:
			command, args = self.queue.get(True, 2)
			self.l.info("Got command: %s, args: %s" %(command, args))
			if not hasattr(self.xbmcCmmd, command):
				self.l.error("Command %s not implemented yet" % command)
			else:
				func = getattr(self.xbmcCmmd, command)
				# Retun the function + it's arguments
				return [func, args]
		except Queue.Empty:
			pass

	def stop(self):
		"""Stop pyPlex"""
		self.xbmcCmmd.Stop("")
		self.udp.stop()
		self.http.stop()
		self.service.unpublish()
		self.l.info('Stopped PyPlex')

		

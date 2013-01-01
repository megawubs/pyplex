import logging, os

class pyPlexLogger:

	def __init__(self, name):
		self.logger = logging.getLogger(name)
		handler = logging.FileHandler('pyplex.log')
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		self.logger.setLevel(logging.INFO)
		self.logger.propagate = False

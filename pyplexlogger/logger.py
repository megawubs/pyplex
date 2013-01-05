import logging, os

class pyPlexLogger:

	def __init__(self, name):
		self.logger = logging.getLogger(name)
		path = os.path.dirname(os.path.realpath(__file__))
		path = path.split('/')
		pyplexRoot = '/'.join(path[0:5])
		handler = logging.FileHandler(os.path.join(pyplexRoot, 'pyplex.log'))
		formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
		handler.setFormatter(formatter)
		self.logger.addHandler(handler)
		self.logger.setLevel(logging.INFO)
		self.logger.propagate = False

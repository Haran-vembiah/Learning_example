'''
Loggers are plain Python objects. The addHandler() method has no minimum or maximum quota for the number of handlers you may add. Sometimes it will be beneficial for an application to log all messages of all severities to a text file while simultaneously logging errors or above to the console. To set this up, simply configure the appropriate handlers. The logging calls in the application code will remain unchanged. Here is a slight modification to the previous simple module-based configuration example:
'''
import logging


logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
# logger1 = logging.getLogger('simple1_example')
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
# ch1 = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# formatter1 = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# ch1.setFormatter(formatter1)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
# logger1.addHandler(ch1)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')
# logger1.error('From logger1')
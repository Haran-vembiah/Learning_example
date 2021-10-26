import logging.config
import yaml

with open('E:\python_Works\Projects\Learning_example\Logging_modules\config.yaml', 'r') as stream:
    my_yaml = yaml.load(stream, Loader=yaml.FullLoader)
print(my_yaml)
logging.config.dictConfig(my_yaml)
my_logger = logging.getLogger('simpleExample')

logging.info('info msg')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
logging.critical('Critical error')
logging.warning('warning msg')
logging.debug('This message should go to the log file')
logging.info('So should this')
my_logger.info('my_logger info')
my_logger.debug('my_logger debug')
my_logger.warning('my_logger warning')
my_logger.error('my_logger Error')
my_logger.critical('my_logger critical')

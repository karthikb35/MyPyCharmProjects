import configparser
import sys
import logging
import time, os

logging.basicConfig(level=logging.DEBUG)
config = configparser.ConfigParser()
config.sections()
config.read('C:\Work\Waste\config_test.txt')
# print(config.sections())
# print(config['DNA_DB']['DNA_DB_NAME'])
ts = str ( int ( time.time ( ) ) )
os.mkdir(ts)
logger=logging.getLogger(__name__)
f_handler = logging.FileHandler(f'{ts}/main.log')
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


if os.path.isfile('config.txt'):
    logger.info('config file found')
else:
    logger.error('config.txt file not found. Exiting...')
    sys.exit()




try:
    config = configparser.ConfigParser()
    config.sections()
    config.read('C:\Work\Waste\config_test2.txt')


    RUN_PURPOSE=config['RUN']['PURPOSE']
    DNA_RELEASE=config['RUN']['DNA_RELEASE']

    DNA_IP=config['DNA_SERVER']['DNA_IP']
    DNA_USER_NAME=config['DNA_SERVER']['DNA_USER_NAME']
    DNA_USER_PASSWORD=config['DNA_SERVER']['DNA_USER_PASSWORD']
    EMS_PATH=config['DNA_SERVER']['DNA_HOME']+'/EMS/'
    DNA_DB_USERNAME=config['DNA_DB']['DNA_DB_USERNAME']
    DNA_DB_PASSWD=config['DNA_DB']['DNA_DB_PASSWD']
    DNA_DB_NAME=config['DNA_DB']['DNA_DB_NAME']
    INTERVAL=config['PERIODIC_DISCOVERY']['INTERVAL']
    TOTAL_DURATION=config['PERIODIC_DISCOVERY']['TOTAL_DURATION']
    SQL_SERVER_IP=config['SQL_SERVER']['DB_IP']
    SQL_SERVER_PORT=config['SQL_SERVER']['PORT']
    SQL_SERVER_USER=config['SQL_SERVER']['DB_USER']
    SQL_SERVER_PASSWD=config['SQL_SERVER']['DB_PASSWD']
    SQL_SERVER_DB=config['SQL_SERVER']['DB']
    SQL_SERVER_TABLE=config['SQL_SERVER']['TABLE']
    logger.info('read successfully')

except:
    logger.exception("Error reading config file")
    sys.exit()
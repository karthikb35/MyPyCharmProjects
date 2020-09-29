import sys
from datetime import datetime
import mysql.connector
import paramiko
from paramiko_expect import SSHClientInteraction
import time
import configparser
import logging
import os
import cx_Oracle

ts = str ( int ( time.time ( ) ) )
os.mkdir(ts)


logger=logging.getLogger(__name__)
f_handler = logging.FileHandler(f'{ts}/main.log')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
f_handler.setLevel(logging.DEBUG)
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)

session_logger = logging.getLogger('SESSION')
session_handler = logging.FileHandler ( f'{ts}/session.log' )
session_format = logging.Formatter ( '%(message)s' )
session_handler.setFormatter ( session_format )
session_handler.setLevel(logging.DEBUG)
session_logger.addHandler ( session_handler )
session_logger.setLevel(logging.DEBUG)

if os.path.isfile('config.txt'):
    logger.info('config file found')
else:
    logger.error('config.txt file not found. Exiting...')
    sys.exit()

try:
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.txt')


    RUN_PURPOSE=config['RUN']['PURPOSE']
    DNA_RELEASE=config['RUN']['DNA_RELEASE']

    DNA_IP=config['DNA_SERVER']['DNA_IP']
    DNA_USER_NAME=config['DNA_SERVER']['DNA_USER_NAME']
    DNA_USER_PASSWORD=config['DNA_SERVER']['DNA_USER_PASSWORD']
    EMS_PATH=config['DNA_SERVER']['DNA_HOME']+'/EMS/'

    DNA_DB_TYPE=config['DNA_DB']['DNA_DB_TYPE']
    DNA_DB_USERNAME=config['DNA_DB']['DNA_DB_USERNAME']
    DNA_DB_PASSWD=config['DNA_DB']['DNA_DB_PASSWD']
    DNA_DB_NAME=config['DNA_DB']['DNA_DB_NAME']
    DNA_DB_PORT=config['DNA_DB']['DNA_DB_PORT']
    INTERVAL=config['PERIODIC_DISCOVERY']['INTERVAL']
    TOTAL_DURATION=config['PERIODIC_DISCOVERY']['TOTAL_DURATION']
    SQL_SERVER_IP=config['SQL_SERVER']['DB_IP']
    SQL_SERVER_PORT=config['SQL_SERVER']['PORT']
    SQL_SERVER_USER=config['SQL_SERVER']['DB_USER']
    SQL_SERVER_PASSWD=config['SQL_SERVER']['DB_PASSWD']
    SQL_SERVER_DB=config['SQL_SERVER']['DB']
    SQL_SERVER_TABLE=config['SQL_SERVER']['TABLE']
    logger.info('Successfully read config data')
except:
    logger.exception("Error reading config file")
    sys.exit()
if not(0<int(INTERVAL)<=60):
    logger.error('Enter valid INTERVAL')
    sys.exit()

latest_timestamp =0
DNA_StartTime = int(time.time())


def shutdown_DNA ( DNA_IP, username, password, ems_path ):

    client = paramiko.SSHClient ( )
    client.set_missing_host_key_policy ( paramiko.AutoAddPolicy ( ) )
    client.connect ( DNA_IP, username=username, password=password )
    with SSHClientInteraction ( client, timeout=15, display=True ) as interact:
        try:
            PROMPT = '.*[\$\#]\s*'
            PROMPT_bin = '.*[\$\#]\s*'
            interact.expect ( PROMPT )
            interact.send ( f'cd {ems_path}/bin' )
            interact.expect ( PROMPT_bin, timeout=5 )
            interact.send ( './EMSLauncher.sh' )
            interact.expect ( 'Enter selection:', timeout=5 )
            interact.send ( '3' )


            interact.expect ( 'Enter UserName \[admin\]:', timeout=5 )
            interact.send ( 'admin' )
            interact.expect ( 'Enter Password :', timeout=5 )
            interact.send ( 'infinera1' )

            if 'Do you want to shutdown DNA-M Server?' in interact.current_output_clean:
                interact.send ( 'y' )
            interact.expect ( 'Enter selection:', timeout=180 )
            interact.send ( 'q' )
            interact.expect ( PROMPT_bin, timeout=5 )

            cmd_output_uname = interact.current_output_clean
            session_logger.info( cmd_output_uname )
        except:
            logger.exception('Shutdown failed. Exiting...')
            client.close()
            sys.exit()
        finally:
            logger.info ( datetime.now ( ) )
            client.close ( )



def WarmStart_DNA ( DNA_IP, username, password, ems_path ):
    client = paramiko.SSHClient ( )
    client.set_missing_host_key_policy ( paramiko.AutoAddPolicy ( ) )
    client.connect ( DNA_IP, username=username, password=password )
    with SSHClientInteraction ( client, timeout=15, display=True ) as interact:
        try:
            PROMPT = '.*[\$\#]\s*'
            PROMPT_bin = '.*[\$\#]\s*'
            interact.expect ( PROMPT )
            interact.send ( f'cd {ems_path}/bin' )
            interact.expect ( PROMPT_bin, timeout=5 )
            interact.send ( './EMSLauncher.sh' )
            interact.expect ( 'Enter selection:', timeout=5 )
            interact.send ( '2' )
            interact.expect ( 'Enter selection:', timeout=180 )
            interact.send ( 'q' )
            interact.expect ( PROMPT_bin, timeout=5 )
            interact.send ( f'tail -f {ems_path}/logs/startup.log' )
            interact.expect ( 'Infinera DNA Server modules started successfully at .*', timeout=1800 )
            global DNA_StartTime
            DNA_StartTime = int(time.time())
            cmd_output_uname = interact.current_output_clean

            logger.info ( cmd_output_uname )
        except:
            logger.exception('Warmstart failed.Exiting..')
            client.close()
            sys.exit()
        finally:
            logger.info( datetime.now ( ) )
            client.close ( )




# latest_timestamp = 1576230510447
def periodic_db(DNA_IP, DNA_DB_USERNAME, DNA_DB_PASSWD, interval, total_duration):
    max_iterations=(int(int(total_duration)*60/int(interval)))
    iteration =0

    (ATN, CLOUD_XP, DON, OA, OLA,ROADM,XT,GROOVE) = (0,0,0,0,0,0,0,0)
    logger.info(f'Latest timestamp = {str(latest_timestamp)}')
    while iteration <= max_iterations:

        mydb = mysql.connector.connect ( host=DNA_IP, user=DNA_DB_USERNAME, passwd=DNA_DB_PASSWD, database=DNA_DB_NAME )
        sqldb = mysql.connector.connect (  host=SQL_SERVER_IP, user=SQL_SERVER_USER, passwd=SQL_SERVER_PASSWD, database=SQL_SERVER_DB )
        sqlcursor = sqldb.cursor ( )
        mycursor = mydb.cursor ( )
        iteration=iteration+1
        time_elapsed = int(time.time()) - DNA_StartTime
        (prev_ATN, prev_CLOUD_XP, prev_DON, prev_OA, prev_ROADM, prev_XT, prev_OLA, prev_GROOVE) = (ATN,CLOUD_XP,DON,OA,ROADM,XT,OLA, GROOVE)
        ROADM=0
        mycursor.execute (
            f"SELECT count(distinct(eventstringdata2)),eventstringdata3  FROM {DNA_DB_NAME}.htbl_dnaevent where "
            f"(eventtype = \'DD_END\' and dbinsertiontimestamp > {latest_timestamp}) "
            f"OR (eventsourcemodule like \'%Groove%\' and eventtype =\'SD_END\' and dbinsertiontimestamp > {latest_timestamp} ) group by eventstringdata3 " )
        for i in mycursor:
            ne_type = i[1].decode('ascii')
            if 'ATN' in ne_type:
                ATN=i[0]
            if 'CLOUD_XP' in ne_type:
                CLOUD_XP=i[0]
            if 'DON' in ne_type:
                DON=i[0]
            if ne_type == 'OA':
                OA=i[0]
            if 'ROADM' in ne_type:
                ROADM=ROADM+i[0]
            if 'XT' in ne_type:
                XT=i[0]
            if  ne_type == 'OLA':
                OLA=i[0]
            if ne_type == 'GROOVE_G30':
                GROOVE=i[0]

        if (prev_ATN, prev_CLOUD_XP, prev_DON, prev_OA, prev_ROADM, prev_XT, prev_OLA, prev_GROOVE) != (ATN,CLOUD_XP,DON,OA,ROADM,XT,OLA, GROOVE):
            data = f"INSERT INTO  {SQL_SERVER_TABLE} ( purpose, runid, sampleid, dnarel,  ATN, CX, DON, OA, OLA, ROADM, XT, GROOVE, " \
                f"TimeElapsed, serverip)" \
                f" VALUES( \"{RUN_PURPOSE}\" , {int(ts)}, {int(iteration)}, \"{DNA_RELEASE}\", {int(ATN)},{int(CLOUD_XP)},{int(DON)},{int(OA)}, {int(OLA)}, {int(ROADM)}, {int(XT)} ,{int(GROOVE)},   {int(time_elapsed)} , \"{str(DNA_IP)}\")"
            sqlcursor.execute(data)
            sqldb.commit()
        time.sleep(interval)
        logger.info(f" Sample: {iteration}. | ATN = {ATN}, CX = {CLOUD_XP}, DON = {DON}, OA = {OA}, OLA = {OLA}, ROADM = {ROADM}, XT = {XT}, GROOVE = 0, XTM = 0")


def periodic_db_ORACLE(DNAIP, DNADB_USERNAME, DNADB_PASSWD, DNADB_PORT,  interval, total_duration):
    max_iterations=(int(int(total_duration)*60/int(interval)))
    iteration =0
    (ATN, CLOUD_XP, DON, OA, OLA,ROADM,XT,GROOVE) = (0,0,0,0,0,0,0,0)

    logger.info(f'Latest timestamp = {str(latest_timestamp)}')
    while iteration <= max_iterations:

        dsn_tns = cx_Oracle.makedsn ( DNAIP, DNADB_PORT,
                                      service_name=DNA_DB_NAME )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect ( user=DNADB_USERNAME, password=DNADB_PASSWD,
                                   dsn=dsn_tns )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        cur = conn.cursor ( )
        sqldb = mysql.connector.connect ( host=SQL_SERVER_IP, user=SQL_SERVER_USER, passwd=SQL_SERVER_PASSWD,
                                          database=SQL_SERVER_DB )
        sqlcursor = sqldb.cursor ( )
        iteration=iteration+1
        time_elapsed = int(time.time()) - DNA_StartTime
        (prev_ATN, prev_CLOUD_XP, prev_DON, prev_OA, prev_ROADM, prev_XT, prev_OLA, prev_GROOVE) = (ATN,CLOUD_XP,DON,OA,ROADM,XT,OLA, GROOVE)
        (ATN, CLOUD_XP, DON, OA, OLA,ROADM,XT,GROOVE) = (0,0,0,0,0,0,0,0)
        cur.execute (
            f"SELECT count(distinct(eventstringdata2)),eventstringdata3  FROM htbl_dnaevent where "
            f"(eventtype = \'DD_END\' and dbinsertiontimestamp > {latest_timestamp}) "
            f"OR (eventsourcemodule like \'%Groove%\' and eventtype =\'SD_END\' and dbinsertiontimestamp > {latest_timestamp} ) group by eventstringdata3 " )
        for i in cur:
            ne_type = i[1]
            if 'ATN' in ne_type:
                ATN=i[0]
            if 'CLOUD_XP' in ne_type:
                CLOUD_XP=i[0]
            if 'DON' in ne_type:
                DON=i[0]
            if ne_type == 'OA':
                OA=i[0]
            if 'ROADM' in ne_type:
                ROADM=ROADM+i[0]
            if 'XT' in ne_type:
                XT=i[0]
            if  ne_type == 'OLA':
                OLA=i[0]

            if ne_type == 'GROOVE_G30':
                GROOVE=i[0]
        if (prev_ATN, prev_CLOUD_XP, prev_DON, prev_OA, prev_ROADM, prev_XT, prev_OLA, prev_GROOVE) != (ATN,CLOUD_XP,DON,OA,ROADM,XT,OLA, GROOVE):
            data = f"INSERT INTO  {SQL_SERVER_TABLE} ( purpose, runid, sampleid, dnarel,  ATN, CX, DON, OA, OLA, ROADM, XT, GROOVE, TimeElapsed, serverip) VALUES( \"{RUN_PURPOSE}\" , {int(ts)}, {int(iteration)}, \"{DNA_RELEASE}\", {int(ATN)},{int(CLOUD_XP)},{int(DON)},{int(OA)}, {int(OLA)}, {int(ROADM)}, {int(XT)} ,{int(GROOVE)},   {int(time_elapsed)} , \"{str(DNA_IP)}\")"
            sqlcursor.execute(data)
            sqldb.commit()
        time.sleep(interval)
        logger.info(f" Sample: {iteration}. | ATN = {ATN}, CX = {CLOUD_XP}, DON = {DON}, OA = {OA}, OLA = {OLA}, ROADM = {ROADM}, XT = {XT}, GROOVE = 0, XTM = 0")


logger.info('Shutting down DNA')
shutdown_DNA(DNA_IP,DNA_USER_NAME, DNA_USER_PASSWORD, EMS_PATH)

time.sleep(60)

try:
    if DNA_DB_TYPE.lower()=='oracle' :
        dsn_tns = cx_Oracle.makedsn ( DNA_IP, DNA_DB_PORT,
                                      service_name=DNA_DB_NAME )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect ( user=DNA_DB_USERNAME, password=DNA_DB_PASSWD,
                                   dsn=dsn_tns )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        mycursor = conn.cursor ( )
        mycursor.execute (
            f"select max(dbinsertiontimestamp) from htbl_dnaevent where eventtype = 'DD_END'" )
    else:
        mydb = mysql.connector.connect ( host=DNA_IP, user=DNA_DB_USERNAME, passwd=DNA_DB_PASSWD,   database=DNA_DB_NAME )
        mycursor = mydb.cursor ( )
        mycursor.execute (
            f"select max(dbinsertiontimestamp) from {DNA_DB_NAME}.htbl_dnaevent where eventtype = 'DD_END'" )

    latest_timestamp = int ( next ( mycursor )[0] )

except:
    logger.exception('Error reading timestamp from DNA DB')

logger.info('Warm Starting DNA')
WarmStart_DNA(DNA_IP,DNA_USER_NAME, DNA_USER_PASSWORD,EMS_PATH)
logger.info('Doing periodic DB queries')
try:
    if DNA_DB_TYPE.lower()=='oracle' :
        periodic_db_ORACLE(DNAIP=DNA_IP, DNADB_USERNAME = DNA_DB_USERNAME, DNADB_PASSWD=DNA_DB_PASSWD, DNADB_PORT=DNA_DB_PORT, interval=int(INTERVAL),  total_duration=int(TOTAL_DURATION))
    else:
        periodic_db(DNA_IP=DNA_IP, DNA_DB_USERNAME = DNA_DB_USERNAME, DNA_DB_PASSWD=DNA_DB_PASSWD, interval=int(INTERVAL), total_duration=int(TOTAL_DURATION))
except :
    logger.exception('DB queries failed')

logger.info("Script execution completed")
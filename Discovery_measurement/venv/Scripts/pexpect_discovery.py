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



#
# dsn_tns = cx_Oracle.makedsn ( '10.220.5.169', '1521',
#                               service_name='emsdb' )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
# conn = cx_Oracle.connect ( user='DNAUser', password='emsdb',
#                            dsn=dsn_tns )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
# cur = conn.cursor ( )

mydb = mysql.connector.connect ( host='10.220.5.129', user='DNAUser', passwd='emsdb', database='emsdb' )
cur = mydb.cursor ( )
cur.execute (
            f"SELECT count(distinct(eventstringdata2)),eventstringdata3  FROM emsdb.htbl_dnaevent where (eventtype = \'DD_END\' and dbinsertiontimestamp > 1576230806496) OR (eventsourcemodule like \'%Groove%\' and eventtype =\'SD_END\' and dbinsertiontimestamp > 1576230806496 ) group by eventstringdata3 " )
for i in cur:
    print(i[0], i[1].decode('ascii'))
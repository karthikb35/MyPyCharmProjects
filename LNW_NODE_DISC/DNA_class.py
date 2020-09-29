import socket
import sys
import os
# from sample import *
import telnetlib
import time
class DNA():
    def __init__(self, IP, usr = 'root', passwd = 'infinera1', connection_protocol = 'Telnet', gui_user_id = 'admin', gui_passwd='infinera1' ):
        self.IP = IP
        self.connection_protocol = connection_protocol
        self.server_user_id = usr
        self.server_passwd = passwd
        self.gui_user_id = gui_user_id
        self.gui_passwd = gui_passwd
        self.install_path = '/u02/app/karthik'
        # self.db_user_id = db_user_id
        # self.db_passwd = db_passwd

    # def telnet_to_DNA( self ):
    #
    #     return telnet_to_server(self.IP, self.server_user_id, self.server_passwd)

    def shutdown_DNA( self ):
        print(self.connection_protocol.lower())
        if self.connection_protocol.lower() == 'telnet':
            tn = telnetlib.Telnet('10.220.5.126')
            tn.read_until ( b"login: ", timeout=2 )
            time.sleep ( 1 )
            print(tn.read_all().decode('ascii'))
            tn.write ( self.server_user_id.encode ( 'ascii' ) + b"\n" )
            time.sleep ( 1 )
            print ( tn.read_all ( ).decode ( 'ascii' ) )
            tn.read_until ( b"Password: ", timeout=2 )
            time.sleep ( 1 )
            print ( tn.read_all ( ).decode ( 'ascii' ) )
            tn.write ( self.server_passwd.encode ( 'ascii' ) + b"\n" )
            time.sleep ( 1 )
            tn.read_until ( b"# ", timeout=5 )
            print ( tn.read_all ( ).decode ( 'ascii' ) )
            binary_path = f"{self.install_path}/EMS/bin"
            print(binary_path)
            tn.write ( b"cd " + binary_path.encode('ascii')+ b"\n")
            tn.expect(["# ".encode('ascii')], 5)
            tn.write(b"./ShutDown.sh" + self.gui_user_id.encode('ascii')+self.gui_passwd.encode('ascii')+ b"\n\n")
            print ( tn.read_all ( ).decode ( 'ascii' ) )
            tn.write(b" tail -f ../logs/startup.log\n\n")
            print ( tn.read_all ( ).decode ( 'ascii' ) )

            output = tn.read_until("DNA Server Shutdown successful...", timeout=15*60)
            if "DNA Server Shutdown successful..." in output:
                tn.write('\x03')
                print ( tn.read_all ( ).decode ( 'ascii' ) )
                tn.write ( b"exit\n" )
                print ( tn.read_all ( ).decode ( 'ascii' ) )
                tn.close()
                print("Shutdown successful")
                return 1
            return 0








x= DNA("10.220.5.126", 'root', 'infinera1')
x.shutdown_DNA()



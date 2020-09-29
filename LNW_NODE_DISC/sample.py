import telnetlib
import sys
import getpass
import time



def telnet_to_server(IP, usr, passwd):
     try:
        tn= telnetlib.Telnet(IP)
        tn.read_until(b"login: ",  timeout=2)
        time.sleep(1)
        tn.write(usr.encode('ascii')+ b"\n")
        time.sleep(1)
        tn.read_until(b"Password: ",  timeout=2)
        time.sleep(1)
        tn.write ( passwd.encode ( 'ascii' ) + b"\n" )
        time.sleep(1)
        tn.read_until ( b"# ", timeout=5 )
        tn.write ( b"ls\n")


        print ( tn.read_all ( ).decode ( 'ascii' ) )
        tn.write(b"pwd\n")


        print ( tn.read_all ( ).decode ( 'ascii' ) )
        # tn.expect(["# ".encode('ascii')], 5)
        #
        # install_path='/u02/app/karthik'
        #
        #
        # gui_user_id = 'admin'
        # gui_passwd = 'infinera1'
        # binary_path = f"{install_path}/DNA/EMS/bin"
        # print ( binary_path )
        # tn.write ( b"cd " + binary_path.encode ( 'ascii' ) + b"\n" )
        # # tn.expect ( ["# ".encode ( 'ascii' )], 5 )
        # tn.write ( b"./ShutDown.sh " + gui_user_id.encode ( 'ascii' ) + b" " +gui_passwd.encode ( 'ascii' ) + b"\n\n" )
        # print ( tn.read_all ( ).decode ( 'ascii' ) )
        # tn.write ( b" tail -f ../logs/startup.log\n\n" )
        # print ( tn.read_all ( ).decode ( 'ascii' ) )
        #
        # output = tn.read_until ( b"DNA Server Shutdown successful...", timeout=15 * 60 )
        # if "DNA Server Shutdown successful..." in output.decode('ascii'):
        #     tn.write ( '\x03' )
        #     print ( tn.read_all ( ).decode ( 'ascii' ) )
        #     tn.write ( b"exit\n" )
        #     print ( tn.read_all ( ).decode ( 'ascii' ) )
        #     tn.close ( )
        #     print ( "Shutdown successful" )
        #     # return 1

        tn.write ( b"exit\n" )
        print ( tn.read_all ( ).decode ( 'ascii' ) )



        #c= tn.read_until(b"# ", timeout=5)
        return tn



    # except:
    #     print("failed")
    #     return 0

telnet_to_server("10.220.5.126", "root", "infinera1")

    # print(c)
    # i = "/u02/app/karthik/DNA/EMS"
    # tn.write(b"cd " + i.encode('ascii') + b"\n")
    # time.sleep(2)
    # tn.write(b"exit\n")
    # print(tn.read_all().decode('ascii'))

# import pexpect
#
# import time,sys
# #
# # pexpect.spawn()
# telconn = pexpect.popen_spawn.PopenSpawn('10.220.5.126')
# time.sleep(20)
# telconn.logfile = sys.stdout
# telconn.expect(":")
# time.sleep(20)
# telconn.send("root" + "\r")
# telconn.expect(":")
# telconn.send("infinera1" + "\r")
# telconn.send("\r\n")
# time.sleep(20)
# telconn.expect("#")

from pacelib.Simulator.Setup import CardType
from pacelib.GRPC.GRPCLib import *
from pacelib.security.User import *
from pacelib.ntp.NTP import *
from pacelib.declarative_config.DeclarativeConfig import *
from pace.neapi.operations import *
from pace.utility.parser import checkSystemRechability
from pacelib.SW.SW import *
import json
import sys, os




system_under_test = "LocalNode"
software_image = SW ( sut=system_under_test, image_name=SetupConfig.getSetupEnvDict ( )["Common"]["Variables"]["ImageName"], image_verification= SetupConfig.getSetupEnvDict ( )["Common"]["Variables"]["ImageName"])

print(software_image)

env = 'ThanOSServer_1'
vm_setup = SW ( sut=env )

def create_setup ( vm_name, template='template1' ):
    cmd = f'chassisx.py create {vm_name} {template}'
    NE_SSH ( sut=env, cmd=cmd, appId='setup' )
    time.sleep ( 240 )
    cmd = f'chassisx.py start chassis {vm_name}'
    NE_SSH ( sut=env, cmd=cmd, appId='setup' )
    time.sleep ( 120 )


def config_dcn ( vm_name, ipaddr, netmask, gateway ):
    cmd = f'virsh console {vm_name}_cc1 --force'
    NE_SSH ( sut=env, cmd=cmd, toVerify={Output.CONTAINS: ['Escape character is ^]']}, waitTime=60, appId='setup' )
    NE_SSH ( sut=env, cmd='', toVerify={Output.CONTAINS: ['localhost login:']}, waitTime=60, appId='setup' )
    NE_SSH ( sut=env, cmd='root', toVerify={Output.CONTAINS: ['Password:']}, waitTime=10, appId='setup' )
    NE_SSH ( sut=env, cmd='onl', toVerify={Output.CONTAINS: ['root@localhost:~#']}, waitTime=10, appId='setup' )
    print ( 'Connected to VM' )

    cmd = '/opt/infinera/thanos/local/bin/client'
    NE_SSH ( sut=env, cmd=cmd, toVerify={Output.CONTAINS: ['root@THANOS>']}, waitTime=30, appId='setup' )
    # # 1. Loopback IP
    # NE_SSH ( sut=env, cmd="add ipv4-address-1-loopback-mgmt/2.2.2.99 netmask 255.255.255.255", waitTime=5,
    #          appId='setup' )

    # 2. DCN
    cmd = f'add ipv4-address-DCN/{ipaddr} netmask {netmask}'
    NE_SSH ( sut=env, cmd=cmd, toVerify={Output.CONTAINS: ['root@THANOS>']}, appId='setup' )

    # 3. Static Route
    cmd = f'add ipv4-static-route-0.0.0.0/0/MGMT next-hop-address {gateway}'
    NE_SSH ( sut=env, cmd=cmd, toVerify={Output.CONTAINS: ['root@THANOS>']}, appId='setup' )
    #
    # NE_SSH ( sut=env, cmd='ping 10.220.224.136', waitTime=5, appId='setup',
    #          toVerify={Output.CONTAINS: ['64 bytes from 10.220.224.136:']} )
    NE_SSH ( sut=env, cmd='exit -f', appId='setup' )


@pytest.fixture()
def del_old_setup ( ):
    vm_name = SetupConfig.getSetupEnvDict ( )[env]['Global']['vmName'].strip ( )
    user = 'karthik'
    cmd = f'chassisx.py delete chassis {vm_name}'
    NE_SSH ( sut=env, cmd=cmd, appId=1, toVerify={Output.CONTAINS: [f'{user}@']} )
    time.sleep ( 30 )

@pytest.fixture()
def check_system_reachability ( ):
    if not checkSystemRechability ( ip=SetupConfig.getSetupEnvDict ( )[system_under_test]["Login"]["IpAddress"],
                                    maxTime=10 ):
        print(system_under_test)
        pytest.skip ( "System under test is not reachable.. Hence skipping the test.." )

@pytest.fixture()
def verify_installation_status ( ):
    software_image.verify_installed_image ( )



def test_JIRA_THANOS_6972(del_old_setup):
    """
    Create template1 VM setup and configures DCN IP
    """
    vm_name = SetupConfig.getSetupEnvDict()[env]['Global']['vmName'].strip()
    ipaddr = SetupConfig.getSetupEnvDict()[system_under_test]['Login']['IpAddress'].strip()
    netmask = SetupConfig.getSetupEnvDict()[system_under_test]['Login']['Netmask'].strip()
    gateway = SetupConfig.getSetupEnvDict()[system_under_test]['Login']['Gateway'].strip()
    create_setup(vm_name, template='template0')
    # time.sleep(60*3*2)
    # config_dcn(vm_name, ipaddr, netmask, gateway)


def test_JIRA_THANOS_6429():

    """ Image installation via CLI and configuring DCN IP via CLI"""

    #1. Dowloads build from artifactory location to thanos-server
    #2. Downloads the image to the NE via CLI Interface via SFTP Protocol
    #3. Installs image on the chassis
    #4. Verify that the pre-upgrade went fine.
    #5. Activates the newly downloaded software.
    #6. Waits for 300 seconds for activation to complete.
    #7. Once installation is done, Script connects to the console of the VM and login to the CLI Interface and perform DCN IP configuration.
    #8. Verfies whether the image has been installed from the CLI interface.

    if str ( SetupConfig.getSetupEnvDict ( )["Common"]["Variables"][
                 "DownloadImageFromArtifactory"] ).upper ( ) == "TRUE":

        artifactory_path = SetupConfig.getSetupEnvDict ( ).get ( "Common" ).get ( "Variables" ).get ( "ArtifactoryPath",
                                                                                                      None )

        software_image.download_image_from_artifactory ( thanos_server="ThanOSServer_1",
                                                         artifactory_path=artifactory_path, local_download_path=
                                                         SetupConfig.getSetupEnvDict ( )["ThanOSServer_1"]["Global"][
                                                             "BuildPath"] )
        logger.info('Done downloading build to Sim server')
    else:

        #TODO : Plugin API to download image from other server and update image Name and image_verification file
        # Added this for CI Sanity to proceed
        logger.debug("Intentionally failing this now.. Need to be removed once TODO is completed")
        pytest.evaluate(False)

    software_image.download(file_transfer_mode="sftp",image_location_details={"username"    :  SetupConfig.getSetupEnvDict()["ThanOSServer_1"]["Login"]["UserName"],
                                                                              "password"    :  SetupConfig.getSetupEnvDict()["ThanOSServer_1"]["Login"]["Password"],
                                                                              "ServerIP"    :  SetupConfig.getSetupEnvDict()["ThanOSServer_1"]["Login"]["IpAddress"],
                                                                              "path"        :  SetupConfig.getSetupEnvDict()["ThanOSServer_1"]["Global"]["BuildPath"],},wait_time=240)

    # Pre-upgrade retry time is marked as 300. Not defined in SRD.. needs to be updated after SRD update
    logger.info("Pre-paring for Upgrade")
    software_image.install(pre_upgrade_wait_time=300)

    software_image.verify_installable_image(retry=30)

    #Activate wait time is 13 mins now. Needs to be changed as per SRD.
    logger.info("Activating SW")
    software_image.activate(wait_time=780)
    logger.info ( "Activated SW. Sleeping for 300 seconds for NE bring-up" )
    time.sleep(380)
    software_image.verify_installed_image()
    logger.info ( "Configuring DCN" )
    vm_name = SetupConfig.getSetupEnvDict ( )[env]['Global']['vmName'].strip ( )
    ipaddr = SetupConfig.getSetupEnvDict ( )[system_under_test]['Login']['IpAddress'].strip ( )
    netmask = SetupConfig.getSetupEnvDict ( )[system_under_test]['Login']['Netmask'].strip ( )
    gateway = SetupConfig.getSetupEnvDict ( )[system_under_test]['Login']['Gateway'].strip ( )

    config_dcn ( vm_name, ipaddr, netmask, gateway )





import json
import mysql.connector
from Deserialization_example import *
import telnetlib
import time


from Deserialization_example import DNA_DB_PASSWD, DNA_DB_USERNAME, DNA_IP


class CarrierCtp:

    def __init__(self, moid, node_id, node_name, aid):
        self.moid = moid
        self.alarm_state = "CLEAR"
        self.label = None
        self.lifecycle_state = None
        self.node_id = node_id
        self.node_name = node_name
        self.aid = aid
        mydb = mysql.connector.connect ( host=DNA_IP, user=DNA_DB_USERNAME, passwd=DNA_DB_PASSWD, database='emsdb' )
        mycursor = mydb.cursor ( )
        mycursor.execute ( f'SELECT frequency, modulation, baudrate, INSTFECITERATIONS, FFCRMODE, CHROMATICDISPERSIONSET, FFCRAVERAGING, CDCOMPMODE, INSTTXCD, FFCRBLOCKSIZE , CLOCKMODE, GAINSHARING, PROVLATENCY, NLCSETTING  FROM emsdb.htbl_carrierctp where moid =   "{str ( self.moid )}" ' )
        for i in mycursor:
            self.carrier_center_frequency, self.modulation , self.baud_rate = (i[x] for x in range(3))
            self.fec_iterations = i[3]
            self.ffcr_mode = i[4].decode('ascii')
            self.cd_value= i[5]
            self.ffcr_averaging= i[6].decode('ascii')
            self.cd_mode= i[7].decode('ascii')
            self.tx_cd= i[8]
            self.ffcr_block_size= i[9]
            self.clock_mode= i[10]
            self.gain_sharing_mode= i[11].decode('ascii').upper()
            self.carrier_latency= i[12].decode('ascii')
            self.nlc_setting = i[13]

        self.modulation = (self.modulation.decode('ascii')).replace('_', '-')
        self.baud_rate = (self.baud_rate.decode('ascii')).split('_')[1]
        # print(self.carrier_center_frequency, self.modulation, self.baud_rate)
        baud_rate_map = { '17G' : 17000 , '22G' : 25000 , '33G': 33000}
        self.carrier_width = baud_rate_map[self.baud_rate]
        self.ice4_paramters = {
            "fec_iterations": str(self.fec_iterations),
            "ffcr_mode": self.ffcr_mode,
            "cd_value": self.cd_value,
            "ffcr_averaging": self.ffcr_averaging,
            "cd_mode": self.cd_mode,
            "tx_cd": self.tx_cd,
            "ffcr_block_size": str(self.ffcr_block_size),
            "clock_mode": str(self.clock_mode),
            "gain_sharing_mode": self.gain_sharing_mode,
            "carrier_latency": self.carrier_latency,
            "nlc_setting": str(self.nlc_setting)
        }
        self.advanced_parameters = json.dumps(self.ice4_paramters)
        self.data = {
            "qvalueBaseline": {
                "QValueType": 17.0
            },
            "qvalueCommissioningLimit": {
                "QValueType": 17.0
            },
            "moid": self.moid,
            "endpoint_identifier": {
                "aid": self.aid,
                "node_id": self.node_id,
                "node_name": self.node_name
            },
            "modulation": self.modulation,
            "baud_rate": self.baud_rate,
            "alarm_state": "CLEAR",
            "label": None,
            "carrier_width": {
                "frequency": int(self.carrier_width)
            },
            "administrative_state": "UNLOCKED",
            "ice4-paramters" : self.ice4_paramters,
            "advanced_parameters": self.advanced_parameters,
            "advanced_parameters_payload_type_enum": "ICE4",
            "lifecycle_state": None,
            "carrier_center_frequency": {
                "frequency": int(self.carrier_center_frequency)
            },
            "operational_state": "ENABLED"
        }






        # self.operational_state="ENABLED"
        # self.qvalueBaseline = 1
        # self.qvalueCommissioningLimit=1





class SchCtp:
    def __init__(self, moid, aid, node_id, node_name):
        self.moid = moid
        self.frequency_slot_plan_type = 'FFREQ_SLOT_PLAN_NONE'
        self.super_channel_number = None
        self.aid = aid
        self.node_id=node_id
        self.node_name=node_name
        self.alarm_state = "CLEAR"
        self.label = None
        self.igcc_config_enable_igcc = True
        self.igcc_config_lifecycle_state = None
        self.operational_state = "DISABLED"
        self.administrative_state = "UNLOCKED"
        self.lifecycle_state = None


        mydb = mysql.connector.connect ( host=DNA_IP, user=DNA_DB_USERNAME, passwd=DNA_DB_PASSWD, database='emsdb' )
        mycursor = mydb.cursor ( )
        mycursor.execute ( f'select PASSBANDLIST from emsdb.htbl_schctp where MOID =  "{str(self.moid)}" '  )
        for i in mycursor:
            self.start_frequency, self.end_frequency = str ( i[0].decode ( 'ascii' ) ).split ( '#' )

        mydb = mysql.connector.connect ( host=DNA_IP, user=DNA_DB_USERNAME, passwd=DNA_DB_PASSWD, database='emsdb' )
        mycursor = mydb.cursor ( )
        mycursor.execute ( f'SELECT netmask,ipaddress FROM emsdb.htbl_igcc where MOID = "/{str(self.node_id)}/IGCC={str(self.aid)}"')
        for i in mycursor:
            #print(i[0].decode('ascii') , i[1].decode('ascii'))
            self.igcc_config_netmask = str(i[0].decode('ascii'))
            self.igcc_config_ip_address = str(i[1].decode('ascii'))
        self.carrier_list = self.get_associated_carrier_list()
        self.data = {
            "endpoint_identifier": {
                "aid": self.aid,
                "node_id": self.node_id,
                "node_name": self.node_name
            },
            "passband_list": [
                {
                    "index": "0",
                    "start-frequency": {
                        "frequency": int(self.start_frequency)
                    },
                    "end-frequency": {
                        "frequency": int(self.end_frequency)
                    }
                }
            ],
            "alarm_state": "CLEAR",
            "carrier_list": [
            i.data
            for i in self.carrier_list],
            "alarm_state": "CLEAR",
            "protection_q_limit": {
                "QValueType": 9.0
            },
            "label": None,
            "igcc-config": {
                "netmask": self.igcc_config_netmask,
                "ip_address": self.igcc_config_ip_address,
                "enable_igcc": True,
                "lifecycle_state": None
            },
            "operational_state": "DISABLED",
            "moid": self.moid,
            "administrative_state": "UNLOCKED",
            "lifecycle_state": None,
            "frequency_slot_plan_type": "FFREQ_SLOT_PLAN_NONE",
            "sch_type": "LM",
            "super_channel_number": None
        }





    def get_associated_carrier_list( self ):
        mydb = mysql.connector.connect ( host=DNA_IP, user=DNA_DB_USERNAME , passwd=DNA_DB_PASSWD , database='emsdb')
        mycursor = mydb.cursor ( )
        mycursor.execute ( f'select supportedobjectstr from emsdb.htbl_schctp where MOID = "{str(self.moid)}" ' )
        for i in mycursor:
            supported_obj_list = str ( i[0].decode ( 'ascii' ) ).split ( ',' )
            carrier_list = []
            for item in supported_obj_list:
                if 'CARRIERCTP' in item:
                    c_aid = item.split('=')[1]
                    carrier_list.append ( CarrierCtp(f'/{self.node_id}/CARRIERCTP={c_aid}' , self.node_id, self.node_name, c_aid)  )
        return carrier_list

class Oxcon:
    def __init__(self, node_name, aid, node_id , moid):
        self.node_name = node_name
        self.aid = aid
        self.node_id = node_id
        self.moid = moid
        self.lifecycle_state = None
        self.operational_state = "ENABLED"
        self.cross_connect_type = "Bidirection"
        self.super_channel_number = None
        self.administrative_state = "UNLOCKED"
        self.frequency_slot_plan_type = 'FFREQ_SLOT_PLAN_NONE'

        self.aep_aid = self.aid.split('%')[0]
        self.zep_aid = self.aid.split('%')[1]
        mydb = mysql.connector.connect ( host=DNA_IP, user=DNA_DB_USERNAME, passwd=DNA_DB_PASSWD, database='emsdb' )
        mycursor = mydb.cursor ( )
        mycursor.execute ( f'SELECT passbandlist, carrierlist, xctype , rxschpoweroffset, schpoweroffset , BAUDRATEDISPVAL FROM emsdb.htbl_oxcon where MOID =   "{self.moid}" ' )
        for i in mycursor:
            self.start_frequency, self.end_frequency = i[0].decode().split('#')[0] , i[0].decode().split('#')[1]
            carrier_list_decoded_list = i[1].decode().split(',')
            self.carrier_list_dict = [
                {
                    "carrier_width": {
                      "frequency":  int(j.split('#')[1])
                    },
                    "carrier-center-frequency": {
                        "frequency": int(j.split('#')[0])
                    }
                } for j in carrier_list_decoded_list

            ]

            self.connectivity_type = i[2].decode()
            self.rx_sch_power_offset = float(i[3])
            self.sch_power_offset = float(i[4])
            self.baudrate = i[5].decode()
            self.data = {
                "passband_list": [
                    {
                        "index": "0",
                        "start-frequency": {
                            "frequency": int(self.start_frequency)
                        },
                        "end-frequency": {
                            "frequency": int(self.end_frequency)
                        }
                    }
                ],
                "lifecycle_state": self.lifecycle_state,
                "carrier_list": self.carrier_list_dict,
                "aep_aid": {
                    "aid": self.aep_aid,
                    "node_id": self.node_id,
                    "node_name": self.node_name
                },
                "connectivity_type": self.connectivity_type,
                "operational_state": "ENABLED",
                "cross-connect-type": "Bidirection",
                "zep_aid": {
                    "aid": self.zep_aid,
                    "node_id": self.node_id,
                    "node_name": self.node_name
                },
                "baud_rate": self.baudrate,
                "moid": self.moid,
                "administrative_state": "UNLOCKED",
                "sch_power_offset": {
                    "power-dBm": float(self.sch_power_offset)
                },
                "rx_sch_power_offset": {
                    "power-dBm": float(self.rx_sch_power_offset)
                },
                "label": ROS_name+ " " + E2E_Path_name+ " " +Optical_Service_name,
                "frequency_slot_plan_type": "FFREQ_SLOT_PLAN_NONE",
                "node_id": None,
                "super_channel_number": None
            }






        # self.baud_rate

        # self.sch_power_offset
        # self.rx_sch_power_offset
        # self.label

        # self.node_id

class protected_oxcon(Oxcon):
    def __init__(self, node_name, aid, node_id , moid):
        super().__init__(node_name, aid, node_id , moid)
        self.linesch_aid = self.aid.split('%')[1]
        self.baseline_sch_power = 1.7
        mydb = mysql.connector.connect ( host=DNA_IP, user=DNA_DB_USERNAME, passwd=DNA_DB_PASSWD, database='emsdb' )
        mycursor = mydb.cursor ( )
        mycursor.execute ( f'SELECT PGAID from emsdb.htbl_oxcon where MOID =   "{self.moid}" ' )
        for i in mycursor:

            self.pg_aid = i[0].decode()
            print(self.pg_aid)
            print(self.node_id)
        mycursor.execute ( f'SELECT MOID from emsdb.htbl_oxcon where PGAID =   "{self.pg_aid}" and FREQUENCYSLOTPLANTYPE = "FREQ_SLOT_PLAN_ASE_IDLER" and HIBNODEID = "{self.node_id}"' )
        for i in mycursor:
            #print("h ==" + i[0].decode())
            self.ase_moid = i[0].decode()
        mycursor.execute(f'SELECT DCNIP from emsdb.htbl_toponode where MENAME =  ' + f'"{self.node_name}" ' )
        for i in mycursor:
            self.node_ip = i[0].decode()
        tn = telnetlib.Telnet(self.node_ip, port = 9090)
        s1 = tn.read_until ( b">>", timeout=2 )
        cmd = f'rtrv-pm-SCH::{self.linesch_aid}:a::;'
        tn.write (b'act-user::secadmin:a::Infinera2!;;')
        s2 = tn.read_until ( b">>", timeout=2 )
        tn.write(cmd.encode('utf-8'))
        s2= tn.read_until ( b">>", timeout=2 )

        time.sleep ( 1 )

        s3 = tn.read_until ( b">>", timeout=2 )
        tn.write ( cmd.encode('utf-8') )
        s5 = tn.expect ( [b",,NEND"], 2 )

        i = s5[2].decode ( ).split ( ',' )

        x = i.index ( 'SCH:OPT' )
        self.baseline_sch_power = float(i[x+1])
        self.ase_aep = (self.ase_moid.split('=')[1]).split('%')[0]
        self.ase_zep = (self.ase_moid.split ( '=' )[1]).split ( '%' )[1]
        self.data = {
        "pg-moid": "/"+self.node_id+"/OPTICAL_SCH_PG="+self.pg_aid,
        "signal_oxcon": {
            "passband_list": [
                {
                    "index": "0",
                    "start-frequency": {
                        "frequency": int(self.start_frequency)
                    },
                    "end-frequency": {
                        "frequency": int(self.end_frequency)
                    }
                }
            ],
            "lifecycle_state": None,
            "carrier_list":  self.carrier_list_dict,

            "aep_aid": {
                "aid": self.aep_aid,
                "node_id": self.node_id,
                "node_name": self.node_name
            },
            "connectivity_type": "AddDrop",
            "operational_state": "ENABLED",
            "cross-connect-type": "Bidirection",
            "zep_aid": {
                "aid": self.zep_aid,
                "node_id": self.node_id,
                "node_name": self.node_name
            },
            "baud_rate": self.baudrate,
            "moid": self.moid,
            "administrative_state": "UNLOCKED",
            "sch_power_offset": {
                "power-dBm": float(self.sch_power_offset)
            },
            "rx_sch_power_offset": {
                "power-dBm": float(self.rx_sch_power_offset)
            },
            "label": None,
            "frequency_slot_plan_type": "FFREQ_SLOT_PLAN_NONE",
            "node_id": None,
            "super_channel_number": None
        },
        "ase_oxcon": {
            "passband_list": [
                {
                    "index": "0",
                    "start-frequency": {
                        "frequency": int(self.start_frequency)
                    },
                    "end-frequency": {
                        "frequency": int(self.end_frequency)
                    }
                }
            ],
            "lifecycle_state": None,
            "carrier_list": self.carrier_list_dict,

            "aep_aid": {
                "aid": self.ase_aep,
                "node_id": self.node_id,
                "node_name": self.node_name
            },
            "connectivity_type": "AddDrop",
            "operational_state": "ENABLED",
            "cross-connect-type": "Bidirection",
            "zep_aid": {
                "aid": self.ase_zep,
                "node_id": self.node_id,
                "node_name": self.node_name
            },
            "baud_rate": "NA",
            "moid": self.ase_moid,
            "administrative_state": "UNLOCKED",
            "sch_power_offset": {
                                        "power-dBm": 0.0
                                    },
            "rx_sch_power_offset": {
                                        "power-dBm": 0.0
                                    },
            "label": "",
            "frequency_slot_plan_type": "FREQ_SLOT_PLAN_ASE_IDLER",
            "node_id": None,
            "super_channel_number": None
    },
            "passband_resize_config": {
                "resize-steps": Passband_step,
                "passband_resizing_order": passband_resizing_order
            },
            "baseline_sch_power": {
                "power-dBm": self.baseline_sch_power
            }
        }
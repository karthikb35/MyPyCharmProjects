import cx_Oracle

class BMM:
    def __init__(self, nodeid, aid):
        self.nodeid = nodeid
        self.aid = aid
        self.ocg = []
        self.sncs = []
    def get_ocg( self ):
        dsn_tns = cx_Oracle.makedsn ( '10.220.160.155', '1521',
                                      service_name='emsdb' )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect ( user=r'DNAUser', password='emsdb',
                                   dsn=dsn_tns )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        cur = conn.cursor ( )
        cur.execute (
            f'select MOID from htbl_bmmocgptp  where HIBNODEID = \'{self.nodeid}\' and SUPPORTINGOBJECTSTR = \'BMM={self.aid}\' ' )
        for i in cur:
            self.ocg.append(BMMOCG(i[0]))
    def get_sncs( self ):
        for ocg in self.ocg:
            dsn_tns = cx_Oracle.makedsn ( '10.220.160.155', '1521',
                                          service_name='emsdb' )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
            conn = cx_Oracle.connect ( user=r'DNAUser', password='emsdb',
                                       dsn=dsn_tns )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
            cur = conn.cursor ( )
            cur.execute (
                f'select MOID from htbl_bmmocgptp  where HIBNODEID = \'{self.nodeid}\' and SUPPORTINGOBJECTSTR = \'BMM={self.aid}\' ' )
            for i in cur:
                self.ocg.append ( BMMOCG ( i[0] ) )

class BMMOCG:
    def __init__(self, MOID):
        self.moid = MOID
        dsn_tns = cx_Oracle.makedsn ( '10.220.160.155', '1521',
                                      service_name='emsdb' )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
        conn = cx_Oracle.connect ( user=r'DNAUser', password='emsdb',
                                   dsn=dsn_tns )  # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'
        cur = conn.cursor ( )
        cur.execute (
            f'select PROVISIONEDOCGTP from htbl_bmmocgptp where moid = \'{self.moid}\' ')
        self.discoveredocgtp = next(cur)[0]



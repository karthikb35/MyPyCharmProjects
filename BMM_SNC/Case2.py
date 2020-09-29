import cx_Oracle


dsn_tns = cx_Oracle.makedsn('10.220.5.169', '1521', service_name='emsdb') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
conn = cx_Oracle.connect(user=r'DNAUser', password='emsdb', dsn=dsn_tns) # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

# con = cx_Oracle.connect('DNAUser/emsdb@10.220.160.155/orcl')
node_id_list = []
cur = conn.cursor()
cur.execute( f"SELECT count(eventtype), eventstringdata3 FROM htbl_dnaevent where (eventtype = \'DD_END\' and dbinsertiontimestamp > 1579513369882) group by eventstringdata3 ")
for i in cur:
    print(i[0], i[1])


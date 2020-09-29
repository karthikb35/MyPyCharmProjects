import mysql.connector

class UseDatabase():
    def __init__(self, config):
        self.config = config

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect ( **self.config )
            self.cursor = self.conn.cursor ( )
            return self.cursor
        except Exception as err:
            print('got exception: ' + str(err))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

# db_config = {'host': '127.0.0.1',
#              'user': 'vsearch',
#              'password' : 'vsearchlogDB',
#              'database' : 'vsearchlogDB'}
# with UseDatabase(db_config) as cursor:
#     cursor.execute("""show tables""")
#     data = cursor.fetchall()
#     print(data)
import pymysql
import pymysql.cursors
 
 
def connect():
    """ Connect to MySQL database """
    try:
        conn = pymysql.connect(host='45.55.0.197',
                                       database='jobdb',
                                       user='vvaradar',
                                       password='arjkar123')
        if conn.:
            print('Connected to MySQL database')
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()
 
 
if __name__ == '__main__':
    connect()
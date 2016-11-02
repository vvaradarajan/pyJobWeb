import pymysql
import pymysql.cursors
 
 
def connect():
    """ Connect to MySQL database """
    try:
        conn = pymysql.connect(host='45.55.0.197',
                                       database='jobdb',
                                       user='vvaradar',
                                       password='arjkar123')
        if conn.open:
            print('Connected to MySQL database')
            testCursor=conn.cursor()
            sql='select * from junk'
            testCursor.execute(sql)
            for row in testCursor:
                print (row)
            isql="insert into junk(i) values(%s)"
            for i in range(2,10):
                testCursor.execute(isql,i)
            conn.commit()
                
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()
 
 
if __name__ == '__main__':
    connect()
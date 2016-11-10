import pymysql
import pymysql.cursors
import json
class job:
    #(jobId:String,jobClass:String,jobPrams:String)
    @staticmethod
    def getJob(jobId,jobClass,jobParams):
        job=[]
        job.append(jobId)
        job.append(jobClass)
        job.append(jobParams)
        return job
    @staticmethod 
    def getJobList(categ):
        try:
            conn = pymysql.connect(host='45.55.0.197',
                                           database='jobdb',
                                           user='vvaradar',
                                           password='arjkar123')
            if conn.open:
                print('Connected to MySQL database')
                testCursor=conn.cursor()
                sql= "select j.jobId,j.jobClass,j.jobParams from jobs j inner join jobCategory jc " \
                    + " on j.jobid=jc.jobid and jc.category='"+categ+"'"
                print(sql)
                testCursor.execute(sql)
                jobList=[] #return array of jobs - each job an array of Strings
                hdr=testCursor.description #returns an array of nm, type,etc for each column
                jobList.append(job.getJob(hdr[0][0],hdr[1][0],hdr[2][0]))
                for row in testCursor:
                    jobList.append(job.getJob(row[0],row[1],row[2]))
                return jobList
            else:
                print('Conn not open: '+conn.open)       
 
        except Exception as e:
            print(e)
 
        finally:
            conn.close()
 
    @staticmethod
    def getJobListOld():
        jobList=[] #return array of jobs - each job an array of Strings
        jobList.append(job.getJob("#Format: jobId","jobClass","jobParams"))
        jobList.append(job.getJob("a","jobClass","{\"Dependents\":[\"d\",\"e\"],\"jobTime\":1}"))
        jobList.append(job.getJob("b","jobClass","{\"Dependents\":[\"d\",\"e\"],\"jobTime\":1}"))
        return jobList
    @staticmethod
    def getLinealTime(jobList):
        lt=0
        for j in jobList:
            print(j)
            if j[0].startswith('#'):
                pass
            else:
                try:
                    jb=json.loads(j[2]) #decode into json object
                    lt += jb['jobTime']
                except Exception as err:
                    print("json error for "+ j[2])
        return lt    
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
            sql= """select j.jobId,j.jobClass,j.jobParams from jobs j inner join jobCategory jc
 on j.jobid=jc.jobid and jc.category='ProjectG'"""
            testCursor.execute(sql)
            for row in testCursor:
                
                print (row)
#             isql="insert into junk(i) values(%s)"
#             for i in range(2,10):
#                 testCursor.execute(isql,i)
#             conn.commit()
        else:
            print('Conn not open: '+conn.open)       
 
    except Error as e:
        print(e)
 
    finally:
        conn.close()
 
 
if __name__ == '__main__':
    jl=job.getJobList("ProjectG")
    print('Lineal time = '+str(job.getLinealTime(jl)))
    #connect()
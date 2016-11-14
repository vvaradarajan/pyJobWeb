import pymysql
import pymysql.cursors
import json
def dbReconnect():
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except  Exception as inst:
                print ("DB error({0}):".format(inst))
                print ("Reconnecting")
                job.conn=None
                job.setConn()
            return function(*args, **kwargs)
        return wrapper
    return real_decorator
class job:
    #(jobId:String,jobClass:String,jobPrams:String)
    conn=None
    @staticmethod
    def setConn():
        if job.conn != None:
            #check for dead connection
            testCursor=job.conn.cursor()
            testCursor.execute("select 1")
            rows = testCursor.fetchall()
            if len(rows) <=0:
                jon.conn = None
            testCursor.close()
        if job.conn==None :
            job.conn = pymysql.connect(host='45.55.0.197',
                                           database='jobdb',
                                           user='vvaradar',
                                           password='arjkar123')
        if job.conn==None:
            print('Connect to database not made - aborting!' )
            sys.exit(1)
    @staticmethod
    def getJob(jobId,jobClass,jobParams):
        job=[]
        job.append(jobId)
        job.append(jobClass)
        job.append(jobParams)
        return job
    @staticmethod 
    @dbReconnect()
    def getJobList(categ):
        #job.setConn()
        sql= "select j.jobId,j.jobClass,j.jobParams from jobs j inner join jobCategory jc " \
        + " on j.jobid=jc.jobid and jc.category='"+categ+"'"
        print(sql)
        try:
            testCursor=job.conn.cursor()
            testCursor.execute(sql)
            jobList=[] #return array of jobs - each job an array of Strings
            hdr=testCursor.description #returns an array of nm, type,etc for each column
            jobList.append(job.getJob(hdr[0][0],hdr[1][0],hdr[2][0]))
            for row in testCursor:
                jobList.append(job.getJob(row[0],row[1],row[2]))
            testCursor.close()
            return jobList 
        except Exception as e:
            print(e)
            raise
            
        
    @staticmethod 
    @dbReconnect()
    def getJobCategList():
        job.setConn()
        sql = "select distinct category from jobCategory"
        try:
            testCursor=job.conn.cursor()
            testCursor.execute(sql)
            categList=[] #return array of jobs - each job an array of Strings
            for row in testCursor:
                categList.append(row[0])
            return categList 
        except Exception as e:
            print(e)
        finally:
            testCursor.close()
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
    @staticmethod
    def cleanup():
        job.conn.close()
if __name__ == '__main__':
    jl=job.getJobList("ProjectG")
    print('Lineal time = '+str(job.getLinealTime(jl)))
    print('category List = '+str(job.getJobCategList()))
    #connect()
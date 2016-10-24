'''
Created on Oct 15, 2016

@author: vasan
'''
import os
import errno
import json
import inspect
class jobStatus:
    '''Reads the status file and returns a json '''
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    ## The stuff below is to help in creating the google visualization data table
    @staticmethod
    def newColumn(self,colNM,colType):
        col={}
        col["id"]="";col['label']=colNM;col['pattern']="";col['type']=colType
        return col
        
    def convertJsonLineToGoogleDataTable(self,jsonline):
        #do the cols object
        print(jsonline.__class__)
        for key in jsonline:
            print (key, 'corresponds to', jsonline[key])
            jobset=jsonline[key]
            #explicitly put in the cols array (needs to be ordered!)
            cols=[]
            col=['jobId','idle','executing','complete']
            cols.append(col)
            col=['string','number','number','number']
            cols.append(col)
            #Now put the data in the order of the cols
            
            print(jobset.__class__)
            for job in jobset:
                print (job)
                row=[]
                for attr in cols[0]:
                    if attr in job:
                        row.append(job[attr])
                    else:
                         row.append(0)
                cols.append(row)
        print(cols)
        return cols
#         cols=[]
#         j=jsonline[0]
#         for k in j:
#           print (k)
        
        
        
        
    def getStatus(self):
        try:
            lf = os.open(self.lfNM, jobStatus.flags)
            os.close(lf)
        except OSError as e:
            if e.errno == errno.EEXIST:  # Failed as the file already exists.
                pass
            else:  # Notsure what the error is, so return nunn
                print("Unknown error: "+ e.errno);
            return {}    #return status
        #Read Json from file and returnhttps://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&ved=0ahUKEwiV_7CK193PAhVnsFQKHRZVB64QFggkMAI&url=http%3A%2F%2Fstackoverflow.com%2Fquestions%2F68645%2Fstatic-class-variables-in-python&usg=AFQjCNENgcl06PKrGi1TimZ6rpA7AYv6Mg&sig2=X2n2Jcr38nxF4oAH6tkXFA
        with open(self.dfNM) as f:
            jsonLine=json.load(f);
        os.remove(self.lfNM)
        return self.convertJsonLineToGoogleDataTable(jsonLine)

        return jsonLine
    def __init__(self, lfNM, dfNM):
            """Constructor"""
            self.lfNM=lfNM
            self.dfNM=dfNM
            
#for testing
if __name__ == "__main__":
# execute only if run as a script
    lfNM="C:/junk/junk.lock"
    dfNM="C:/junk/report.txt"
    ji=jobStatus(lfNM,dfNM)
    print(inspect.getmembers(ji))
    ji.getStatus()

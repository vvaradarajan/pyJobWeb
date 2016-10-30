import re
import json
from subprocess import Popen, call
import sys, os, subprocess
from multiprocessing import cpu_count
import _thread
class jarFile:
    def __init__(self,jarNM,jarVers):
        self.jarNM=jarNM
        self.jarVers=jarVers
        self.deleteFlag=0
    def toString(self):
        return self.jarNM + ":" + self.jarVers               
class cmdOutputParser:
    cpuRegex=re.compile("\\s*[0-9]+\\s([A-Za-z0-9]+)(?:\\s+[A-Za-z0-9]+){6}\\s+([0-9\\.]+)\\s+([0-9\\.]+).*")
    diskRegex=re.compile("\\s*([0-9]+(?:\\.[0-9]+)?[MG])(?:\\s+[A-Za-z0-9/-]+)+.*")
    @staticmethod
    def getGroups(line,pattern):
        result=pattern.match(line)
        if (result != None):
                #print result.group(1)
                pass
        else:
                pass
                #print "No Match"
        return result
    @staticmethod
    def parse(command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                break
            stdout.append(line)
            result = cmdOutputParser.getGroups(line)
            if (result != None):
                pass
                #print result.group(1) + " cpu:" + result.group(2) + " mem:" + result.group(3)
            #print line
            
        output = ''.join(stdout)
        return output
    @staticmethod
    def parseDupJars():
        jarFileRegex=re.compile("(.*?)-([0-9].*).jar")
        dirNM = os.getcwd()
        print ("Taking directory of " + dirNM)
        #command="cmd.exe /C dir *.jar \/b \/a-d "+dirNM;
        command="ls -1"
        fileNMs = []
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                break
            fileNMs.append(line)
            fileNMs.sort();
        # replace the fileNMs from a file for debugging
#         textFileNM="C:\\vasan\\workspace\\Team_UNOdvl\\junk.txt"
#         with open(textFileNM) as f:
#             fileNMs = f.readlines()
#         fileNMs.sort()
        jars = []
        dupJars = set()
        for s in fileNMs:
            result = cmdOutputParser.getGroups(s,jarFileRegex)
            if (result != None and result.groups >= 2):
                x=jarFile(result.group(1),result.group(2))
                jars.append(x)
                pkgNM=result.group(1)
                pkgVer=result.group(2)
        xPrev=jarFile("dummy","1.0dummy")
        for x in jars:
            if (x.jarNM==xPrev.jarNM):
                dupJars.add(x.jarNM)
            else:
                xPrev=x
        jarsToDelete=[]
        print ("No of Jar files found = "+ str(len(jars)) +"; No of files= "+str(len(fileNMs)))
        if len(dupJars) !=0 :
            print ("Duplicate jar files found! Recommended delete script is displayed below as rm commands")
            print ("The rm command is commented out for the recommended jar file")
            print ("Execute these commands to remove the duplicate jars!")
            print ("**Carefully review the recommendations and change them as appropiate!")
            print ("====================================================")
            for s in dupJars:
                for x in jars:
                    if (x.jarNM==s):
                      x.deleteFlag=1
                      jarsToDelete.append(x)
                jarsToDelete[len(jarsToDelete)-1].deleteFlag=0;
            jarsToDelete.sort(key=lambda x: x.jarNM)
            for x in jarsToDelete:
                commentChar=""
                if (x.deleteFlag==0):
                    commentChar="#"
                print (commentChar +"rm "+x.jarNM +"-"+x.jarVers+".jar")
                #print x.jarNM+" : "+x.jarVers
        else:
             print ("No duplicate Jars in: " + dirNM)
        return
    @staticmethod
    def parseCpuMem(inst):
        p = subprocess.Popen("top -bn1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        #calculate cpu usage from appid
        appId=inst.name.split(".")[0]
        cpu=0.0
        mem=0.0
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                break
            stdout.append(line)
            result = cmdOutputParser.getGroups(line,cmdOutputParser.cpuRegex)
            if (result != None):
                if (result.group(1) == appId):
                    cpu+=float(result.group(2))
                    mem+=float(result.group(3))
                    #print result.group(1) + " cpu:" + result.group(2) + " mem:" + result.group(3)
            #print line
        inst.cpu=round(cpu,2)
        inst.ram=round(mem,2)
        return cpu
    @staticmethod
    def parseDisk(inst):
        command="du -h -s /etrade/dvl-"+inst.name.replace(".","-")
        print ("command=" + command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        #calculate cpu usage from appid
        appId=inst.name.split(".")[0]
        disk=0.0
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                break
            stdout.append(line)
            result = cmdOutputParser.getGroups(line,cmdOutputParser.diskRegex)
            if (result != None):
                disk=result.group(1);
                print (" disk:" + disk)
            #print line
        inst.disk=disk
        return disk        
    @staticmethod
    def parseStatus(inst):
        command="edna -d dvl-"+inst.name.replace(".","-")
        print ("command=" + command)
        statusOut=0
        try:
            statusOut = subprocess.check_output(command, shell=True)
            inst.status="up"                       
        except subprocess.CalledProcessError as grepexc:                                                                                                   
            print ("error code", grepexc.returncode, grepexc.output)
            inst.status="down"
        return statusOut
    dvlCpuRegex=re.compile("\\s*([0-9]+)\\s+.*")
    dvlMemRegex=re.compile("\\s*Mem:\\s+([0-9]+)\\s.*")
    @staticmethod
    def parseDVlMem(dvl):
        command="free"
        print ("command=" + command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        #calculate cpu usage from appid
        noOfCpus=0
        mem=0
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                break
            stdout.append(line)
            result = cmdOutputParser.getGroups(line,cmdOutputParser.dvlMemRegex)
            if (result != None):
                mem=result.group(1)
                print ("mem:" + str(mem))
                break
        
        command="cat /proc/cpuinfo|grep processor|wc"
        print ("command=" + command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        #calculate cpu usage from appid
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                break
            stdout.append(line)
            result = cmdOutputParser.getGroups(line,cmdOutputParser.dvlCpuRegex)
            if (result != None):
                noOfCpus=result.group(1);
                print ("noOfCpus:" + str(noOfCpus))
                break
        
            #print line
        dvl.noOfCpus=noOfCpus
        dvl.mem=mem
        return       
    @staticmethod
    def parseSvcProfile():
        svcProfileRegex=re.compile(".*etrpmadd\\s-p\\s([a-zA-Z0-9-._]+)\\s-v\\s([a-zA-Z0-9-._]+)")
        try:
            SVC_HOME=os.environ['SVC_HOME']
        except KeyError:
            print ("SVC_HOME not defined as environment variable - process aborted")
            return
        command="which edna"
        try:
            statusOut = subprocess.check_output(command, shell=True)
            dvl="edna"                       
        except subprocess.CalledProcessError as grepexc:  
            dvl="em"    
        print ("DVL Type: " + dvl)                                                                                             
        command="${SVC_HOME}/services/tools/profile-svc"
        print ("Executing: " + command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        pkgsToAdd = []
        #calculate cpu usage from appid
        prevLine="" #used for printing error line in case of error
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                #check return code
                exit_code = p.wait()
            if (exit_code > 0):
                print ("Error Exit code ="+str(exit_code)+ "; ErrorMsg: " + prevLine)
                break
            prevLine=line
            if line.startswith("SOLVE"):
                line1 = p.stdout.readline()
                print (line)
                print (line1)
                if not line1.startswith("IGNORE"):
                    print ("Parsing")
                    result = cmdOutputParser.getGroups(line,svcProfileRegex)
                    if (result != None):
                        pkgNM=result.group(1)
                        pkgVer=result.group(2)
                        if (dvl == "edna"):
                            addCommand = "edna -d dvl-etrade-app-promote -c stage -p " + pkgNM + " -v "+pkgVer+"-0 -f"
                        else:
                            addCommand = "etexec -e dvl -a etrade -s app -i promote etrpmadd -p " + pkgNM + " -v "+pkgVer
                        pkgsToAdd.append(addCommand)
                        print (addCommand)
                    else:
                        print ("could not parse: "+line)
        return pkgsToAdd
    @staticmethod
    def threadOsCommand(cmd):
        #split string into components without spaces and pass a tuple
        try:
            _thread.start_new_thread(cmdOutputParser.execCmd ,(cmd,))
            return {}
        except Exception as e:
            print ("Error: unable to start thread: " +str(e))
    @staticmethod
    def execCmd(cmd):
        retcode=call(cmd.split()); #call takes an array of strings with the first part being the cmd and the others args
        print ("Thread " + cmd +": ret="+str(retcode))
    @staticmethod
    def execCmdAndShowOutput(cmd):
        command=cmd
        print (">"+cmd)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                break
            print (line)

from localPkgs.commandHandler import cmdOutputParser
import time
import sys,getopt
#Python gives this program a name of __main__, if this is run from the python command
# if __name__ == "__main__":
#     line="13376 vvaradar 20 0 13140 1012 732 R 2.0 0.0 0:00.01 top"
#     cmdOutputParser.getGroups(line,cmdOutputParser.cpuRegex)
#     # This is the code to make the app run (above are just test code)
#     pkgsToAdd = cmdOutputParser.parseSvcProfile()
#     if (len(pkgsToAdd) > 0) :
#      for s in pkgsToAdd:
#         print "Adding following package-versions:"
#         print s
#      time.sleep(5) # delays for 5 seconds
#     else :
#      print "All required packages for build are present"
#     for s in pkgsToAdd:
#         cmdOutputParser.execCmdAndShowOutput(s)
def main(argv):
    try:
      opts, args = getopt.getopt(argv,"")
    except getopt.GetoptError:
      print "Argument list is invalid: " + args
      sys.exit(2)
    if (len(args)==0): #no args so execute importServices
        # line="13376 vvaradar 20 0 13140 1012 732 R 2.0 0.0 0:00.01 top"
        # cmdOutputParser.getGroups(line,cmdOutputParser.cpuRegex)
        # This is the code to make the app run (above are just test code)
        pkgsToAdd = cmdOutputParser.parseSvcProfile()
        if (len(pkgsToAdd) > 0) :
         for s in pkgsToAdd:
            print "Adding following package-versions:"
            print s
         time.sleep(5) # delays for 5 seconds
        else :
         print "All required packages for build are present"
        for s in pkgsToAdd:
            cmdOutputParser.execCmdAndShowOutput(s)
    else:
        ### This is for DupJars
        cmdOutputParser.parseDupJars()
if __name__ == "__main__":
    main(sys.argv[1:])        
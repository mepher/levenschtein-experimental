import os,re,sys,time,argparse
# fx is the list of files ending .txt
# txt files (mcconfx.xml) nicked from https://github.com/JR0driguezB/malware_configs

# neat logging function?
def log( s ):
    s=re.sub('[\(\)\']','',str(s))
    print ('%s::  %s' % (time.ctime(),s))
    sys.stdout.flush()

# the actual distance function (C2ServerList1, C2ServerList2 -> returns number of editops 5)
def distance(C2ServerList1, C2ServerList2):
	# Levenshtein distance with ... anything in a list [] . 
	# This version uses the Wagner-Fischer algorithm.
    C2List_1=C2ServerList1
    C2List_2=C2ServerList2
    # get the lengths
    len_1 = len(C2List_1)+1
    len_2 = len(C2List_2)+1
    # create some sort of matrix        
    d = [0] * ((len_1)*(len_2))
    # do things with it (perhaps make matrix the right size)
	# https://github.com/toastdriven/pylev/blob/master/pylev.py
    for i in range(len_1):
        d[i] = i
    for j in range(len_2):
        d[j*len_1] = j
    # cost the difference between the items in the list.
	# yah. see that link.  
    for j in range (1, len_2):
        for i in range (1, len_1):
            if C2List_1[i-1] == C2List_2[j-1]:
                d[i + j * len_1] = d[i - 1 + (j - 1) * len_1]
            else:
                d[i + j * len_1] = min(
                    d[i - 1 + j * len_1] + 1,        # deletion
                    d[i + (j - 1) * len_1] + 1,      # insertion
                    d[i - 1 + (j - 1) * len_1] + 1,  # substitution
                )
    return d[-1]

# prepare the file list set (folder -> returns list of file names ['file1.txt','file2.txt'])
def createfilelist(folder=".\\confs\\"):
    # fx becomes the file list
    fx=[]
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            #print ("[+] file: " +(os.path.join(".", file)))
            fx.append(file)
    return fx

# create a list of lists (file -> returns list of lists [[ip,port],[ip,port]])
def buildserverlistfromfile(file):
    serverlist = []
    f = open(".\\confs\\"+str(file)).readlines()
    for lines in f:
        ip = None
        port = None
        # because re.findall returns a list, and we dont want a list in a list in a list, only a list in a list...
        # https://stackoverflow.com/questions/29325809/python-re-findall-prints-output-as-list-instead-of-string
        if re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',lines):
            ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',lines)[0]
        
        if re.findall(r'\:\d{1,5}',lines):
            port = re.findall(r'\:\d{1,5}',lines)[0]
        
        if (ip and port):
            #entry.append([ip,port])
            # entry.append(port)
            serverlist.append([ip,port])
    #print (serverlist)
    return serverlist

# create a mean me list from the file list
def createmeanmelist(filelist):
    mm=[]
    for index,file in enumerate(filelist):
        if index == len(filelist)-1:
            return mm
        else:
            firstlist   = buildserverlistfromfile(filelist[index])
            secondlist  = buildserverlistfromfile(filelist[index+1])
            diff = distance(firstlist,secondlist)
            #log (filelist[index])
            #log (filelist[index+1])
            #log (diff)
            mm.append(diff)
    return mm    

# compare a new file to all the files in the list, and return the score list    
def comparenewfile(filelist,newfile):
    mm=[]
    for index,file in enumerate(filelist):
        firstlist   = buildserverlistfromfile(filelist[index])
        secondlist  = buildserverlistfromfile(newfile)
        diff = distance(firstlist,secondlist)
        mm.append(diff)
    return mm        
    
if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument ('-F','--folder', help='The folder containing the conf files, with a .txt extension. defaults to .\confs\ ', required=False, default='.\\confs\\')
    parser.add_argument ('-n','--newfile', help='the location of a new trickbot file to be tested against the set',required=False)
    #parser.add_argument('-h','--help', help='echo the string you use here')
    args = parser.parse_args()
    #log ('begin!')            
    filelist=createfilelist(args.folder)
    #log ('the file list:')
    #log (filelist)
    log ('do it!')    
    # mm is the list of scores (mean me)
    mm=createmeanmelist(filelist)
    log (( 'the actual mean me list',mm ))
    #log (mm)
    #log (type(mm))
    log (( 'Total' ,sum(mm,0.0) ))
    log (( 'Mean Average' ,sum(mm,0.0) / len(mm) ))
    
    if args.newfile:
        log ('like a fool, you have hard coded the folder path. needs fixing. line 55... and BOOM you need class!')
        newfilecomparison=comparenewfile(filelist,args.newfile)
        log (( 'How the new file compares against all the files in list (any low score implies botnet membership)',newfilecomparison ))

    

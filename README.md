# levenschtein-experimental

# sudo pip install python-Levenshtein
# Challenge (set by James Sellwood @escinsecurity)
# detect new trickbot C2 infrastructures by measuring levenshtein distance changes over C2 conf file IP list updates over time.
# take x conf files, select only the IP addresses
# ... work out the best way to measure 'change'. thought. might be easier to measure sameness
# anyway
    # this could probably do with sorting, or ***somthing***, as a straight edit distance on this might be ... wrong
    # ...and it is. a change in the order of the list, off setting the rest of the (same) IP's ruins everything. consider total list turnover. TLT.  
    # the sample was too perfect. https://gist.github.com/hasherezade/0c464f970018f509444243b67a0c5447
    # also, deviation over time - a 2 week (i.e. after a total list turnover) old list will be so different from a 1 day deviation, as to be dilute the over all value.
    # ?
    # some kind of chronological limitation. a sliding window of 7 (...tweakable... argparse) days comparison?
    # make a list of all the unique IPs across all (of the sliding window) of the files (aswlists all-sliding-window). 
    # it has a len (awslen)
    # populate the elements such that same IP's occupy the same position across aswlists
    # populate gaps with '0.0.0.0' ??? 
    # hash each element, and concaternate into one string 
    # stay with me here... 
    # the hashing will result in the same string-section for empty sets, the hashing normalises the lengh, and standardises the difference while ignoring 
    # the misleading distance between similar IP address numbers. 
    # is this a 'good idea'? numerically similar IPs are misleading - they may not necessarily be in the same family. hmmm. ports... wise to include. 
    # therefore hashing them makes them levenshtein as distant as possible. MAX . which is fair and desirable? 
    # therfore identical samples will have no distance, and the slightest deviation will slide the distance to MAX. which IS fair and accurate. 
    # so then the length of the list, and number of concaternated hashes. hmmm. the zerodot infill MUST be the same length.
    # do we need to increase the value of same IPs over missing IPs? why? how? what is a good way to measure change?
    # imagine a list that suddenly loses half it IP set, when compared to a list with an entirely different IP set. 
    # this would be either the difference between two entirely different trickbot nets. 
    # OR ones a few weeks apart, if that.
    
    # fuck. I feel some tricky maths incoming. 
    
    # https://en.wikipedia.org/wiki/Edit_distance#Common_algorithm
    
    # anyway before reading that. consider the 'magnetism' of a new, test sample.
    # sweep it past all your 'control' or baseline IP sets / samples / conf files / whatever, that you know represents a single C2 inf.
    # how highly does it ever score? does it score more or less highly that the lowest scoring member of the control set? and using what scoring plan / technique?
    # i imagine a graph, with lev distance from its neighbour(s) (y? multiple lines / plans in different colors?) over time (x) 
    # (each point is labelled by the file name)
    # the new sample is then plotted against each point / file / group, and its relative score computed using the same / multiple plans
    
    # is this (the sliding window, max length list, zerodot infill, hash string concat plan) a sound plan? 
    # plans:
    # the sliding window(time), max length list, zerodot infill, hash string concat plan
    # the sliding window(chronologically ordered), max length list, zerodot infill, hash string concat plan
    
    # now reading: https://en.wikipedia.org/wiki/Edit_distance#Common_algorithm
    
    # ...the set of primative operations...
    # and so. it appears that HAMMING distance is actually what you have aimed for. good?
    # Similarly, by only allowing substitutions (again at unit cost), HAMMING distance is obtained; this must be restricted to equal-length strings.
    # if you can make a 'hash' a represent a single character?
    # or does the randomness of the total hash in fact simply just make the numbers scale up, but retain their meaning?
    # and...In [84]: x=Levenshtein.                  
    #                    Levenshtein.apply_edit      Levenshtein.hamming         Levenshtein.jaro_winkler    Levenshtein.median_improve  Levenshtein.ratio           Levenshtein.setratio        
    #                    Levenshtein.distance        Levenshtein.inverse         Levenshtein.matching_blocks Levenshtein.opcodes         Levenshtein.seqratio        Levenshtein.subtract_edit   
    #                    Levenshtein.editops         Levenshtein.jaro            Levenshtein.median          Levenshtein.quickmedian     Levenshtein.setmedian 
    # so plenty to paste in and look at... :)
    # refactor string prep to a function, and pass to the various methods.
    
    # *************** Levenshtein.seqratio works with lists ***************
    # does in fill matter? does hashing? do we have a winner?
    # and what of setratio, and the new file? 
    # apply_edit - ANY OF THEM?
    # hmm. maths. stop now.

# this code needs to be refactored with functions (maybe a class or two?)

import Levenshtein 
import os,re
# fx is the list of files ending .conf
# conf files (mcconfx.xml) nicked from https://gist.github.com/hasherezade/0c464f970018f509444243b67a0c5447
fx=[]
# mm is the list of scores (mean me)
mm=[]
print "[>] a trickbot baselining exercise...."
print "[>] list and append to an array the local (./) .conf files:"

for file in os.listdir("."):
    if file.endswith(".conf"):
        print"[+] file: " +(os.path.join(".", file))
        fx.append(file)
# we now have our list of files (names)

print "[>] cycle through the list, comparing each element to each element"
print "[-] NOTE: this compares the entire file," 
print "[-] without checking the version, or regexing out the IP"

# some magic from the internets...
# read a file as a string: https://stackoverflow.com/questions/8369219/how-do-i-read-a-text-file-into-a-string-variable-in-python
# comparing all elements in a list: https://stackoverflow.com/questions/16603282/how-to-compare-each-item-in-a-list-with-the-rest-only-once
# ...its like the 6th answer down.
for index,this in enumerate(fx):
    for that in fx[index+1:]:
    	print "[+] comparing "+this+" "+that
        x=Levenshtein.distance(open(this).read(),open(that).read())
        print "[+] the Levenshtein.distance: "+str(x)
        mm.append(x)

print "[>] the resulting list, total, and average (mean)"
# https://stackoverflow.com/questions/9039961/finding-the-average-of-a-list
print "[>] the list of file comparison scores "+str(mm)
print "[>] the total "+str(sum(mm,0.0))
print "[>] the average (mean) "+str(sum(mm,0.0) / len(mm))

print "[!] IP -- lets do that again, but only with IPs"

counter=0
mmip=[]

for index,this in enumerate(fx):
    # make a string of a list of a regex of the IPs in the lines in the file...
    # open the 'first' file..
    thisrexfile=open(this).read()
    # extract all the IPs, line by line, into a list...
    thisrex=re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',thisrexfile)
    # turn the list into a string.
    # thought

    # then calculate distance. 
    # if the list, is say, missing a single early element. 
    thisrex.sort()
    strthisrex=str(thisrex)
    #print "[!] IP -- strthisrex...: "+strthisrex
    
    # do it all again for its pal. 
    for that in fx[index+1:]:
        thatrexfile=open(that).read()
        thatrex=re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',thatrexfile)
    	# sort the list ... function opp missed.
    	thatrex.sort()        
        strthatrex=str(thatrex)
        #print "[!] IP -- strthatrex...: "+strthatrex
    	print "================================="
    	print "[!] IP --  comparing: "#+strthisrex+" "+strthatrex    	
    	print "[!] IP -- "+strthisrex
    	print "[!] IP -- "+strthatrex
    	# actually compare the two 'active' lists. 
        x=Levenshtein.distance(strthisrex,strthatrex)
        print "[!] IP --  the Levenshtein.distance: "+str(x)
    	print "================================="
        mmip.append(x)

print "[!] IP --  the resulting list, total, and average (mean)"
print "[!] IP --  the list of file comparison scores "+str(mmip)
print "[!] IP --  the total "+str(sum(mmip,0.0))
print "[!] IP --  the average (mean) "+str(sum(mmip,0.0) / len(mmip))

#a magic distance oneliner
#Levenshtein.distance(open('trickbot3.conf','rt').read(),open('trickbot2.conf','rt').read())

def preparestring(afile):
    thatrexfile=open(afile).read()
    thatrex=re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',thatrexfile)
    strthatrex=str(thatrex)
    return strthatrex

# and then
print "[x] ah, and then"
print "(Levenshtein.distance(preparestring(fx[0]),preparestring(fx[1])))"
print Levenshtein.distance(preparestring(fx[0]),preparestring(fx[1]))

print "(Levenshtein.editops(preparestring(fx[0]),preparestring(fx[1])))"
print Levenshtein.editops(preparestring(fx[0]),preparestring(fx[1]))

print "Levenshtein.jaro(preparestring(fx[0]),preparestring(fx[1]))"
print Levenshtein.jaro(preparestring(fx[0]),preparestring(fx[1]))

print "Levenshtein.jaro_winkler(preparestring(fx[0]),preparestring(fx[1]))"
print Levenshtein.jaro_winkler(preparestring(fx[0]),preparestring(fx[1]))

print "Levenshtein.ratio(preparestring(fx[0]),preparestring(fx[1]))"
print Levenshtein.ratio(preparestring(fx[0]),preparestring(fx[1]))

print "do we have a winner? seqratio - it wants a list ..."
print "Levenshtein.seqratio(preparestring(fx[0]),preparestring(fx[1]))"
print Levenshtein.seqratio(preparestring(fx[0]),preparestring(fx[1]))

print """Compute similarity ratio of two sequences of strings.
seqratio(string_sequence1, string_sequence2)
This is like ratio(), but for string sequences.  A kind of ratio()
is used to to measure the cost of item change operation for the
strings.
Examples: seqratio(['newspaper', 'litter bin', 'tinny', 'antelope'],['caribou', 'sausage', 'gorn', 'woody'])"""

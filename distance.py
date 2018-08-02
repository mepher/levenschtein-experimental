https://github.com/JR0driguezB/malware_configs/tree/master/TrickBot

l1=[]
l2=[]

a=['1.1.1.1',443]
b=['2.2.2.2',443]
c=['3.3.3.3',443]
x=['7.7.7.7',443]
y=['8.8.8.8',443]
z=['9.9.9.9',443]

l1.append(a)
l1.append(b)
l1.append(c)

l2.append(x)
l2.append(y)
l2.append(z)

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
    

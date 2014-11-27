#this program will extract IBM generated data and forms a binary matrix.

import re
import sys

#checks if the number of file passed are enough
if not len(sys.argv)== 4:
	print "less file arguments"
else:
	queryfile=open(sys.argv[1],'r')
	outputfile=open(sys.argv[2],'w')
	nitems=int(sys.argv[3])

def _sparsedata():
	#puts all the number of items in the file
	for j in range(0,nitems):
		outputfile.write(','+str(j))
	outputfile.write('\n')
	count=0
	_items_=[]
	trans=0
	del _items_[:]
	for i in queryfile:
		istrip=i.strip()  #removes new line if present 
		iline=istrip.split()
		if count == 0:  #for first transaction
			trans=iline[0] #sets first transaction number
			_items_.append(iline[1])	#stores first itemnumber in the list
			count=1
			outputfile.write(trans)		#outputs the first transaction number
		else: 
			if trans==iline[0]:		
				_items_.append(iline[1])	#stores items that belong to same transactions
			else:
				count=0
				temptrans=iline[0]		#keeping track of transaction
				tempitem=iline[1]		#keeping track of item of that above transaction
				rem=queryfile.next()		#checks the next string in the file
				remsplit=rem.split()		#splits the words
				if len(_items_)>0:		
					k=0
					for ab in range(0,nitems):    #outputs the boolean value for each itemsets in the transactions
						if k < len(_items_):
							if str(ab)==_items_[k]:
								outputfile.write(','+str(1))	#if the item is present it sets to 1
								k=k+1
							else:
								outputfile.write(','+str(0))	#if the item is absent it sets to 0
						else:
							outputfile.write(','+str(0))		# items absent from that transaction	
					outputfile.write('\n')
				del _items_[:]							#deletes the list
				if not remsplit[0]==iline[0]:					#checks if the next transaction is same
					outputfile.write(iline[0])
					for ab in range(0,nitems):
						if str(ab)==iline[1]:
							outputfile.write(','+str(1))
						else:
							outputfile.write(','+str(0))
					outputfile.write('\n')
					trans=remsplit[0]
					_items_.append(remsplit[1])
					count=1
					outputfile.write(trans)
				else:
					trans=temptrans
					_items_.append(tempitem)
					_items_.append(remsplit[1])
					count=1
					outputfile.write(trans)
# its weird I know but I didn't wanted to waste more time so for the last transaction the program has to go through another loop so this loop will input the last transactions. 
	ts=0
	for ab in range(0,nitems):
		if ts<len(_items_):
			if str(ab)==_items_[ts]:
				outputfile.write(','+str(1))
				ts=ts+1
			else:
				outputfile.write(','+str(0))
		else:
			outputfile.write(','+str(0))
	outputfile.close()
#extracts the binary matrix 
def binmatrix():
	_sparsedata()	
	binaryfile=open(sys.argv[2],'r')
	L=[[]]
	binaryfile.next()
	for line in binaryfile:
		linestrip=line.strip()
		_items=linestrip[2:]
		L.append([int(i) for i in _items.split(',')])
	L=L[1:]
	return L
binary_matrix=binmatrix()
print binary_matrix

'''
attempt to reduce the number of tags
Principal Component Analysis
We did not test this as the other bits and pieces to complete the learning with the reduced dimensions is not ready
Also we did not experiment to find out number of dimensions to reduce
'''

from collections import  defaultdict
import numpy as np
import csv
import math
def prob(pos,neg):
	if( (pos+neg) == 0):
		return -1
	else : return (pos*1.0)/(pos+neg)

#'''
train = csv.reader(open(sys.argv[1],'r'))
test = csv.reader(open(sys.argv[2],'r'))

'''
train = csv.reader(open('dummy_data/tr.csv','r'))
test = csv.reader(open('dummy_data/ts.csv','r'))
'''

ques_ind = 3
tag_ind = 8

ques_tags = {} 
# the tags a re unique to each ques_id : so store the tags for each ques_id
for line in train:
	if(line[0]=='correct' or line[1] == '3' or line[1] == '4' ): continue
	ques_tags[line[ques_ind]] = line[tag_ind]


tagMatr = [] 
#add all the tags to a sparse matrix to reduce the dimensions
for ques_id,tags in ques_tags.iteritems():	
	tags = map(int,tags.split(' '))
	mean = len(tags)/300.0
	pres = [0]*300
	for tag in tags:	
		pres[tag]= 1
	tagMatr.append(pres)



#normalise the data (tags)
tagMatr = np.matrix(tagMatr)
means   = np.mean(tagMatr)

tagMatr =  (tagMatr-means)
variaces= np.var(tagMatr)
tagMatr = tagMatr/variaces


print np.mean(tagMatr)
tagMatrT = tagMatr.H


sigma  = tagMatrT*tagMatr
U, pca_score, V = np.linalg.svd(sigma)
#the matrix formed by first k columns of U is  the tranformation matrix which reduces the dimension from 300 to k

print U
print means
print variaces

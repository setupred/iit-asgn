'''
Decision Tree Regression
'''


from time import gmtime, strftime
from collections import  defaultdict
from sklearn import  tree
import csv

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

ques_ind = 4
track_ind = 6
subtrack_ind = 7
game_ind = 13


X = []
y = []


for line in train:
	if(line[0]=='correct' or line[1] == '3' or line[1] == '4' ): continue
	res = int(line[0])
	user = int(line[2])
	st = int(line[subtrack_ind])
	t = int(line[track_ind])
	q = int(line[ques_ind])
	g= (line[subtrack_ind])
	X.append([user,st,q])
	y.append(res)
	


print "data ready"
clf = tree.DecisionTreeRegressor()
clf = clf.fit(X,y)
print "training done"


ques_ind = 2
track_ind = 4
subtrack_ind = 5
game_ind = 11

time = strftime("%d:%b:%Y-%H:%M:%S", gmtime())
final = open('result-'+str(time),'w')
for line in test:
	if(line[0]=='user_id' ): continue
	user = int(line[0])	
	st = int(line[subtrack_ind])
	t = int(line[track_ind])
	q = int(line[ques_ind])
	g= (line[subtrack_ind])
	final.write(str(user)+","+str(clf.predict([user,st,q])[0])+"\n")


final.close()
print "end"

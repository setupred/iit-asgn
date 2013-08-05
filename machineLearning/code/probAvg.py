'''
averaging probablities for different features
extension of the basic submission by Pararth
'''

from collections import  defaultdict
import csv
import math
def prob(pos,neg):
	if( (pos+neg) == 0):
		return -1
	else : return (pos*1.0)/(pos+neg)

#'''


train = csv.reader(open(sys.argv[1],'r'))
test = csv.reader(open(sys.argv[2],'r'))
final = open('result','w')

'''
train = csv.reader(open('tr.csv','r'))
test = csv.reader(open('ts.csv','r'))
final = open('result','w')
'''

ques_ind = 4
track_ind = 6
game_ind = 13

p_subtrack = defaultdict(lambda:0) # mapping from (user_id,subtrack) -> #correctAnswers
p_game = defaultdict(lambda:0)
p_question = defaultdict(lambda:0)


n_subtrack = defaultdict(lambda:0)
n_game = defaultdict(lambda:0)
n_question = defaultdict(lambda:0)

p_overall = defaultdict(lambda:0) 
n_overall = defaultdict(lambda:0) 

def rectify(p,user):
	ret = 0
	if(p==-1):
		ret = (p_overall[user]*1.0)/(max(1,p_overall[user]+n_overall[user]))
	else : ret = p
	#if(ret==0): return 0.5
	return ret

def func(p1,p2,p3,user):
	#if (rectify(p1,user)+rectify(p2,user)+rectify(p3,user)+rectify(p4,user)) > 2.0 : return 1
	p1 = rectify(p1,user)
	p2 = rectify(p2,user)
	p3 = rectify(p3,user)
	print p1,p2,p3
	return 	(p1+p2+p3)/3
	
user_ids = set()
wc = 0

for line in train:
	if(line[0]=='correct' or line[1] == '3' or line[1] == '4' ): continue
	res = int(line[0])
	user = int(line[2])
	st = int(line[subtrack_ind])
	q = int(line[ques_ind])
	g= int(line[game_ind])
	
	if(res==1):
		p_subtrack[(user,st)]+=1
		p_question[(user,q)]+=1
		p_game[(user,g)]+=1
		p_overall[user]+=1
	
	else:
		n_subtrack[(user,st)]+=1
		n_question[(user,q)]+=1
		n_game[(user,g)]+=1
		n_overall[user]+=1

print "training vover"

ques_ind = 2
subtrack_ind = 5
game_ind = 11


for line in test:
	if(line[0]=='user_id' ): continue
	user = int(line[0])
	
	st = int(line[subtrack_ind])
	q = int(line[ques_ind])
	g= int(line[game_ind])
		
	p1 = prob(p_subtrack[(user,st)],n_subtrack[(user,st)])
	p2 = prob(p_question[(user,q)],n_question[(user,q)])
	p3 = prob(p_game[(user,g)],n_game[(user,g)])


	p = func(p1,p2,p3,user)
	final.write(str(user)+","+str(p)+"\n")

import sys
import os
from datetime import datetime
from collections import defaultdict as dd

def MapFile(filename,DestDir,kv):
	cnt,tot=0,0
	if(DestDir[-1]=='/'): DestDir = DestDir[:-1]
	files = [open(DestDir+"/"+str(i),'a') for i in xrange(26)]
	for line in open(filename):
		tot+=1
		line=line[:-1]
		if(line==''): continue
		#print line
		s=0
		if(kv==(1,0)):
			if(line[-1]!='\t'):
				a,b = line.split('\t')
				line = b+'\t'+a
				s= 11
			else: continue
		if(s>=len(line)): continue
		
		dest = ord(line[s])-ord('a')
		if(dest<=25 and dest>=0): pass
		else: dest = ord(line[s])-ord('A')
		
			
		if(dest<=25 and dest>=0): files[dest].write(line+"\n")
		else: cnt+=1

	for f in files:
		f.close()
	print cnt,tot;

def reduceFile(SrcFile,DestFile):
	dic = dd(lambda: dd(lambda:0))
	for line in open(SrcFile):
		if(line=='\n'): continue
		line=line[:-1]
		#print line
		if(line[-1]=='\t'):
			line+="---"
		tmp = line.split('\t')
		q,r = tmp
		dic[q][r]+=1
	w = open(DestFile,'w')
	for q in dic:
		string = q+"\t"
		for r,val in dic[q].items():
			string+=(r+";"+str(val)+"\t")
		w.write(string+"\n")
	w.close()


def MapAllFiles(SrcDir,DestDir,kv):
	start = datetime.now()
	for files in os.listdir(SrcDir):
		if(files[:13]!="clean-user-ct"): continue
		print str(datetime.now())+"  ::::  "+files
		MapFile(SrcDir+"/"+files,DestDir,kv)
	print (datetime.now()-start).seconds


def ReduceAll(SrcDir,DestDir):
	start = datetime.now()
	for files in os.listdir(SrcDir):
		if(len(files)>=3): continue
		print str(datetime.now())+"  ::::  "+files
		reduceFile(SrcDir+"/"+files,DestDir+"/"+files)
	print (datetime.now()-start).seconds

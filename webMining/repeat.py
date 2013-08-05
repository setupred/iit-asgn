import sys
import os
from group import *
DirPath = sys.argv[1]
Destpath = sys.argv[2]

if(DirPath[-1]=="/"):DirPath = DirPath[:-1]
if(DestPath[-1]=="/"):DestPath = DestPath[:-1]
try:
	os.system("mkdir "+DirPath)
	os.system("mkdir "+DirPath+"-r")
	os.system("mkdir "+DirPath+"-Final")
	os.system("mkdir "+DirPath+"-rFinal")
except: pass

MapAllFiles(DirPath,Destpath,(0,1))
ReduceAll(Destpath,Destpath+"-Final")

MapAllFiles(DirPath,Destpath+'-r',(1,0))
ReduceAll(Destpath+'-r',Destpath+"-rFinal")

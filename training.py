import json,csv,sys,os,psycopg2
import numpy as np
from collections import Counter 
from processingFunctions import  computeAppStats, countAppOccur, appTimeIntervals



day = 86400
uids = ['u00','u01','u02','u03','u04','u05','u07','u08','u09','u10','u12','u13','u14','u15','u16','u17','u18','u19','u20','u22','u23','u24',
'u25','u27','u30','u31','u32','u33','u34','u35','u36','u39','u41','u42','u43','u44','u45','u46','u47','u49','u50','u51','u52','u53','u54',
'u56','u57','u58','u59']

# returns feature vector corresponing to 'timestamp' stress report (label)
def appStatsL(cur,uid,timestamp):
	appOccurTotal = countAppOccur(cur,uid)
	print(len(appOccurTotal))
	appStats=[]
	
	tStart = timestamp - 2*day

	cur.execute("""SELECT running_task_id  FROM appusage WHERE uid = %s AND time_stamp > %s AND time_stamp < %s ; """, [uid,tStart,timestamp] )
	records= Counter( cur.fetchall() )

	#transforming keys to be in readable format
	for k in records.keys():
		records[k[0]] = records.pop(k)	

	# number of unique applications 
	uniqueApps = len(records.keys())
	# usageFrequency:  number of times in timeWin / total times
	usageFrequency= {k: float(records[k])*100/float(appOccurTotal[k]) for k in appOccurTotal.viewkeys() & records.viewkeys() }
	appStats.append(usageFrequency)

	return uniqueApps

#---------------------------------------------------------------------
# computes the total time (sec) that screen was on during the past day
def timeScreenOn(cur,uid,timestamp):
	uid = uid +'dark'
	#tStart is exactly 24h before given timestamp
	tStart = timestamp - day

	#fetching all records that fall within this time period
	cur.execute('SELECT timeStart,timeStop FROM {0} WHERE timeStart >= {1} AND timeStop <= {2}'.format(uid,tStart,timestamp))
	records = cur.fetchall()

	totalTime =0
	for k in records:
		totalTime += k[1]-k[0]

	return totalTime






con = psycopg2.connect(database='dataset', user='tabrianos')
cur = con.cursor()
timeScreenOn(cur,'u12',1365809051)
#for i in uids:
#	print(appStatsL(cur,i,1366248106))	





"""
def main(argv):

	#connecting to database
	try:
		con = psycopg2.connect(database='dataset', user='tabrianos')
		cur = con.cursor()

	except psycopg2.DatabaseError as err:
		print('Error %s' % err)
		exit()





	if sys.argv[1]=='-insert':


		#do stuff
		

	elif sys.argv[1]=='-drop':
		#do stuff


























if __name__ == '__main__':
	main()


	"""

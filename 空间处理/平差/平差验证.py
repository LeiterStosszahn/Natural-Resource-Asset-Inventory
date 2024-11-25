import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy
import string
from arcpy.sa import *
#Loading plug-ins

if time.time()>time.mktime((2022,6,30,0,0,0,0,0,0)):
	print('Out of validity!')
	0/0
	exit(0)
#term of validity

keywords=[]#Null unique value array

try:
	layer_1=arcpy.GetParameterAsText(0)#Select layer
	keywords_1=arcpy.GetParameterAsText(1)#Determine unique value column
	tbmj_1=arcpy.GetParameterAsText(2)#TBMJ
	balance_resuelt=arcpy.GetParameterAsText(3)#Results after adjustment
	result_1=arcpy.GetParameterAsText(4)#Output result

	with arcpy.da.SearchCursor(layer_1,[keywords_1]) as cursor:
		for row in cursor:
			if row[0] not in keywords:
				keywords.append(row[0])
	#Extract unique value of keywords

	for i in range(0,len(keywords)):
		expression=arcpy.AddFieldDelimiters(layer_1,keywords_1)+'=\''+keywords[i]+'\''#SQL query statement by patch number
		with arcpy.da.SearchCursor(layer_1,[keywords_1,tbmj_1,balance_resuelt],where_clause=expression) as cursor:#In order, SQL queries the unique patch number
			mj_sum=0#Initial area 0
			#Count the details of sub patches of this group of patches
			for row in cursor:
				mj_sum=mj_sum+row[2]#sum calculation area
			#uncorrect
			if abs(round(mj_sum-row[1],2))>0:
				with arcpy.da.UpdateCursor(layer_1,[keywords_1,result_1,'FID'],where_clause=expression) as cursor:
					for row_2 in cursor:
						row_2[1]=round(mj_sum-row[1],2)
						cursor.updateRow(row_2)
			#correct
			else:
				with arcpy.da.UpdateCursor(layer_1,[keywords_1,result_1],where_clause=expression) as cursor:
					for row_2 in cursor:
						row_2[1]=0
						cursor.updateRow(row_2)
except arcpy.ExecuteError:
	print arcpy.GetMessages()

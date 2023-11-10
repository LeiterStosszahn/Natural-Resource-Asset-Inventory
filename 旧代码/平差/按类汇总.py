import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy
import string
from arcpy.sa import *
#Loading plug-ins

if time.time()>time.mktime((2022,12,30,0,0,0,0,0,0)):
	arcpy.AddMessage('Term out of validity!')
	exit(0)
#term of validity

keywords=[]#Null unique value array

layer_1=arcpy.GetParameterAsText(0)#Select layer
keywords_1=arcpy.GetParameterAsText(1)#Determine unique value column
tbmj_1=arcpy.GetParameterAsText(2)
result_1=arcpy.GetParameterAsText(3)

with arcpy.da.SearchCursor(layer_1,[keywords_1]) as cursor:
	for row in cursor:
		if row[0]==' ' or row[0]==None or row[0]==0:
			continue
		if row[0] not in keywords:
			keywords.append(row[0])

for i in range(0,len(keywords)):
	expression=arcpy.AddFieldDelimiters(layer_1,keywords_1)+'=\''+keywords[i]+'\''#SQL query statement by patch number
	with arcpy.da.SearchCursor(layer_1,[keywords_1,tbmj_1],where_clause=expression) as cursor:
		mj_sum=0#Initial area 0
		for row_1 in cursor:
			mj_sum+=row_1[1]
	with arcpy.da.UpdateCursor(layer_1,[keywords_1,result_1],where_clause=expression) as cursor_2:
		for row_2 in cursor_2:
			row_2[1]=mj_sum
			cursor_2.updateRow(row_2)
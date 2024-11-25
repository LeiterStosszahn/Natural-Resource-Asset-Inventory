import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy
import string
from arcpy.sa import *
#Loading plug-ins

if time.time()>time.mktime((2022,11,30,0,0,0,0,0,0)):
	arcpy.AddMessage('Term out of validity!')
	exit(0)
#term of validity

keywords=[]#Null unique value array

layer_1=arcpy.GetParameterAsText(0)#Select layer
keywords_1=arcpy.GetParameterAsText(1)#Determine unique value column
tbmj_1=arcpy.GetParameterAsText(2)
ytbmj_1=arcpy.GetParameterAsText(3)
jj_1=arcpy.GetParameterAsText(4)
result_1=arcpy.GetParameterAsText(5)

with arcpy.da.SearchCursor(layer_1,[keywords_1]) as cursor:
	for row in cursor:
		if row[0]==' ' or row[0]==None or row[0]==0:
			continue
		if row[0] not in keywords:
			keywords.append(row[0])

for i in range(0,len(keywords)):
	expression=arcpy.AddFieldDelimiters(layer_1,keywords_1)+'=\''+keywords[i]+'\''#SQL query statement by patch number
	with arcpy.da.SearchCursor(layer_1,[keywords_1,tbmj_1,ytbmj_1,jj_1],where_clause=expression) as cursor_1:#In order, SQL queries the unique patch number
		jj=percentage=0
		for row_1 in cursor_1:
			percentage=row_1[1]/row_1[2]
			if percentage>0.9:
				jj=row_1[3]
				break
			else:
				jj+=row_1[3]*percentage
	with arcpy.da.UpdateCursor(layer_1,[keywords_1,result_1],where_clause=expression) as cursor_2:
		for row_2 in cursor_2:
			arcpy.AddMessage(row_2[0])
			row_2[1]=jj
			cursor_2.updateRow(row_2)



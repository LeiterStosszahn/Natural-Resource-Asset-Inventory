import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy
import string
from arcpy.sa import *
#Loading plug-ins

if time.time()>time.mktime((2023,12,30,0,0,0,0,0,0)):
	arcpy.AddMessage(u'\u6388\u6743\u8d85\u671f\uff01')
	exit(0)
#term of validity

keywords_dict={}#Null BSM dict

layer_arr=arcpy.GetParameter(0)
keywords_1="ZCQCBSM"

for layer_1 in layer_arr:
	with arcpy.da.SearchCursor(layer_1,[keywords_1]) as cursor:
		for row in cursor:
			keywords_dict[row[0][0:18]]=keywords_dict.get(row[0][0:18],0)+1
		#Extract unique value

	keywords=keywords_dict.keys()
	keynums=keywords_dict.values()

	for i in range(0,len(keywords)):
		expression=arcpy.AddFieldDelimiters(layer_1,keywords_1)+'like\''+keywords[i]+'%\''#SQL query statement by keywords
		with arcpy.da.UpdateCursor(layer_1,[keywords_1,"ZCQCBSM_ZB"],where_clause=expression) as cursor_3:
			if keynums[i]==1:
				for row_3 in cursor_3:
					row_3[1]=keywords[i]+"0000"
					cursor_3.updateRow(row_3)
			else:
				j=1
				for row_3 in cursor_3:
					row_3[1]=keywords[i]+str(j).zfill(4)
					cursor_3.updateRow(row_3)
					j+=1







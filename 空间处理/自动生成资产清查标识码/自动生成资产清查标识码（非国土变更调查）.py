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

layer_1=arcpy.GetParameterAsText(0)#Select layer
zcqcbsm_1=arcpy.GetParameterAsText(1)#ZCQCBSM
xzqdm_1=arcpy.GetParameterAsText(2)#GBT2260
cdm_1=arcpy.GetParameterAsText(3)#Layer code
keywords_1=arcpy.GetParameterAsText(4)#The Keywords to distinguish

if arcpy.GetParameter(5)==True:
	#Self increasing
	with arcpy.da.UpdateCursor(layer_1,[zcqcbsm_1]) as cursor_4:
		i=1
		for row_4 in cursor_4:
			row_4[0]=xzqdm_1+cdm_1+str(i).zfill(8)+"0000"
			i+=1
			cursor_4.updateRow(row_4)
else:
	with arcpy.da.SearchCursor(layer_1,[keywords_1]) as cursor:
		for row in cursor:
			keywords_dict[row[0]]=keywords_dict.get(row[0],0)+1
		#Extract unique value

	keywords=keywords_dict.keys()
	keynums=keywords_dict.values()

	for i in range(0,len(keywords)):
		expression=arcpy.AddFieldDelimiters(layer_1,keywords_1)+'=\''+keywords[i]+'\''#SQL query statement by keywords
		with arcpy.da.UpdateCursor(layer_1,[keywords_1,zcqcbsm_1],where_clause=expression) as cursor_3:
			if keynums[i]==1:
				for row_3 in cursor_3:
					row_3[1]=xzqdm_1+cdm_1+str(i+1).zfill(8)+"0000"
					cursor_3.updateRow(row_3)
			else:
				j=1
				for row_3 in cursor_3:
					row_3[1]=xzqdm_1+cdm_1+str(i+1).zfill(8)+str(j).zfill(4)
					cursor_3.updateRow(row_3)
					j+=1







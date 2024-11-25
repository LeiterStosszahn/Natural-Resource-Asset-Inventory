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

bsm_dict={}#Null BSM dict

layer_1=arcpy.GetParameterAsText(0)#Select layer
zcqcbsm_1=arcpy.GetParameterAsText(1)#ZCQCBSM
bsm_1=arcpy.GetParameterAsText(2)#BSM

with arcpy.da.SearchCursor(layer_1,[bsm_1]) as cursor:
	for row in cursor:
		bsm_dict[row[0]]=bsm_dict.get(row[0],0)+1
	#Extract unique value of BSM

bsm=bsm_dict.keys()
bsmnum=bsm_dict.values()

for i in range(0,len(bsm)):
	expression=arcpy.AddFieldDelimiters(layer_1,bsm_1)+'=\''+bsm[i]+'\''#SQL query statement by BSM
	with arcpy.da.UpdateCursor(layer_1,[bsm_1,zcqcbsm_1],where_clause=expression) as cursor_3:
		if bsm_dict[bsm[i]]==1:
			for row_3 in cursor_3:
				row_3[1]=row_3[0]+"0000"
				cursor_3.updateRow(row_3)
		else:
			j=1
			for row_3 in cursor_3:
				row_3[1]=row_3[0]+str(j).zfill(4)
				cursor_3.updateRow(row_3)
				j+=1







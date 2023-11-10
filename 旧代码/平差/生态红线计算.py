import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy
import string
from arcpy.sa import *
#Loading plug-ins

if time.time()>time.mktime((2023,11,30,0,0,0,0,0,0)):
	arcpy.AddMessage('Term out of validity!')
	exit(0)
#term of validity

keywords=[]#Null unique value array

layer_1=arcpy.GetParameterAsText(0)#Select layer
layer_STBHHX=arcpy.GetParameterAsText(1)
tbmj_1=arcpy.GetParameterAsText(2)
accuracy=int(arcpy.GetParameterAsText(3))

layer_out="stbhhx_identity"
keywords_1="ZCQCBSM"
balance_resuelt="STBHHXMJ"

arcpy.AddMessage('Creating identity layer...')
arcpy.Identity_analysis(layer_1,layer_STBHHX,layer_out) 
arcpy.AddMessage('Calculate Geodesic Area...')
arcpy.AddField_management(layer_out,"GeoAreaCalculate","DOUBLE")
arcpy.management.CalculateField(layer_out,"GeoAreaCalculate","!shape.geodesicArea!","PYTHON_9.3")

tar_table="FID_"+arcpy.Describe(layer_STBHHX).baseName
tar_table=tar_table.replace('(','_')
tar_table=tar_table.replace(')','_')
with arcpy.da.SearchCursor(layer_out,[tar_table,"ZCQCBSM"]) as cursor:
	for row in cursor:
		if row[0]!=-1 and row[1] not in keywords:
			keywords.append(row[1])
			arcpy.AddMessage(str(row[1])+' is in STBHHX')
#Extract unique value of keywords

for i in range(0,len(keywords)):
	expression=arcpy.AddFieldDelimiters(layer_out,"ZCQCBSM")+'=\''+keywords[i]+'\''#SQL query statement by patch number
	with arcpy.da.SearchCursor(layer_out,[keywords_1,tbmj_1,"GeoAreaCalculate"],where_clause=expression) as cursor:#In order, SQL queries the unique patch number
		mj_sum=0#Initial area 0
		k=0#Count the number of subgraphs
		mj_cal=[]#calculation area
		mj_TBMJ=[]
		#Count the details of sub patches of this group of patches
		for row in cursor:
			mj_sum=mj_sum+row[2]#sum calculation area
			mj_cal.append(row[2])#calculation area array
			mj_TBMJ.append(row[1])#TBMJ array
			k+=1
		#Only one keyworsds,no need to adjust
		if k==1:
			with arcpy.da.UpdateCursor(layer_out,[keywords_1,balance_resuelt],where_clause=expression) as cursor_2:#SQL query unique patch number assignment
				for row_2 in cursor_2:
					row_2[1]=mj_TBMJ[0]
					cursor_2.updateRow(row_2)
			continue
		#adjustment
		if abs(mj_sum-row[1])>0:
			j=0
			with arcpy.da.UpdateCursor(layer_out,[keywords_1,balance_resuelt],where_clause=expression) as cursor_3:
				for row_3 in cursor_3:
					row_3[1]=round(mj_TBMJ[j]*mj_cal[j]/mj_sum,accuracy)
					cursor_3.updateRow(row_3)
					j+=1
		#no need to adjust
		else:
			j=0
			with arcpy.da.UpdateCursor(layer_out,[keywords_1,balance_resuelt,tbmj_1],where_clause=expression) as cursor_4:
				for row_4 in cursor_4:
					row_4[1]=round(mj_cal[j],accuracy)
					cursor_4.updateRow(row_4)
					j+=1
#second adjust
arcpy.AddMessage('In second adjustment, waiting...')
for i in range(0,len(keywords)):
	expression=arcpy.AddFieldDelimiters(layer_out,keywords_1)+'=\''+keywords[i]+'\''
	with arcpy.da.SearchCursor(layer_out,[keywords_1,tbmj_1,balance_resuelt],where_clause=expression) as cursor_5:
		mj_sum=key_num=0#Initial area 0
		wrong_result=[]#Record error BSM
		#Count the details of this group of polygon
		for row_5 in cursor_5:
			mj_sum=mj_sum+row_5[2]#Calculated area summation
			wrong_result.append(row_5[2])#Statistical error area
			key_num+=1
		#Inaccurate adjustment
		differ_all=row_5[1]-mj_sum
		differ_long=len(wrong_result)
		differ_accuracy=0.1**accuracy
		#Only different less than 3 times accuracy will be readjust
		# if differ_all!=0 and key_num!=1 and differ_all<differ_long*differ_accuracy*3:
		arcpy.AddMessage(row_5[0]+' is readjusting')
		if differ_all>0:
			accuracy_adjust=round(differ_accuracy,accuracy)
		else:
			accuracy_adjust=0-round(differ_accuracy,accuracy)
		differ=int(round(abs(differ_all/accuracy_adjust),0))
		cycle=int(round(abs(math.floor(differ/differ_long)),0))
		order_wrong_result=wrong_result[:]
		order_wrong_result.sort()
		order_wrong_result.reverse()
		values_index_list=[]
		for rows in range(0,len(order_wrong_result)):
			values_index_list.append(wrong_result.index(order_wrong_result[rows]))
		if cycle>1:
			for n in range(0,cycle):
				for j in range(0,differ_long):
					wrong_result[j]+=accuracy_adjust#adjust in one cycle
		for m in range(0,differ-cycle*differ_long):
			wrong_result[values_index_list[m]]+=accuracy_adjust#adjust the left
		k=0
		with arcpy.da.UpdateCursor(layer_out,[balance_resuelt],where_clause=expression) as cursor_7:
			for row_7 in cursor_7:
				row_7[0]=wrong_result[k]
				cursor_7.updateRow(row_7)
				k+=1

#delete not in STBHHX
arcpy.AddMessage('Deleting useless value...')
expression=arcpy.AddFieldDelimiters(layer_out,tar_table)+'=-1'
arcpy.MakeTableView_management(layer_out,"accidentTableView")
arcpy.SelectLayerByAttribute_management("accidentTableView","NEW_SELECTION",expression)
arcpy.DeleteRows_management("accidentTableView")

#value back
arcpy.AddMessage('In summarizing...')
mj_total=dict([(k,0) for k in keywords])
for i in range(0,len(keywords)):
	expression=arcpy.AddFieldDelimiters(layer_out,keywords_1)+'=\''+keywords[i]+'\''
	temp=0
	with arcpy.da.SearchCursor(layer_out,[keywords_1,balance_resuelt],where_clause=expression) as cursor_8:
		for row_8 in cursor_8:
			temp+=row_8[1]
	mj_total.update({keywords[i]:temp})

arcpy.AddMessage('In value back...')
for i in range(0,len(keywords)):
	expression=arcpy.AddFieldDelimiters(layer_out,keywords_1)+'=\''+keywords[i]+'\''
	temp=0
	with arcpy.da.UpdateCursor(layer_1,[keywords_1,balance_resuelt],where_clause=expression) as cursor_9:
		for row_9 in cursor_9:
			row_9[1]=mj_total.get(keywords[i])
			cursor_9.updateRow(row_9)

arcpy.Delete_management(layer_out)










import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy,string
from arcpy.sa import *
from decimal import Decimal,ROUND_HALF_UP
#Loading plug-ins

if time.time()>time.mktime((2023,6,30,0,0,0,0,0,0)):
	arcpy.AddMessage(u'\u6388\u6743\u8d85\u671f\uff01')
	exit(0)
#term of validity

def right_round(num,keep_n):
    if isinstance(num,float):
        num = str(num)
    return Decimal(num).quantize((Decimal('0.' + '0'*keep_n)),rounding=ROUND_HALF_UP)

keywords=[]#Null unique value array

try:
	layer_1=arcpy.GetParameterAsText(0)#Select layer
	keywords_1=arcpy.GetParameterAsText(1)#Determine unique value column
	tbmj_1=arcpy.GetParameterAsText(2)#TBMJ
	shaparea_cal=arcpy.GetParameterAsText(3)#Area calculation field column
	balance_resuelt=arcpy.GetParameterAsText(4)#Results after adjustment
	accuracy=int(arcpy.GetParameterAsText(5))

	with arcpy.da.SearchCursor(layer_1,[keywords_1]) as cursor:
		for row in cursor:
			if row[0]==' ' or row[0]==None or row[0]==0:
				continue
			if row[0] not in keywords:
				keywords.append(row[0])
	#Extract unique value of keywords

	for i in range(0,len(keywords)):
		expression=arcpy.AddFieldDelimiters(layer_1,keywords_1)+'=\''+keywords[i]+'\''#SQL query statement by patch number
		with arcpy.da.SearchCursor(layer_1,[keywords_1,tbmj_1,shaparea_cal],where_clause=expression) as cursor:#In order, SQL queries the unique patch number
			arcpy.AddMessage(row[0])
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
				with arcpy.da.UpdateCursor(layer_1,[keywords_1,balance_resuelt],where_clause=expression) as cursor_2:#SQL query unique patch number assignment
					for row_2 in cursor_2:
						row_2[1]=mj_TBMJ[0]
						cursor_2.updateRow(row_2)
				continue
			#adjustment
			if abs(mj_sum-row[1])>0:
				j=0
				with arcpy.da.UpdateCursor(layer_1,[keywords_1,balance_resuelt],where_clause=expression) as cursor_3:
					for row_3 in cursor_3:
						row_3[1]=right_round(mj_TBMJ[j]*mj_cal[j]/mj_sum,accuracy)
						cursor_3.updateRow(row_3)
						j+=1
			#no need to adjust
			else:
				j=0
				with arcpy.da.UpdateCursor(layer_1,[keywords_1,balance_resuelt,tbmj_1],where_clause=expression) as cursor_4:
					for row_4 in cursor_4:
						if arcpy.GetParameter(6)==True:
							row_4[1]=row_4[2]
						else:
							row_4[1]=right_round(mj_cal[j],accuracy)
						cursor_4.updateRow(row_4)
						j+=1
	#second adjust
	arcpy.AddMessage(u'\u4e8c\u6b21\u5e73\u5dee\u4e2d...')
	for i in range(0,len(keywords)):
		expression=arcpy.AddFieldDelimiters(layer_1,keywords_1)+'=\''+keywords[i]+'\''
		with arcpy.da.SearchCursor(layer_1,[keywords_1,tbmj_1,balance_resuelt],where_clause=expression) as cursor_5:
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
			arcpy.AddMessage(row_5[0]+u'\u6b63\u5728\u91cd\u65b0\u5e73\u5dee')
			if differ_all>0:
				accuracy_adjust=float(right_round(differ_accuracy,accuracy))
			else:
				accuracy_adjust=0-float(right_round(differ_accuracy,accuracy))
			differ=int(right_round(abs(differ_all/accuracy_adjust),0))
			cycle=int(right_round(abs(math.floor(differ/differ_long)),0))
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
			with arcpy.da.UpdateCursor(layer_1,[balance_resuelt],where_clause=expression) as cursor_7:
				for row_7 in cursor_7:
					row_7[0]=wrong_result[k]
					cursor_7.updateRow(row_7)
					k+=1
			# else:
			# 	#Polygon differed more than 3 times accuracy will be reassigned calculated area, cause it may not be the segmented one.
			# 	with arcpy.da.UpdateCursor(layer_1,[balance_resuelt,shaparea_cal],where_clause=expression) as cursor_7:
			# 		for row_7 in cursor_7:
			# 			row_7[0]=round(row_7[1],2)
			# 			cursor_7.updateRow(row_7)

except arcpy.ExecuteError:
	print arcpy.GetMessages()
















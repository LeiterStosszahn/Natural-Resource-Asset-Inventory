import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy,string
from arcpy.sa import *
import pandas as pd
from decimal import Decimal,ROUND_HALF_UP

if time.time()>time.mktime((2023,11,30,0,0,0,0,0,0)):
	arcpy.AddMessage(u'\u6388\u6743\u8d85\u671f\uff01')
	exit(0)
#term of validity

def right_round(num,keep_n):
	if isinstance(num,float):
		num = str(num)
	return Decimal(num).quantize((Decimal('0.' + '0'*keep_n)),rounding=ROUND_HALF_UP)

layer_in=arcpy.GetParameter(0)#select layer
system=arcpy.GetParameterAsText(1)

#Load excel's sheet
arcpy.AddMessage(u'\u5bfc\u5165\u4ef7\u683c\u4f53\u7cfb\u6570\u636e\u4e2d')
code=pd.read_excel(system, sheetname=0, skiprows=0, usecols=[2,3], names=["XZQDM","code"])
farmland_price=pd.read_excel(system, sheetname=1, skiprows=0, usecols=[1,2,3], names=["code","rank","price"])
otherland_price=pd.read_excel(system, sheetname=2, skiprows=0, usecols=[1,3,4], names=["code","land_type","price"])
arcpy.AddMessage(code)
arcpy.AddMessage(farmland_price)
arcpy.AddMessage(otherland_price)
def cal_res(area,price):
	result=area*price/10000
	result_2=right_round(result,2)
	if result_2 !=0:
		return result_2
	else:
		return right_round(result,4)

def judge_null(input_result):
	if len(input_result)==0:
		return -10000
	else:
		return float(input_result[0][0])

for num in range(0,len(layer_in)):
	layer_1=str(layer_in[num])
	resurse_type=layer_1[8:]
	# if resurse_type!='C_XJFDDY':
	# 	arcpy.AddMessage(u'\u56fe\u5c42'+layer_1+u'\u4e0d\u662f\u519c\u7528\u5730')#Not XJFDDY
	# 	break
	# else:
	# 	arcpy.AddMessage(u'\u8ba1\u7b97'+layer_1+u'\u4ef7\u683c\u4e2d')
	
	with arcpy.da.UpdateCursor(layer_1,["XZQDM","DLBM","GDLYDB","QCJG","TBJJJZ","XJJGGSFF","TBDLMJ","ZCQCBSM"]) as cursor:
		for row in cursor:
			arcpy.AddMessage(u'\u8ba1\u7b97'+row[7]+u'\u4ef7\u683c\u4e2d')
			JZQ_code=str(code.loc[code['XZQDM']==int(row[0]),["code"]].values[0][0])
			land_type=int(row[1][0:4])
			#QCJG
			if land_type in (101,102,103):
				QCJG=judge_null(farmland_price.loc[(farmland_price['code']==JZQ_code) & (farmland_price['rank']==int(row[2])),["price"]].values)
			elif land_type in (1006,1107,1203):
				QCJG=0
			else:
				#chang 1103 to 1104
				if land_type==1103:
					land_type=1104
				QCJG=judge_null(otherland_price.loc[(otherland_price['code']==JZQ_code) & (otherland_price['land_type']==land_type),["price"]].values)
			row[3]=right_round(QCJG*0.0015,2)
			
			#price
			row[4]=cal_res(row[6],QCJG)
			row[5]="3"

			# #Update Value	
			cursor.updateRow(row)



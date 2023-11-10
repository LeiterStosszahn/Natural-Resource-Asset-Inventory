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
LD_price=pd.read_excel(system, sheetname=0, skiprows=4, usecols=[2,4,5,6,7,8,9], names=["XZQMC","QML","GM_JJ","GM_YB","ZL","QT","QS"])
YCL_price=pd.read_excel(system, sheetname=1, skiprows=2, usecols=[2,4,5,6,7], names=["XZQMC","SZ","QY","LZ","JG"])
ZL_price=pd.read_excel(system, sheetname=2, skiprows=2, usecols=[2,4,5], names=["XZQMC","SZ","JG"])
JJL_price=pd.read_excel(system, sheetname=3, skiprows=2, usecols=[2,4,5,6], names=["XZQMC","SZ","CQ","JG"])
LYL_price=pd.read_excel(system, sheetname=4, skiprows=2, usecols=[2,4,5], names=["XZQMC","SZ","JG"])

QS_dict={"1":2,"2":2,"3":3,"4":3}
DLBM_dict={"0301":"QML","0302":"ZL","0307":"QT"}
GM_QY_dict={"25":"GM_JJ"}
SZ_dict={
	"210000":290000,
	"320000":310000,
	"410001":410000,"410003":410000,
	"421000":420000,
	"530002":530000,
	"595006":595099,"595015":595099,"595021":595099,"595038":595099,"595039":595099,
	"999000":999099,"999008":999099,"943000":999099,
}
QY_dict={"1":u'\u5929\u7136',"2":u'\u4eba\u5de5'}
CQ_dict={
	u'\u5e7c\u9f84\u6797':u'\u4ea7\u524d\u671f',
	u'\u4e2d\u9f84\u6797':u'\u4ea7\u679c\u671f',
	u'\u8fd1\u719f\u6797':u'\u4ea7\u679c\u671f',
	u'\u6210\u719f\u6797':u'\u4ea7\u679c\u671f',
	u'\u8fc7\u719f\u6797':u'\u4ea7\u679c\u671f',
}
LZ_dict={'1':u'\u5e7c\u9f84\u6797','2':u'\u4e2d\u9f84\u6797','3':u'\u8fd1\u719f\u6797','4':u'\u6210\u719f\u6797','5':u'\u5e7c\u9f84\u6797'}
#'5':u'\u8fc7\u719f\u6797' Guoshu lin

def cal_res(area,price):
	result=area*price*0.0015/10000
	result_2=right_round(result,2)
	if result_2 !=0:
		return result_2
	else:
		return right_round(result,4)

def judge_null(input_result):
	if len(input_result)==0:
		return -10000
	else:
		return input_result[0][0]

for num in range(0,len(layer_in)):
	layer_1=str(layer_in[num])
	resurse_type=layer_1[8:]
	if resurse_type!='C_SL_GYTD' and resurse_type!='C_SL_YLTD' and resurse_type!='SLZYZC':
		arcpy.AddMessage(u'\u56fe\u5c42'+layer_1+u'\u4e0d\u5c5e\u4e8e\u6797\u5730\u56fe\u5c42')#Not SLZC
		break
	else:
		arcpy.AddMessage(u'\u8ba1\u7b97'+layer_1+u'\u4ef7\u683c\u4e2d')
	
	with arcpy.da.UpdateCursor(layer_1,["XZQMC","GTDCDLBM","GTDCTDQS","ZTBMJ","LZ","YSSZ","QY","LING_ZU","LDZC","LMZC","JJJZ","ZCQCBSM","LM_SUOYQ"]) as cursor:
		for row in cursor:
			arcpy.AddMessage(u'\u8ba1\u7b97'+row[11]+u'\u4ef7\u683c\u4e2d')
			#Price of YLTD
			LD_p=LD_price.loc[(LD_price['QS']==QS_dict.get(row[2][0:1])) & (LD_price['XZQMC']==row[0]),[DLBM_dict.get(row[1][0:4],GM_QY_dict.get(row[4][0:2],"GM_YB"))]].values[0][0]
			row[8]=cal_res(row[3],LD_p)
			# #If LM_SUOYQ is not nationalized, don't need to calculate the price of trees
			# if row[12]!="1":
			# 	row[9]=0
			# 	row[10]=row[8]
			# 	cursor.updateRow(row)
			# 	continue
			
			ZL_bool=(row[5]=="660000" or row[5]=="670000" or row[5]=="680000" or row[5]=="690000")

			#Price of ZL
			if ZL_bool:
				ZL_p=ZL_price.loc[(ZL_price['XZQMC']==row[0]) & (ZL_price['SZ']==int(row[5])),["JG"]].values[0][0]
				row[9]=cal_res(row[3],ZL_p)

			#Price of 230(LZ)
			if (row[4][0:2]=="23" or row[4][0:2]=="11" or row[4][0:2]=="12") and ZL_bool!=True:
				YCL_p_arr=YCL_price.loc[(YCL_price['XZQMC']==row[0]) & (YCL_price['SZ']==SZ_dict.get(row[5],int(row[5]))) & (YCL_price['QY']==QY_dict.get(row[6][0:1],u'\u4eba\u5de5')) & (YCL_price['LZ']==LZ_dict.get(row[7],u'\u5e7c\u9f84\u6797')),["JG"]].values
				YCL_p=judge_null(YCL_p_arr)
				row[9]=cal_res(row[3],YCL_p)

			#Price of 240(LZ)
			if row[4][0:2]=="24":
				LYL_p_arr=LYL_price.loc[LYL_price['XZQMC']==row[0],["JG"]].values
				LYL_p=judge_null(LYL_p_arr)
				row[9]=cal_res(row[3],LYL_p)

			#Pirce of 250(LZ)
			if row[4][0:2]=="25" and ZL_bool!=True:
				JJL_p_arr=JJL_price.loc[(JJL_price['XZQMC']==row[0]) & (JJL_price['SZ']==SZ_dict.get(row[5],int(row[5]))) & (JJL_price['CQ']==CQ_dict.get(row[5],u'\u4ea7\u524d\u671f')),["JG"]].values
				JJL_p=judge_null(JJL_p_arr)
				row[9]=cal_res(row[3],JJL_p)

			#sum
			row[10]=right_round(float(row[8])+float(row[9]),4)

			# #Update Value	
			cursor.updateRow(row)



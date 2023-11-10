import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy,string
from arcpy.sa import *
import pandas as pd
from decimal import Decimal,ROUND_HALF_UP

if time.time()>time.mktime((2022,11,30,0,0,0,0,0,0)):
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
LD_price=pd.read_excel(system, sheetname=0, skiprows=4, usecols=[1,4,5,6,7,8], names=["XZQDM","QML","GM_JJ","GM_YB","ZL","QT"])
YCL_price=pd.read_excel(system, sheetname=1, skiprows=2, usecols=[1,4,5,6,7], names=["XZQDM","SZ","QY","LZ","JG"])
ZL_price=pd.read_excel(system, sheetname=2, skiprows=2, usecols=[1,4,5], names=["XZQDM","SZ","JG"])
JJL_price=pd.read_excel(system, sheetname=3, skiprows=2, usecols=[1,4,5,6], names=["XZQDM","SZ","CQ","JG"])
LYL_price=pd.read_excel(system, sheetname=4, skiprows=2, usecols=[1,4,5], names=["XZQDM","SZ","JG"])

DLBM_dict={"0301":"QML","0302":"ZL","0307":"QT"}
GM_QY_dict={"25":"GM_JJ"}
ZLSZ_dict={"660000":u'\u6bdb\u7af9',"670000":u'\u6563\u751f\u6742\u7af9\u7c7b',"680000":u'\u4e1b\u751f\u6742\u7af9\u7c7b',"690000":u'\u6df7\u751f\u6742\u7af9\u7c7b'}
SZ_dict={
	"100000":u'\u5176\u4ed6\u6749',"804000":u'\u5176\u4ed6\u6749',#Both are ginkgo
	"220000":u'\u9a6c\u5c3e\u677e',
	"261000":u'\u6e7f\u5730\u677e',
	"310000":u'\u6749\u6728',"320000":u'\u67f3\u6749',"330000":u'\u6c34\u6749',"350000":u'\u67cf\u6728',
	"399000":u'\u5176\u5b83\u6749\u7c7b\uff08\u9488\u53f6\u6811\u79cd\uff09',
	"410000":u'\u680e\u7c7b',"418000":u'\u680e\u7c7b',
	"440000":u'\u9999\u6a1f',"441000":u'\u9999\u6a1f',
	"460000":u'\u6986\u6811',"464000":u'\u6986\u6811',
	"477000":u'\u6728\u8377',
	"480000":u'\u67ab\u9999',"489000":u'\u67ab\u9999',
	"490000":u'\u5176\u5b83\u786c\u9614\u7c7b\uff08\u9614\u53f6\u6811\u79cd\uff09',"494000":u'\u5176\u5b83\u786c\u9614\u7c7b\uff08\u9614\u53f6\u6811\u79cd\uff09',
	"512000":u'\u6934\u6811',"515000":u'\u6934\u6811',
	"520000":u'\u6aab\u6728',"521000":u'\u6aab\u6728',
	"530000":u'\u6768\u6811',"534000":u'\u6768\u6811',
	"540000":u'\u6ce1\u6850',
	"565000":u'\u76f8\u601d',
	"570000":u'\u6728\u9ebb\u9ec4',"579000":u'\u6728\u9ebb\u9ec4',
	"590000":u'\u5176\u5b83\u8f6f\u9614\u7c7b',"593000":u'\u5176\u5b83\u8f6f\u9614\u7c7b',"594000":u'\u5176\u5b83\u8f6f\u9614\u7c7b',"598000":u'\u5176\u5b83\u8f6f\u9614\u7c7b',
	"610000":u'\u9488\u53f6\u6df7',
	"620000":u'\u9614\u53f6\u6df7',
	"630000":u'\u9488\u9614\u6df7',
	"700000":u'\u5176\u4ed6\u679c\u6811',
	"701000":u'\u67d1\u6854\u7c7b',"703000":u'\u68a8',"704000":u'\u6843',"705000":u'\u674e',"707000":u'\u67a3',
	"711000":u'\u677f\u6817',
	"751000":u'\u6cb9\u8336',"755000":u'\u8336\u53f6',
	"761000":u'\u6842\u82b1',
	"806000":u'\u5176\u5b83\uff08\u5176\u5b83\u7ecf\u6d4e\u7c7b\uff09',
	"819000":u'\u5176\u5b83',
	"823000":u'\u6cb9\u6850',
	"859000":u'\u5176\u5b83\uff08\u5176\u5b83\u7ecf\u6d4e\u7c7b\uff09',
	"900000":u'\u5176\u4ed6\u704c\u6728',"907000":u'\u5176\u4ed6\u704c\u6728',
	"943000":u'\u680e\u704c',"945000":u'\u5176\u4ed6\u704c\u6728',"948000":u'\u5176\u4ed6\u704c\u6728',
	"981000":u'\u7af9\u704c',"999000":u'\u5176\u4ed6\u704c\u6728',
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

for num in range(0,len(layer_in)):
	layer_1=str(layer_in[num])
	resurse_type=layer_1[8:]
	if resurse_type!='C_SL_GYTD' and resurse_type!='C_SL_YLTD' and resurse_type!='SLZYZC':
		arcpy.AddMessage(u'\u56fe\u5c42'+layer_1+u'\u4e0d\u5c5e\u4e8e\u6797\u5730\u56fe\u5c42')#Not SLZC
		break
	else:
		arcpy.AddMessage(u'\u8ba1\u7b97'+layer_1+u'\u4ef7\u683c\u4e2d')
	
	with arcpy.da.UpdateCursor(layer_1,["XZQDM","GTDCDLBM","GTDCTDQS","ZTBMJ","LZ","YSSZ","QY","LING_ZU","LDZC","LMZC","JJJZ","ZCQCBSM","LM_SUOYQ"]) as cursor:
		for row in cursor:
			arcpy.AddMessage(u'\u8ba1\u7b97'+row[11]+u'\u4ef7\u683c\u4e2d')
			#Price of YLTD
			if row[2][0:1]=="1" or row[2][0:1]=="2":
				LD_p=LD_price.loc[LD_price['XZQDM']==int(row[0]),[DLBM_dict.get(row[1][0:4],GM_QY_dict.get(row[4][0:2],"GM_YB"))]].values[0][0]
				row[8]=cal_res(row[3],LD_p)
				#If LM_SUOYQ is not nationalized, don't need to calculate the price of trees
				if row[12]!="1":
					row[9]=0
					row[10]=row[8]
					cursor.updateRow(row)
					continue
			
			ZL_bool=(row[5]=="660000" or row[5]=="670000" or row[5]=="680000" or row[5]=="690000")

			#Price of ZL
			if ZL_bool:
				ZL_p=ZL_price.loc[(ZL_price['XZQDM']==int(row[0])) & (ZL_price['SZ']==ZLSZ_dict.get(row[5])),["JG"]].values[0][0]
				row[9]=cal_res(row[3],ZL_p)

			#Price of 230(LZ)
			if (row[4][0:2]=="23" or row[4][0:2]=="11" or row[4][0:2]=="12") and ZL_bool!=True:
				YCL_p_arr=YCL_price.loc[(YCL_price['XZQDM']==int(row[0])) & (YCL_price['SZ']==SZ_dict.get(row[5])) & (YCL_price['QY']==QY_dict.get(row[6][0:1],u'\u4eba\u5de5')) & (YCL_price['LZ']==LZ_dict.get(row[7],u'\u5e7c\u9f84\u6797')),["JG"]].values
				if len(YCL_p_arr)==0:
					YCL_p=0
				else:
					YCL_p=YCL_p_arr[0][0]
				row[9]=cal_res(row[3],YCL_p)

			#Price of 240(LZ)
			if row[4][0:2]=="24":
				LYL_p_arr=LYL_price.loc[(LYL_price['XZQDM']==int(row[0])) & (LYL_price['SZ']==SZ_dict.get(row[5])),["JG"]].values
				if len(LYL_p_arr)==0:
					LYL_p=0
				else:
					LYL_p=LYL_p_arr[0][0]
				row[9]=cal_res(row[3],LYL_p)

			#Pirce of 250(LZ)
			if row[4][0:2]=="25" and ZL_bool!=True:
				JJL_p_arr=JJL_price.loc[(JJL_price['XZQDM']==int(row[0])) & (JJL_price['SZ']==SZ_dict.get(row[5])) & (JJL_price['CQ']==CQ_dict.get(row[5],u'\u4ea7\u524d\u671f')),["JG"]].values
				if len(JJL_p_arr)==0:
					JJL_p=0
				else:
					JJL_p=JJL_p_arr[0][0]
				row[9]=cal_res(row[3],JJL_p)

			#sum
			row[10]=right_round(float(row[8])+float(row[9]),4)

			#Update Value	
			cursor.updateRow(row)


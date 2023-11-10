import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy,string
from arcpy.sa import *
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
system=system.split(',')

def split_price(types,manual,natural,other):
	if types=="0401":
		return float(natural)
	elif types=="0403":
		return float(manual)
	else:
		return float(other)

for num in range(0,len(layer_in)):
	layer_1=str(layer_in[num])
	resurse_type=layer_1[8:]
	# if resurse_type!='C_XJFDDY':
	# 	arcpy.AddMessage(u'\u56fe\u5c42'+layer_1+u'\u4e0d\u662f\u519c\u7528\u5730')#Not XJFDDY
	# 	break
	# else:
	# 	arcpy.AddMessage(u'\u8ba1\u7b97'+layer_1+u'\u4ef7\u683c\u4e2d')
	
	with arcpy.da.UpdateCursor(layer_1,["GTDCDLBM","GTDCQSXZ","JJJZ","ZTBMJ","ZCQCBSM"]) as cursor:
		for row in cursor:
			arcpy.AddMessage(u'\u8ba1\u7b97'+row[4]+u'\u4ef7\u683c\u4e2d')
			types=row[0]
			if row[1][0:1]=="2":
				price=split_price(types,system[0],system[1],system[2])
			else:
				price=split_price(types,system[3],system[4],system[5])

			#price
			row[2]=right_round(price*0.0015*row[3],4)

			#Update Value	
			cursor.updateRow(row)



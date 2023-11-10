import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy,string,random
import pandas as pd
from arcpy.sa import *
from decimal import Decimal,ROUND_HALF_UP

#Term of validity
if time.time()>time.mktime((2023,11,30,0,0,0,0,0,0)):
	arcpy.AddMessage(u'\u6388\u6743\u8d85\u671f\uff01')
	exit(0)

def right_round(num,keep_n):
	if isinstance(num,float):
		num = str(num)
	return Decimal(num).quantize((Decimal('0.' + '0'*keep_n)),rounding=ROUND_HALF_UP)

layer_in=arcpy.GetParameter(0)
system=arcpy.GetParameter(1)
bool_land=arcpy.GetParameter(2)
bool_date=arcpy.GetParameter(4)
system_list=map(lambda x:str(x)[12:], system)#change system layer in a list to indicate index


DL_dict={"0602":"CKYD","0601":"GYYD","0701":"CZZZYD","0810":"GYYLD","0809":"GYSSYD","08H1":"JGTTXWCBYD","08H2":"KJWWYD","1002":"GDJTYD","1003":"GLYD","1004":"CZCDLYD","1005":"JTFWCZYD","1007":"JCYD","1008":"GKMTYD","1009":"GDYSYD","0702":"NCZJD","1109":"SGJZYD","05H1":"SYFWYSSYD","09":"TSYD","0508":"WLCCYD"}
DLDM_dict={"CKYD":"0602","GYYD":"0601","CZZZYD":"0701","GYYLD":"0810","GYSSYD":"0809","JGTTXWCBYD":"08H1","KJWWYD":"08H2","GDJTYD":"1002","GLYD":"1003","CZCDLYD":"1004","JTFWCZYD":"1005","JCYD":"1007","GKMTYD":"1008","GDYSYD":"1009","NCZJD":"0702","SGJZYD":"1109","SYFWYSSYD":"05H1","TSYD":"09","WLCCYD":"0508"}
dl_yeardirt={"05":40,"07":70}
date_dict={"CKYD":{},"GYYD":{},"CZZZYD":{},"GYYLD":{},"GYSSYD":{},"JGTTXWCBYD":{},"KJWWYD":{},"GDJTYD":{},"GLYD":{},"CZCDLYD":{},"JTFWCZYD":{},"JCYD":{},"GKMTYD":{},"GDYSYD":{},"NCZJD":{},"SGJZYD":{},"SYFWYSSYD":{},"TSYD":{},"WLCCYD":{}}

#Defination of date amend 
if bool_date:
	arcpy.AddMessage(u'\u8bfb\u53d6\u4fee\u6b63\u8868\u4e2d')
	system_basic_date=arcpy.GetParameterAsText(5)
	date_pd=pd.read_excel(system_basic_date, sheetname=0, skiprows=1, usecols=[1,3,4], names=["XZQMC","DL","coefficient"])
	for DL_key in date_dict.keys():
		date_arr=date_pd.loc[date_pd['DL']==DL_key,["XZQMC","coefficient"]].values
		for value in date_arr:
			date_dict[DL_key][value[0]]=value[1]

#Result precision control
def cal_res(area,price):
	result=area*price
	result_2=right_round(result,2)
	if result_2 !=0:
		return result_2
	else:
		return right_round(result,4)

def random_name(name,lenth):
    return name+"_"+"".join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',lenth))

#Main
for num in range(0,len(layer_in)):
	layer_1=str(layer_in[num])
	DL=[]
	# #Inspect the layer, not necessary
	# resurse_type=layer_1[8:]
	# if resurse_type!='C_SL_GYTD' and resurse_type!='C_SL_YLTD' and resurse_type!='SLZYZC':
	# 	arcpy.AddMessage(u'\u56fe\u5c42'+layer_1+u'\u4e0d\u5c5e\u4e8e\u6797\u5730\u56fe\u5c42')#Invalid
	# 	break
	# else:
	# 	arcpy.AddMessage(u'\u8ba1\u7b97'+layer_1+u'\u4ef7\u683c\u4e2d')
	
	JB_BZ=random_name("JB",5)
	arcpy.AddField_management(layer_1,JB_BZ,"TEXT")

	#Serach for DL
	with arcpy.da.SearchCursor(layer_1,["EJDLBM"]) as cursor1:
		for row1 in cursor1:
			if row1[0]==' ' or row1[0]==None or row1[0]==0:
				continue
			# if row1[0][0:2]=="10":
			# 	DL_name="JTYSYD"
			else:
				DL_name=DL_dict.get(row1[0])
			if DL_name not in DL:
				DL.append(DL_name)

	for DL_single in DL:
		#Select the propared identify layer
		try:
			index=system_list.index(DL_single)
		except:
			arcpy.AddMessage(u'\u7f3a\u5c11\u56fe\u5c42\u540d\u4e3a'+DL_single+u'\u7684\u4ef7\u683c\u4f53\u7cfb\u56fe\u5c42\uff0c\u8ba1\u7b97\u7ec8\u6b62')
			exit()
		system_layer=system[index]
		EJDLBM=DLDM_dict.get(DL_single)

		#Identity
		arcpy.AddMessage(u'\u6807\u8bc6'+str(layer_1)+u'\u4e0e'+str(system_layer)+u'\u4e2d')
		layer_identity=random_name("identity_"+DL_single,10)
		arcpy.Identity_analysis(layer_1,system_layer,layer_identity)

		#Get keywords
		keywords=[]
		expression_DL=arcpy.AddFieldDelimiters(layer_identity,"EJDLBM")+'like\''+EJDLBM+'%\''#SQL
		with arcpy.da.SearchCursor(layer_identity,["ZCQCBSM"],where_clause=expression_DL) as cursor:
			for row in cursor:
				if row[0]==' ' or row[0]==None or row[0]==0:
					continue
				if row[0] not in keywords:
					keywords.append(row[0])

		#Calculate average price in a single DL
		for i in keywords:
			arcpy.AddMessage(i)
			expression=arcpy.AddFieldDelimiters(layer_identity,"ZCQCBSM")+'=\''+i+'\''#SQL
			with arcpy.da.SearchCursor(layer_identity,["ZCQCBSM","Shape_Area","ZTBMJ","JBJG","JB","XZQMC"],where_clause=expression) as cursor_1:
				land_price=percentage=0
				JB=""
				for row_1 in cursor_1:
					percentage=row_1[1]/row_1[2]
					date_amend=date_dict.get(DL_single,{}).get(row_1[5],1)
					if percentage>0.9 or row_1[1]<=0.01:
						land_price=row_1[3]*date_amend
						JB=row_1[4]+"_100"
						break
					else:
						land_price+=row_1[3]*percentage*date_amend
						JB+=row_1[4]+"_"+str(round(percentage*100,0))+"_"
			#Value back
			with arcpy.da.UpdateCursor(layer_1,["ZCQCBSM","QYQCJGSP",JB_BZ,"ZTBMJ","JJJZL1","GYFS","GYNX","YSYNX","YJDLBM","SYZQYXS","QSXZ"],where_clause=expression) as cursor_2:
				for row_2 in cursor_2:
					if row_2[10][0:1] in("1","2"):
						land_price=float(right_round(land_price,2))
					else:
						#National change to collective, may need refining according to the specific conidition
						land_price=float(right_round(land_price*0.5,2))
						##If it is unnecessary to calculate collective lands' preice
						#continue
					row_2[1]=land_price
					#import rank
					row_2[2]=str(JB)
					row_2[4]=cal_res(row_2[3]/10000,land_price)
					#SYZQYXS
					if row_2[5]=="6":
						SYZQYXS=1
					elif row_2[5] in("1","7"):
						SYZQYXS=0.4
					elif row_2[5]=="3":
						SYZQYXS=float(right_round((20-row_2[6]+row_2[7])/20,4))
					elif row_2[6]==0:
						SYZQYXS=0
					else:
						year_full=dl_yeardirt.get(row_2[8],50)
						remain_year=year_full-row_2[6]
						if remain_year<0:
							remain_year=0
							year_full=row_2[6]
						SYZQYXS=float(right_round((remain_year+row_2[7])/year_full,4))
					row_2[9]=SYZQYXS
					cursor_2.updateRow(row_2)
		arcpy.Delete_management(layer_identity)

	#Plot ratio amend
	if bool_land:
		system_basic_land=arcpy.GetParameterAsText(3)
		land_pd=pd.read_excel(system_basic_land, sheetname=0, skiprows=1)
		#Chagne TDYT into list
		land_pd['TDYT']=land_pd.TDYT.map(lambda x:x.split(','))
		with arcpy.da.UpdateCursor(layer_1,["XZQDM","TDYT","RJL",JB_BZ,"QYQCJGSP","XZQCDJSP","JJJZL2","ZTBMJ","JJJZL1","ZCQCBSM"]) as cursor:
			for row in cursor:
				if row[2]==0 or row[2] is None:
					arcpy.AddMessage(row[9]+u'\u5bb9\u79ef\u7387\u4e3a\u7a7a\uff0c\u672a\u8ba1\u7b97\u5bb9\u79ef\u7387')
					row[5]=row[4]
					row[6]=row[8]
					cursor.updateRow(row)
					continue
				XZQDM=int(row[0])
				ranks_and_percent=row[3].split('_')
				ranks=ranks_and_percent[0::2]
				percent=map(lambda x:float(x)/100,ranks_and_percent[1::2])
				ranks_dict=dict(zip(ranks,percent))
				RJL_up=int(row[2]*10)/float(10)
				difference=land_pd.loc[land_pd['XZQDM']==XZQDM,'RJL'].values[1]-land_pd.loc[land_pd['XZQDM']==XZQDM,'RJL'].values[0]
				RJL_down=RJL_up+difference
				RJL_min=land_pd.loc[land_pd['XZQDM']==XZQDM,'RJL'].values[0]
				RJL_max=land_pd.loc[land_pd['XZQDM']==XZQDM,'RJL'].values[-1]
				RJL_correct=0
				for rank in ranks:
					if float(row[2])<=RJL_min:
						RJL_correct+=land_pd.loc[(land_pd['XZQDM']==XZQDM)&(land_pd["RJL"]==RJL_min),[rank]].values[0][0]*ranks_dict.get(rank)
					elif float(row[2])>=RJL_max:
						RJL_correct+=land_pd.loc[(land_pd['XZQDM']==XZQDM)&(land_pd["RJL"]==RJL_max),[rank]].values[0][0]*ranks_dict.get(rank)
					else:
						RJL_correct_up=land_pd.loc[(land_pd['XZQDM']==XZQDM)&(land_pd["RJL"]==RJL_up),[rank]].values[0][0]
						RJL_correct_down=land_pd.loc[(land_pd['XZQDM']==XZQDM)&(land_pd["RJL"]==RJL_down),[rank]].values[0][0]
						RJL_correct+=(RJL_correct_up+(row[2]-RJL_up)*(RJL_correct_down-RJL_correct_up)/difference)*ranks_dict.get(rank)
				row[5]=float(right_round(row[4]*RJL_correct,2))
				row[6]=cal_res(row[5],row[7]/10000)
				cursor.updateRow(row)
	else:
		arcpy.management.CalculateField(layer_1,"XZQCDJSP","!QYQCJGSP!","PYTHON_9.3")
		arcpy.management.CalculateField(layer_1,"JJJZL2","!JJJZL1!","PYTHON_9.3")

	with arcpy.da.UpdateCursor(layer_1,["SYZQYGSZ","SYZQYXS","JJJZL2"]) as cursor_f:
		for row_f in cursor_f:
			row_f[0]=cal_res(row_f[1],row_f[2])
			cursor_f.updateRow(row_f)


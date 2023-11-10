import arcpy
import pandas as pd

from decimal import Decimal,ROUND_HALF_UP
def right_round(num,keep_n):
    if isinstance(num,float):
        num = str(num)
    return Decimal(num).quantize((Decimal('0.' + '0'*keep_n)),rounding=ROUND_HALF_UP)

if time.time()>time.mktime((2022,11,30,0,0,0,0,0,0)):
	arcpy.AddMessage(u'\u6388\u6743\u8d85\u671f\uff01')
	exit(0)
#term of validity

def get_keywords(layer,*key_in):
	arcpy.AddMessage(u'\u5728\u56fe\u5c42'+str(layer)+u'\u4e2d\u83b7\u53d6\u552f\u4e00\u503c\uff1a'+str(key_in))
	l=len(key_in)
	outlist=()
	if l==1:
		key1=[]
		outlist=(key1)
		with arcpy.da.UpdateCursor(layer,key_in) as cursor:
			for row in cursor:
				if row[0] not in key1:
					key1.append(row[0])
	else: 
		for i in range(0,l):
			exec('key_{}={}'.format(i,[])) in locals()
			outlist=outlist+(locals().get('key_'+str(i)),)
		with arcpy.da.UpdateCursor(layer,key_in) as cursor:
			for row in cursor:
				for j in range(0,l):
					keyj=locals().get('key_'+str(j))
					if row[j] not in keyj:
						keyj.append(row[j])
	return outlist

def del_null_list(result,head_list,k):
	arcpy.AddMessage(u'\u5220\u9664\u7a7a\u884c\uff1a'+str(k))
	for i in range(0,len(head_list)):
		del result.get(head_list[i])[k]

#Sum for row
def calculate_sum_row(form,column,row_result,*row_add):
	arcpy.AddMessage(u'\u6b63\u5728\u8ba1\u7b97\u7b2c'+str(row_result+1)+u'\u884c\u7b2c'+str(column)+u'\u5217\u6c42\u548c\u6570\u636e')
	for i in range(0,len(row_add)):
		form.get(column)[row_result]+=form.get(column)[row_add[i]]

layer_1=arcpy.GetParameterAsText(0)#select begining layer of LD
layer_2=arcpy.GetParameterAsText(1)#select ending layer of LD
layer_3=arcpy.GetParameterAsText(2)#select begining layer of LM
layer_4=arcpy.GetParameterAsText(3)#select ending layer of LM
path_outp=arcpy.GetParameterAsText(4)#output

key3_1=get_keywords(layer_3,'GTDCDLBM')
key4_1=get_keywords(layer_4,'GTDCDLBM')
result_1={'GTDCDLBM':[],'ZTBMJ':[],'JJJZ':[]}
result_2={'GTDCDLBM':[],'ZTBMJ':[],'JJJZ':[]}
result_3={'GTDCDLBM':[],'ZTBMJ':[],'ZTBZS':[],'JJJZ':[]}
result_4={'GTDCDLBM':[],'ZTBMJ':[],'ZTBZS':[],'JJJZ':[]}
order=['GTDCDLBM','ZTBMJ','ZTBZS','JJJZ']#excle's order
#Beginning of the period 
ZTBMJ_1=JJJZ_1=0
with arcpy.da.SearchCursor(layer_1,order) as cursor_1:
	for row_1 in cursor_1:
		ZTBMJ_1+=row_1[1]
		JJJZ_1+=row_1[3]
result_1.get('GTDCDLBM').append('LD')
result_1.get('ZTBMJ').append(right_round(ZTBMJ_1/10000,2))
result_1.get('JJJZ').append(right_round(JJJZ_1,2))

for n in range(0,len(key3_1)):
	ZTBMJ_3=JJJZ_3=ZTBZS_3=0
	expression_3=arcpy.AddFieldDelimiters(layer_3,'GTDCDLBM')+'=\''+key3_1[n]+'\''
	with arcpy.da.SearchCursor(layer_3,order,where_clause=expression_3) as cursor_3:
		for row_3 in cursor_3:
			ZTBMJ_3+=row_3[1]
			ZTBZS_3+=row_3[2]
			JJJZ_3+=row_3[3]
	result_3.get('GTDCDLBM').append(str(row_3[0]))
	result_3.get('ZTBMJ').append(right_round(ZTBMJ_3/10000,2))
	result_3.get('ZTBZS').append(right_round(ZTBZS_3/10000,2))
	result_3.get('JJJZ').append(right_round(JJJZ_3,2))

#Ending of the period
ZTBMJ_2=JJJZ_2=0
with arcpy.da.SearchCursor(layer_2,order) as cursor_2:
	for row_2 in cursor_2:
		ZTBMJ_2+=row_2[1]
		JJJZ_2+=row_2[3]
result_2.get('GTDCDLBM').append('LD')
result_2.get('ZTBMJ').append(right_round(ZTBMJ_2/10000,2))
result_2.get('JJJZ').append(right_round(JJJZ_2,2))

for j in range(0,len(key4_1)):
	ZTBMJ_4=JJJZ_4=ZTBZS_4=0
	expression_4=arcpy.AddFieldDelimiters(layer_4,'GTDCDLBM')+'=\''+key4_1[j]+'\''
	with arcpy.da.SearchCursor(layer_4,order,where_clause=expression_4) as cursor_4:
		for row_4 in cursor_4:
			ZTBMJ_4+=row_4[1]
			ZTBZS_4+=row_4[2]
			JJJZ_4+=row_4[3]
	result_4.get('GTDCDLBM').append(str(row_4[0]))
	result_4.get('ZTBMJ').append(right_round(ZTBMJ_4/10000,2))
	result_4.get('ZTBZS').append(right_round(ZTBZS_4/10000,2))
	result_4.get('JJJZ').append(right_round(JJJZ_4,2))

#delete NULL list
res_check_1=res_check_2=res_check_3=res_check_4=0
while res_check_1<len(result_1.get('GTDCDLBM')):
	if (
		result_1.get('ZTBMJ')[res_check_1]==
		result_1.get('JJJZ')[res_check_1]==0
		):
		del_null_list(result_1,order,res_check_1)
	else:
		res_check_1+=1
while res_check_2<len(result_2.get('GTDCDLBM')):
	if (
		result_2.get('ZTBMJ')[res_check_2]==
		result_2.get('JJJZ')[res_check_2]==0
		):
		del_null_list(result_2,order,res_check_2)
	else:
		res_check_2+=1
while res_check_3<len(result_3.get('GTDCDLBM')):
	if (
		result_3.get('ZTBMJ')[res_check_3]==
		result_3.get('ZTBZS')[res_check_3]==
		result_3.get('JJJZ')[res_check_3]==0
		):
		del_null_list(result_3,order,res_check_3)
	else:
		res_check_3+=1
while res_check_4<len(result_4.get('GTDCDLBM')):
	if (
		result_4.get('ZTBMJ')[res_check_4]==
		result_4.get('ZTBZS')[res_check_4]==
		result_4.get('JJJZ')[res_check_4]==0
		):
		del_null_list(result_4,order,res_check_4)
	else:
		res_check_4+=1
#final resault
result_fin={
	'SYZQY':['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20'],
	'SL_QC':[0,0,0,0,0,'--','--','--','--','--',0,0,0,0,0,0,0,0,0,0],
	'SL_QM':[0,0,0,0,0,'--','--','--','--','--',0,0,0,0,0,0,0,0,0,0],
	'JE_QC':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	'JE_QM':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}
order_fin=['SYZQY','SL_QC','SL_QM','JE_QC','JE_QM']

result_fin.get('SL_QC')[1]=result_1.get('ZTBMJ')[0]
result_fin.get('JE_QC')[1]=result_1.get('JJJZ')[0]
result_fin.get('SL_QM')[1]=result_2.get('ZTBMJ')[0]
result_fin.get('JE_QM')[1]=result_2.get('JJJZ')[0]
for j in range(0,len(result_3.get('GTDCDLBM'))):
	if str(result_3.get('GTDCDLBM')[j])[0:4]=='0301':
		result_fin.get('SL_QC')[11]=result_3.get('ZTBMJ')[j]
		result_fin.get('JE_QC')[11]=result_3.get('JJJZ')[j]
	elif str(result_3.get('GTDCDLBM')[j])[0:4]=='0302':
		result_fin.get('SL_QC')[16]=result_3.get('ZTBMJ')[j]
		result_fin.get('JE_QC')[16]=result_3.get('JJJZ')[j]
for k in range(0,len(result_4.get('GTDCDLBM'))):
	if str(result_4.get('GTDCDLBM')[k])[0:4]=='0301':
		result_fin.get('SL_QM')[11]=result_4.get('ZTBMJ')[k]
		result_fin.get('JE_QM')[11]=result_4.get('JJJZ')[k]
	elif str(result_4.get('GTDCDLBM')[k])[0:4]=='0302':
		result_fin.get('SL_QM')[16]=result_4.get('ZTBZS')[k]
		result_fin.get('JE_QM')[16]=result_4.get('JJJZ')[k]
for order_i in ['SL_QC','SL_QM','JE_QC','JE_QM']:
	calculate_sum_row(result_fin,order_i,0,1,2,3,4)
	calculate_sum_row(result_fin,order_i,10,11,12,13,14)
	calculate_sum_row(result_fin,order_i,15,16,17,18,19)
for order_i in ['JE_QC','JE_QM']:
	calculate_sum_row(result_fin,order_i,5,10,15)
	calculate_sum_row(result_fin,order_i,6,11,16)
	calculate_sum_row(result_fin,order_i,7,12,17)
	calculate_sum_row(result_fin,order_i,8,13,18)
	calculate_sum_row(result_fin,order_i,9,14,19)

output=pd.DataFrame(result_fin)[order_fin]
#change header to chinese(test)
# if resurse_type=='CYZYZC_JJL':
# 	output.columns=[u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe5\x90\x8d\xe7\xa7\xb0',u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe4\xbb\xa3\xe7\xa0\x81',
# 					u'\xe5\x9c\xb0\xe7\xb1\xbb',u'\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\x88\x92\xe5\x85\xa5\xe7\x94\x9f\xe6\x80\x81\xe4\xbf\x9d\xe6\x8a\xa4\xe7\xba\xa2\xe7\xba\xbf\xe7\x9a\x84\xe9\x9d\xa2\xe7\xa7\xaf',u'\xe8\x87\xaa\xe7\x84\xb6\xe4\xbf\x9d\xe6\x8a\xa4\xe5\x9c\xb0\xe6\xa0\xb8\xe5\xbf\x83\xe5\x8c\xba\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\xb9\xb2\xe8\x8d\x89\xe4\xba\xa7\xe9\x87\x8f',u'\xe7\x90\x86\xe8\xae\xba\xe8\xbd\xbd\xe7\x95\x9c\xe9\x87\x8f',u'\xe8\x8d\x89\xe5\x9c\xb0\xe4\xbb\xb7\xe5\x80\xbc']
output.to_excel(path_outp,index=False)#output result








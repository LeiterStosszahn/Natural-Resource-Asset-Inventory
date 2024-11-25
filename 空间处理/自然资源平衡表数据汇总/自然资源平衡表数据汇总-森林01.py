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

layer_1=arcpy.GetParameterAsText(0)#select begining layer
layer_2=arcpy.GetParameterAsText(1)#select ending layer
path_outp=arcpy.GetParameterAsText(2)#output


key1_1,key1_2=get_keywords(layer_1,'GTDCDLBM','LZ')
key2_1,key2_2=get_keywords(layer_2,'GTDCDLBM','LZ')
result_1={'GTDCDLBM':[],'LZ':[],'ZTBMJ':[],'JJJZ':[],'ZTBZS':[]}#Beginning of the period excel's header
result_2={'GTDCDLBM':[],'LZ':[],'ZTBMJ':[],'JJJZ':[],'ZTBZS':[]}#Ending of the period excel's header
order=['GTDCDLBM','LZ','ZTBMJ','JJJZ','ZTBZS']#excle's order
#Beginning of the period 
for i in range(0,len(key1_1)):
	for n in range(0,len(key1_2)):
		ZTBMJ_1=JJJZ_1=ZTBZS_1=0
		expression_1=arcpy.AddFieldDelimiters(layer_1,'GTDCDLBM')+'=\''+key1_1[i]+'\''
		expression_2=arcpy.AddFieldDelimiters(layer_1,'LZ')+'=\''+key1_2[n]+'\''
		with arcpy.da.SearchCursor(layer_1,order,where_clause=expression_1+'AND'+expression_2) as cursor_1:
			for row_1 in cursor_1:
				ZTBMJ_1+=row_1[2]
				JJJZ_1+=row_1[3]
				ZTBZS_1+=row_1[4]
		result_1.get('GTDCDLBM').append(str(row_1[0]))
		result_1.get('LZ').append(str(row_1[1]))
		result_1.get('ZTBMJ').append(right_round(ZTBMJ_1/10000,2))
		result_1.get('ZTBZS').append(right_round(ZTBZS_1/10000,2))
		result_1.get('JJJZ').append(right_round(JJJZ_1,2))
#Ending of the period
for j in range(0,len(key2_1)):
	for m in range(0,len(key2_2)):
		ZTBMJ_2=JJJZ_2=ZTBZS_2=0
		expression_1=arcpy.AddFieldDelimiters(layer_2,'GTDCDLBM')+'=\''+key2_1[j]+'\''
		expression_2=arcpy.AddFieldDelimiters(layer_2,'LZ')+'=\''+key2_2[m]+'\''
		with arcpy.da.SearchCursor(layer_2,order,where_clause=expression_1+'AND'+expression_2) as cursor_2:
			for row_2 in cursor_2:
				ZTBMJ_2+=row_2[2]
				JJJZ_2+=row_2[3]
				ZTBZS_2+=row_2[4]
		result_2.get('GTDCDLBM').append(str(row_2[0]))
		result_2.get('LZ').append(str(row_2[1]))
		result_2.get('ZTBMJ').append(right_round(ZTBMJ_2/10000,2))
		result_2.get('ZTBZS').append(right_round(ZTBZS_2/10000,2))
		result_2.get('JJJZ').append(right_round(JJJZ_2,2))

#delete NULL list
res_check_1=res_check_2=0
while res_check_1<len(result_1.get('GTDCDLBM')):
	if (
		result_1.get('ZTBMJ')[res_check_1]==
		result_1.get('ZTBZS')[res_check_1]==
		result_1.get('JJJZ')[res_check_1]==0
		):
		del_null_list(result_1,order,res_check_1)
	else:
		res_check_1+=1
while res_check_2<len(result_2.get('GTDCDLBM')):
	if (
		result_2.get('ZTBMJ')[res_check_2]==
		result_2.get('ZTBZS')[res_check_2]==
		result_2.get('JJJZ')[res_check_2]==0
		):
		del_null_list(result_2,order,res_check_2)
	else:
		res_check_2+=1
#final resault
result_3={
	'ZBMC':[u'\u4e54\u6728\u6797',u'\u7528\u6750\u6797',u'\u7ecf\u6d4e\u6797',u'\u80fd\u6e90\u6797',u'\u9632\u62a4\u6797',u'\u7279\u79cd\u7528\u9014\u6797',u'\u7af9\u6797',u'\u7528\u6750\u6797',u'\u7ecf\u6d4e\u6797',u'\u80fd\u6e90\u6797',u'\u9632\u62a4\u6797',u'\u7279\u79cd\u7528\u9014\u6797',u'\u603b\u8ba1'],
	'SL_QC':[0,0,0,0,0,0,0,0,0,0,0,0,'--'],
	'SL_QM':[0,0,0,0,0,0,0,0,0,0,0,0,'--'],
	'JG_QC':[0,0,0,0,0,0,0,0,0,0,0,0,'--'],
	'JG_QM':[0,0,0,0,0,0,0,0,0,0,0,0,'--'],
	'JE_QC':[0,0,0,0,0,0,0,0,0,0,0,0,0],
	'JE_QM':[0,0,0,0,0,0,0,0,0,0,0,0,0]
}
order_3=['ZBMC','SL_QC','SL_QM','JG_QC','JG_QM','JE_QC','JE_QM']
ZBMC_3=['QML','23','25','24','11','12','ZL','23','25','24','11','12']

for i in range(1,6):
	for j in range(0,len(result_1.get('GTDCDLBM'))):
		if result_1.get('GTDCDLBM')[j][0:4]=='0301' and ZBMC_3[i]==result_1.get('LZ')[j][0:2]:
			result_3.get('SL_QC')[i]=result_1.get('ZTBMJ')[j]
			result_3.get('JE_QC')[i]=result_1.get('JJJZ')[j]
			result_3.get('JG_QC')[i]=right_round(result_1.get('JJJZ')[j]/result_1.get('ZTBMJ')[j],2)
	for k in range(0,len(result_2.get('GTDCDLBM'))):
		if result_2.get('GTDCDLBM')[k][0:4]=='0301' and ZBMC_3[i]==result_2.get('LZ')[k][0:2]:
			result_3.get('SL_QM')[i]=result_2.get('ZTBMJ')[k]
			result_3.get('JE_QM')[i]=result_2.get('JJJZ')[k]
			result_3.get('JG_QM')[i]=right_round(result_2.get('JJJZ')[k]/result_1.get('ZTBMJ')[k],2)
for i in range(7,12):
	for j in range(0,len(result_1.get('GTDCDLBM'))):
		if str(result_1.get('GTDCDLBM')[j])[0:4]=='0302' and ZBMC_3[i]==result_1.get('LZ')[j][0:2]:
			result_3.get('SL_QC')[i]=result_1.get('ZTBZS')[j]
			result_3.get('JE_QC')[i]=result_1.get('JJJZ')[j]
			if result_1.get('ZTBZS')[j]==0:
				result_3.get('JG_QC')[i]=0
			else:
				result_3.get('JG_QC')[i]=right_round(result_1.get('JJJZ')[j]/result_1.get('ZTBZS')[j],2)
	for k in range(0,len(result_2.get('GTDCDLBM'))):
		if result_2.get('GTDCDLBM')[k][0:4]=='0302' and ZBMC_3[i]==result_2.get('LZ')[k][0:2]:
			result_3.get('SL_QM')[i]=result_2.get('ZTBZS')[k]
			result_3.get('JE_QM')[i]=result_2.get('JJJZ')[k]
			if result_1.get('ZTBZS')[k]==0:
				result_3.get('JG_QM')[i]=0
			else:
				result_3.get('JG_QM')[i]=right_round(result_2.get('JJJZ')[k]/result_1.get('ZTBZS')[k],2)
for order_i in ['SL_QC','SL_QM','JE_QC','JE_QM']:
	calculate_sum_row(result_3,order_i,0,1,2,3,4,5)
	calculate_sum_row(result_3,order_i,6,7,8,9,10,11)
calculate_sum_row(result_3,'JE_QC',12,0,6)
calculate_sum_row(result_3,'JE_QM',12,0,6)

output=pd.DataFrame(result_3)[order_3]
#change header to chinese(test)
# if resurse_type=='CYZYZC_JJL':
# 	output.columns=[u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe5\x90\x8d\xe7\xa7\xb0',u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe4\xbb\xa3\xe7\xa0\x81',
# 					u'\xe5\x9c\xb0\xe7\xb1\xbb',u'\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\x88\x92\xe5\x85\xa5\xe7\x94\x9f\xe6\x80\x81\xe4\xbf\x9d\xe6\x8a\xa4\xe7\xba\xa2\xe7\xba\xbf\xe7\x9a\x84\xe9\x9d\xa2\xe7\xa7\xaf',u'\xe8\x87\xaa\xe7\x84\xb6\xe4\xbf\x9d\xe6\x8a\xa4\xe5\x9c\xb0\xe6\xa0\xb8\xe5\xbf\x83\xe5\x8c\xba\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\xb9\xb2\xe8\x8d\x89\xe4\xba\xa7\xe9\x87\x8f',u'\xe7\x90\x86\xe8\xae\xba\xe8\xbd\xbd\xe7\x95\x9c\xe9\x87\x8f',u'\xe8\x8d\x89\xe5\x9c\xb0\xe4\xbb\xb7\xe5\x80\xbc']
output.to_excel(path_outp,index=False)#output result










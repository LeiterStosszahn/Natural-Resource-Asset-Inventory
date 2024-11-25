import arcpy
import pandas as pd

if time.time()>time.mktime((2022,11,30,0,0,0,0,0,0)):
	arcpy.AddMessage('Term out of validity!')
	exit(0)
#term of validity

def get_keywords(layer,*key_in):
	arcpy.AddMessage('Get keyword: '+str(key_in)+' in layer '+str(layer))
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
	arcpy.AddMessage('Clear null row: '+str(k))
	for i in range(0,len(head_list)):
		del result.get(head_list[i])[k]

#Sum for row
def calculate_sum_row(form,column,row_result,*row_add):
	arcpy.AddMessage('Calculating the result of '+str(row_result)+' in the column of '+str(column))
	for i in range(0,len(row_add)):
		form.get(column)[row_result]+=form.get(column)[row_add[i]]

layer_1=arcpy.GetParameterAsText(0)#select begining layer
layer_2=arcpy.GetParameterAsText(1)#select ending layer
path_outp=arcpy.GetParameterAsText(2)#output


key1_1=get_keywords(layer_1,'GTDCDLBM')
key1_2=get_keywords(layer_2,'GTDCDLBM')
result_1={'GTDCDLBM':[],'ZTBMJ':[],'JJJZ':[]}#Beginning of the period excel's header
result_2={'GTDCDLBM':[],'ZTBMJ':[],'JJJZ':[]}#Ending of the period excel's header
order=['GTDCDLBM','ZTBMJ','JJJZ']#excle's order
#Beginning of the period 
for i in range(0,len(key1_1)):
	ZTBMJ_1=JJJZ_1=0
	expression_1=arcpy.AddFieldDelimiters(layer_1,'GTDCDLBM')+'=\''+key1_1[i]+'\''
	with arcpy.da.SearchCursor(layer_1,order,where_clause=expression_1) as cursor_1:
		for row_1 in cursor_1:
			ZTBMJ_1+=row_1[1]
			JJJZ_1+=row_1[2]
	result_1.get('GTDCDLBM').append(row_1[0])
	result_1.get('ZTBMJ').append(round(ZTBMJ_1/10000,2))
	result_1.get('JJJZ').append(JJJZ_1)
#Ending of the period
for j in range(0,len(key1_2)):
	ZTBMJ_2=JJJZ_2=0
	expression_2=arcpy.AddFieldDelimiters(layer_2,'GTDCDLBM')+'=\''+key1_2[j]+'\''
	with arcpy.da.SearchCursor(layer_2,order,where_clause=expression_2) as cursor_2:
		for row_2 in cursor_2:
			ZTBMJ_2+=row_2[1]
			JJJZ_2+=row_2[2]
	result_2.get('GTDCDLBM').append(row_2[0])
	result_2.get('ZTBMJ').append(round(ZTBMJ_2/10000,2))
	result_2.get('JJJZ').append(JJJZ_2)
#delete NULL list
res_check_1=res_check_2=0
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
#final resault
result_3={
	'GTDCDLBM':['01','0101','0102','0103','02','0201','0202','0203','0204','03','0301','0302','0305','0307','04','0401','0403','0404','05','05H1','0508','06','0601','0602','07','0701','0702','08','08H1','08H2','0809','0810','09','10','1001','1002','1003','1004','1005','1006','1007','1008','1009','11','1101','1102','1103','1104','1107','1109','1110','12','1201','1202','1203','1204','1205','1206','1207','sum'],
	'SL_QC':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	'SL_QM':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	'JG_QC':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'--'],
	'JG_QM':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'--'],
	'JE_QC':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	'JE_QM':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}
order_3=['GTDCDLBM','SL_QC','SL_QM','JG_QC','JG_QM','JE_QC','JE_QM']
for i in range(0,59):
	for j in range(0,len(result_1.get('GTDCDLBM'))):
		if result_3.get('GTDCDLBM')[i]==result_1.get('GTDCDLBM')[j][0:4]:
			result_3.get('SL_QC')[i]=result_1.get('ZTBMJ')[j]
			result_3.get('JE_QC')[i]=result_1.get('JJJZ')[j]
			result_3.get('JG_QC')[i]=round(result_1.get('JJJZ')[j]/result_1.get('ZTBMJ')[j],2)
	for k in range(0,len(result_2.get('GTDCDLBM'))):
		if result_3.get('GTDCDLBM')[i]==result_2.get('GTDCDLBM')[k][0:4]:
			result_3.get('SL_QM')[i]=result_2.get('ZTBMJ')[k]
			result_3.get('JE_QM')[i]=result_2.get('JJJZ')[k]
			result_3.get('JG_QM')[i]=round(result_2.get('JJJZ')[k]/result_1.get('ZTBMJ')[k],2)
for order_i in ['SL_QC','SL_QM','JE_QC','JE_QM']:
	calculate_sum_row(result_3,order_i,0,1,2,3)
	calculate_sum_row(result_3,order_i,4,5,6,7,8)
	calculate_sum_row(result_3,order_i,9,10,11,12,13)
	calculate_sum_row(result_3,order_i,14,15,16,17)
	calculate_sum_row(result_3,order_i,18,19,20)
	calculate_sum_row(result_3,order_i,21,22,23)
	calculate_sum_row(result_3,order_i,24,25,26)
	calculate_sum_row(result_3,order_i,27,28,29,30,31)
	calculate_sum_row(result_3,order_i,33,34,35,36,37,38,39,40,41,42)
	calculate_sum_row(result_3,order_i,43,44,45,46,47,48,49,50)
	calculate_sum_row(result_3,order_i,51,52,53,54,55,56,57,58)
	calculate_sum_row(result_3,order_i,59,0,4,9,14,18,21,24,27,32,33,43,51)
for i in [0,4,9,14,18,21,24,27,32,33,43,51]:
	if result_3.get('SL_QC')[i]==0:
		result_3.get('JG_QC')[i]=0
	else:
		result_3.get('JG_QC')[i]=round(result_3.get('JE_QC')[i]/result_3.get('SL_QC')[i],2)
	if result_3.get('SL_QM')[i]==0:
		result_3.get('JG_QM')[i]=0
	else:
		result_3.get('JG_QM')[i]=round(result_3.get('JE_QM')[i]/result_3.get('SL_QM')[i],2)

output=pd.DataFrame(result_3)[order_3]
#change header to chinese(test)
# if resurse_type=='CYZYZC_JJL':
# 	output.columns=[u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe5\x90\x8d\xe7\xa7\xb0',u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe4\xbb\xa3\xe7\xa0\x81',
# 					u'\xe5\x9c\xb0\xe7\xb1\xbb',u'\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\x88\x92\xe5\x85\xa5\xe7\x94\x9f\xe6\x80\x81\xe4\xbf\x9d\xe6\x8a\xa4\xe7\xba\xa2\xe7\xba\xbf\xe7\x9a\x84\xe9\x9d\xa2\xe7\xa7\xaf',u'\xe8\x87\xaa\xe7\x84\xb6\xe4\xbf\x9d\xe6\x8a\xa4\xe5\x9c\xb0\xe6\xa0\xb8\xe5\xbf\x83\xe5\x8c\xba\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\xb9\xb2\xe8\x8d\x89\xe4\xba\xa7\xe9\x87\x8f',u'\xe7\x90\x86\xe8\xae\xba\xe8\xbd\xbd\xe7\x95\x9c\xe9\x87\x8f',u'\xe8\x8d\x89\xe5\x9c\xb0\xe4\xbb\xb7\xe5\x80\xbc']
output.to_excel(path_outp)#output result








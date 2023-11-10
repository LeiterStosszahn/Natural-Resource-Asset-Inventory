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

layer_1=arcpy.GetParameterAsText(0)#select begining layer of land
layer_2=arcpy.GetParameterAsText(1)#select ending layer of land
layer_3=arcpy.GetParameterAsText(2)#select ending layer of CBTD
layer_4=arcpy.GetParameterAsText(3)#select ending layer of CBTD
path_outp=arcpy.GetParameterAsText(4)#output


key1_1=get_keywords(layer_1,'GTDCDLBM')
key1_2=get_keywords(layer_2,'GTDCDLBM')
result_1={'GTDCDLBM':[],'ZTBMJ':[],'JJJZ':[]}#Beginning of the period excel's header
result_2={'GTDCDLBM':[],'ZTBMJ':[],'JJJZ':[]}#Ending of the period excel's header
result_3={'DKMJ':[],'JJJZ':[]}
result_4={'DKMJ':[],'JJJZ':[]}
order_1=['GTDCDLBM','ZTBMJ','JJJZ']#excle's order
order_2=['DKMJ','JJJZ']
#land
#Beginning of the period
for i in range(0,len(key1_1)):
	ZTBMJ_1=JJJZ_1=0
	expression_1=arcpy.AddFieldDelimiters(layer_1,'GTDCDLBM')+'=\''+key1_1[i]+'\''
	with arcpy.da.SearchCursor(layer_1,order_1,where_clause=expression_1) as cursor_1:
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
	with arcpy.da.SearchCursor(layer_2,order_1,where_clause=expression_2) as cursor_2:
		for row_2 in cursor_2:
			ZTBMJ_2+=row_2[1]
			JJJZ_2+=row_2[2]
	result_2.get('GTDCDLBM').append(row_2[0])
	result_2.get('ZTBMJ').append(round(ZTBMJ_2/10000,2))
	result_2.get('JJJZ').append(JJJZ_2)

#CBTD
#Beginning of the period
DKMJ_1=JJJZ_1=DKMJ_2=JJJZ_2=0
with arcpy.da.SearchCursor(layer_3,order_2) as cursor_3:
	for row_3 in cursor_3:
		DKMJ_1+=row_3[0]
		JJJZ_1=row_3[1]
result_3.get('DKMJ').append(DKMJ_1)
result_3.get('JJJZ').append(JJJZ_1)
#Ending of the period
with arcpy.da.SearchCursor(layer_4,order_2) as cursor_4:
	for row_4 in cursor_4:
		DKMJ_2+=row_4[0]
		JJJZ_2=row_4[1]
result_4.get('DKMJ').append(DKMJ_2)
result_4.get('JJJZ').append(JJJZ_2)

#delete NULL list
res_check_1=res_check_2=0
while res_check_1<len(result_1.get('GTDCDLBM')):
	if (
		result_1.get('ZTBMJ')[res_check_1]==
		result_1.get('JJJZ')[res_check_1]==0
		):
		del_null_list(result_1,order_1,res_check_1)
	else:
		res_check_1+=1
while res_check_2<len(result_2.get('GTDCDLBM')):
	if (
		result_2.get('ZTBMJ')[res_check_2]==
		result_2.get('JJJZ')[res_check_2]==0
		):
		del_null_list(result_2,order_1,res_check_2)
	else:
		res_check_2+=1

#final resault
result_fin={
	'SL_QC':[0,0,0,0,0,0,0,0,0,0],
	'SL_QM':[0,0,0,0,0,0,0,0,0,0],
	'JE_QC':[0,0,0,0,0,0,0,0,0,0],
	'JE_QM':[0,0,0,0,0,0,0,0,0,0]
}
order_fin=['SL_QC','SL_QM','JE_QC','JE_QM']
def land_need_to_sum(DLBM):
	if DLBM[0:2]!='03' and DLBM[0:2]!='04' and DLBM!='0603' and DLBM!='1105' and DLBM!='1106' and DLBM!='1108':
		return 0
for j in range(0,len(result_1.get('GTDCDLBM'))):
	if land_need_to_sum(result_1.get('GTDCDLBM')[j])==0:
		result_fin.get('SL_QC')[0]+=result_1.get('ZTBMJ')[j]
		result_fin.get('JE_QC')[0]+=result_1.get('JJJZ')[j]
for k in range(0,len(result_2.get('GTDCDLBM'))):
	if land_need_to_sum(result_2.get('GTDCDLBM')[j])==0:
		result_fin.get('SL_QM')[0]+=result_2.get('ZTBMJ')[k]
		result_fin.get('JE_QM')[0]+=result_2.get('JJJZ')[k]
result_fin.get('SL_QC')[5]=result_3.get('DKMJ')[0]
result_fin.get('JE_QC')[5]=result_3.get('JJJZ')[0]
result_fin.get('SL_QM')[5]=result_4.get('DKMJ')[0]
result_fin.get('JE_QM')[5]=result_3.get('JJJZ')[0]

output=pd.DataFrame(result_fin)[order_fin]
#change header to chinese(test)
# if resurse_type=='CYZYZC_JJL':
# 	output.columns=[u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe5\x90\x8d\xe7\xa7\xb0',u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe4\xbb\xa3\xe7\xa0\x81',
# 					u'\xe5\x9c\xb0\xe7\xb1\xbb',u'\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\x88\x92\xe5\x85\xa5\xe7\x94\x9f\xe6\x80\x81\xe4\xbf\x9d\xe6\x8a\xa4\xe7\xba\xa2\xe7\xba\xbf\xe7\x9a\x84\xe9\x9d\xa2\xe7\xa7\xaf',u'\xe8\x87\xaa\xe7\x84\xb6\xe4\xbf\x9d\xe6\x8a\xa4\xe5\x9c\xb0\xe6\xa0\xb8\xe5\xbf\x83\xe5\x8c\xba\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\xb9\xb2\xe8\x8d\x89\xe4\xba\xa7\xe9\x87\x8f',u'\xe7\x90\x86\xe8\xae\xba\xe8\xbd\xbd\xe7\x95\x9c\xe9\x87\x8f',u'\xe8\x8d\x89\xe5\x9c\xb0\xe4\xbb\xb7\xe5\x80\xbc']
output.to_excel(path_outp)#output result





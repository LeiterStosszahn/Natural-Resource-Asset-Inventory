import arcpy
import pandas as pd

if time.time()>time.mktime((2022,12,30,0,0,0,0,0,0)):
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

def del_null_list(head_list,k):
	arcpy.AddMessage('Clear null row: '+str(k))
	for i in range(0,len(head_list)):
		del result_1.get(head_list[i])[k]

layer_1=arcpy.GetParameterAsText(0)#select layer
resurse_type=arcpy.GetParameterAsText(1)#select types
path_outp=arcpy.GetParameterAsText(2)#output

#Function for SLZY Only
if resurse_type=='SLZYZC_SWL' or resurse_type=='GYLM_SWL':
	#Age Group (according LYT2908-2017)
	tree_group={'160000':1,'120000':1,'130000':1,'360000':1,
	'350000':2,
	'150000':3,'110000':3,'170000':3,'180000':3,'190000':3,
	'200000':4,'220000':4,'230000':4,'240000':4,'210000':4,'250000':4,
	'530000':5,'535000':5,'520000':5,'540000':5,
	'580000':6,
	'570000':8,'550000':8,
	'422000':9,'420000':9,'460000':9,'470000':9,'480000':9,
	'410000':10,'440000':10,'450000':10,'510000':10,'430000':10,
	'310000':11,'320000':11,'330000':11,
	'749000':12}
	#Origin Group(1 means natural, 2 means artifical)
	origin_group={'11':1,'12':1,'13':1,
	'20':2,'21':2,'22':2,'23':2}
	#0 means NULL, 1 means YLL, 2 means ZLL, 3 means JSL, 4 means CSL, 5 means GSL
	def age_if(age,YLL,ZLL,JSL,CSL):
		if age<=YLL and age>0:
			return 1
		elif age>YLL and age <=ZLL:
			return 2
		elif age>ZLL and age<=JSL:
			return 3
		elif age>JSL and age<=CSL:
			return 4
		elif age>CSL:
			return 5
		else:
			return 0
	#South
	def age_group_s(tree,origin,age):
		if (tree_group.get(tree,0)==1 or tree_group.get(tree,0)==2) and origin_group[origin]==1:
			return age_if(age,40,60,80,120)
		elif (tree_group.get(tree,0)==1 or tree_group.get(tree,0)==2) and origin_group[origin]==2:
			return age_if(age,30,50,60,80)
		elif tree_group.get(tree,0)==3 and origin_group[origin]==1:
			return age_if(age,40,60,80,120)
		elif tree_group.get(tree,0)==3 and origin_group[origin]==2:
			return age_if(age,20,30,40,60)
		elif tree_group.get(tree,0)==4 and origin_group[origin]==1:
			return age_if(age,20,30,40,60)
		elif tree_group.get(tree,0)==4 and origin_group[origin]==2:
			return age_if(age,10,20,30,50)
		elif tree_group.get(tree,0)==5 and origin_group[origin]==1:
			return 0
		elif tree_group.get(tree,0)==5 and origin_group[origin]==2:
			return age_if(age,5,10,15,25)
		elif tree_group.get(tree,0)==6 and origin_group[origin]==1:
			return age_if(age,20,30,40,60)
		elif tree_group.get(tree,0)==6 and origin_group[origin]==2:
			return age_if(age,5,10,15,25)
		elif tree_group.get(tree,0)==7:
			return age_if(age,5,10,15,25)
		elif tree_group.get(tree,0)==8 and origin_group[origin]==1:
			return 0
		elif tree_group.get(tree,0)==8 and origin_group[origin]==2:
			return age_if(age,5,10,15,25)
		elif tree_group.get(tree,0)==9 and origin_group[origin]==1:
			return age_if(age,20,40,50,70)
		elif tree_group.get(tree,0)==9 and origin_group[origin]==2:
			return age_if(age,10,20,30,50)
		elif tree_group.get(tree,0)==10 and origin_group[origin]==1:
			return 0
		elif tree_group.get(tree,0)==10 and origin_group[origin]==2:
			return age_if(age,20,40,50,70)
		elif tree_group.get(tree,0)==11 and origin_group[origin]==1:
			return 0
		elif tree_group.get(tree,0)==11 and origin_group[origin]==2:
			return age_if(age,10,20,25,35)
		else:
			return 0
	#North not Defind
	#def age_group_n(tree,origin,age):

if resurse_type=='GYNYD':
	result_1={'ZCQCBSM':[],'YSDM':[],'XZQDM':[],'XZQMC':[],'GTDCTBBSM':[],'GTDCTBBH':[],'DLBM':[],'DLMC':[],'QSDWDM':[],'QSDWMC':[],'ZLDWDM':[],'ZLDWMC':[],'GDLYDB':[],'TBDLMJ':[],'TKMJ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'QCJG':[],'TBJJJZ':[],'XJJGGSFF':[],'FRDBS':[],'QYKZDM':[],'BZ':[]}#excel's header
	order=['ZCQCBSM','YSDM','XZQDM','XZQMC','GTDCTBBSM','GTDCTBBH','DLBM','DLMC','QSDWDM','QSDWMC','ZLDWDM','ZLDWMC','GDLYDB','TBDLMJ','TKMJ','STBHHXMJ','ZRBHDHXQMJ','QCJG','TBJJJZ','XJJGGSFF','FRDBS','QYKZDM','BZ']#excle's order
	with arcpy.da.SearchCursor(layer_1,order) as cursor_2:
		for row_2 in cursor_2:
			for i in order:
				result_1.get(i).append(row_2[order.index(i)])

elif resurse_type=='GYWLYD':
	result_1={'ZCQCBSM':[],'GTDCTBBSM':[],'GTDCTBBH':[],'YSDM':[],'XZQMC':[],'XZQDM':[],'DLBM':[],'DLMC':[],'ZLDWDM':[],'ZLDWMC':[],'QSDWDM':[],'QSDWMC':[],'TBDLMJ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'FRDBS':[],'QYKZDM':[],'BZ':[]}#excel's header
	order=['ZCQCBSM','GTDCTBBSM','GTDCTBBH','YSDM','XZQMC','XZQDM','DLBM','DLMC','ZLDWDM','ZLDWMC','QSDWDM','QSDWMC','TBDLMJ','STBHHXMJ','ZRBHDHXQMJ','FRDBS','QYKZDM','BZ']#excle's order
	with arcpy.da.SearchCursor(layer_1,order) as cursor_2:
		for row_2 in cursor_2:
			for i in order:
				result_1.get(i).append(row_2[order.index(i)])

elif resurse_type=='SL':
	result_1={'ZCQCBSM':[],'YSDM':[],'XZQDM':[],'XZQMC':[],'GTDCTBBSM':[],'GTDCTBBH':[],'GTDCDLBM':[],'GTDCDLMC':[],'QSDWDM':[],'QSDWMC':[],'ZLDWDM':[],'ZLDWMC':[],'GTDCTBMJ':[],'SLZYGLLYJ':[],'SLZYGLLC':[],'SLZYGLTBBM':[],'SLZYGLDL':[],'ZTBMJ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'GTDCTDQS':[],'LM_SUOYQ':[],'SLLB':[],'LZ':[],'YSSZ':[],'QY':[],'YBD':[],'PJNL':[],'LING_ZU':[],'PJSG':[],'PJXJ':[],'MGQZS':[],'ZTBZS':[],'GQXJ':[],'ZTBXJ':[],'DI_MAO':[],'PO_XIANG':[],'PO_WEI':[],'PO_DU':[],'TRLX':[],'TCHD':[],'TDTHLX':[],'LDZC':[],'LMZC':[],'JJJZ':[],'FRDBS':[],'QYKZDM':[],'BZ':[]}#excel's header
	order=['ZCQCBSM','YSDM','XZQDM','XZQMC','GTDCTBBSM','GTDCTBBH','GTDCDLBM','GTDCDLMC','QSDWDM','QSDWMC','ZLDWDM','ZLDWMC','GTDCTBMJ','SLZYGLLYJ','SLZYGLLC','SLZYGLTBBM','SLZYGLDL','ZTBMJ','STBHHXMJ','ZRBHDHXQMJ','GTDCTDQS','LM_SUOYQ','SLLB','LZ','YSSZ','QY','YBD','PJNL','LING_ZU','PJSG','PJXJ','MGQZS','ZTBZS','GQXJ','ZTBXJ','DI_MAO','PO_XIANG','PO_WEI','PO_DU','TRLX','TCHD','TDTHLX','LDZC','LMZC','JJJZ','FRDBS','QYKZDM','BZ']#excle's order
	with arcpy.da.SearchCursor(layer_1,order) as cursor_2:
		for row_2 in cursor_2:
			for i in order:
				result_1.get(i).append(row_2[order.index(i)])

elif resurse_type=='C_CBTD':
	result_1={'ZCQCBSM':[],'XZQDM':[],'XZQMC':[],'DKBH':[],'DYTBBH':[],'DKMC':[],'DKMJ':[],'DKCB':[],'CBGC':[],'YSJXTRCB':[],'JJJZ':[],'DKDGZT':[],'SCSJ':[],'BZ':[]}#excel's header
	order=['ZCQCBSM','XZQDM','XZQMC','DKBH','DYTBBH','DKMC','DKMJ','DKCB','CBGC','YSJXTRCB','JJJZ','DKDGZT','SCSJ','BZ']#excle's order
	with arcpy.da.SearchCursor(layer_1,order) as cursor_2:
		for row_2 in cursor_2:
			for i in order:
				result_1.get(i).append(row_2[order.index(i)])

elif resurse_type=='C_JSYDGY':
	result_1={'XZQMC':[],'ZCQCBSM':[],'ZTBMJ':[],'YJDLBM':[],'YJDLMC':[],'EJDLBM':[],'EJDLMC':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'ZDBH':[],'ZDMJ':[],'TDYT':[],'HTBH':[],'HTJK':[],'GYFS':[],'GYSJ':[],'GYNX':[],'RJL':[],'BZ':[]}#excel's header
	order=['XZQMC','ZCQCBSM','ZTBMJ','YJDLBM','YJDLMC','EJDLBM','EJDLMC','STBHHXMJ','ZRBHDHXQMJ','ZDBH','ZDMJ','TDYT','HTBH','HTJK','GYFS','GYSJ','GYNX','RJL','BZ']#excle's order
	with arcpy.da.SearchCursor(layer_1,order) as cursor_2:
		for row_2 in cursor_2:
			for i in order:
				result_1.get(i).append(row_2[order.index(i)])

elif resurse_type=='C_SDZY':
	result_1={'ZCQCBSM':[],'YSDM':[],'XZQDM':[],'XZQMC':[],'GTDCTBBSM':[],'GTDCTBBH':[],'GTDCDLBM':[],'GTDCDLMC':[],'GTDCTDQSXZ':[],'QSDWDM':[],'QSDWMC':[],'ZLDWDM':[],'ZLDWMC':[],'GTDCTBMJ':[],'ZTBMJ':[],'SDDCTBBM':[],'TRLX':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'SDL':[],'SSLY':[],'ZBLX':[],'ZBFGMJ':[],'ZYYSZWZ':[],'SWXYZ':[],'SWXZKDJ':[],'THMJ':[],'BHZK':[],'LYFS':[],'JJJZHJ':[],'FRDBS':[],'QYKZDM':[],'BZ':[]}#excel's header
	order=['ZCQCBSM','YSDM','XZQDM','XZQMC','GTDCTBBSM','GTDCTBBH','GTDCDLBM','GTDCDLMC','GTDCTDQSXZ','QSDWDM','QSDWMC','ZLDWDM','ZLDWMC','GTDCTBMJ','ZTBMJ','SDDCTBBM','TRLX','STBHHXMJ','ZRBHDHXQMJ','SDL','SSLY','ZBLX','ZBFGMJ','ZYYSZWZ','SWXYZ','SWXZKDJ','THMJ','BHZK','LYFS','JJJZHJ','FRDBS','QYKZDM','BZ']#excle's order
	with arcpy.da.SearchCursor(layer_1,order) as cursor_2:
		for row_2 in cursor_2:
			for i in order:
				result_1.get(i).append(row_2[order.index(i)])

output=pd.DataFrame(result_1)[order]
#change header to chinese(test)
# if resurse_type=='CYZYZC_JJL':
# 	output.columns=[u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe5\x90\x8d\xe7\xa7\xb0',u'\xe8\xa1\x8c\xe6\x94\xbf\xe5\x8c\xba\xe4\xbb\xa3\xe7\xa0\x81',
# 					u'\xe5\x9c\xb0\xe7\xb1\xbb',u'\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\x88\x92\xe5\x85\xa5\xe7\x94\x9f\xe6\x80\x81\xe4\xbf\x9d\xe6\x8a\xa4\xe7\xba\xa2\xe7\xba\xbf\xe7\x9a\x84\xe9\x9d\xa2\xe7\xa7\xaf',u'\xe8\x87\xaa\xe7\x84\xb6\xe4\xbf\x9d\xe6\x8a\xa4\xe5\x9c\xb0\xe6\xa0\xb8\xe5\xbf\x83\xe5\x8c\xba\xe9\x9d\xa2\xe7\xa7\xaf',
# 					u'\xe5\xb9\xb2\xe8\x8d\x89\xe4\xba\xa7\xe9\x87\x8f',u'\xe7\x90\x86\xe8\xae\xba\xe8\xbd\xbd\xe7\x95\x9c\xe9\x87\x8f',u'\xe8\x8d\x89\xe5\x9c\xb0\xe4\xbb\xb7\xe5\x80\xbc']
output.to_excel(path_outp)#output result




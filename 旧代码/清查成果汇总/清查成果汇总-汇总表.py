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

def del_null_list(head_list,k):
	arcpy.AddMessage(u'\u5220\u9664\u7a7a\u884c\uff1a'+str(k))
	for i in range(0,len(head_list)):
		del result_1.get(head_list[i])[k]

layer_1=arcpy.GetParameterAsText(0)#select layer
resurse_type=arcpy.GetParameterAsText(1)#select types
path_outp=arcpy.GetParameterAsText(2)#output
accuracy=int(arcpy.GetParameterAsText(3))

# #Function for SLZY Only
# if resurse_type=='SLZYZC_SWL' or resurse_type=='GYLM_SWL':
# 	#Age Group (according LYT2908-2017)
# 	tree_group={'160000':1,'120000':1,'130000':1,'360000':1,
# 	'350000':2,
# 	'150000':3,'110000':3,'170000':3,'180000':3,'190000':3,
# 	'200000':4,'220000':4,'230000':4,'240000':4,'210000':4,'250000':4,
# 	'530000':5,'535000':5,'520000':5,'540000':5,
# 	'580000':6,
# 	'570000':8,'550000':8,
# 	'422000':9,'420000':9,'460000':9,'470000':9,'480000':9,
# 	'410000':10,'440000':10,'450000':10,'510000':10,'430000':10,
# 	'310000':11,'320000':11,'330000':11,
# 	'749000':12}
# 	#Origin Group(1 means natural, 2 means artifical)
# 	origin_group={'11':1,'12':1,'13':1,
# 	'20':2,'21':2,'22':2,'23':2}
# 	#0 means NULL, 1 means YLL, 2 means ZLL, 3 means JSL, 4 means CSL, 5 means GSL
# 	def age_if(age,YLL,ZLL,JSL,CSL):
# 		if age<=YLL and age>0:
# 			return 1
# 		elif age>YLL and age <=ZLL:
# 			return 2
# 		elif age>ZLL and age<=JSL:
# 			return 3
# 		elif age>JSL and age<=CSL:
# 			return 4
# 		elif age>CSL:
# 			return 5
# 		else:
# 			return 0
# 	#South
# 	def age_group_s(tree,origin,age):
# 		if (tree_group.get(tree,0)==1 or tree_group.get(tree,0)==2) and origin_group[origin]==1:
# 			return age_if(age,40,60,80,120)
# 		elif (tree_group.get(tree,0)==1 or tree_group.get(tree,0)==2) and origin_group[origin]==2:
# 			return age_if(age,30,500,80)
# 		elif tree_group.get(tree,0)==3 and origin_group[origin]==1:
# 			return age_if(age,40,60,80,120)
# 		elif tree_group.get(tree,0)==3 and origin_group[origin]==2:
# 			return age_if(age,20,30,40,60)
# 		elif tree_group.get(tree,0)==4 and origin_group[origin]==1:
# 			return age_if(age,20,30,40,60)
# 		elif tree_group.get(tree,0)==4 and origin_group[origin]==2:
# 			return age_if(age,10,20,30,50)
# 		elif tree_group.get(tree,0)==5 and origin_group[origin]==1:
# 			return 0
# 		elif tree_group.get(tree,0)==5 and origin_group[origin]==2:
# 			return age_if(age,5,10,15,25)
# 		elif tree_group.get(tree,0)==6 and origin_group[origin]==1:
# 			return age_if(age,20,30,40,60)
# 		elif tree_group.get(tree,0)==6 and origin_group[origin]==2:
# 			return age_if(age,5,10,15,25)
# 		elif tree_group.get(tree,0)==7:
# 			return age_if(age,5,10,15,25)
# 		elif tree_group.get(tree,0)==8 and origin_group[origin]==1:
# 			return 0
# 		elif tree_group.get(tree,0)==8 and origin_group[origin]==2:
# 			return age_if(age,5,10,15,25)
# 		elif tree_group.get(tree,0)==9 and origin_group[origin]==1:
# 			return age_if(age,20,40,50,70)
# 		elif tree_group.get(tree,0)==9 and origin_group[origin]==2:
# 			return age_if(age,10,20,30,50)
# 		elif tree_group.get(tree,0)==10 and origin_group[origin]==1:
# 			return 0
# 		elif tree_group.get(tree,0)==10 and origin_group[origin]==2:
# 			return age_if(age,20,40,50,70)
# 		elif tree_group.get(tree,0)==11 and origin_group[origin]==1:
# 			return 0
# 		elif tree_group.get(tree,0)==11 and origin_group[origin]==2:
# 			return age_if(age,10,20,25,35)
# 		else:
# 			return 0
# 	#North not Defind
# 	#def age_group_n(tree,origin,age):

if resurse_type=='WLYDZYZC':
	key1,key2=get_keywords(layer_1,'XZQDM','DLBM')
	result_1={'XZQDM':[],'XZQMC':[],'DLBM':[],'DLMC':[],'TBDLMJ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[]}#excel's header
	order=['XZQDM','XZQMC','DLBM','DLMC','TBDLMJ','STBHHXMJ','ZRBHDHXQMJ']#excle's order
	for i in range(0,len(key1)):
		for j in range(0,len(key2)):
			TBDLMJ=STBHHXMJ=ZRBHDHXQMJ=0
			expression_1=arcpy.AddFieldDelimiters(layer_1,'XZQDM')+'=\''+key1[i]+'\''
			expression_2=arcpy.AddFieldDelimiters(layer_1,'DLBM')+'=\''+key2[j]+'\''
			with arcpy.da.SearchCursor(layer_1,['XZQDM','XZQMC','DLBM','DLMC','TBDLMJ','STBHHXMJ','ZRBHDHXQMJ'],where_clause=expression_1+'AND'+expression_2) as cursor_2:
				for row_2 in cursor_2:
					TBDLMJ=TBDLMJ+row_2[4]
					STBHHXMJ=STBHHXMJ+row_2[5]
					ZRBHDHXQMJ=ZRBHDHXQMJ+row_2[6]
			result_1.get('XZQDM').append(row_2[0])
			result_1.get('XZQMC').append(row_2[1])
			result_1.get('DLBM').append(row_2[2])
			result_1.get('DLMC').append(row_2[3])
			result_1.get('TBDLMJ').append(right_round(TBDLMJ/10000,accuracy))
			result_1.get('STBHHXMJ').append(right_round(STBHHXMJ/10000,accuracy))
			result_1.get('ZRBHDHXQMJ').append(right_round(ZRBHDHXQMJ/10000,accuracy))
	#delete NULL list
	res_check=0
	while res_check<len(result_1.get('XZQDM')):
		if (
			result_1.get('TBDLMJ')[res_check]==
			result_1.get('STBHHXMJ')[res_check]==
			result_1.get('ZRBHDHXQMJ')[res_check]==0
			):
			del_null_list(order,res_check)
		else:
			res_check+=1

elif resurse_type=='NYDZYZC':
	key1,key2=get_keywords(layer_1,'XZQDM','DLBM')
	result_1={'XZQDM':[],'XZQMC':[],'DLBM':[],'DLMC':[],'TBDLMJ':[],'GDLYDB':[],'QCJG':[],'TBJJJZ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[]}#excel's header
	order=['XZQDM','XZQMC','DLBM','DLMC','TBDLMJ','GDLYDB','QCJG','TBJJJZ','STBHHXMJ','ZRBHDHXQMJ']#excle's order
	MJ_SUM=MJ_NOTK_SUM=GDLYDB_SUM=JJJZ_SUM=STBH_SUM=ZRBHD_SUM=TKMJ_SUM=MJ_CAL=0
	for i in range(0,len(key1)):
		for j in range(0,len(key2)):
			TBDLMJ_NOTK=TBDLMJ=GDLYDB=TBJJJZ=STBHHXMJ=ZRBHDHXQMJ=0
			expression_1=arcpy.AddFieldDelimiters(layer_1,'XZQDM')+'=\''+key1[i]+'\''
			expression_2=arcpy.AddFieldDelimiters(layer_1,'DLBM')+'=\''+key2[j]+'\''
			with arcpy.da.SearchCursor(layer_1,['XZQMC','XZQDM','DLBM','DLMC','TBDLMJ','GDLYDB','QCJG','TBJJJZ','STBHHXMJ','ZRBHDHXQMJ','TKMJ'],where_clause=expression_1+'AND'+expression_2) as cursor_2:
				for row_2 in cursor_2:
					TBDLMJ+=row_2[4]#+row_2[10]
					TBDLMJ_NOTK+=row_2[4]
					TKMJ_SUM+=row_2[10]
					GDLYDB+=row_2[5]*row_2[4]
					TBJJJZ+=row_2[7]
					STBHHXMJ+=row_2[8]
					ZRBHDHXQMJ+=row_2[9]
					if TBJJJZ!=0:
						MJ_CAL+=row_2[4]
			MJ_SUM+=TBDLMJ
			if key2[j][0:2]=='01':
				MJ_NOTK_SUM+=TBDLMJ_NOTK
			GDLYDB_SUM+=GDLYDB
			JJJZ_SUM+=TBJJJZ
			STBH_SUM+=STBHHXMJ
			ZRBHD_SUM+=ZRBHDHXQMJ
			result_1.get('XZQMC').append(row_2[0])
			result_1.get('XZQDM').append(row_2[1])
			result_1.get('DLBM').append(row_2[2])
			result_1.get('DLMC').append(row_2[3])
			result_1.get('TBDLMJ').append(right_round(TBDLMJ/10000,accuracy))
			if TBDLMJ==0:
				result_1.get('GDLYDB').append(0)
				result_1.get('QCJG').append(0)
			else:
				result_1.get('GDLYDB').append(right_round(GDLYDB/TBDLMJ_NOTK,2))
				result_1.get('QCJG').append(right_round(TBJJJZ/TBDLMJ,2))
			result_1.get('TBJJJZ').append(right_round(TBJJJZ/10000,2))
			result_1.get('STBHHXMJ').append(right_round(STBHHXMJ/10000,accuracy))
			result_1.get('ZRBHDHXQMJ').append(right_round(ZRBHDHXQMJ/10000,accuracy))
	#delete NULL list
	res_check=0
	while res_check<len(result_1.get('XZQDM')):
		if (
			result_1.get('TBDLMJ')[res_check]==
			result_1.get('GDLYDB')[res_check]==
			result_1.get('QCJG')[res_check]==
			result_1.get('TBJJJZ')[res_check]==
			result_1.get('STBHHXMJ')[res_check]==
			result_1.get('ZRBHDHXQMJ')[res_check]==0
			):
			del_null_list(order,res_check)
		else:
			res_check+=1
	#TKMJ
	if TKMJ_SUM!=0:
		result_1.get('XZQMC').append(row_2[0])
		result_1.get('XZQDM').append(row_2[1])
		result_1.get('DLBM').append('1203')
		result_1.get('DLMC').append(u'\u7530\u574e')
		result_1.get('TBDLMJ').append(right_round(TKMJ_SUM/10000,accuracy))
		result_1.get('GDLYDB').append(0)
		result_1.get('QCJG').append(0)
		result_1.get('TBJJJZ').append(0)
		result_1.get('STBHHXMJ').append(0)
		result_1.get('ZRBHDHXQMJ').append(0)
	#SUM
	result_1.get('XZQDM').append(u'\u5408\u8ba1')
	result_1.get('XZQMC').append('')
	result_1.get('DLBM').append('')
	result_1.get('DLMC').append('')
	result_1.get('TBDLMJ').append(right_round((MJ_SUM+TKMJ_SUM)/10000,accuracy))
	result_1.get('GDLYDB').append(right_round(GDLYDB_SUM/MJ_NOTK_SUM,2))
	result_1.get('QCJG').append(right_round(JJJZ_SUM/MJ_CAL,2))
	result_1.get('TBJJJZ').append(right_round(JJJZ_SUM/10000,2))
	result_1.get('STBHHXMJ').append(right_round(STBH_SUM/10000,accuracy))
	result_1.get('ZRBHDHXQMJ').append(right_round(ZRBHD_SUM/10000,accuracy))

elif resurse_type=='SDZYZC':
	result_1={'XZQMC':[],'XZQDM':[],'GTDCDLMC':[],'SDL':[],'SSLY':[],'ZBLX':[],'ZBFGMJ':[],'ZTBMJ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'BHZK':[],'LYFS':[],'BZ':[]}#excel's header
	order=['XZQMC','XZQDM','GTDCDLMC','SDL','SSLY','ZBLX','ZBFGMJ','ZTBMJ','STBHHXMJ','ZRBHDHXQMJ','BHZK','LYFS','BZ']#excle's order
	key1,key2,key3,key4,key5=get_keywords(layer_1,'XZQDM','GTDCDLMC','SDL','SSLY','ZBLX')
	for i in range(0,len(key1)):
		for j in range(0,len(key2)):
			for k in range(0,len(key3)):
				for l in range(0,len(key4)):
					for m in range(0,len(key5)):
						ZBFGMJ=ZTBMJ=STBHHXMJ=ZRBHDHXQMJ=0
						BHZK=[]
						LYFS=[]
						BZ=[]
						expression_1=arcpy.AddFieldDelimiters(layer_1,'XZQDM')+'=\''+key1[i]+'\''
						expression_2=arcpy.AddFieldDelimiters(layer_1,'GTDCDLMC')+'=\''+key2[j]+'\''
						expression_3=arcpy.AddFieldDelimiters(layer_1,'SDL')+'=\''+key3[k]+'\''
						expression_4=arcpy.AddFieldDelimiters(layer_1,'SSLY')+'=\''+key4[l]+'\''
						expression_5=arcpy.AddFieldDelimiters(layer_1,'ZBLX')+'=\''+key5[m]+'\''
						with arcpy.da.SearchCursor(layer_1,['XZQMC','XZQDM','GTDCDLMC','SDL','SSLY','ZBLX','ZBFGMJ','ZTBMJ','STBHHXMJ','ZRBHDHXQMJ','BHZK','LYFS','BZ'],where_clause=expression_1+'AND'+expression_2+'AND'+expression_3+'AND'+expression_4+'AND'+expression_5) as cursor_2:
							for row_2 in cursor_2:
								ZBFGMJ=ZBFGMJ+row_2[6]
								ZTBMJ=ZTBMJ+row_2[7]
								STBHHXMJ=STBHHXMJ+row_2[8]
								ZRBHDHXQMJ=ZRBHDHXQMJ+row_2[9]
								if row_2[10] not in BHZK:
									BHZK.append(row_2[10])
								if row_2[11] not in LYFS:
									LYFS.append(row_2[11])
								if row_2[12] not in BZ:
									BZ.append(row_2[12])
						result_1.get('XZQMC').append(row_2[0])
						result_1.get('XZQDM').append(row_2[1])
						result_1.get('GTDCDLMC').append(row_2[2])
						result_1.get('SDL').append(row_2[3])
						result_1.get('SSLY').append(row_2[4])
						result_1.get('ZBLX').append(row_2[5])
						result_1.get('ZBFGMJ').append(right_round(ZBFGMJ/10000,accuracy))
						result_1.get('ZTBMJ').append(right_round(ZTBMJ/10000,accuracy))
						result_1.get('STBHHXMJ').append(right_round(STBHHXMJ/10000,accuracy))
						result_1.get('ZRBHDHXQMJ').append(right_round(ZRBHDHXQMJ/10000,accuracy))
						result_1.get('BHZK').append('\xe3\x80\x81'.join(BHZK))
						result_1.get('LYFS').append('\xe3\x80\x81'.join(LYFS))
						result_1.get('BZ').append('\xe3\x80\x81'.join(BZ))
	#delete NULL list
	res_check=0
	while res_check<len(result_1.get('XZQDM')):
		if (
			result_1.get('ZBFGMJ')[res_check]==
			result_1.get('ZTBMJ')[res_check]==
			result_1.get('STBHHXMJ')[res_check]==
			result_1.get('ZRBHDHXQMJ')[res_check]==0
			):
			del_null_list(order,res_check)
		else:
			res_check+=1

elif resurse_type=='SLZYZC_SWL' or resurse_type=='GYLM_SWL':
	key1,key2,key3,key4=get_keywords(layer_1,'XZQDM','SLLB','LZ','QY')
	if resurse_type=='SLZYZC_SWL':
		result_1={'XZQMC':[],'XZQDM':[],'SLLB':[],'LZ':[],'QY':[],'ZTBMJ':[],'ZTBXJ':[],
		'YLD_XJ_MJ':[],
		'QMLD_XJ_MJ':[],'QMLD_XJ_XJ':[],
		#'QMLD_WLZ_MJ':[],'QMLD_WLZ_XJ':[],
		'QMLD_YNL_MJ':[],'QMLD_YNL_XJ':[],'QMLD_ZNL_MJ':[],'QMLD_ZNL_XJ':[],'QMLD_JSL_MJ':[],'QMLD_JSL_XJ':[],'QMLD_CSL_MJ':[],'QMLD_CSL_XJ':[],'QMLD_GSL_MJ':[],'QMLD_GSL_XJ':[],
		'ZLD_MJ':[],'ZLD_ZS':[],
		'GMLD_MJ':[],'QTLD_MJ':[]}#excel's header
		order=['XZQMC','XZQDM','SLLB','LZ','QY','ZTBMJ','ZTBXJ',
		'YLD_XJ_MJ',
		'QMLD_XJ_MJ','QMLD_XJ_XJ',
		#'QMLD_WLZ_MJ','QMLD_WLZ_XJ',
		'QMLD_YNL_MJ','QMLD_YNL_XJ','QMLD_ZNL_MJ','QMLD_ZNL_XJ','QMLD_JSL_MJ','QMLD_JSL_XJ','QMLD_CSL_MJ','QMLD_CSL_XJ','QMLD_GSL_MJ','QMLD_GSL_XJ',
		'ZLD_MJ','ZLD_ZS',
		'GMLD_MJ','QTLD_MJ']#excle's order
	elif resurse_type=='GYLM_SWL':
		result_1={'XZQMC':[],'XZQDM':[],'SLLB':[],'LZ':[],'QY':[],'ZTBMJ':[],'ZTBXJ':[],
		'YLD_XJ_MJ':[],
		'QMLD_XJ_MJ':[],'QMLD_XJ_XJ':[],
		#'QMLD_WLZ_MJ':[],'QMLD_WLZ_XJ':[],
		'QMLD_YNL_MJ':[],'QMLD_YNL_XJ':[],'QMLD_ZNL_MJ':[],'QMLD_ZNL_XJ':[],'QMLD_JSL_MJ':[],'QMLD_JSL_XJ':[],'QMLD_CSL_MJ':[],'QMLD_CSL_XJ':[],'QMLD_GSL_MJ':[],'QMLD_GSL_XJ':[],
		'ZLD_MJ':[],'ZLD_ZS':[],
		'QTLM_MJ':[],'QTLM_XJ':[],
		'GMLD_MJ':[],
		'XJY_MJ':[],'CY_MJ':[],'GY_MJ':[],'QTYD_MJ':[]}#excel's header
		order=['XZQMC','XZQDM','SLLB','LZ','QY','ZTBMJ','ZTBXJ',
		'YLD_XJ_MJ',
		'QMLD_XJ_MJ','QMLD_XJ_XJ',
		#'QMLD_WLZ_MJ','QMLD_WLZ_XJ',
		'QMLD_YNL_MJ','QMLD_YNL_XJ','QMLD_ZNL_MJ','QMLD_ZNL_XJ','QMLD_JSL_MJ','QMLD_JSL_XJ','QMLD_CSL_MJ','QMLD_CSL_XJ','QMLD_GSL_MJ','QMLD_GSL_XJ',
		'ZLD_MJ','ZLD_ZS',
		'QTLM_MJ','QTLM_XJ',
		'GMLD_MJ',
		'XJY_MJ','CY_MJ','GY_MJ','QTYD_MJ']#excle's order
	for i in range(0,len(key1)):
		for j in range(0,len(key2)):
			for k in range(0,len(key3)):
				for l in range(0,len(key4)):
					ZTBMJ=ZTBXJ=YLD_XJ_MJ=0
					QMLD_XJ_MJ=QMLD_XJ_XJ=0
					QMLD_WLZ_MJ=QMLD_WLZ_XJ=QMLD_YNL_MJ=QMLD_YNL_XJ=QMLD_ZNL_MJ=QMLD_ZNL_XJ=QMLD_JSL_MJ=QMLD_JSL_XJ=QMLD_CSL_MJ=QMLD_CSL_XJ=QMLD_GSL_MJ=QMLD_GSL_XJ=0
					ZLD_MJ=ZLD_ZS=GMLD_MJ=GMLD_XJ=QTLM_MJ=QTLM_XJ=QTLD_MJ=0
					XJY_MJ=CY_MJ=GY_MJ=QTYD_MJ=0
					expression_1=arcpy.AddFieldDelimiters(layer_1,'XZQDM')+'=\''+key1[i]+'\''
					expression_2=arcpy.AddFieldDelimiters(layer_1,'SLLB')+'=\''+key2[j]+'\''
					expression_3=arcpy.AddFieldDelimiters(layer_1,'LZ')+'=\''+key3[k]+'\''
					expression_4=arcpy.AddFieldDelimiters(layer_1,'QY')+'=\''+key4[l]+'\''
					with arcpy.da.SearchCursor(layer_1,['XZQMC','XZQDM','SLLB','LZ','QY','ZTBMJ','ZTBXJ','YSSZ','PJNL','GTDCDLBM','ZTBZS','LING_ZU'],where_clause=expression_1+'AND'+expression_2+'AND'+expression_3+'AND'+expression_4) as cursor_2:
						for row_2 in cursor_2:
							ZTBMJ+=row_2[5]
							ZTBXJ+=row_2[6]
							if row_2[9]=='0301' or row_2[9]=='0301K':
								YLD_XJ_MJ+=row_2[5]
								QMLD_XJ_MJ+=row_2[5]
								QMLD_XJ_XJ+=row_2[6]
								#1
								if row_2[11]=='1':
									QMLD_YNL_MJ+=row_2[5]
									QMLD_YNL_XJ+=row_2[6]
								#2
								elif row_2[11]=='2':
									QMLD_ZNL_MJ+=row_2[5]
									QMLD_ZNL_XJ+=row_2[6]
								#3
								elif row_2[11]=='3':
									QMLD_JSL_MJ+=row_2[5]
									QMLD_JSL_XJ+=row_2[6]
								#4
								elif row_2[11]=='4':
									QMLD_CSL_MJ+=row_2[5]
									QMLD_CSL_XJ+=row_2[6]
								#5
								elif row_2[11]=='5':
									QMLD_GSL_MJ+=row_2[5]
									QMLD_GSL_XJ+=row_2[6]
								else:
									QMLD_WLZ_MJ+=row_2[5]
									QMLD_WLZ_XJ+=row_2[6]
								##Not have LING_ZU
								# elif age_group_s(row_2[7],row_2[4],row_2[8])==0:
								# 	QMLD_WLZ_MJ+=row_2[5]
								# 	QMLD_WLZ_XJ+=row_2[6]
								# elif age_group_s(row_2[7],row_2[4],row_2[8])==1:
								# 	QMLD_YNL_MJ+=row_2[5]
								# 	QMLD_YNL_XJ+=row_2[6]
								# elif age_group_s(row_2[7],row_2[4],row_2[8])==2:
								# 	QMLD_ZNL_MJ+=row_2[5]
								# 	QMLD_ZNL_XJ+=row_2[6]
								# elif age_group_s(row_2[7],row_2[4],row_2[8])==3:
								# 	QMLD_JSL_MJ+=row_2[5]
								# 	QMLD_JSL_XJ+=row_2[6]
								# elif age_group_s(row_2[7],row_2[4],row_2[8])==4:
								# 	QMLD_CSL_MJ+=row_2[5]
								# 	QMLD_CSL_XJ+=row_2[6]
								# elif age_group_s(row_2[7],row_2[4],row_2[8])==5:
								# 	QMLD_GSL_MJ+=row_2[5]
								# 	QMLD_GSL_XJ+=row_2[6]
							elif row_2[9]=='0302' or row_2[9]=='0302K':
								ZLD_MJ+=row_2[5]
								ZLD_ZS+=row_2[10]
								YLD_XJ_MJ+=row_2[5]
							elif row_2[9]=='0305':
								GMLD_MJ+=row_2[5]
								GMLD_XJ+=row_2[6]
							elif (row_2[9]=='0307' or row_2[9]=='0307K') and resurse_type=='SLZYZC_SWL':
								QTLD_MJ+=row_2[5]
							elif (row_2[9]=='0307' or row_2[9]=='0307K') and resurse_type=='GYLM_SWL':
								QTLM_MJ+=row_2[5]
								QTLM_XJ+=row_2[6]
							elif row_2[9]=='0203' and resurse_type=='GYLM_SWL':
								XJY_MJ+=row_2[5]
							elif row_2[9]=='0202' and resurse_type=='GYLM_SWL':
								CY_MJ+=row_2[5]
							elif row_2[9]=='0201' and resurse_type=='GYLM_SWL':
								GY_MJ+=row_2[5]
							elif row_2[9]=='0204' and resurse_type=='GYLM_SWL':
								QTYD_MJ+=row_2[5]
					result_1.get('XZQMC').append(row_2[0])
					result_1.get('XZQDM').append(row_2[1])
					result_1.get('SLLB').append(row_2[2])
					result_1.get('LZ').append(row_2[3])
					if row_2[4]!=' ':
						result_1.get('QY').append(row_2[4])
					else:
						result_1.get('QY').append('')
					result_1.get('ZTBMJ').append(right_round(ZTBMJ/10000,accuracy))
					result_1.get('ZTBXJ').append(right_round(ZTBXJ/10000,accuracy))
					result_1.get('YLD_XJ_MJ').append(right_round(YLD_XJ_MJ/10000,accuracy))
					result_1.get('QMLD_XJ_MJ').append(right_round(QMLD_XJ_MJ/10000,accuracy))
					result_1.get('QMLD_XJ_XJ').append(right_round(QMLD_XJ_XJ/10000,accuracy))
					#result_1.get('QMLD_WLZ_MJ').append(QMLD_WLZ_MJ)
					#result_1.get('QMLD_WLZ_XJ').append(QMLD_WLZ_XJ)
					result_1.get('QMLD_YNL_MJ').append(right_round(QMLD_YNL_MJ/10000,accuracy))
					result_1.get('QMLD_YNL_XJ').append(right_round(QMLD_YNL_XJ/10000,accuracy))
					result_1.get('QMLD_ZNL_MJ').append(right_round(QMLD_ZNL_MJ/10000,accuracy))
					result_1.get('QMLD_ZNL_XJ').append(right_round(QMLD_ZNL_XJ/10000,accuracy))
					result_1.get('QMLD_JSL_MJ').append(right_round(QMLD_JSL_MJ/10000,accuracy))
					result_1.get('QMLD_JSL_XJ').append(right_round(QMLD_JSL_XJ/10000,accuracy))
					result_1.get('QMLD_CSL_MJ').append(right_round(QMLD_CSL_MJ/10000,accuracy))
					result_1.get('QMLD_CSL_XJ').append(right_round(QMLD_CSL_XJ/10000,accuracy))
					result_1.get('QMLD_GSL_MJ').append(right_round(QMLD_GSL_MJ/10000,accuracy))
					result_1.get('QMLD_GSL_XJ').append(right_round(QMLD_GSL_XJ/10000,accuracy))
					result_1.get('ZLD_MJ').append(right_round(ZLD_MJ/10000,accuracy))
					result_1.get('ZLD_ZS').append(right_round(float(ZLD_ZS)/10000,accuracy))
					result_1.get('GMLD_MJ').append(right_round(GMLD_MJ/10000,accuracy))
					if resurse_type=='SLZYZC_SWL':
						result_1.get('QTLD_MJ').append(right_round(QTLD_MJ/10000,accuracy))
					elif resurse_type=='GYLM_SWL':
						result_1.get('QTLM_MJ').append(right_round(QTLM_MJ/10000,accuracy))
						result_1.get('QTLM_XJ').append(right_round(QTLM_XJ/10000,accuracy))
						result_1.get('XJY_MJ').append(right_round(XJY_MJ/10000,accuracy))
						result_1.get('CY_MJ').append(right_round(CY_MJ/10000,accuracy))
						result_1.get('GY_MJ').append(right_round(GY_MJ/10000,accuracy))
						result_1.get('QTYD_MJ').append(right_round(QTYD_MJ/10000,accuracy))
	#delete NULL list
	res_check=0
	while res_check<len(result_1.get('XZQDM')):
		if resurse_type=='SLZYZC_SWL':
			if (
				result_1.get('ZTBMJ')[res_check]==
				result_1.get('ZTBXJ')[res_check]==
				result_1.get('YLD_XJ_MJ')[res_check]==
				result_1.get('QMLD_XJ_MJ')[res_check]==
				result_1.get('QMLD_XJ_XJ')[res_check]==
				#result_1.get('QMLD_WLZ_MJ')[res_check]==
				#result_1.get('QMLD_WLZ_XJ')[res_check]==
				result_1.get('QMLD_YNL_MJ')[res_check]==
				result_1.get('QMLD_YNL_XJ')[res_check]==
				result_1.get('QMLD_ZNL_MJ')[res_check]==
				result_1.get('QMLD_ZNL_XJ')[res_check]==
				result_1.get('QMLD_JSL_MJ')[res_check]==
				result_1.get('QMLD_JSL_XJ')[res_check]==
				result_1.get('QMLD_CSL_MJ')[res_check]==
				result_1.get('QMLD_CSL_XJ')[res_check]==
				result_1.get('QMLD_GSL_MJ')[res_check]==
				result_1.get('QMLD_GSL_XJ')[res_check]==
				result_1.get('ZLD_MJ')[res_check]==
				result_1.get('ZLD_ZS')[res_check]==
				result_1.get('GMLD_MJ')[res_check]==
				result_1.get('QTLD_MJ')[res_check]==0
				):
				del_null_list(order,res_check)
			else:
				res_check+=1
		elif resurse_type=='GYLM_SWL':
			if (
				result_1.get('ZTBMJ')[res_check]==
				result_1.get('ZTBXJ')[res_check]==
				result_1.get('YLD_XJ_MJ')[res_check]==
				result_1.get('QMLD_XJ_MJ')[res_check]==
				result_1.get('QMLD_XJ_XJ')[res_check]==
				#result_1.get('QMLD_WLZ_MJ')[res_check]==
				#result_1.get('QMLD_WLZ_XJ')[res_check]==
				result_1.get('QMLD_YNL_MJ')[res_check]==
				result_1.get('QMLD_YNL_XJ')[res_check]==
				result_1.get('QMLD_ZNL_MJ')[res_check]==
				result_1.get('QMLD_ZNL_XJ')[res_check]==
				result_1.get('QMLD_JSL_MJ')[res_check]==
				result_1.get('QMLD_JSL_XJ')[res_check]==
				result_1.get('QMLD_CSL_MJ')[res_check]==
				result_1.get('QMLD_CSL_XJ')[res_check]==
				result_1.get('QMLD_GSL_MJ')[res_check]==
				result_1.get('QMLD_GSL_XJ')[res_check]==
				result_1.get('ZLD_MJ')[res_check]==
				result_1.get('ZLD_ZS')[res_check]==
				result_1.get('QTLM_MJ')[res_check]==
				result_1.get('QTLM_XJ')[res_check]==
				result_1.get('GMLD_MJ')[res_check]==
				result_1.get('XJY_MJ')[res_check]==
				result_1.get('CY_MJ')[res_check]==
				result_1.get('GY_MJ')[res_check]==
				result_1.get('QTYD_MJ')[res_check]==0
				):
				del_null_list(order,res_check)
			else:
				res_check+=1

elif resurse_type=='SLZYZC_JJL' or resurse_type=='GYLM_JJL':
	key1,key2,key3,key4=get_keywords(layer_1,'XZQDM','GTDCTDQS','SLLB','GTDCDLMC')
	if resurse_type=='SLZYZC_JJL':
		result_1={'XZQMC':[],'XZQDM':[],'GTDCTDQS':[],'SLLB':[],'GTDCDLMC':[],'ZTBMJ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'LDZC':[],'LMZC':[],'JJJZ':[]}#excel's header
		order=['XZQMC','XZQDM','GTDCTDQS','SLLB','GTDCDLMC','ZTBMJ','STBHHXMJ','ZRBHDHXQMJ','LDZC','LMZC','JJJZ']#excle's order
	elif resurse_type=='GYLM_JJL':
		result_1={'XZQMC':[],'XZQDM':[],'GTDCTDQS':[],'SLLB':[],'GTDCDLMC':[],'ZTBMJ':[],'LMZC':[]}#excel's header
		order=['XZQMC','XZQDM','GTDCTDQS','SLLB','GTDCDLMC','ZTBMJ','LMZC']#excle's order
	for i in range(0,len(key1)):
		for j in range(0,len(key2)):
			for k in range(0,len(key3)):
				for l in range(0,len(key4)):
					ZTBMJ=STBHHXMJ=ZRBHDHXQMJ=LDZC=LMZC=JJJZ=0
					expression_1=arcpy.AddFieldDelimiters(layer_1,'XZQDM')+'=\''+key1[i]+'\''
					expression_2=arcpy.AddFieldDelimiters(layer_1,'GTDCTDQS')+'=\''+key2[j]+'\''
					expression_3=arcpy.AddFieldDelimiters(layer_1,'SLLB')+'=\''+key3[k]+'\''
					expression_4=arcpy.AddFieldDelimiters(layer_1,'GTDCDLMC')+'=\''+key4[l]+'\''
					with arcpy.da.SearchCursor(layer_1,['XZQMC','XZQDM','GTDCTDQS','SLLB','GTDCDLMC','ZTBMJ','STBHHXMJ','ZRBHDHXQMJ','LDZC','LMZC','JJJZ'],where_clause=expression_1+'AND'+expression_2+'AND'+expression_3+'AND'+expression_4) as cursor_2:
						for row_2 in cursor_2:
							ZTBMJ=ZTBMJ+row_2[5]
							LMZC=LMZC+row_2[9]
							if resurse_type=='SLZYZC_JJL':
								STBHHXMJ=STBHHXMJ+row_2[6]
								ZRBHDHXQMJ=ZRBHDHXQMJ+row_2[7]
								LDZC=LDZC+row_2[8]
								JJJZ=JJJZ+row_2[10]
					result_1.get('XZQMC').append(row_2[0])
					result_1.get('XZQDM').append(row_2[1])
					result_1.get('GTDCTDQS').append(row_2[2])
					result_1.get('SLLB').append(row_2[3])
					result_1.get('GTDCDLMC').append(row_2[4])
					result_1.get('ZTBMJ').append(right_round(ZTBMJ/10000,accuracy))
					result_1.get('LMZC').append(LMZC)
					if resurse_type=='SLZYZC_JJL':
						result_1.get('STBHHXMJ').append(right_round(STBHHXMJ/10000,accuracy))
						result_1.get('ZRBHDHXQMJ').append(right_round(ZRBHDHXQMJ/10000,accuracy))
						result_1.get('LDZC').append(LDZC)
						result_1.get('JJJZ').append(JJJZ)
	#delete NULL list
	res_check=0
	while res_check<len(result_1.get('XZQDM')):
		if resurse_type=='SLZYZC_JJL':
			if (
				result_1.get('ZTBMJ')[res_check]==
				result_1.get('STBHHXMJ')[res_check]==
				result_1.get('ZRBHDHXQMJ')[res_check]==
				result_1.get('LDZC')[res_check]==
				result_1.get('LMZC')[res_check]==
				result_1.get('JJJZ')[res_check]==0
				):
				del_null_list(order,res_check)
			else:
				res_check+=1
		elif resurse_type=='GYLM_JJL':
			if (
				result_1.get('ZTBMJ')[res_check]==
				result_1.get('LMZC')[res_check]==0
				):
				del_null_list(order,res_check)
			else:
				res_check+=1

elif resurse_type=='SLZYZC_GYLM_Sum':
	key1,key2,key3=get_keywords(layer_1,'XZQDM','GTDCTDQS','LM_SUOYQ')
	result_1={'XZQMC':[],'XZQDM':[],'GTDCTDQS':[],'LM_SUOYQ':[],'ZTBMJ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'LDZC':[],'LMZC':[],'JJJZ':[]}#excel's header
	order=['XZQMC','XZQDM','GTDCTDQS','LM_SUOYQ','ZTBMJ','STBHHXMJ','ZRBHDHXQMJ','LDZC','LMZC','JJJZ']#excle's order
	for i in range(0,len(key1)):
		for j in range(0,len(key2)):
			for k in range(0,len(key3)):
				ZTBMJ=STBHHXMJ=ZRBHDHXQMJ=LDZC=LMZC=JJJZ=0
				expression_1=arcpy.AddFieldDelimiters(layer_1,'XZQDM')+'=\''+key1[i]+'\''
				expression_2=arcpy.AddFieldDelimiters(layer_1,'GTDCTDQS')+'=\''+key2[j]+'\''
				expression_3=arcpy.AddFieldDelimiters(layer_1,'LM_SUOYQ')+'=\''+key3[k]+'\''
				with arcpy.da.SearchCursor(layer_1,order,where_clause=expression_1+'AND'+expression_2+'AND'+expression_3) as cursor_2:
					for row_2 in cursor_2:
						ZTBMJ+=row_2[4]
						STBHHXMJ+=row_2[5]
						ZRBHDHXQMJ+=row_2[6]
						LDZC+=row_2[7]
						LMZC+=row_2[8]
						JJJZ+=row_2[9]
				result_1.get('XZQMC').append(row_2[0])
				result_1.get('XZQDM').append(row_2[1])
				result_1.get('GTDCTDQS').append(row_2[2])
				result_1.get('LM_SUOYQ').append(row_2[3])
				result_1.get('ZTBMJ').append(right_round(ZTBMJ/10000,accuracy))
				result_1.get('STBHHXMJ').append(right_round(STBHHXMJ/10000,accuracy))
				result_1.get('ZRBHDHXQMJ').append(right_round(ZRBHDHXQMJ/10000,accuracy))
				result_1.get('LDZC').append(LDZC)
				result_1.get('LMZC').append(LMZC)
				result_1.get('JJJZ').append(JJJZ)
	#delete NULL list
	res_check=0
	while res_check<len(result_1.get('XZQDM')):
		if (
			result_1.get('ZTBMJ')[res_check]==
			result_1.get('STBHHXMJ')[res_check]==
			result_1.get('ZRBHDHXQMJ')[res_check]==
			result_1.get('LDZC')[res_check]==
			result_1.get('LMZC')[res_check]==
			result_1.get('JJJZ')[res_check]==0
			):
			del_null_list(order,res_check)
		else:
			res_check+=1

elif resurse_type=='CYZYZC_SWL':
	key1,key2=get_keywords(layer_1,'XZQDM','GTDCDLMC')
	result_1={'XZQMC':[],'XZQDM':[],'GTDCDLMC':[],'ZTBMJ':[],'MGQGCCL':[],'ZBGD':[]}#excel's header
	order=['XZQMC','XZQDM','GTDCDLMC','ZTBMJ','MGQGCCL','ZBGD']#excle's order
	for i in range(0,len(key1)):
		for j in range(0,len(key2)):
			ZTBMJ=GCCL=ZBGD_sum=0
			expression_1=arcpy.AddFieldDelimiters(layer_1,'XZQDM')+'=\''+key1[i]+'\''
			expression_2=arcpy.AddFieldDelimiters(layer_1,'GTDCDLMC')+'=\''+key2[j]+'\''
			with arcpy.da.SearchCursor(layer_1,order,where_clause=expression_1+'AND'+expression_2) as cursor_2:
				for row_2 in cursor_2:
					ZTBMJ=ZTBMJ+row_2[3]
					GCCL=GCCL+row_2[4]*row_2[3]/10000
					ZBGD_sum=ZBGD_sum+row_2[5]*row_2[3]
			result_1.get('XZQMC').append(row_2[0])
			result_1.get('XZQDM').append(row_2[1])
			result_1.get('GTDCDLMC').append(row_2[2])
			result_1.get('ZTBMJ').append(right_round(ZTBMJ/10000,accuracy))
			result_1.get('MGQGCCL').append(right_round(GCCL,2))
			if ZTBMJ==0:
				result_1.get('ZBGD').append(0)
			else:
				result_1.get('ZBGD').append(right_round(ZBGD_sum/ZTBMJ,2))
	#delete NULL list
	res_check=0
	while res_check<len(result_1.get('XZQDM')):
		if (
			result_1.get('ZTBMJ')[res_check]==
			result_1.get('MGQGCCL')[res_check]==
			result_1.get('ZBGD')[res_check]==0
			):
			del_null_list(order,res_check)
		else:
			res_check+=1

elif resurse_type=='CYZYZC_JJL':
	key1,key2=get_keywords(layer_1,'XZQDM','GTDCDLMC')
	result_1={'XZQMC':[],'XZQDM':[],'GTDCDLMC':[],'ZTBMJ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'MGQGCCL':[],'LLZXL':[],'JJJZ':[]}#excel's header
	order=['XZQMC','XZQDM','GTDCDLMC','ZTBMJ','STBHHXMJ','ZRBHDHXQMJ','MGQGCCL','LLZXL','JJJZ']#excle's order
	for i in range(0,len(key1)):
		for j in range(0,len(key2)):
			ZTBMJ=STBHHXMJ=ZRBHDHXQMJ=GCCL=LLZXL=JJJZ=0
			expression_1=arcpy.AddFieldDelimiters(layer_1,'XZQDM')+'=\''+key1[i]+'\''
			expression_2=arcpy.AddFieldDelimiters(layer_1,'GTDCDLMC')+'=\''+key2[j]+'\''
			with arcpy.da.SearchCursor(layer_1,order,where_clause=expression_1+'AND'+expression_2) as cursor_2:
				for row_2 in cursor_2:
					ZTBMJ+=row_2[3]
					STBHHXMJ+=row_2[4]
					ZRBHDHXQMJ+=row_2[5]
					GCCL=GCCL+right_round(row_2[6]*row_2[3]/10000,accuracy)
					LLZXL+=row_2[7]
					JJJZ+=row_2[8]
			result_1.get('XZQMC').append(row_2[0])
			result_1.get('XZQDM').append(row_2[1])
			result_1.get('GTDCDLMC').append(row_2[2])
			result_1.get('ZTBMJ').append(right_round(ZTBMJ/10000,accuracy))
			result_1.get('STBHHXMJ').append(right_round(STBHHXMJ/10000,accuracy))
			result_1.get('ZRBHDHXQMJ').append(right_round(ZRBHDHXQMJ/10000,accuracy))
			result_1.get('MGQGCCL').append(GCCL)
			result_1.get('LLZXL').append(LLZXL)
			result_1.get('JJJZ').append(JJJZ)
	#delete NULL list
	res_check=0
	while res_check<len(result_1.get('XZQDM')):
		if (
			result_1.get('ZTBMJ')[res_check]==
			result_1.get('STBHHXMJ')[res_check]==
			result_1.get('ZRBHDHXQMJ')[res_check]==
			result_1.get('MGQGCCL')[res_check]==
			result_1.get('LLZXL')[res_check]==
			result_1.get('JJJZ')[res_check]==0
			):
			del_null_list(order,res_check)
		else:
			res_check+=1

elif resurse_type=='JSYDZYZC':
	key1,key2=get_keywords(layer_1,'XZQMC','EJDLBM')
	result_1={'XZQMC':[],'YJDLBM':[],'YJDLMC':[],'EJDLBM':[],'EJDLMC':[],'ZTBMJ':[],'STBHHXMJ':[],'ZRBHDHXQMJ':[],'QYQCJGSP':[],'JJJZL1':[],'JJJZL2':[],'SYZQYGSZ':[],'BZ':[]}#excel's header
	order=['XZQMC','YJDLBM','YJDLMC','EJDLBM','EJDLMC','ZTBMJ','STBHHXMJ','ZRBHDHXQMJ','QYQCJGSP','JJJZL1','JJJZL2','SYZQYGSZ','BZ']#excle's order
	MJ_SUM=STHX_SUM=ZRBHD_SUM=JJJZL1_SUM=JJJZL2_SUM=SYZQYGSZ_SUM=0
	for i in range(0,len(key1)):
		for j in range(0,len(key2)):
			ZTBMJ=STBHHXMJ=ZRBHDHXQMJ=QYQCJGSP=JJJZL1=JJJZL2=SYZQYGSZ=0
			BZ=[]
			expression_1=arcpy.AddFieldDelimiters(layer_1,'XZQMC')+'=\''+key1[i]+'\''
			expression_2=arcpy.AddFieldDelimiters(layer_1,'EJDLBM')+'=\''+key2[j]+'\''
			with arcpy.da.SearchCursor(layer_1,order,where_clause=expression_1+'AND'+expression_2) as cursor_2:
				for row_2 in cursor_2:
					ZTBMJ+=row_2[5]
					STBHHXMJ+=row_2[6]
					ZRBHDHXQMJ+=row_2[7]
					JJJZL1+=row_2[9]
					JJJZL2+=row_2[10]
					SYZQYGSZ+=row_2[11]
					if row_2[12] not in BZ and row_2[12]!=' ':
						BZ.append(row_2[12])
			MJ_SUM+=ZTBMJ
			STHX_SUM+=STBHHXMJ
			ZRBHD_SUM+=ZRBHDHXQMJ
			JJJZL1_SUM+=JJJZL1
			JJJZL2_SUM+=JJJZL2
			SYZQYGSZ_SUM+=SYZQYGSZ
			result_1.get('XZQMC').append(row_2[0])
			result_1.get('YJDLBM').append(row_2[1])
			result_1.get('YJDLMC').append(row_2[2])
			result_1.get('EJDLBM').append(row_2[3])
			result_1.get('EJDLMC').append(row_2[4])
			result_1.get('ZTBMJ').append(right_round(ZTBMJ/10000,accuracy))
			result_1.get('STBHHXMJ').append(right_round(STBHHXMJ/10000,accuracy))
			result_1.get('ZRBHDHXQMJ').append(right_round(ZRBHDHXQMJ/10000,accuracy))
			if ZTBMJ==0:
				result_1.get('QYQCJGSP').append(0)
			else:
				result_1.get('QYQCJGSP').append(right_round((JJJZL1*10000)/ZTBMJ,2))
			result_1.get('JJJZL1').append(right_round(JJJZL1,2))
			result_1.get('JJJZL2').append(right_round(JJJZL2,2))
			result_1.get('SYZQYGSZ').append(right_round(SYZQYGSZ,2))
			result_1.get('BZ').append(u'\u3001'.join(BZ))
	#delete NULL list
	res_check=0
	while res_check<len(result_1.get('XZQMC')):
		if (
			result_1.get('ZTBMJ')[res_check]==
			result_1.get('STBHHXMJ')[res_check]==
			result_1.get('ZRBHDHXQMJ')[res_check]==
			result_1.get('QYQCJGSP')[res_check]==
			result_1.get('JJJZL1')[res_check]==
			result_1.get('JJJZL2')[res_check]==
			result_1.get('SYZQYGSZ')[res_check]==0
			):
			del_null_list(order,res_check)
		else:
			res_check+=1
	#SUM
	result_1.get('XZQMC').append(row_2[0]+u'\uff08\u5408\u8ba1\uff09')
	result_1.get('YJDLBM').append('')
	result_1.get('YJDLMC').append('')
	result_1.get('EJDLBM').append('')
	result_1.get('EJDLMC').append('')
	result_1.get('ZTBMJ').append(right_round(MJ_SUM/10000,2))
	result_1.get('STBHHXMJ').append(right_round(STHX_SUM/10000,2))
	result_1.get('ZRBHDHXQMJ').append(right_round(ZRBHD_SUM/10000,2))
	result_1.get('QYQCJGSP').append(right_round(JJJZL1_SUM*10000/MJ_SUM,2))
	result_1.get('JJJZL1').append(right_round(JJJZL1_SUM,2))
	result_1.get('JJJZL2').append(right_round(JJJZL2_SUM,2))
	result_1.get('SYZQYGSZ').append(right_round(SYZQYGSZ_SUM,2))
	result_1.get('BZ').append('')

output=pd.DataFrame(result_1)[order]
#change header to chinese(test)
if resurse_type=='WLYDZYZC':
	output.columns=[u'\u884c\u653f\u533a\u4ee3\u7801',
					u'\u884c\u653f\u533a\u540d\u79f0',
					u'\u5730\u7c7b\u7f16\u7801',
					u'\u5730\u7c7b\u540d\u79f0',
					u'\u9762\u79ef',
					u'\u5212\u5165\u751f\u6001\u4fdd\u62a4\u7ea2\u7ebf\u9762\u79ef',
					u'\u5212\u5165\u81ea\u7136\u4fdd\u62a4\u5730\u6838\u5fc3\u533a\u9762\u79ef']
output.to_excel(path_outp,index=False)#output result














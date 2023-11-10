import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import string,random
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

def random_name(name):
    return name+"_"+"".join(random.sample('zyxwvutsrqponmlkjihgfedcba1234567890',10))

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

layer_in=arcpy.GetParameter(0)
layer_in_CB=arcpy.GetParameterAsText(1)

#Merge all layers and save the economic value
arcpy.AddMessage(u'\u5408\u5e76\u6240\u6709\u56fe\u5c42\u4e2d')

layer_merge=random_name("merge")

##Get all fileds and target what resource is involved
fms=arcpy.FieldMappings()
field_involoved=["ZCQCBSM"]
for i in layer_in:
    fms.addTable(i)
    resource_type=str(i)[8:]
    if resource_type in ["C_CYZY","C_SL_GYTD"] and "JJJZ" not in field_involoved:
        field_involoved.append("JJJZ")
    elif resource_type=="C_JSYDGY" and "JJJZL1" not in field_involoved:
        field_involoved.append("JJJZL1")
    elif resource_type=="C_XJFDDY" and "TBJJJZ" not in field_involoved:
        field_involoved.append("TBJJJZ")

for field in fms.fields:
    if field.name not in field_involoved:
        fms.removeFieldMap(fms.findFieldMapIndex(field.name))

arcpy.Merge_management(layer_in,layer_merge,fms) 

#Add a field for sum and calculate it
arcpy.AddField_management(layer_merge,"SUM","DOUBLE")
codeblock = """
def cal(*a):
    for i in a:
        if i is not None:
            return i"""
formula="cal(!"
for i in field_involoved:
    if i!="ZCQCBSM":
        formula=formula+i+"!,!"
    if i=="TBJJJZ":
        arcpy.management.CalculateField(layer_merge,"TBJJJZ","!TBJJJZ!/10000","PYTHON_9.3")
arcpy.management.CalculateField(layer_merge,"SUM",formula[:-2]+")","PYTHON_9.3",codeblock)

#Identity
layer_identity=random_name("identity")
arcpy.AddMessage(u'\u5f00\u59cb\u5e73\u5dee\uff1a')
arcpy.Identity_analysis(layer_merge,layer_in_CB,layer_identity) 
arcpy.Delete_management(layer_merge)
arcpy.AddMessage(u'\u8ba1\u7b97\u692d\u7403\u9762\u79ef\u4e2d...')
arcpy.AddField_management(layer_identity,"GeoAreaCalculate","DOUBLE")
arcpy.management.CalculateField(layer_identity,"GeoAreaCalculate","!shape.geodesicArea!","PYTHON_9.3")

#Area adjustment
keywords=[]
tar_table="FID_"+arcpy.Describe(layer_in_CB).baseName
tar_table=tar_table.replace('(','_')
tar_table=tar_table.replace(')','_')

##Extract unique value of keywords
with arcpy.da.SearchCursor(layer_identity,[tar_table,"ZCQCBSM"]) as cursor:
    for row in cursor:
        if row[0]!=-1 and row[1] not in keywords:
            keywords.append(row[1])
            arcpy.AddMessage(u'\u5176\u4ed6\u8d44\u6e90'+str(row[1])+u'\u4e0e\u50a8\u5907\u571f\u5730\u6709\u91cd\u53e0')

arcpy.AddMessage(u'\u5e73\u5dee\u4e2d...')
for i in keywords:
    expression=arcpy.AddFieldDelimiters(layer_identity,"ZCQCBSM")+'=\''+i+'\''#SQL query statement by patch number
    with arcpy.da.SearchCursor(layer_identity,["SUM","GeoAreaCalculate"],where_clause=expression) as cursor:#In order, SQL queries the unique patch number
        mj_sum=0#Initial area 0
        k=0#Count the number of subgraphs
        mj_cal=[]#calculation area
        mj_TBMJ=[]
        #Count the details of sub patches of this group of patches
        for row in cursor:
            mj_sum+=row[1]#sum calculation area
            mj_cal.append(row[1])#calculation area array
            mj_TBMJ.append(row[0])#TBMJ array
            k+=1
        #Only one keyworsds,no need to adjust
        if k==1:
            with arcpy.da.UpdateCursor(layer_identity,["QT_JJJZ"],where_clause=expression) as cursor_2:#SQL query unique patch number assignment
                for row_2 in cursor_2:
                    row_2[0]=mj_TBMJ[0]
                    cursor_2.updateRow(row_2)
            continue
        #adjustment
        else:
            j=0
            with arcpy.da.UpdateCursor(layer_identity,["QT_JJJZ"],where_clause=expression) as cursor_3:
                for row_3 in cursor_3:
                    row_3[0]=right_round(mj_TBMJ[j]*mj_cal[j]/mj_sum,2)
                    cursor_3.updateRow(row_3)
                    j+=1
##second adjust
arcpy.AddMessage(u'\u4e8c\u6b21\u5e73\u5dee\u4e2d...')
for i in keywords:
    expression=arcpy.AddFieldDelimiters(layer_identity,"ZCQCBSM")+'=\''+i+'\''
    with arcpy.da.SearchCursor(layer_identity,["SUM","QT_JJJZ"],where_clause=expression) as cursor_5:
        mj_sum=key_num=0#Initial area 0
        wrong_result=[]#Record error BSM
        #Count the details of this group of polygon
        for row_5 in cursor_5:
            mj_sum+=row_5[1]#Calculated area summation
            wrong_result.append(row_5[1])#Statistical error area
            key_num+=1
        #Inaccurate adjustment
        differ_all=row_5[0]-mj_sum
        differ_long=len(wrong_result)
        differ_accuracy=0.01
        #Only different less than 3 times accuracy will be readjust
        # if differ_all!=0 and key_num!=1 and differ_all<differ_long*differ_accuracy*3:
        if differ_all>0:
            accuracy_adjust=0.01
        else:
            accuracy_adjust=-0.01
        differ=int(round(abs(differ_all/accuracy_adjust),0))
        cycle=int(round(abs(math.floor(differ/differ_long)),0))
        order_wrong_result=wrong_result[:]
        order_wrong_result.sort()
        order_wrong_result.reverse()
        values_index_list=[]
        for rows in range(0,len(order_wrong_result)):
            values_index_list.append(wrong_result.index(order_wrong_result[rows]))
        if cycle>1:
            for n in range(0,cycle):
                for j in range(0,differ_long):
                    wrong_result[j]+=accuracy_adjust#adjust in one cycle
        for m in range(0,differ-cycle*differ_long):
            wrong_result[values_index_list[m]]+=accuracy_adjust#adjust the left
        k=0
        with arcpy.da.UpdateCursor(layer_identity,["QT_JJJZ"],where_clause=expression) as cursor_7:
            for row_7 in cursor_7:
                row_7[0]=wrong_result[k]
                cursor_7.updateRow(row_7)
                k+=1

#Delete redundant data
arcpy.AddMessage(u'\u5220\u9664\u591a\u4f59\u56fe\u6591\u4e2d...')
expression=arcpy.AddFieldDelimiters(layer_identity,tar_table)+'=-1'
arcpy.MakeTableView_management(layer_identity,"accidentTableView")
arcpy.SelectLayerByAttribute_management("accidentTableView","NEW_SELECTION",expression)
arcpy.DeleteRows_management("accidentTableView")

#value back
arcpy.AddMessage(u'\u4ef7\u683c\u8ba1\u7b97\u5b8c\u6210\uff0c\u66f4\u65b0\u6570\u636e\u4e2d...')
keywords_ZB=get_keywords(layer_identity,"ZCQCBSM_ZB")
for i in keywords_ZB:
    expression=arcpy.AddFieldDelimiters(layer_identity,"ZCQCBSM_ZB")+'=\''+i+'\''
    temp=0
    with arcpy.da.SearchCursor(layer_identity,["QT_JJJZ"],where_clause=expression) as cursor_8:
        for row_8 in cursor_8:
            temp+=row_8[0]
    with arcpy.da.UpdateCursor(layer_in_CB,["QT_JJJZ"],where_clause=expression) as cursor_9:
        for row_9 in cursor_9:
            row_9[0]=temp
            cursor_9.updateRow(row_9)

arcpy.Delete_management(layer_identity)

#Calculate the unit-price
arcpy.AddMessage(u'\u8ba1\u7b97\u5355\u4ef7\u4e2d...')
keywords_unit=get_keywords(layer_in_CB,"ZCQCBSM")
# for i in keywords_unit:
#     expression=arcpy.AddFieldDelimiters(layer_in_CB,"ZCQCBSM")+'=\''+i+'\''
#     price_sum=area_sum=0
#     with arcpy.da.SearchCursor(layer_in_CB,["QT_JJJZ","ZTBTDMJ"],where_clause=expression) as cursor_10:
#         for row_10 in cursor_10:
#             price_sum+=row_10[0]
#             area_sum+=row_10[1]
#     price=right_round(price_sum/area_sum,2)
#     with arcpy.da.UpdateCursor(layer_in_CB,["QT_QCJG","QT_QS"],where_clause=expression) as cursor_11:
#         for row_11 in cursor_11:
#             if row_11[1]!=u'\u96c6\u4f53':
#                 row_11[0]=price
#                 cursor_11.updateRow(row_11)
with arcpy.da.UpdateCursor(layer_in_CB,["ZTBTDMJ","QT_QCJG","QT_JJJZ"]) as cursor_10:
    for row_10 in cursor_10:
        row_10[1]=right_round(row_10[2]/row_10[0],2)
        cursor_10.updateRow(row_10)


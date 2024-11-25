
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
    if resource_type=="C_SL_GYTD":
        MXD=arcpy.mapping.MapDocument ('current')
        layers=arcpy.mapping.ListLayers(MXD,i)
        arcpy.management.CalculateField(i,"JJJZ","!JJJZ!-!LMZC!","PYTHON_9.3")
    if resource_type in ["C_CYZY","C_SL_GYTD"] and "JJJZ" not in field_involoved:
        field_involoved.append("JJJZ")
    elif resource_type=="C_JSYDGY" and "JJJZL1" not in field_involoved:
        field_involoved.append("JJJZL1")
    elif resource_type=="C_XJFDDY" and "TBJJJZ" not in field_involoved:
        field_involoved.append("TBJJJZ")
        field_involoved.append("TBDLMJ")
        field_involoved.append("TKMJ")
    if resource_type!="C_XJFDDY" and "ZTBMJ" not in field_involoved:
        field_involoved.append("ZTBMJ")

for field in fms.fields:
    if field.name not in field_involoved:
        fms.removeFieldMap(fms.findFieldMapIndex(field.name))

arcpy.Merge_management(layer_in,layer_merge,fms) 

for i in layer_in:
    resource_type=str(i)[8:]
    if resource_type=="C_SL_GYTD":
        MXD=arcpy.mapping.MapDocument ('current')
        layers=arcpy.mapping.ListLayers(MXD,i)
        arcpy.management.CalculateField(i,"JJJZ","!JJJZ!+!LMZC!","PYTHON_9.3")

#Add a field for sum and calculate it
arcpy.AddField_management(layer_merge,"SUM","DOUBLE")
arcpy.AddField_management(layer_merge,"MJ","DOUBLE")
arcpy.AddField_management(layer_merge,"unit_price","DOUBLE")
codeblock = """
def cal(*a):
    b=0
    for i in a:
        if i is not None:
            b+=i
    return b"""
formula="cal(!"
for i in field_involoved:
    if i!="ZCQCBSM" and i!="ZTBMJ" and i!="TBDLMJ" and i!="TKMJ":
        formula=formula+i+"!,!"
    if i=="TBJJJZ":
        arcpy.management.CalculateField(layer_merge,"TBJJJZ","!TBJJJZ!/10000","PYTHON_9.3")
arcpy.management.CalculateField(layer_merge,"SUM",formula[:-2]+")","PYTHON_9.3",codeblock)

if "ZTBMJ" in field_involoved:
    if "TBDLMJ" in field_involoved:
        arcpy.management.CalculateField(layer_merge,"MJ","cal(!ZTBMJ!,!TBDLMJ!,!TKMJ!)","PYTHON_9.3",codeblock)
    else:
        arcpy.management.CalculateField(layer_merge,"MJ","cal(!TBDLMJ!,!TKMJ!)","PYTHON_9.3",codeblock)
else:
    arcpy.management.CalculateField(layer_merge,"MJ","!ZTBMJ!","PYTHON_9.3")

codeblock_2 = """
from decimal import Decimal,ROUND_HALF_UP
def right_round(num,keep_n):
    if isinstance(num,float):
        num = str(num)
    return Decimal(num).quantize((Decimal('0.' + '0'*keep_n)),rounding=ROUND_HALF_UP)"""
arcpy.management.CalculateField(layer_merge,"unit_price","float(right_round(!SUM!*10000/!MJ!,2))","PYTHON_9.3",codeblock_2)

#Identity
layer_identity=random_name("identity")
arcpy.AddMessage(u'\u5f00\u59cb\u5e73\u5dee')
arcpy.Identity_analysis(layer_merge,layer_in_CB,layer_identity)
arcpy.Delete_management(layer_merge)

#Delete duplicate data
arcpy.AddMessage(u'\u5220\u9664\u591a\u4f59\u56fe\u6591\u4e2d...')
layer_sort=random_name("sort")
arcpy.Sort_management(layer_identity,layer_sort,[["Shape_Area","DESCENDING"]]) 
arcpy.Delete_management(layer_identity)
arcpy.DeleteIdentical_management(layer_sort,["ZCQCBSM_ZB"]) 

#value back
arcpy.AddMessage(u'\u4ef7\u683c\u8ba1\u7b97\u5b8c\u6210\uff0c\u66f4\u65b0\u6570\u636e\u4e2d...')
in_layer=arcpy.GetParameter(1)
arcpy.AddJoin_management(in_layer,"ZCQCBSM_ZB",layer_sort,"ZCQCBSM_ZB")
arcpy.management.CalculateField(layer_in_CB,layer_in_CB+".QT_QCJG","cal(!"+layer_sort+".unit_price!)","PYTHON_9.3",codeblock)
arcpy.RemoveJoin_management(in_layer,layer_sort)
arcpy.Delete_management(layer_sort)
arcpy.management.CalculateField(layer_in_CB,"QT_JJJZ","float(right_round(!QT_QCJG!*!ZTBTDMJ!,2))","PYTHON_9.3",codeblock_2)

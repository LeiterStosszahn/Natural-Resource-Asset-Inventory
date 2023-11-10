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
price=arcpy.GetParameterAsText(1)
fishnet=arcpy.GetParameter(2)
save_in=arcpy.GetParameterAsText(3)

#Identity
arcpy.AddMessage(u'\u6807\u8bc6\u4e2d...')
arcpy.management.CalculateField(fishnet,"ID","str(!FID!)","PYTHON_9.3")
layer_identity=random_name("identity")
arcpy.Identity_analysis(fishnet,layer_in,layer_identity)

#calculate price, unaccurate
# arcpy.AddMessage(u'\u8ba1\u7b97\u692d\u7403\u9762\u79ef\u4e2d...')
# arcpy.AddField_management(layer_identity,"GeoAreaCalculate","DOUBLE")
# tar_table="FID_"+arcpy.Describe(layer_in).baseName
# tar_table=tar_table.replace('(','_')
# tar_table=tar_table.replace(')','_')
# codeblock = """
# def cal(a,b):
#     if a!=-1:
#         return b"""
# arcpy.management.CalculateField(layer_identity,"GeoAreaCalculate","cal(!"+tar_table+"!,!shape.geodesicArea!)","PYTHON_9.3",codeblock)

arcpy.AddField_management(layer_identity,"price_","DOUBLE")
arcpy.AddMessage(u'\u5e73\u5dee\u4e2d...')

keywords_ZB=get_keywords(layer_identity,"ZCQCBSM")
for i in keywords_ZB:
    if i==None or i=="" or i==" ":
        continue
    expression=arcpy.AddFieldDelimiters(layer_identity,"ZCQCBSM")+'=\''+i+'\''#SQL query statement by patch number
    with arcpy.da.SearchCursor(layer_identity,[price,"Shape_Area"],where_clause=expression) as cursor:#In order, SQL queries the unique patch number
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
            with arcpy.da.UpdateCursor(layer_identity,["price_"],where_clause=expression) as cursor_2:#SQL query unique patch number assignment
                for row_2 in cursor_2:
                    row_2[0]=mj_TBMJ[0]
                    cursor_2.updateRow(row_2)
            continue
        #adjustment
        else:
            j=0
            with arcpy.da.UpdateCursor(layer_identity,["price_"],where_clause=expression) as cursor_3:
                for row_3 in cursor_3:
                    row_3[0]=right_round(mj_TBMJ[j]*mj_cal[j]/mj_sum,2)
                    cursor_3.updateRow(row_3)
                    j+=1

#Disslove
layer_disslove=random_name("disslove")
arcpy.Dissolve_management(layer_identity,layer_disslove,["ID"],[["price_","SUM"]])
arcpy.Delete_management(layer_identity)

#to raster
arcpy.PolygonToRaster_conversion (layer_disslove,"SUM_price_",save_in)
arcpy.Delete_management(layer_disslove)

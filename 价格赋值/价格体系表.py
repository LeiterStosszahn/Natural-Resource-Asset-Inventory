import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import arcpy
import pandas as pd
from arcpy.sa import *

#Term of validity
if time.time()>time.mktime((2023,11,30,0,0,0,0,0,0)):
	arcpy.AddMessage(u'\u6388\u6743\u8d85\u671f\uff01')
	exit(0)

save_route=arcpy.GetParameterAsText(0)

system_name=[u'\u4ea4\u6613\u671f\u65e5\u4fee\u6b63\u7cfb\u6570',
			u'\u68ee\u6797\u8d44\u6e90\u4ef7\u683c\u4f53\u7cfb\u8868',
			u'\u519c\u7528\u5730\u4ef7\u683c\u4f53\u7cfb\u8868',
			]
#Construction date amend, Forest, Famerland, no grasslands

#Construction
#Date amend
date_order=[u'\u7f16\u53f7',
		u'\u884c\u653f\u533a\u540d\u79f0',
		u'\u5730\u7c7b\u540d\u79f0',
		u'\u5730\u7c7b\u540d\u79f0\u4ee3\u7801',
		u'\u5e74\u671f\u4fee\u6b63\u7cfb\u6570']
date=pd.DataFrame(
	{u'\u7f16\u53f7':range(1,14),
	u'\u884c\u653f\u533a\u540d\u79f0':13*["xxx"],
	u'\u5730\u7c7b\u540d\u79f0':[u'\u5546\u4e1a\u670d\u52a1\u4e1a\u8bbe\u65bd\u7528\u5730',u'\u7269\u6d41\u4ed3\u50a8\u7528\u5730',u'\u91c7\u77ff\u7528\u5730',
								u'\u5de5\u4e1a\u7528\u5730',u'\u57ce\u9547\u4f4f\u5b85\u7528\u5730',u'\u519c\u6751\u5b85\u57fa\u5730',
								u'\u516c\u7528\u8bbe\u65bd\u7528\u5730',u'\u516c\u56ed\u4e0e\u7eff\u5730',u'\u673a\u5173\u56e2\u4f53\u65b0\u95fb\u51fa\u7248\u7528\u5730',
								u'\u79d1\u6559\u6587\u536b\u7528\u5730',u'\u7279\u6b8a\u7528\u5730',u'\u4ea4\u901a\u8fd0\u8f93\u7528\u5730',
								u'\u6c34\u5de5\u5efa\u7b51\u7528\u5730'],
	u'\u5730\u7c7b\u540d\u79f0\u4ee3\u7801':["SYFWYSSYD","WLCCYD","CKYD",
											"GYYD","CZZZYD","NCZJD",
											"GYSSYD","GYYLD","JGTTXWCBYD",
											"KJWWYD","TSYD","JTYSYD",
											"SGJZYD"],
	u'\u5e74\u671f\u4fee\u6b63\u7cfb\u6570':13*[1]}
	)[date_order]

farmland_writer=pd.ExcelWriter(save_route+'\\'+system_name[0]+'.xls')
date.to_excel(farmland_writer,index=False)
farmland_writer.save()
farmland_writer.close()


#forest
LD_order=[u'\u7f16\u53f7',
		u'\u53bf\u4ee3\u7801',
		u'\u53bf\u540d',
		u'\u6240\u5728\u5747\u8d28\u533a',
		u'\u4e54\u6728\u6797',
		u'\u704c\u6728\u7ecf\u6d4e\u6797',
		u'\u4e00\u822c\u704c\u6728\u6797',
		u'\u7af9\u6797',
		u'\u5176\u4ed6\u6797\u5730']
LD=pd.DataFrame(
	{u'\u7f16\u53f7':["1"],
	u'\u53bf\u4ee3\u7801':["xxxxxx"],
	u'\u53bf\u540d':[u'xx\u53bf'],
	u'\u6240\u5728\u5747\u8d28\u533a':[u'xx\u533a'],
	u'\u4e54\u6728\u6797':[0],
	u'\u704c\u6728\u7ecf\u6d4e\u6797':[0],
	u'\u4e00\u822c\u704c\u6728\u6797':[0],
	u'\u7af9\u6797':[0],
	u'\u5176\u4ed6\u6797\u5730':[0]}
	)[LD_order]
YCL_order=[u'\u7f16\u53f7',
		u'\u53bf\u4ee3\u7801',
		u'\u53bf\u540d',
		u'\u6240\u5728\u5747\u8d28\u533a',
		u'\u6811\u79cd',
		u'\u8d77\u6e90',
		u'\u9f84\u7ec4',
		u'\u7701\u7ea7\u4ef7\u683c\u4f53\u7cfb\u6797\u6728\u4ef7\u683c']
YCL=pd.DataFrame(
	{u'\u7f16\u53f7':["1"],
	u'\u53bf\u4ee3\u7801':["xxxxxx"],
	u'\u53bf\u540d':[u'xx\u53bf'],
	u'\u6240\u5728\u5747\u8d28\u533a':[u'xx\u533a'],
	u'\u6811\u79cd':["xxxxxx"],
	u'\u8d77\u6e90':[u'\u4eba\u5de5'],
	u'\u9f84\u7ec4':[u'xx\u6797'],
	u'\u7701\u7ea7\u4ef7\u683c\u4f53\u7cfb\u6797\u6728\u4ef7\u683c':[0]}
	)[YCL_order]
#Also NYL
ZL_order=[u'\u7f16\u53f7',
		u'\u53bf\u4ee3\u7801',
		u'\u53bf\u540d',
		u'\u6240\u5728\u5747\u8d28\u533a',
		u'\u6811\u79cd',
		u'\u7701\u7ea7\u4ef7\u683c\u4f53\u7cfb\u6797\u6728\u4ef7\u683c']
ZL=pd.DataFrame(
	{u'\u7f16\u53f7':["1"],
	u'\u53bf\u4ee3\u7801':["xxxxxx"],
	u'\u53bf\u540d':[u'xx\u53bf'],
	u'\u6240\u5728\u5747\u8d28\u533a':[u'xx\u533a'],
	u'\u6811\u79cd':["xxxxxx"],
	u'\u7701\u7ea7\u4ef7\u683c\u4f53\u7cfb\u6797\u6728\u4ef7\u683c':[0]}
	)[ZL_order]
JJL_order=[u'\u7f16\u53f7',
		u'\u53bf\u4ee3\u7801',
		u'\u53bf\u540d',
		u'\u6240\u5728\u5747\u8d28\u533a',
		u'\u6811\u79cd',
		u'\u4ea7\u671f',
		u'\u7701\u7ea7\u4ef7\u683c\u4f53\u7cfb\u6797\u6728\u4ef7\u683c']
JJL=pd.DataFrame(
	{u'\u7f16\u53f7':["1"],
	u'\u53bf\u4ee3\u7801':["xxxxxx"],
	u'\u53bf\u540d':[u'xx\u53bf'],
	u'\u6240\u5728\u5747\u8d28\u533a':[u'xx\u533a'],
	u'\u6811\u79cd':["xxxxxx"],
	u'\u4ea7\u671f':[u'xx\u671f'],
	u'\u7701\u7ea7\u4ef7\u683c\u4f53\u7cfb\u6797\u6728\u4ef7\u683c':[0]}
	)[JJL_order]

forest_writer=pd.ExcelWriter(save_route+'\\'+system_name[1]+'.xls')
LD.to_excel(forest_writer,startrow=4,sheet_name=u'\u88681 \u6797\u5730\u4ef7\u683c\uff0870\u5e74\u671f\uff09',index=False)
YCL.to_excel(forest_writer,startrow=2,sheet_name=u'\u88683 \u7528\u6750\u6797\u6797\u6728\u4ef7\u683c',index=False)
ZL.to_excel(forest_writer,startrow=2,sheet_name=u'\u88684 \u7af9\u6797\u6797\u6728\u4ef7\u683c',index=False)
JJL.to_excel(forest_writer,startrow=2,sheet_name=u'\u88685 \u7ecf\u6d4e\u6797\u6797\u6728\u4ef7\u683c',index=False)
ZL.to_excel(forest_writer,startrow=2,sheet_name=u'\u88686 \u80fd\u6e90\u6797\u6797\u6728\u4ef7\u683c',index=False)
forest_writer.save()
forest_writer.close()

#farmland
JZQ_order=[u'\u7f16\u53f7',
		u'\u884c\u653f\u533a\u540d\u79f0',
		u'\u884c\u653f\u533a\u4ee3\u7801',
		u'\u5747\u8d28\u533a\u7f16\u53f7']
JZQ=pd.DataFrame(
	{u'\u7f16\u53f7':["1"],
	u'\u884c\u653f\u533a\u540d\u79f0':[u'xx\u53bf'],
	u'\u884c\u653f\u533a\u4ee3\u7801':["xxxxxx"],
	u'\u5747\u8d28\u533a\u7f16\u53f7':["Gxxxx"]}
	)[JZQ_order]
GD_order=[u'\u7f16\u53f7',
		u'\u5747\u8d28\u533a\u7f16\u53f7',
		u'\u8015\u5730\u5229\u7528\u7b49\u522b',
		u'\u4ef7\u683c\uff08\u5143/\u516c\u9877\uff09']
GD=pd.DataFrame(
	{u'\u7f16\u53f7':["1"],
	u'\u5747\u8d28\u533a\u7f16\u53f7':["Gxxxx"],
	u'\u8015\u5730\u5229\u7528\u7b49\u522b':[0],
	u'\u4ef7\u683c\uff08\u5143/\u516c\u9877\uff09':[0]}
	)[GD_order]
QTNYD_order=[u'\u7f16\u53f7',
		u'\u5747\u8d28\u533a\u7f16\u53f7',
		u'\u4e8c\u7ea7\u5730\u7c7b',
		u'\u4e8c\u7ea7\u5730\u7c7b\u4ee3\u7801',
		u'\u4ef7\u683c\uff08\u5143/\u516c\u9877\uff09']
QTNYD=pd.DataFrame(
	{u'\u7f16\u53f7':["1"],
	u'\u5747\u8d28\u533a\u7f16\u53f7':["Gxxxx"],
	u'\u4e8c\u7ea7\u5730\u7c7b':["xx"],
	u'\u4e8c\u7ea7\u5730\u7c7b\u4ee3\u7801':["xxxx"],
	u'\u4ef7\u683c\uff08\u5143/\u516c\u9877\uff09':[0]}
	)[QTNYD_order]

farmland_writer=pd.ExcelWriter(save_route+'\\'+system_name[2]+'.xls')
JZQ.to_excel(farmland_writer,sheet_name=u'\u5747\u8d28\u533a',index=False)
GD.to_excel(farmland_writer,sheet_name=u'\u8015\u5730',index=False)
QTNYD.to_excel(farmland_writer,sheet_name=u'\u5176\u4ed6\u519c\u7528\u5730',index=False)
farmland_writer.save()
farmland_writer.close()
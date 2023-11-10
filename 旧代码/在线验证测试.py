import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# import arcpy
# import os,sys,string

# import shlex,subprocess
# password=arcpy.GetParameterAsText(0)#to grant authorization
# hash_password=str(hash('idontkonw'+password+'iswhat'))
# p=subprocess.Popen(shlex.split("nslookup -q=TXT "+password+".tengdingkang.fun"), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# out,err=p.communicate()
# if len(out.split("\n"))==4:
# 	arcpy.AddMessage(password+' is not authorizated!')
# 	exit(0)
# elif filter(str.isdigit,out.split("\n")[5])!=hash_password:
# 	arcpy.AddMessage(password+' is not authorizated!')
# 	exit(0)
# #confirm authorization
arcpy.AddMessage("可以用中文了，很窒息的问题")
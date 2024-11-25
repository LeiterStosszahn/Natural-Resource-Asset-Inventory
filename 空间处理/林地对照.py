import arcpy

if time.time()>time.mktime((2022,6,30,0,0,0,0,0,0)):
	print('Out of validity!')
	0/0
	exit(0)
#term of validity

keywords=[]

switch_case={'0301':1,'0301K':1,'0302':2,'0302K':2,'0305':3,'0307':4,'0307K':4,
'0111':1,'0113':2,'0131':3,'0132':3,'0120':4,'0141':4,'0142':4,'0150':4,'0161':4,'0162':4,'0163':4,'0180':4,'0171':4,'0172':4,'0173':4}

def switch(data):
	return switch_case.get(data,5)

layer_1=arcpy.GetParameterAsText(0)#select layer
result_1=arcpy.GetParameterAsText(1)#Output result
dlbm_1=arcpy.GetParameterAsText(2)#DLBM
dilei_2=arcpy.GetParameterAsText(3)#A picture of the forest's DLBM

k=0
j=0

with arcpy.da.UpdateCursor(layer_1,[result_1,dlbm_1,dilei_2]) as cursor:
	for row in cursor:
		if switch(row[1])==switch(row[2]):
			row[0]="True"
			cursor.updateRow(row)
		elif switch(row[2])==5:
			row[0]="Not forest"
			cursor.updateRow(row)
			k=k+1
		else:
			row[0]="False"
			cursor.updateRow(row)
			j=j+1

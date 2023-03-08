''' Import Statements '''
import numpy as np
import pandas as pd
import os

Save = False
Download = False
Drop_data = True
Change_lables = True
Merge_data = True

data_dir = './data/HMS/'
temp_dir = './data/Temp/'
Fin_dir = './data/Data/'

def download():
	from pydrive.auth import GoogleAuth
	from pydrive.drive import GoogleDrive
	gauth = GoogleAuth()
	drive = GoogleDrive(gauth)
	real_id = '1U2SaFH7GzpcI1cZTWwmVk6YFZMI1T-LJ'
	# get folder id
	file_list = drive.ListFile({'q': "title='"+folder_name+"' and trashed=false"}).GetList()
	folder_id = file_list[0]['id'] if file_list[0]['id']==real_id else TypeError("id error")
	file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_id)}).GetList()
	#get files and save them
	for file in file_list:
		print(file['title'])
		content = drive.CreateFile({'id': file['id']})
		content.GetContentFile(data_dir+file['title'])
		content = ""
print('successfully downloaded')

''' Step 1 '''
def drop_data(Save):
	print('---drop data---')
	from list_of_variables import get_lists
	list_1, list_2, list_3, list_4, list_5 = get_lists()
	for i in os.listdir(data_dir):
		# get year of data
		year = int(i.replace('HMS_', '').replace('.csv', ''))
		print('year:', year)
		# read data here
		df = pd.read_csv(data_dir + i)
		df.drop(df.query('deprawsc != deprawsc').index, inplace=True)

		# pick out variables base on list from pervious part
		if year == 2021:
			dp = df[list_1].copy()
		elif year > 2017:
			dp = df[list_2].copy()
		elif year > 2016:
			dp = df[list_3].copy()
		elif year > 2015:
			dp = df[list_4].copy()
		else:
			dp = df[list_5].copy()
		df = ""

		# reorder index
		dp.reset_index(drop = True , inplace = True)
		dp.to_csv(temp_dir + 'temp_' + str(year) + '.csv', index=False) if Save else None
		dp = ""
	print('---step 1 completed---')

''' Step 2 '''
def change_lables(Save):
	print('---start rename---')
	from list_of_variables import lables_unification
	for i in os.listdir(temp_dir):
		df = pd.read_csv(temp_dir + i)
		year = int(i.replace('temp_', '').replace('.csv', ''))
		print(year)
		# change labes in this file
		df = lables_unification(df, year)
		# reorder variables names
		df = df.iloc[:, df.columns.argsort()]
		#print(df.columns)
		df.fillna(-1, inplace=True)
		df.to_csv(Fin_dir + str(year) + '.csv', index=False) if Save else None

	#Check if variable labels in different files are the same
	df1 = pd.read_csv(Fin_dir + '2021.csv')
	for i in os.listdir(Fin_dir):
		df2 = pd.read_csv(Fin_dir + i)
		diff1 = set(df1.columns) - set(df2.columns)
		diff2 = set(df2.columns) - set(df1.columns)

		if diff1 != diff2:
			print("These two data frames have different column names:")
			print(i, diff1, diff2)
			raise ValueError("Data frames have different columns")
		else:
			print(i, '->', "All data frames so far have the same column names")
	print('---complete---')
	df1 = ""
	df2 = ""

''' Step 3 '''
def merge_data(Save):
	print('---merge data---')
	data = pd.read_csv(Fin_dir + '2021.csv')
	# merge data from different files
	for i in os.listdir(Fin_dir):
		print(i)
		if (i == '2021.csv'):
			continue
		df = pd.read_csv(Fin_dir + i)
		data = pd.concat([data, df])
		data.reset_index(drop = True , inplace = True)
		df = ""

	data.fillna(-1, inplace=True)
	# change str to number
	data = data.apply(pd.to_numeric, errors='coerce')
	# depression score -> depression
	data['Depression'] = (data['Depression_point'] > 14)
	#data = data.drop("Depression_point", axis=1)

	data = data.replace({'void due to nonresponse':-1})
	#print(data)
	data.to_csv('./data/Fin_Data.csv', index=False) if Save else None
	print('---complete---')
	data = ""

''' * '''
# run these step functions
download(folder_name = 'HMS') if Download else None
drop_data(Save) if Drop_data else None
change_lables(Save) if Change_lables else None
merge_data(Save) if Merge_data else None
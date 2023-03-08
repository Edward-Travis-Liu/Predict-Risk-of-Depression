''' Import Statements '''
import pandas as pd
import os

file_id = '1FNEqCh25EyoOaC1_5-Vn0FqiyJCs_lQD'
Download_data = False
Sampling_percentage = 1.0

def download(file_id):
  from pydrive.auth import GoogleAuth
  from pydrive.drive import GoogleDrive
  gauth = GoogleAuth()
  drive = GoogleDrive(gauth)
  file = drive.CreateFile({'id':file_id})
  file.GetContentFile('./data/temp.csv')
  print('connection succeeded')
  file = ""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.metrics.pairwise import normalize
import matplotlib.pyplot as plt

#file = './data/temp.csv'
file = './data/HMS/HMS_2021.csv'

# chi squared feature selection for categorical data
from sklearn.feature_selection import chi2
from sklearn.feature_selection import mutual_info_classif
 
# load the dataset
def load_dataset(filename, Sampling_percentage):
  # load the dataset as a pandas DataFrame
  data = pd.read_csv(filename)
  data = data.sample(frac=Sampling_percentage)
  data.drop(data[data['degree_md'] != 1].index, inplace=True)
  # retrieve numpy array
  data = data.replace({'Yes': 1, 'No': 0, 'None': -1, True: 1, False: 0})
  data = data.apply(pd.to_numeric, errors='coerce')
  data.fillna(-1, inplace=True)
  # split into input (X) and output (y) variables
  list_X = data.drop("deprawsc", axis=1).columns
  X = data.drop("deprawsc", axis=1)#.values
  y = data["deprawsc"]#.values
  data = ""
  # format all fields as string
  #X = normalize(X).round(1) * 10
  #X = X.astype(str)
  return X, y, list_X
 
# prepare input data
def prepare_inputs(X_train, X_test):
  oe = OrdinalEncoder()
  oe.fit(X_train)
  X_train_enc = oe.transform(X_train)
  X_test_enc = oe.transform(X_test)
  return X_train_enc, X_test_enc
 
# Calculate scores of importance for each features
def mic(X, y):
  sl_scores = mutual_info_classif(X, y)
  features = pd.DataFrame({'feature': X.columns, 'score': sl_scores})
  reordered_features = features.sort_values('score', ascending=False).reset_index(drop=True)
  return reordered_features, sl_scores

# prepare target
def prepare_targets(y_train, y_test):
  le = LabelEncoder()
  le.fit(y_train)
  y_train_enc = le.transform(y_train)
  y_test_enc = le.transform(y_test)
  return y_train_enc, y_test_enc
 
# feature selection chi
def select_features_chi(X_train, y_train, X_test):
  fs = SelectKBest(score_func=chi2, k='all')
  fs.fit(X_train, y_train)
  X_train_fs = fs.transform(X_train)
  X_test_fs = fs.transform(X_test)
  return X_train_fs, X_test_fs, fs

# feature selection mic
def select_features_mic(X_train, y_train, X_test):
  fs = SelectKBest(score_func=mutual_info_classif, k='all')
  fs.fit(X_train, y_train)
  X_train_fs = fs.transform(X_train)
  X_test_fs = fs.transform(X_test)
  return X_train_fs, X_test_fs, fs

# download file
download(file_id) if Download_data else None
# load the dataset
X, y, list_X = load_dataset(file, Sampling_percentage)
# split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)
# prepare input data
X_train_enc, X_test_enc = prepare_inputs(X_train, X_test)
# prepare output data
y_train_enc, y_test_enc = prepare_targets(y_train, y_test)
# feature selection
X_train_fs, X_test_fs, fs = select_features_mic(X_train_enc, y_train_enc, X_test_enc)
# create dict with features and score
features = pd.DataFrame({'feature': list_X, 'score': fs.scores_})
re_features = features.sort_values('score', ascending=False).reset_index(drop=True)
#re_features, sl_scores = mic(X, y)
# plot the scores
#plt.bar([i for i in range(len(fs.scores_))], re_features['score'])
#plt.show()

# show scores for the features
sl_scores = fs.scores_
for i in range(len(sl_scores)):
  print('Feature %s: %f' % (re_features['feature'][i], re_features['score'][i]))

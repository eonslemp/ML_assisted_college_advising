import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split

from sklearn.impute import KNNImputer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
import imblearn

from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn import metrics
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.metrics import auc, precision_recall_curve



def drop_stuff(df, l):
    #dropping selected columns
    for i in l:
        df.drop(i, axis = 1, inplace = True)
    return df

def x_y_split(df):    
    #splits target from data
    x = df.iloc[:,(df.columns!='graduated_Y')]
    y = df.graduated_Y
    
    #creates test train split
    X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=4, test_size=0.2)
    
    #rejoins target to dataset 
    test = pd.concat([X_test, y_test], axis = 1)
    train = pd.concat([X_train, y_train], axis = 1)
    
    return train, test

def add_cool_features(df):
    df.loc[:,'effort'] = (df.homework*df.hs_ac_load)
    df.loc[:,'testing'] = df.math_b+df.reading_b+df.math_1
    df.loc[:,'v_facility'] = df.reading_b*(df.literacy_home + 1)
    df.loc[:,'m_facility'] = df.math_status_1*df.math_1
    df.loc[:,'academic_p'] = (df.effort)*df.hs_gpa
    df.loc[:,'iq_by_concientiousness'] = (df.v_facility+df.m_facility)*(df.homework+df.hs_ac_load)
    df.loc[:,'delinquency'] = df.risk_factors*(df.hedonics_b + df.hedonics_1)
    #df['effort'] = (df.homework+df.hs_ac_load)
    df.loc[:,'wages_cont'] = df.testing*df.wages_yr
    return df

def rename_cols(df):
    rename_list = ['literacy_home','risk_factors','aspired_occ_b','math_b',
                    'reading_b','math_conf_b','verbal_confidence','writing','sports','by_xcurr',
                    'homework','hedonics_b','hours_working_b','edu_confidence',
                    'aspired_occ_1','math_1','math_status_1','ps_step_1','f1_xcurr','hours_working_1',
                    'hedonics_1','math_conf_1','hs_ac_load','hs_gpa','any_ps','ps_level','graduated_Y',
                    'time_to_grad','edu_achievment','expected_edu','wages_yr']
    df.columns = rename_list
    return df

def rename_cols_x(df,columns_df):
    df.columns = columns_df.columns
    return df

def KNNimpute_DF(df):
    #filling in missing values with knn imputer
    imputer_knn = KNNImputer(n_neighbors = 10)
    imputer_knn.fit(df)

    x = imputer_knn.transform(df)
    
    #casting the numpy array to dataframe
    df = pd.DataFrame(x)
    return df

def round_ordinals(x):
    ordinal_feature_list = ['literacy_home','risk_factors','aspired_occ_b','sports','by_xcurr',
                    'homework','hedonics_b','hours_working_b','edu_confidence',
                    'aspired_occ_1','math_status_1','hs_gpa','f1_xcurr','hours_working_1',
                    'hedonics_1','hs_ac_load', 'testing','academic_p','graduated_Y']
    
    for k in ordinal_feature_list:
        x[k] = x.loc[:,k].apply(round)
    return x

def create_exploratory_set(df): 
    #imputes missing values
    z = KNNimpute_DF(df)  
    
    #renames columns
    rename_list = list(df.columns)
    z.columns = rename_list
    
    #rounds ordinal value cast as continious from imputation
    round_ordinals(z)    
    return z
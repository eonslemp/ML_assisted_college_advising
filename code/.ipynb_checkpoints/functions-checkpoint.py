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
    df['effort'] = (df.homework+df.hs_ac_load)
    df['testing'] = df.math_b+df.reading_b+df.math_1
    df['v_facility'] = df.reading_b*(df.literacy_home +1)
    df['m_facility'] = df.math_status_1*df.math_1
    df['academic_p'] = (df.effort)*df.hs_gpa
    df['iq_by_concientiousness'] = (df.v_facility+df.m_facility)*(df.homework+df.hs_ac_load)
    df['delinquency'] = df.risk_factors*(df.hedonics_b + df.hedonics_1)
    df['effort'] = (df.homework+df.hs_ac_load)
    df['wages_cont'] = df.testing*df.wages_yr
    return df
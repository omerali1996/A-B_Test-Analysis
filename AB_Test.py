import itertools
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene,\
    ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

Control = pd.read_excel("measurement_problems/ab_testing.xlsx",
                        sheet_name="Control Group")


df_control= Control.copy()

Test= pd.read_excel("measurement_problems/ab_testing.xlsx",
                    sheet_name="Test Group")

df_test = Test.copy()

df_test.head()

df_control.head()

def Analysis(df1,df2):
    print(5*"*"+"DF1 Data Analysis"+"*"*5)
    print("\nGENERAL INFORMATION")
    print(f"\n{df1.info()}")
    print(f"\n\nDESCRİBE \n{df1.describe().T}")
    print(f"\n\nCOLUMNS \n{[col for col in df1.columns]}")
    print(f"\n\nSHAPE\n{df1.shape}")
    print(f"\n\nNULL VALUES\n{df1.isnull().sum()}\n\n")


    print(5*"*"+"DF2 Data Analysis"+"*"*5)
    print("\nGENERAL INFORMATION")
    print(f"\n{df1.info()}")
    print(f"\n\nDESCRİBE \n{df1.describe().T}")
    print(f"\n\nCOLUMNS \n{[col for col in df1.columns]}")
    print(f"\n\nSHAPE\n{df1.shape}")
    print(f"\n\nNULL VALUES\n{df1.isnull().sum()}\n\n")

##############################################################

Analysis(df_test,df_control)


df_control.columns = [col+"_Control" for col in Control.columns]

df_test.columns = [col+"_Test" for col in Test.columns]

all_df = pd.concat([df_test,df_control],axis=1)

all_df.head()


#Görev2

#Kontrol için

#H0 : M1 = M2

#H1 : M1!= M2

test_ort=round(all_df['Purchase_Test'].mean(),5)

cont_ort=round(all_df['Purchase_Control'].mean(),5)

#Görev3

"""
Normal Distribution :
H0: Normal Distribution  OK .
H1: Normal Distribution not OK .

p < 0.05 H0 REJECTED , p > 0.05 H0 DO NOT REJECTED
"""

#Normal Distribution

p_value_control = shapiro(all_df["Purchase_Control"])[1]
p_value_test = shapiro(all_df["Purchase_Test"])[1]


#Variance Homogeneity

p_value_levene = levene(all_df['Purchase_Control'],
                        all_df['Purchase_Test'])[1]


#Result

p_value_ttest = ttest_ind(all_df['Purchase_Control'],
                          all_df['Purchase_Test'],
                          equal_var=True)[1]




############# All_Step_Function ###########

def AB_Test(df1, df2, pthres=0.05):
    Analysis(df1, df2)

    print(5 * "*" + "Combining Data" + 5 * "*"+"\n")

    df1.columns = (col + "_Test" for col in Test.columns)
    df2.columns = (col + "_Control" for col in Control.columns)

    all_df = pd.concat([df1, df2], axis=1)
    print(all_df.head(3))
    print("\n\n"+5 * "*" + "First Look " + 5 * "*"+"\n")


    test_ort = round(all_df['Purchase_Test'].mean(),5)
    cont_ort = round(all_df['Purchase_Control'].mean(), 5)
    print(f"Purchase Average of Test_Value => "
          f"{test_ort}")
    print(f"Purchase Average of Control_Value => "
          f"{cont_ort}\n\n")

    print(5 * "*" + "Normal Distribution Analysis" + 5 * "*"+"\n")

    p_value_control = shapiro(all_df['Purchase_Control'])[1]
    p_value_test = shapiro(all_df['Purchase_Test'])[1]
    print(f"p_value_control =>{p_value_control}")
    print(f"p_value_test =>{p_value_test}\n")

    if (p_value_test > pthres) & (p_value_control > pthres):
        print("HO DO NOT REJECTED\n\n")
    else:
        print("Review Dataset !!\n\n")



    print(5 * "*" + "Varience Homogeneity Analysis" + 5 * "*"+"\n")

    p_value_levene = levene(all_df['Purchase_Control'],
                            all_df['Purchase_Test'])[1]

    print(f"p_value_levene =>{p_value_levene}\n")

    if p_value_levene > pthres:
        print("VARIENCE HOMOGENEITY HO DO NOT REJECTED.\n")

    else:
        print("Review Dataset !!\n")

    if ((p_value_test > pthres) &
        (p_value_control > pthres)) & \
            (p_value_levene > pthres):
        print("Parametric Test Be Done.\n\n"
              "Explanation:\n'equal_var = True' applied on "
              "'test_index' func.\n\n")
    elif ((p_value_test > pthres) &
          (p_value_control > pthres)) & \
            (p_value_levene < pthres):
        print("Parametric Test Be Done.\n\n"
              "Explanation:\n'equal_var = False' applied on "
              "'test_index' func.\n\n")
    else:
        print("Non-Parametric Test Be Done.\n\n")

    print(5 * "*" + "RESULT" + 5 * "*"+"\n")
    "\n"
    p_value_ttest = ttest_ind(all_df['Purchase_Control'],
                              all_df['Purchase_Test'],
                              equal_var=True)[1]

    print(f"p_value_ttest =>{p_value_ttest}\n")

    if p_value_ttest > pthres:
        print(f"Although First Averages \nTest_Value  =>{test_ort},  Control_Value =>{cont_ort}\n,"
              f"averages are same statisticaly.\nIt is coincidence that Averages are different before analysis.\n"
              f"p_value_ttest_value is {round(p_value_ttest, 5)}.")

    else:
        print(f"p_value_ttest_value is lower than {pthres}")

AB_Test(df_test,df_control)


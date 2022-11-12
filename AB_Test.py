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
    print(5*"*"+"DF1 Verisinin Analizi"+"*"*5)
    print("\nGENEL BİLGİ")
    print(f"\n{df1.info()}")
    print(f"\n\nDESCRİBE \n{df1.describe().T}")
    print(f"\n\nSÜTUNLAR \n{[col for col in df1.columns]}")
    print(f"\n\nSHAPE\n{df1.shape}")
    print(f"\n\nBOŞ DEĞER\n{df1.isnull().sum()}\n\n")

    print(5*"*"+"DF2 Verisinin Analizi"+"*"*5)
    print("\nGENEL BİLGİ")
    print(f"\n{df2.info()}")
    print(f"\n\nDESCRİBE \n{df2.describe().T}")
    print(f"\n\nSÜTUNLAR \n{[col for col in df2.columns]}")
    print(f"\n\nSHAPE\n{df2.shape}")
    print(f"\n\nBOŞ DEĞER\n{df2.isnull().sum()}\n\n")

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
Normallik Varsayımı :
H0: Normal dağılım varsayımı sağlanmaktadır.
H1: Normal dağılım varsayımı sağlanmamaktadır.

p < 0.05 H0 RED , p > 0.05 H0 REDDEDİLEMEZ
Test sonucuna göre normallik varsayımı kontrol ve 
test grupları için sağlanıyor mu ?
Elde edilen p-value değerlerini yorumlayınız. 
"""

#Normal Dağılım

p_value_control = shapiro(all_df["Purchase_Control"])[1]
p_value_test = shapiro(all_df["Purchase_Test"])[1]


#Varyans Homojenliği

p_value_levene = levene(all_df['Purchase_Control'],
                        all_df['Purchase_Test'])[1]


#Sonuç

p_value_ttest = ttest_ind(all_df['Purchase_Control'],
                          all_df['Purchase_Test'],
                          equal_var=True)[1]




########################## Fonksiyonlaştırma

def AB_Test(df1, df2, pthres=0.05):
    Analysis(df1, df2)

    print(5 * "*" + "VERİ BİRLEŞTİRME" + 5 * "*"+"\n")

    df1.columns = (col + "_Test" for col in Test.columns)
    df2.columns = (col + "_Control" for col in Control.columns)

    all_df = pd.concat([df1, df2], axis=1)
    print(all_df.head(3))
    print("\n\n"+5 * "*" + "İLK İNCELEME" + 5 * "*"+"\n")


    test_ort = round(all_df['Purchase_Test'].mean(),5)
    cont_ort = round(all_df['Purchase_Control'].mean(), 5)
    print(f"Test Değişkenin Kazanç ortalaması => "
          f"{test_ort}")
    print(f"Control Değişkenin Kazanç ortalaması => "
          f"{cont_ort}\n\n")

    print(5 * "*" + "NORMAL DAĞILIM İNCELEME" + 5 * "*"+"\n")

    p_value_control = shapiro(all_df['Purchase_Control'])[1]
    p_value_test = shapiro(all_df['Purchase_Test'])[1]
    print(f"p_value_control =>{p_value_control}")
    print(f"p_value_test =>{p_value_test}\n")

    if (p_value_test > pthres) & (p_value_control > pthres):
        print("Normallik H0 Hipotezi Reddedilemez.\n\n")
    else:
        print("Veriyi incele !!\n\n")



    print(5 * "*" + "VARYANS HOMOJENLİĞİ İNCELEME" + 5 * "*"+"\n")

    p_value_levene = levene(all_df['Purchase_Control'],
                            all_df['Purchase_Test'])[1]

    print(f"p_value_levene =>{p_value_levene}\n")

    if p_value_levene > pthres:
        print("Varyans Homojenliği H0 Hipotezi Reddedilemez.\n")

    else:
        print("Veriyi incele !!\n")

    if ((p_value_test > pthres) &
        (p_value_control > pthres)) & \
            (p_value_levene > pthres):
        print("Parametrik Test yapılmalıdır.\n\n"
              "Açıklama:\n'test_index' fonksiyonunda"
              "'equal_var = True' yapılmalıdır.\n\n")
    elif ((p_value_test > pthres) &
          (p_value_control > pthres)) & \
            (p_value_levene < pthres):
        print("Parametrik Test yapılmalıdır.\n "
              "Açıklama:ttest_index fonksiyonunda,\n"
              "'equal_var = False' yapılmalıdır.\n\n")
    else:
        print("Non-Parametrik Test yapılmalıdır.\n\n")

    print(5 * "*" + "SONUÇ" + 5 * "*"+"\n")
    "\n"
    p_value_ttest = ttest_ind(all_df['Purchase_Control'],
                              all_df['Purchase_Test'],
                              equal_var=True)[1]

    print(f"p_value_ttest =>{p_value_ttest}\n")

    if p_value_ttest > pthres:
        print(f"İlk Ortalamalar \nTest için =>{test_ort},  Kontrol için =>{cont_ort}\nolmasına rağmen,"
              f"ortalamalar birbirine eşittir.\nFark olması istatistiksel olarak şanstır.\n"
              f"p_value_ttest değeri {round(p_value_ttest, 5)} çıkmıştır.")

    else:
        print(f"p_value_ttest değeri {pthres}'ten küçük")

AB_Test(df_test,df_control)


from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import scipy.special
import pandas as pd
from numeriska_metoder import newton_raphson
# pdf = lambda x: 2*np.exp(-2*x);
# Finv = lambda u: -(1/2)*np.log(u)
df = pd.read_csv("SLS22.csv") #data frame 
Lcq_ids = ["Majerus", "Oliveira","Decenzo","Santiago", "Papa", "Eaton", "Mota", "Shirai", "Jordan", "Hoefler", "Hoban", "Gustavo", "Ribeiro C", "O’neill", "Foy", "Midler"]

def init_normal_dataframe():
    ndf = df
    ndf["run 1"] = [x/10 for x in df["run 1"]]
    ndf["run 2"] = [x/10 for x in df["run 2"]]
    ndf["trick 1"] = [x/10 for x in df["trick 1"]]
    ndf["trick 2"] = [x/10 for x in df["trick 2"]]
    ndf["trick 3"] = [x/10 for x in df["trick 3"]]
    ndf["trick 4"] = [x/10 for x in df["trick 4"]]
    ndf["trick 5"] = [x/10 for x in df["trick 5"]]
    ndf["trick 6"] = [x/10 for x in df["trick 6"]]
    ndf["make 1"] = [int(bool(x)) for x in df["trick 1"].values.tolist()]
    ndf["make 2"] = [int(bool(x)) for x in df["trick 2"].values.tolist()]
    ndf["make 3"] = [int(bool(x)) for x in df["trick 3"].values.tolist()]
    ndf["make 4"] = [int(bool(x)) for x in df["trick 4"].values.tolist()]
    return ndf
ndf = init_normal_dataframe()
global_trick_data = np.concatenate([ndf[f"trick {i}"].values for i in range(1,5)])
global_svariance = np.var(global_trick_data,ddof=1)
global_smean = np.mean(global_trick_data)

ids = []
for name in ndf['id']:
    if name not in ids:
        ids.append(name)

# print(len(ids))

def make_histogram():
    # fig, ax = plt.subplots(1, 1)
    plt.hist(ndf["trick 1"], density=True, histtype='stepfilled', alpha=0.5, label = "Trick 1")
    plt.hist(ndf["trick 2"], density=True, histtype='stepfilled', alpha=0.5, label = "Trick 2")
    plt.hist(ndf["trick 3"], density=True, histtype='stepfilled', alpha=0.5, label = "Trick 3")
    plt.hist(ndf["trick 4"], density=True, histtype='stepfilled', alpha=0.5, label = "Trick 4")
    plt.legend()
    plt.show()


def make_histogram_runs():
    # fig, ax = plt.subplots(1, 1)
    plt.hist(ndf["run 1"], density=True,
             histtype='stepfilled', alpha=0.5, label="run 1")
    plt.hist(ndf["run 2"], density=True,
             histtype='stepfilled', alpha=0.5, label="run 2")
    plt.legend()
    plt.show()

def calculate_Q1_partd():
    count_lands = ndf["make 1"].values.tolist().count(1) + ndf["make 2"].values.tolist().count(1) +ndf["make 3"].values.tolist().count(1) + ndf["make 4"].values.tolist().count(1) 
    count_bigger_than6 = 0;
    alltricks = ndf["trick 1"].values.tolist() + ndf["trick 2"].values.tolist() + ndf["trick 3"].values.tolist() + ndf["trick 4"].values.tolist()
    for x in alltricks:
        if x>0.6:
            count_bigger_than6+=1
    return float(count_bigger_than6)/float(count_lands)


def plot_run1_run2():
    plt.scatter(ndf["run 1"],ndf["run 2"],color='blue', marker='o')
    plt.xlabel('run 1')
    plt.ylabel('run 2')
    plt.legend()
    plt.show()


def init_trick_data():
    ndf.set_index('id',inplace=True)
    tricks_data = {}
    n = len(ndf)
    for name in list(ids):
        namesdata = ndf.loc[name]
        if isinstance(namesdata['trick 1'],float):
            tricks_data[name] = np.array([namesdata['trick 1']]+[namesdata['trick 2']]+[namesdata['trick 3']]+[namesdata['trick 4']])
        else:
            tricks_data[name] = np.array(list(namesdata['trick 1'])+list(namesdata['trick 2'])+list(namesdata['trick 3'])+list(namesdata['trick 4']))
    return tricks_data

tricks_data = init_trick_data()

# average_svariance = 0
# for eachdata in tricks_data.values():
#     a = np.array([k for k in eachdata if k>0])
#     average_svariance+=np.var(a)
# average_svariance/=len(ids)

def get_pooled_var():
    täljare = 0
    nämnare = 0
    for eachdata in tricks_data.values():
        zi = np.array([k for k in eachdata if k>0])
        if len(zi)==1:
            si = 0
            ni = len(zi)-1
            täljare+=si*ni
            nämnare+=ni
        else:
            si = np.var(zi,ddof=1)
            ni = len(zi)-1
            täljare+=si*(ni)
            nämnare+=ni
    return täljare/nämnare

pooled_var = get_pooled_var()


def Theta_MoM_skattning(xdata):
    data = xdata>0.0
    return np.mean(data)

def AlphaBeta_MoM_skattning(xdata):
    data = [x for x in xdata if x>0]
    if len(data)==1:
        svariance = pooled_var
    else:
        svariance = np.var(data,ddof=1)
    svariance = global_svariance
    alpha_0 = np.mean(data)*((1-np.mean(data))/svariance-1)
    beta_0 = (1-np.mean(data))*((1-np.mean(data))/svariance-1)
    return np.array([alpha_0,beta_0])   



def get_parameters():
    result = {}
    for name in ids:
        theta = Theta_MoM_skattning(np.array(tricks_data[name]))
        alpha = AlphaBeta_MoM_skattning(np.array(tricks_data[name]))[0]
        beta = AlphaBeta_MoM_skattning(np.array(tricks_data[name]))[1]
        result[name] = [theta,alpha,beta]
    return result

def get_parameters_tricks():
    result = {}
    for name in ids:
        theta = Theta_MoM_skattning(np.array(tricks_data[name]))
        alpha = newton_raphson(np.array(tricks_data[name]))[0]
        beta = newton_raphson(np.array(tricks_data[name]))[1]
        result[name] = [theta,alpha,beta]
    return result
get_parameters_tricks()
# params = get_parameters_tricks()
# for key,value in params.items():
#     print(key,*value)

def init_run_data():
    tricks_data = {}
    n = len(ndf)
    for name in list(ids):
        namesdata = ndf.loc[name]
        if isinstance(namesdata['run 1'],float):
            tricks_data[name] = np.array([namesdata['run 1']]+[namesdata['run 2']])
        else:
            tricks_data[name] = np.array(list(namesdata['run 1'])+list(namesdata['run 2']))
    return tricks_data

run_data = init_run_data()

def get_parameters_runs():
    result = {}
    for name in ids:
        alpha = newton_raphson(np.array(run_data[name]))[0]
        beta = newton_raphson(np.array(run_data[name]))[1]
        result[name] = [alpha,beta]
    return result

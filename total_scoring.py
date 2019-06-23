import numpy as np
import matplotlib.pyplot as plt
import scipy.sparse.linalg
import pandas as pd

print("Episode","\t",'Total_Lot',"\t","Assigned_Lot","\t","TN","\t","FP","\t","FN","\t","TP")
for i in range(70,105):
    data = pd.read_excel("./result/20190519_total_result_64x10_"+str(i)+"_2.xlsx")
    assigned_lot = data[data['RESULT']==1]
    non_assigned_lot = data[data['RESULT']==0]
    correct_assigned_lot = assigned_lot[assigned_lot['RESULT_pred']==1]
    wrong_assigned_lot = assigned_lot[assigned_lot['RESULT_pred']==0]
    correct_non_assigned_lot = non_assigned_lot[non_assigned_lot['RESULT_pred']==0]
    wrong_non_assigned_lot = non_assigned_lot[non_assigned_lot['RESULT_pred']==1]

    print(i,"\t",len(data),"\t",len(assigned_lot),"\t",len(correct_non_assigned_lot),"\t",len(wrong_non_assigned_lot),"\t",len(wrong_assigned_lot),"\t",len(correct_assigned_lot))
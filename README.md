import xlrd            
from numpy import random, dot, exp, array  
import numpy as np
import pandas as pd    
import traceback  
import time







































































def AHP():
    def is_identity_matrix(matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        if rows != cols:
            return False
        for i in range(rows):
            for j in range(cols):
                if i == j and matrix[i][j] != 1:
                    return False
                elif i != j and matrix[i][j] != 0:
                    return False
        return True
        
   def gm():
        list1 = []
        list2 = []
        num = 1
        for i in range(rowNum):
            list1.append(list(judmat_arr_empty[i]))
        for i in range(len(list1)):
            for j in range(len(list1[i])):
                num = num * list1[i][j]
            list2.append(num ** (1 / len(list1)))
            num = 1
        if sum(list2)==0:                              
            gm_wi = list2
        else:
            gm_wi = list2 / sum(list2)                
        list2 = np.array(gm_wi).reshape(rowNum, 1)
        gm_va_pro = judmat_arr_empty @ list2
        if sum(list2)==0:                              
            gm_va= np.array([0])
        else:
            gm_va = sum(gm_va_pro / list2) / rowNum 
        if rowNum==1 :                                
            gm_CI = [0]
        else:                                          
            gm_CI = (gm_va-rowNum)/(rowNum-1)
        if RI[rowNum-1]==0:
            gm_CR = [0]
        else:
            gm_CR = gm_CI/RI[rowNum-1]
        gm_list=list(gm_wi)+list(gm_va)+list(gm_CI)+list(gm_CR)
        return gm_list
        
   def amm():
        col_sum = np.sum(judmat_arr_empty, axis=0)  
        a = np.sum(bljz_arr_empty / col_sum, axis=1)  
        asum = sum(a)  
        amm_wi = a / asum  
        list2 = np.array(amm_wi).reshape(rowNum, 1)
        amm_va_pro = judmat_arr_empty @ list2  
        amm_va = sum(amm_va_pro / list2) / rowNum  
        if rowNum==1:                                  
            amm_CI = [0]
        else:
            amm_CI = (amm_va - rowNum) / (rowNum - 1)        
        if RI[rowNum-1]==0:
            amm_CR = [0]
        else:
            amm_CR = amm_CI / RI[rowNum-1]
        amm_list=list(amm_wi)+list(amm_va)+list(amm_CI)+list(amm_CR)
        return amm_list

   def eig():
        eigen_values, eigen_vectors = np.linalg.eig(judmat_arr_empty)
        max_eigen_value_index = np.argmax(eigen_values)    
        eig_va=eigen_values[max_eigen_value_index]
        eig_vec=eigen_vectors[:,max_eigen_value_index]

        if is_identity_matrix(judmat_arr_empty):      
            eig_wi = []
            for i in range(len(judmat_arr_empty)):
                eig_wi.append(0)
        else:                                         
            eig_wi=eigen_vectors[:,max_eigen_value_index]/sum(eigen_vectors[:,max_eigen_value_index])
        print(rowNum)
        print(eig_wi)
        if rowNum ==1 :
            arr_eig_wi = np.array(eig_wi)  
            rowNum_nozero = np.count_nonzero(arr_eig_wi)
            eig_CI = 0
        else:
            arr_eig_wi = np.array(eig_wi)  
            rowNum_nozero = np.count_nonzero(arr_eig_wi)
            eig_CI = (eig_va - rowNum_nozero) / (rowNum_nozero - 1)
        if RI[rowNum_nozero-1]==0:
            eig_CR = 0
        else:
            eig_CR = eig_CI / RI[rowNum_nozero-1]                      
        eig_list = np.array([eig_va.real,eig_CI.real,eig_CR.real])                     
        eig_arr=np.append(eig_wi,eig_list).real
        return eig_arr

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('max_colwidth', 200)

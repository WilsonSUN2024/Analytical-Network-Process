# -*- coding = utf-8 -*-
# @Software : PyCharm

import xlrd
from numpy import random, dot, exp, array
import numpy as np
import pandas as pd
import traceback
import time

def AHP():
    # Check if it's an identity matrix
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

    def gm():                                   # Eigenvector Method
        list1 = []
        list2 = []
        num = 1
        for i in range(rowNum):
            list1.append(list(judgment_matrix_arr_empty[i]))
        for i in range(len(list1)):
            for j in range(len(list1[i])):
                num = num * list1[i][j]
            list2.append(num ** (1 / len(list1)))
            num = 1
        if sum(list2)==0:                              # Fix denominator=0
            gm_wi = list2
        else:
            gm_wi = list2 / sum(list2)                 # Fix completed
        list2 = np.array(gm_wi).reshape(rowNum, 1)
        gm_va_pro = judgment_matrix_arr_empty @ list2
        if sum(list2)==0:                               # Fix denominator=0
            gm_va= np.array([0])
        else:
            gm_va = sum(gm_va_pro / list2) / rowNum     # Fix completed
        if rowNum==1 :                                 # Fix denominator=0
            gm_CI = [0]
        else:                                          # Fix completed
            gm_CI = (gm_va-rowNum)/(rowNum-1)
        if RI[rowNum-1]==0:
            gm_CR = [0]
        else:
            gm_CR = gm_CI/RI[rowNum-1]
        gm_list=list(gm_wi)+list(gm_va)+list(gm_CI)+list(gm_CR)
        return gm_list
    def amm():
        col_sum = np.sum(judgment_matrix_arr_empty, axis=0)  # Calculate column sums

        a = np.sum(judgment_matrix_arr_empty / col_sum, axis=1)  # Calculate row sums after matrix/column sum division
        asum = sum(a)  # Total row sum
        amm_wi = a / asum  # Calculate weights
        list2 = np.array(amm_wi).reshape(rowNum, 1)
        amm_va_pro = judgment_matrix_arr_empty @ list2  
        amm_va = sum(amm_va_pro / list2) / rowNum  # λ
        if rowNum==1:                                   # Fix denominator=0
            amm_CI = [0]
        else:
            amm_CI = (amm_va - rowNum) / (rowNum - 1)        # Fix completed
        if RI[rowNum-1]==0:
            amm_CR = [0]
        else:
            amm_CR = amm_CI / RI[rowNum-1]
        amm_list=list(amm_wi)+list(amm_va)+list(amm_CI)+list(amm_CR)
        return amm_list

    def eig():
        # Eigenvector Method
        # Use numpy's eig() function to find eigenvalues and eigenvectors
        eigen_values, eigen_vectors = np.linalg.eig(judgment_matrix_arr_empty)
        # Find the index of the maximum eigenvalue
        max_eigen_value_index = np.argmax(eigen_values)
        # Get maximum eigenvalue
        # print("Eigenvector Method - Maximum Eigenvalue:", eigen_values[max_eigen_value_index])       
        eig_va=eigen_values[max_eigen_value_index]
        # Get corresponding eigenvector
        # print("Eigenvector Method - Maximum Eigenvalue：",eigen_vectors[:,max_eigen_value_index])
        eig_vec=eigen_vectors[:,max_eigen_value_index]
        # print("Eigenvector Method - Weights:",eigen_vectors[:,max_eigen_value_index]/sum(eigen_vectors[:,max_eigen_value_index]))

        # print(judgment_matrix_arr_empty)
        if is_identity_matrix(judgment_matrix_arr_empty):         # Check if it's an identity matrix, set weights to 0 if true
            eig_wi = []
            for i in range(len(judgment_matrix_arr_empty)):
                eig_wi.append(0)
        else:                                         # Normal calculation for non-identity matrix
            eig_wi=eigen_vectors[:,max_eigen_value_index]/sum(eigen_vectors[:,max_eigen_value_index])
        print(rowNum)
        print(eig_wi)
        if rowNum ==1 :
            arr_eig_wi = np.array(eig_wi)  # Process CI CR calculation using actual wi count
            rowNum_nozero = np.count_nonzero(arr_eig_wi)
            eig_CI = 0
        else:
            arr_eig_wi = np.array(eig_wi)  # Process CI CR calculation using actual wi count
            rowNum_nozero = np.count_nonzero(arr_eig_wi)
            eig_CI = (eig_va - rowNum_nozero) / (rowNum_nozero - 1)
        if RI[rowNum_nozero-1]==0:
            eig_CR = 0
        else:
            eig_CR = eig_CI / RI[rowNum_nozero-1]    # rownum -1 because 5 rows, ronum is 5, but the 5th position in list is 4 (list starts from 0)
        eig_list = np.array([eig_va.real,eig_CI.real,eig_CR.real])    # Use real part .real, use imaginary part attribute .imag
        eig_arr=np.append(eig_wi,eig_list).real
        return eig_arr

    # Display all columns in DataFrame (None means show all rows, can also set numbers)
    pd.set_option('display.max_columns', None)

    # Display all rows in DataFrame
    pd.set_option('display.max_rows', None)

    # Set display length for DataFrame data, default is 50
    pd.set_option('max_colwidth', 200)

    table_ys = xlrd.open_workbook(r".\ANP_data1.xls", 'rb')
    sheet_ys = table_ys.sheet_names()
    sheet_num = len(sheet_ys)
    writer = pd.ExcelWriter('001-ANP_result.xls')  # Create worksheet for data writing
    # print(sheet_num)                           # Check number of worksheets
    for k in range(sheet_num):                   # Read each worksheet
        sheet_ys = table_ys.sheet_by_index(k)
        rowNum = sheet_ys.nrows - 1
        colNum = sheet_ys.ncols - 1
        newlist = []
        for i in range(rowNum):
            rowi = sheet_ys.row_values(i+1)
            newlist.append((rowi[1:]))
        judgment_matrix_arr_empty = np.empty([rowNum, colNum])
        for i in range(rowNum):
            judgment_matrix_arr_empty[i] = array(newlist[i])

        RI=[0,0,0.52,0.89,1.12,1.24,1.36,1.41,1.46,1.49,1.52,1.54,1.56,1.58,1.59,1.5943]   # 16 RI values corresponding to different n values
        colname=[]
        for i in range(rowNum):
            colname.append('w{}'.format(i+1))
        list333=['lmax','CI','CR']
        for i in list333:
            colname.append(i)
        rowname = ['Geometric Mean Method', 'Arithmetic Mean Method', 'Eigenvector Method']
        # Check if it's an identity matrix
        if rowNum==1:
            c = np.random.uniform(0, 0, [3, len(judgment_matrix_arr_empty) + 3])
            print(c)
            for i in range(len(c)):
                c[i,0]=1
        elif is_identity_matrix(judgment_matrix_arr_empty):
            c=np.random.uniform(0,0,[3,len(judgment_matrix_arr_empty)+3]) # Use np.random.uniform(0,0,size) to output all-zero matrix
            # print(c)
        else:
            c=np.array([gm(),amm(),eig()])
        # print(c)
        # Replace NaN values in c with 0
        # c[np.isnan(c)]=0
        df = pd.DataFrame(c,columns=colname,index=rowname)
        print(df)
        # Write data to Excel
        df.to_excel(excel_writer=writer, sheet_name='Weight Coefficient{}'.format(k+1)) # Output data to excel
        writer.save()
        writer.close()
def unweighted_supermatrix():                              
    global num_C,A,B
    print('\n--------------------Supermatrix Calculation------------------------------\n')
    num_C= int(input('Please enter the total number of major C (factor sets)：'))
    num_Cij = int(input('Please enter the total number of Cij (factors)：'))
    table_ys = xlrd.open_workbook(r".\001-ANP_result.xls", 'rb')
    sheet_ys = table_ys.sheet_names()
    sheet_num = len(sheet_ys)
    newlist = []
    for k in range(sheet_num-num_C):                        # Extract data to list[]
        sheet_ys = table_ys.sheet_by_index(k+num_C)
        rowNum = sheet_ys.nrows - 3
        colNum = sheet_ys.ncols - 4
        for i in range(rowNum):
            rowi = sheet_ys.row_values(i + 3)
            for j in range(len(rowi[1:][:-3])):         # Split list and add one by one, so all in one list
                newlist.append(rowi[1:][:-3][j])
    # print(newlist)
    # print(len(newlist))
    A = np.array(newlist).reshape(num_Cij,num_Cij).T
    print(A)
    # Save to local
    writer = pd.ExcelWriter('002-Supermatrix-Weight_Matrix.xls')  # Create worksheet for data writing
    A = pd.DataFrame(A)
    A.columns=range(1,len(A.columns)+1)                 # Adjust column labels
    A.index=range(1,len(A.index)+1)                     # Adjust row labels
    A.to_excel(excel_writer=writer, sheet_name='Supermatrix')  # Create worksheet for data writing
    writer.save()

    print('\n---------------------Start Weight Matrix Calculation-------------------\n')
    newlist2 = []
    for k in range(num_C):                            # Extract data to list[] for weight data
        sheet_ys = table_ys.sheet_by_index(k)
        rowNum = sheet_ys.nrows - 3
        colNum = sheet_ys.ncols - 4
        for i in range(rowNum):
            rowi = sheet_ys.row_values(i + 3)
            newlist2.append(rowi[1:][:-3])
    B = np.array(newlist2).reshape(num_C,num_C).T
    print(B)
    B = pd.DataFrame(B)
    B.columns = range(1, len(B.columns) + 1)  # Adjust column labels
    B.index = range(1, len(B.index) + 1)  # Adjust row labels
    B.to_excel(excel_writer=writer, sheet_name='Weight Matrix')  # Output data to Excel
    writer.save()
    writer.close()

def weighted_supermatrix():                         

    print('\n-----------------Start Calculating Weighted Supermatrix------------------\n')
    listCij_num = []
    # Get composition of supermatrix
    for k in range(num_C):
        a = int(input(f'Please enter the number of factors in C{}:'))
        listCij_num.append(a)
    lCs = [0]
    t=0
    for i in listCij_num:                  # Data processing
        t = i+t
        lCs.append(t)
    # print(lCs)
    # Read data for calculation
    C=np.array(A)                     # Convert A to array -- supermatrix
    D=np.array(B)                     # Convert B to array -- weight matrix
    # print(D)
    for i in range(num_C):               # Row count -- major C           # Expand one position of matrix by x times
        for k in range(num_C):           # Column count -- major C        # Expand one position of matrix by x times
            C[lCs[i]:lCs[i+1],lCs[k]:lCs[k+1]]*=D[i,k]

    # Normalize
    C_sum = np.sum(C,axis=0)
    for i in range(len(C_sum)):
        if C_sum[i] == 0 :
            C_sum[i] = 1
    print(C_sum)
    C = C/C_sum
    print(C)
    # Store data
    weighted_supermatrix = pd.DataFrame(C)
    weighted_supermatrix.columns = range(1, len(weighted_supermatrix.columns) + 1)  # Adjust column labels
    weighted_supermatrix.index = range(1, len(weighted_supermatrix.index) + 1)  # Adjust row labels
    writer = pd.ExcelWriter('003-weighted_supermatrix.xls')  # Create worksheet for data writing
    weighted_supermatrix.to_excel(excel_writer=writer, sheet_name='weighted_supermatrix')  # Output data to Excel
    writer.save()
    writer.close()

def limit_supermatrix():
    table_ys = xlrd.open_workbook(r".\003-Weighted Supermatrix.xls", 'rb')
    sheet_ys = table_ys.sheet_names()[0]
    sheet_ys = table_ys.sheet_by_index(0)
    rowNum = sheet_ys.nrows - 1
    colNum = sheet_ys.ncols - 1
    newlist = []
    for i in range(rowNum):
        rowi = sheet_ys.row_values(i+1)
        newlist.append(rowi[1:])
    judgment_matrix_arr_empty = np.empty([rowNum, colNum])
    for i in range(rowNum):
        judgment_matrix_arr_empty[i] = array(newlist[i])
    judgment_matrix = judgment_matrix_arr_empty
    A = judgment_matrix    # Record first power of judgment_matrix
    B = judgment_matrix   # Record first power of judgment_matrix
    C = judgment_matrix
    i = 0
    print('\n-----------------Start Calculating Limit Supermatrix--------------------------\n')
    a,b = int(input('(This software uses iteration to calculate limit matrix, stops when exceeding cycles or below accuracy) Please enter accuracy: ')),\
          float(input('（This software uses iteration to calculate limit matrix, stops when exceeding cycles or below accuracy) Please enter accuracy：'))
    print('Input successful：',a,b)
    while True:
        i += 1
        if i == 1:
            A = np.dot(A, A)
            max_Al1 = np.sum(A,axis=0)
            for i in range(len(max_Al1)):
                if max_Al1[i]==0:
                    max_Al1[i]==1
            A = A/max_Al1
            A[np.isnan(A)]=0
        elif i == a:
            print('Iteration count:', i, ", iteration", i - 1, 'equals iteration', i)
            print('------------Limit Supermatrix------------\n', A)
            break
        elif (A - B>b).any():  # Check if A is different from A's n-1 power. any means compare each element in A and B, if any element is different A != B returns True.
            B = A  # Record A's n-1 power.
            A = np.dot(A, C)  # Increase by one power
            max_Al2 = np.sum(A,axis=0)
            for i in range(len(max_Al2)):
                if max_Al2[i]==0:
                    max_Al2[i]==1
            A = A/max_Al2
            A[np.isnan(A)] = 0

        else:
            print('Iteration count:', i, ", iteration", i - 1, 'equals iteration', i)
            print('------------Limit Supermatrix------------\n', A)
            break
    A = A + 0  # Convert True/False to 0/1
    A = np.round(A,10)
    A = pd.DataFrame(A)
    A.columns = range(1, len(A.columns) + 1)  # Adjust column labels
    A.index = range(1, len(A.index) + 1)  # Adjust row labels
    A.to_excel('004-Limit Supermatrix.xls',encoding='utf_8_sig')   # Save reachability matrix to local
while True:
    try:
        while True:
            print('--------------------------------------------\n'
                  'This program is for ANP (Analytical Network Process) analysis.\n'
                  '\n--------------------------------------------')
            c_c = int(input('This software is for ANP model. Mode 1 requires "ANP_data1.xls", Mode 2 requires "003-Weighted Supermatrix.xls"'
                            '\nPlease select operation mode: 1.Full run (AHP calculation-Supermatrix-Weight Matrix-Weighted Supermatrix-Limit Supermatrix) 2.Partial run (Weighted Supermatrix-Limit Supermatrix) 3.Exit. Please enter 1 or 2 or 3 (1/2/3): '))
            if c_c == 1 :
                AHP()
                unweighted_supermatrix()
                weighted_supermatrix()
                limit_supermatrix()
                print('\nAll files have been generated, please check in the folder\n')
            elif c_c == 2 :
                limit_supermatrix()
                print('\nAll files have been generated, please check in the folder\n')
            elif c_c == 3:
                break
            else:
                print('----------------\nInput error, please enter 1 or 2')
                continue
        break
    except Exception:
        print('-------------------------------')
        traceback.print_exc()
        time.sleep(1)
        print('Input error, please re-enter')
        print('-------------------------------')

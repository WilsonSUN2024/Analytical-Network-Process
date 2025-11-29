# -*- coding: utf-8 -*-
# Analytical Network Process (ANP) Full Script

import xlrd
from numpy import array
import numpy as np
import pandas as pd

# --------------------------------------------------------------
#  AHP SECTION
# --------------------------------------------------------------
def AHP():
    def is_identity_matrix(matrix):
        rows, cols = len(matrix), len(matrix[0])
        if rows != cols:
            return False
        for i in range(rows):
            for j in range(cols):
                if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                    return False
        return True

    def gm():
        list1, list2 = [], []
        num = 1
        for i in range(rowNum):
            list1.append(list(judgment_matrix_arr_empty[i]))
        for row in list1:
            for v in row:
                num *= v
            list2.append(num ** (1 / len(row)))
            num = 1
        gm_wi = list2 / sum(list2) if sum(list2) != 0 else list2
        list2_arr = np.array(gm_wi).reshape(rowNum, 1)
        gm_va_pro = judgment_matrix_arr_empty @ list2_arr
        gm_va = sum(gm_va_pro / list2_arr) / rowNum if sum(list2_arr) != 0 else np.array([0])
        gm_CI = (gm_va - rowNum) / (rowNum - 1) if rowNum != 1 else [0]
        gm_CR = gm_CI / RI[rowNum - 1] if RI[rowNum - 1] != 0 else [0]
        return list(gm_wi) + list(gm_va) + list(gm_CI) + list(gm_CR)

    def amm():
        col_sum = np.sum(judgment_matrix_arr_empty, axis=0)
        a = np.sum(judgment_matrix_arr_empty / col_sum, axis=1)
        amm_wi = a / sum(a)
        list2 = np.array(amm_wi).reshape(rowNum, 1)
        amm_va_pro = judgment_matrix_arr_empty @ list2
        amm_va = sum(amm_va_pro / list2) / rowNum
        amm_CI = (amm_va - rowNum) / (rowNum - 1) if rowNum != 1 else [0]
        amm_CR = amm_CI / RI[rowNum - 1] if RI[rowNum - 1] != 0 else [0]
        return list(amm_wi) + list(amm_va) + list(amm_CI) + list(amm_CR)

    def eig():
        eigen_values, eigen_vectors = np.linalg.eig(judgment_matrix_arr_empty)
        idx = np.argmax(eigen_values)
        eig_va = eigen_values[idx]
        eig_vec = eigen_vectors[:, idx]
        eig_wi = eig_vec / sum(eig_vec) if not is_identity_matrix(judgment_matrix_arr_empty) else [0] * len(judgment_matrix_arr_empty)
        arr_eig_wi = np.array(eig_wi)
        rowNum_nz = np.count_nonzero(arr_eig_wi)
        eig_CI = (eig_va - rowNum_nz) / (rowNum_nz - 1) if rowNum != 1 else 0
        eig_CR = eig_CI / RI[rowNum_nz - 1] if RI[rowNum_nz - 1] != 0 else 0
        eig_list = np.array([eig_va.real, eig_CI.real, eig_CR.real])
        return np.append(eig_wi, eig_list).real

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    table_ys = xlrd.open_workbook(r"./ANP_data1.xls", 'rb')
    sheet_num = len(table_ys.sheet_names())
    writer = pd.ExcelWriter('001-ANP_result.xls')

    for k in range(sheet_num):
        sheet = table_ys.sheet_by_index(k)
        global rowNum, colNum, judgment_matrix_arr_empty
        rowNum = sheet.nrows - 1
        colNum = sheet.ncols - 1
        newlist = [sheet.row_values(i + 1)[1:] for i in range(rowNum)]
        judgment_matrix_arr_empty = np.array(newlist)

        global RI
        RI = [0, 0, 0.52, 0.89, 1.12, 1.24, 1.36, 1.41, 1.46, 1.49, 1.52, 1.54, 1.56, 1.58, 1.59, 1.5943]

        colname = [f"w{i+1}" for i in range(rowNum)] + ['lmax', 'CI', 'CR']
        rowname = ['Geometric Mean Method', 'Arithmetic Mean Method', 'Eigenvector Method']

        if rowNum == 1 or is_identity_matrix(judgment_matrix_arr_empty):
            c = np.zeros([3, len(judgment_matrix_arr_empty) + 3])
            for i in range(len(c)):
                c[i, 0] = 1
        else:
            c = np.array([gm(), amm(), eig()])

        df = pd.DataFrame(c, columns=colname, index=rowname)
        df.to_excel(writer, sheet_name=f'Weight Coefficient{k+1}')

    writer.save()
    writer.close()

# --------------------------------------------------------------
# SUPER MATRIX (UNWEIGHTED)
# --------------------------------------------------------------
def unweighted_supermatrix():
    global num_C, A, B
    num_C = int(input('Enter number of major clusters C: '))
    num_Cij = int(input('Enter number of total factors Cij: '))

    table_ys = xlrd.open_workbook(r"./001-ANP_result.xls", 'rb')
    sheet_num = len(table_ys.sheet_names())

    newlist = []
    for k in range(sheet_num - num_C):
        sheet = table_ys.sheet_by_index(k + num_C)
        rowNum = sheet.nrows - 3
        for i in range(rowNum):
            rowi = sheet.row_values(i + 3)
            newlist.extend(rowi[1:][:-3])

    A = np.array(newlist).reshape(num_Cij, num_Cij).T
    A_df = pd.DataFrame(A)
    A_df.to_excel('002-Supermatrix-Weight_Matrix.xls', sheet_name='Supermatrix')

    newlist2 = []
    for k in range(num_C):
        sheet = table_ys.sheet_by_index(k)
        rowNum = sheet.nrows - 3
        for i in range(rowNum):
            newlist2.append(sheet.row_values(i + 3)[1:][:-3])

    B = np.array(newlist2).reshape(num_C, num_C).T
    B_df = pd.DataFrame(B)
    with pd.ExcelWriter('002-Supermatrix-Weight_Matrix.xls', mode='a') as writer:
        B_df.to_excel(writer, sheet_name='Weight Matrix')

# --------------------------------------------------------------
# WEIGHTED SUPERMATRIX
# --------------------------------------------------------------
def weighted_supermatrix():
    listCij_num = []
    for k in range(num_C):
        a = int(input(f'Enter number of factors in C{k+1}: '))
        listCij_num.append(a)

    lCs = [0]
    t = 0
    for i in listCij_num:
        t += i
        lCs.append(t)

    C_arr = np.array(A)
    D_arr = np.array(B)

    for i in range(num_C):
        for k in range(num_C):
            C_arr[lCs[i]:lCs[i+1], lCs[k]:lCs[k+1]] *= D_arr[i, k]

    C_sum = np.sum(C_arr, axis=0)
    C_sum[C_sum == 0] = 1
    C_arr = C_arr / C_sum

    df = pd.DataFrame(C_arr)
    df.to_excel('003-weighted_supermatrix.xls', sheet_name='weighted_supermatrix')

# --------------------------------------------------------------
# LIMIT SUPER MATRIX
# --------------------------------------------------------------
def limit_supermatrix():
    table_ys = xlrd.open_workbook(r"./003-weighted_supermatrix.xls", 'rb')
    sheet = table_ys.sheet_by_index(0)
    rowNum = sheet.nrows - 1
    newlist = [sheet.row_values(i + 1)[1:] for i in range(rowNum)]

    A = np.array(newlist)
    B = A.copy()
    C = A.copy()

    max_iter = int(input('Enter max iteration count: '))
    tol = float(input('Enter tolerance: '))

    for i in range(1, max_iter + 1):
        A = A @ C
        A = A / np.sum(A, axis=0)
        A[np.isnan(A)] = 0
        if np.all(np.abs(A - B) <= tol):
            break
        B = A.copy()

    A = np.round(A, 10)
    df = pd.DataFrame(A)
    df.to_excel('004-limit_supermatrix_result.xls', sheet_name='limit_supermatrix')

# --------------------------------------------------------------
# MAIN EXECUTION
# --------------------------------------------------------------
if __name__ == "__main__":
    print("ANP Module Loaded. Call functions manually as needed.")

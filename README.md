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

    table_ys = xlrd.open_workbook(r".\ANP_Dataset_1.xls", 'rb')
    sheet_ys = table_ys.sheet_names()
    sheet_num = len(sheet_ys)
    writer = pd.ExcelWriter('001-AHP_Result.xls') 
    # print(sheet_num)                          
    for k in range(sheet_num):                  
        sheet_ys = table_ys.sheet_by_index(k)
        rowNum = sheet_ys.nrows - 1
        colNum = sheet_ys.ncols - 1
        newlist = []
        for i in range(rowNum):
            rowi = sheet_ys.row_values(i+1)
            newlist.append((rowi[1:]))
        bljz_arr_empty = np.empty([rowNum, colNum])
        for i in range(rowNum):
            judmat_arr_empty[i] = array(newlist[i])

        RI=[0,0,0.52,0.89,1.12,1.24,1.36,1.41,1.46,1.49,1.52,1.54,1.56,1.58,1.59,1.5943] 
        colname=[]
        for i in range(rowNum):
            colname.append('w{}'.format(i+1))
        list333=['lmax','CI','CR']
        for i in list333:
            colname.append(i)
        rowname = ['Geometric Mean Method', 'Arithmetic Mean Method', 'Eigenvector Method']
        if rowNum==1:
            c = np.random.uniform(0, 0, [3, len(judmat_arr_empty) + 3])
            print(c)
            for i in range(len(c)):
                c[i,0]=1
        elif is_identity_matrix(judmat_arr_empty):
            c=np.random.uniform(0,0,[3,len(judmat_arr_empty)+3])         
        else:
            c=np.array([gm(),amm(),eig()])
        df = pd.DataFrame(c,columns=colname,index=rowname)
        print(df)
        df.to_excel(excel_writer=writer, sheet_name='Weight Coefficient{}'.format(k+1)) 
        writer.save()
        writer.close()

def construct_general_supermatrix(): 
    global num_C,A,B
    print('\n--------------------Supermatrix Calculation------------------------------\n')
    num_C= int(input('Please enter the total number of major C (factor sets):'))
    num_Cij = int(input('Please enter the total number of Cij (factors): '))
    table_ys = xlrd.open_workbook(r".\001-AHP_Result.xls", 'rb')
    sheet_ys = table_ys.sheet_names()
    sheet_num = len(sheet_ys)
    newlist = []
        for k in range(sheet_num-num_C):                        
        sheet_ys = table_ys.sheet_by_index(k+num_C)
        rowNum = sheet_ys.nrows - 3
        colNum = sheet_ys.ncols - 4
        for i in range(rowNum):
            rowi = sheet_ys.row_values(i + 3)
            for j in range(len(rowi[1:][:-3])):        
                newlist.append(rowi[1:][:-3][j])
    A = np.array(newlist).reshape(num_Cij,num_Cij).T
    print(A)
    writer = pd.ExcelWriter('002-Supermatrix-Weight_Matrix.xls') 
    A = pd.DataFrame(A)
    A.columns=range(1,len(A.columns)+1)            
    A.index=range(1,len(A.index)+1)                     
    A.to_excel(excel_writer=writer, sheet_name='Supermatrix')  
    writer.save()

    print('\n---------------------Start Weight Matrix Calculation-------------------\n')
    newlist2 = []
    for k in range(num_C):                            
        sheet_ys = table_ys.sheet_by_index(k)
        rowNum = sheet_ys.nrows - 3
        colNum = sheet_ys.ncols - 4
        for i in range(rowNum):
            rowi = sheet_ys.row_values(i + 3)
            newlist2.append(rowi[1:][:-3])
    B = np.array(newlist2).reshape(num_C,num_C).T
    print(B)
    B = pd.DataFrame(B)
    B.columns = range(1, len(B.columns) + 1) 
    B.index = range(1, len(B.index) + 1) 
    B.to_excel(excel_writer=writer, sheet_name='Weight Matrix') 
    writer.save()
    writer.close()






    def jqcjz():                         # 加权超矩阵

    print('\n-----------------开始计算加权超矩阵------------------\n')
    listCij_num = []
    #  得知超矩阵的组成
    for k in range(num_C):
        a = int(input(f'请告知您C{k+1}内的因素个数:'))
        listCij_num.append(a)
    lCs = [0]
    t=0
    for i in listCij_num:                  # 数据处理
        t = i+t
        lCs.append(t)
    # print(lCs)
    # 读取数据进行运算
    C=np.array(A)                     # array 化 A --超矩阵
    D=np.array(B)                     # array 化 B --加权矩阵
    # print(D)
    for i in range(num_C):                  # 行次数  --大C           # 矩阵一个位置扩大x倍
        for k in range(num_C):              # 列次数  --大C           # 矩阵一个位置扩大x倍
            C[lCs[i]:lCs[i+1],lCs[k]:lCs[k+1]]*=D[i,k]

    # 归一化
    C_sum = np.sum(C,axis=0)
    for i in range(len(C_sum)):
        if C_sum[i] == 0 :
            C_sum[i] = 1
    print(C_sum)
    C = C/C_sum
    print(C)
    #存储数据
    JQCJZ = pd.DataFrame(C)
    JQCJZ.columns = range(1, len(JQCJZ.columns) + 1)  # 调整列标
    JQCJZ.index = range(1, len(JQCJZ.index) + 1)  # 调整行标
    writer = pd.ExcelWriter('003-加权超矩阵.xls')  # 数据写入的表单创建
    JQCJZ.to_excel(excel_writer=writer, sheet_name='加权超矩阵')  # 把数据输出到excel
    writer.save()
    writer.close()

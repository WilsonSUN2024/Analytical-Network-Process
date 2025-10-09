# Analytical-Network-Process
This is a automated programming to calculate the relative weight of each factors
# -*- coding = utf-8 -*-
# @Software : PyCharm

import xlrd             # 导入Excel文件读取库
from numpy import random, dot, exp, array  #  从np库单独导入几个常用函数
import numpy as np
import pandas as pd    #  导入pandas库并命名为pd
import traceback     #  异常跟踪模块
import time


def AHP():
    # 判断是否为单位矩阵
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
            list1.append(list(bljz_arr_empty[i]))
        for i in range(len(list1)):
            for j in range(len(list1[i])):
                num = num * list1[i][j]
            list2.append(num ** (1 / len(list1)))
            num = 1
        if sum(list2)==0:                              #  修复分母=0
            gm_wi = list2
        else:
            gm_wi = list2 / sum(list2)                 #   修复完毕
        list2 = np.array(gm_wi).reshape(rowNum, 1)
        gm_va_pro = bljz_arr_empty @ list2
        if sum(list2)==0:                               #  修复分母=0
            gm_va= np.array([0])
        else:
            gm_va = sum(gm_va_pro / list2) / rowNum     #   修复完毕
        if rowNum==1 :                                 #  修复分母=0
            gm_CI = [0]
        else:                                          #   修复完毕
            gm_CI = (gm_va-rowNum)/(rowNum-1)
        if RI[rowNum-1]==0:
            gm_CR = [0]
        else:
            gm_CR = gm_CI/RI[rowNum-1]
        gm_list=list(gm_wi)+list(gm_va)+list(gm_CI)+list(gm_CR)
        return gm_list
    def amm():
        col_sum = np.sum(bljz_arr_empty, axis=0)  # 求列和
        a = np.sum(bljz_arr_empty / col_sum, axis=1)  # 求矩阵/列和后的行和
        asum = sum(a)  # 行总和
        amm_wi = a / asum  # 计算权重
        list2 = np.array(amm_wi).reshape(rowNum, 1)
        amm_va_pro = bljz_arr_empty @ list2  # AW
        amm_va = sum(amm_va_pro / list2) / rowNum  # λ
        if rowNum==1:                                   #  修复分母=0
            amm_CI = [0]
        else:
            amm_CI = (amm_va - rowNum) / (rowNum - 1)        #   修复完毕
        if RI[rowNum-1]==0:
            amm_CR = [0]
        else:
            amm_CR = amm_CI / RI[rowNum-1]
        amm_list=list(amm_wi)+list(amm_va)+list(amm_CI)+list(amm_CR)
        return amm_list

    def eig():
        # 特征向量法
        # 使用numpy库中的eig()函数找到矩阵的特征值和特征向量
        eigen_values, eigen_vectors = np.linalg.eig(bljz_arr_empty)
        # 找到最大特征值的索引
        max_eigen_value_index = np.argmax(eigen_values)
        # 打印最大特征值
        # print("特征向量法-最大特征值：", eigen_values[max_eigen_value_index])       # 转换float后 丢失虚数部分,后面的+0j 就是虚数
        eig_va=eigen_values[max_eigen_value_index]
        #打印最大特征向量
        # print("特征向量法-最大特征向量：",eigen_vectors[:,max_eigen_value_index])
        eig_vec=eigen_vectors[:,max_eigen_value_index]
        # print("特征向量法-权重：",eigen_vectors[:,max_eigen_value_index]/sum(eigen_vectors[:,max_eigen_value_index]))

        # print(bljz_arr_empty)
        if is_identity_matrix(bljz_arr_empty):         #  判断是否为单位矩阵,是单位矩阵就让权重都是0
            eig_wi = []
            for i in range(len(bljz_arr_empty)):
                eig_wi.append(0)
        else:                                         #  不是单位矩阵就正常计算
            eig_wi=eigen_vectors[:,max_eigen_value_index]/sum(eigen_vectors[:,max_eigen_value_index])
        print(rowNum)
        print(eig_wi)
        if rowNum ==1 :
            arr_eig_wi = np.array(eig_wi)  # 处理CI CR计算，用实际wi个数计算
            rowNum_nozero = np.count_nonzero(arr_eig_wi)
            eig_CI = 0
        else:
            arr_eig_wi = np.array(eig_wi)  # 处理CI CR计算，用实际wi个数计算
            rowNum_nozero = np.count_nonzero(arr_eig_wi)
            eig_CI = (eig_va - rowNum_nozero) / (rowNum_nozero - 1)
        if RI[rowNum_nozero-1]==0:
            eig_CR = 0
        else:
            eig_CR = eig_CI / RI[rowNum_nozero-1]                       # rownum -1 是因为 5行 ronum是5 ，但列表第五位是4（列表从0开始
        eig_list = np.array([eig_va.real,eig_CI.real,eig_CR.real])                     # 使用实数 .real  使用虚部属性 .imag
        eig_arr=np.append(eig_wi,eig_list).real
        return eig_arr

    # 显示Dateframe所有列(参数设置为None代表显示所有行，也可以自行设置数字)
    pd.set_option('display.max_columns', None)

    # 显示Dateframe所有行
    pd.set_option('display.max_rows', None)

    # 设置Dataframe数据的显示长度，默认为50
    pd.set_option('max_colwidth', 200)


    table_ys = xlrd.open_workbook(r".\ANP数据1.xls", 'rb')
    sheet_ys = table_ys.sheet_names()
    sheet_num = len(sheet_ys)
    writer = pd.ExcelWriter('001-AHP结果.xls')  # 数据写入的表单创建
    # print(sheet_num)                           #  查看表单数量
    for k in range(sheet_num):                   #  读取每一张表单
        sheet_ys = table_ys.sheet_by_index(k)
        rowNum = sheet_ys.nrows - 1
        colNum = sheet_ys.ncols - 1
        newlist = []
        for i in range(rowNum):
            rowi = sheet_ys.row_values(i+1)
            newlist.append((rowi[1:]))
        bljz_arr_empty = np.empty([rowNum, colNum])
        for i in range(rowNum):
            bljz_arr_empty[i] = array(newlist[i])

        RI=[0,0,0.52,0.89,1.12,1.24,1.36,1.41,1.46,1.49,1.52,1.54,1.56,1.58,1.59,1.5943]   # 16个RI的取值 对应不同的n值
        colname=[]
        for i in range(rowNum):
            colname.append('w{}'.format(i+1))
        list333=['lmax','CI','CR']
        for i in list333:
            colname.append(i)
        rowname = ['几何平均法', '算术平均法', '特征向量法']
        # 判断是否为单位阵
        if rowNum==1:
            c = np.random.uniform(0, 0, [3, len(bljz_arr_empty) + 3])
            print(c)
            for i in range(len(c)):
                c[i,0]=1
        elif is_identity_matrix(bljz_arr_empty):
            c=np.random.uniform(0,0,[3,len(bljz_arr_empty)+3])          #  使用 np.random.uniform(0,0,size)  输出全是0的矩阵
            # print(c)
        else:
            c=np.array([gm(),amm(),eig()])
        # print(c)
        #将c中的 Nan 替换为 0
        # c[np.isnan(c)]=0
        df = pd.DataFrame(c,columns=colname,index=rowname)
        print(df)
        # 数据写入
        df.to_excel(excel_writer=writer, sheet_name='权重系数{}'.format(k+1)) # 把数据输出到excel
        writer.save()
        writer.close()
def zcptcjz():                              #组成普通超矩阵
    global num_C,A,B
    print('\n--------------------超矩阵计算------------------------------\n')
    num_C= int(input('请输入总共的大C（因素集合）个数：'))
    num_Cij = int(input('请输入总共的Cij（因素）个数：'))
    table_ys = xlrd.open_workbook(r".\001-AHP结果.xls", 'rb')
    sheet_ys = table_ys.sheet_names()
    sheet_num = len(sheet_ys)
    newlist = []
    for k in range(sheet_num-num_C):                        #   提取数据到列表[]
        sheet_ys = table_ys.sheet_by_index(k+num_C)
        rowNum = sheet_ys.nrows - 3
        colNum = sheet_ys.ncols - 4
        for i in range(rowNum):
            rowi = sheet_ys.row_values(i + 3)
            for j in range(len(rowi[1:][:-3])):         #   拆开列表 挨个添加，这样就都在一个列表里了。
                newlist.append(rowi[1:][:-3][j])
    # print(newlist)
    # print(len(newlist))
    A = np.array(newlist).reshape(num_Cij,num_Cij).T
    print(A)
    #保存到本地
    writer = pd.ExcelWriter('002-超矩阵-权重矩阵.xls')  # 数据写入的表单创建
    # 数据写入
    A = pd.DataFrame(A)
    A.columns=range(1,len(A.columns)+1)                 #  调整列标
    A.index=range(1,len(A.index)+1)                     #  调整行标
    A.to_excel(excel_writer=writer, sheet_name='超矩阵')  # 把数据输出到excel
    writer.save()

    print('\n---------------------开始计算权重矩阵计算-------------------\n')
    newlist2 = []
    for k in range(num_C):                            #   提取数据到列表[]   权重数据
        sheet_ys = table_ys.sheet_by_index(k)
        rowNum = sheet_ys.nrows - 3
        colNum = sheet_ys.ncols - 4
        for i in range(rowNum):
            rowi = sheet_ys.row_values(i + 3)
            newlist2.append(rowi[1:][:-3])
    B = np.array(newlist2).reshape(num_C,num_C).T
    print(B)
    # 数据写入
    B = pd.DataFrame(B)
    B.columns = range(1, len(B.columns) + 1)  # 调整列标
    B.index = range(1, len(B.index) + 1)  # 调整行标
    B.to_excel(excel_writer=writer, sheet_name='权重矩阵')  # 把数据输出到excel
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

def ANPC():
    table_ys = xlrd.open_workbook(r".\003-加权超矩阵.xls", 'rb')
    sheet_ys = table_ys.sheet_names()[0]
    sheet_ys = table_ys.sheet_by_index(0)
    rowNum = sheet_ys.nrows - 1
    colNum = sheet_ys.ncols - 1
    newlist = []
    for i in range(rowNum):
        rowi = sheet_ys.row_values(i+1)
        newlist.append(rowi[1:])
    bljz_arr_empty = np.empty([rowNum, colNum])
    for i in range(rowNum):
        bljz_arr_empty[i] = array(newlist[i])
    bljz = bljz_arr_empty
    A = bljz    # 记录 bljz的一次方
    B = bljz   # 记录 bljz的一次方
    C = bljz
    i = 0
    print('\n-----------------开始计算极限超矩阵--------------------------\n')
    a,b = int(input('（本软件在计算极限矩阵时采用循环方式，当超出循环或小于精度时停止循环）请输入最大循环次数：')),\
          float(input('（本软件在计算极限矩阵时采用循环方式，当超出循环或小于精度时停止循环）请输入精度：'))
    print('输入成功：',a,b)
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
            print('循环次数：', i, "，即：第", i - 1, '次', '与第', i, '次相等')
            print('------------极限超矩阵为------------\n', A)
            break
        elif (A - B>b).any():  # 判断  A 是否与 A的n-1次方相同。   any代表 A与B  中每一个元素进行对比，元素只要有一个不同 A != B 返回True。
            B = A  # 记录 A的n-1次方。
            A = np.dot(A, C)  # 增加一次方
            max_Al2 = np.sum(A,axis=0)
            for i in range(len(max_Al2)):
                if max_Al2[i]==0:
                    max_Al2[i]==1
            A = A/max_Al2
            A[np.isnan(A)] = 0

        else:
            print('循环次数：', i, "，即：第", i - 1, '次', '与第', i, '次相等')
            print('------------极限超矩阵为------------\n', A)
            break
    A = A + 0  # 把 True/Flase 转换为 0/1
    A = np.round(A,10)
    A = pd.DataFrame(A)
    A.columns = range(1, len(A.columns) + 1)  # 调整列标
    A.index = range(1, len(A.index) + 1)  # 调整行标
    A.to_excel('004-极限超矩阵.xls',encoding='utf_8_sig')   #保存可达矩阵到本地

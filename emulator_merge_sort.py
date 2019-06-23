import pandas as pd
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense,BatchNormalization, Dropout
import time
import tensorflow as tf
import networkx as nx

# 파이썬 출력 형식 관련 옵션 설정 (빠져도 무관함)
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 10000)
pd.set_option('display.width', 10000)
pd.set_option('display.max_colwidth', -1)
np.set_printoptions(edgeitems=1000,infstr='inf',linewidth=1000, nanstr='nan', precision=1000, suppress=False, threshold=1000, formatter=None)
pd.options.mode.chained_assignment = None

# Input data 정규화를 위한 함수, 패키지를 사용해도 상관없으나, min = max 등등의 예외값 처리를 위해서 따로 함수를 생성
def min_max_normalization(data):
    data['AI_07_LOT_ESTIMATE_END_TIME'] = pd.to_datetime(data['AI_07_LOT_ESTIMATE_END_TIME'])
    data['AI_08_LPST_DATE'] = pd.to_datetime(data['AI_08_LPST_DATE'])
    data['AI_09_LOT_END_TIME'] = pd.to_datetime(data['AI_09_LOT_END_TIME'])
    data['AI_07_LOT_ESTIMATE_END_TIME'] = (data['AI_07_LOT_ESTIMATE_END_TIME'] - np.datetime64('1910-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    data['AI_08_LPST_DATE'] = (data['AI_08_LPST_DATE'] - np.datetime64('1910-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    data['AI_09_LOT_END_TIME'] = (data['AI_09_LOT_END_TIME'] - np.datetime64('1910-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    if data['AI_06_LOT_PRIORITY'].min() == data['AI_06_LOT_PRIORITY'].max():
        if data['AI_06_LOT_PRIORITY'].min() == 0:
            data['AI_06_LOT_PRIORITY'] = 0
        else:
            data['AI_06_LOT_PRIORITY'] /= data['AI_06_LOT_PRIORITY'].max()
    else:
        data['AI_06_LOT_PRIORITY'] = (data['AI_06_LOT_PRIORITY'] - data['AI_06_LOT_PRIORITY'].min()) / (data['AI_06_LOT_PRIORITY'].max() - data['AI_06_LOT_PRIORITY'].min())

    if data['AI_07_LOT_ESTIMATE_END_TIME'].min() == data['AI_07_LOT_ESTIMATE_END_TIME'].max():
        if data['AI_07_LOT_ESTIMATE_END_TIME'].min() == 0:
            data['AI_07_LOT_ESTIMATE_END_TIME'] = 0
        else:
            data['AI_07_LOT_ESTIMATE_END_TIME'] /= data['AI_07_LOT_ESTIMATE_END_TIME'].max()
    else:
        data['AI_07_LOT_ESTIMATE_END_TIME'] = (data['AI_07_LOT_ESTIMATE_END_TIME'] - data['AI_07_LOT_ESTIMATE_END_TIME'].min()) / (data['AI_07_LOT_ESTIMATE_END_TIME'].max() - data['AI_07_LOT_ESTIMATE_END_TIME'].min())

    if data['AI_08_LPST_DATE'].min() == data['AI_08_LPST_DATE'].max():
        if data['AI_08_LPST_DATE'].min() == 0:
            data['AI_08_LPST_DATE'] = 0
        else:
            data['AI_08_LPST_DATE'] /= data['AI_08_LPST_DATE'].max()
    else:
        data['AI_08_LPST_DATE'] = (data['AI_08_LPST_DATE'] - data['AI_08_LPST_DATE'].min()) / (data['AI_08_LPST_DATE'].max() - data['AI_08_LPST_DATE'].min())

    if data['AI_09_LOT_END_TIME'].min() == data['AI_09_LOT_END_TIME'].max():
        if data['AI_09_LOT_END_TIME'].min() == 0:
            data['AI_09_LOT_END_TIME'] = 0
        else:
            data['AI_09_LOT_END_TIME'] /= data['AI_09_LOT_END_TIME'].max()
    else:
        data['AI_09_LOT_END_TIME'] = (data['AI_09_LOT_END_TIME'] - data['AI_09_LOT_END_TIME'].min()) / (data['AI_09_LOT_END_TIME'].max() - data['AI_09_LOT_END_TIME'].min())
    return data

# 할당이 이 진행되는 함수
def Assigne_start():

    #할당을 진행하면서 사용할 인공신경망 생성, 가중치 불러오기
    nn_number = 128
    nn_layer = 5
    learning_rate = 0.00005
    input_shape = 7
    model = Sequential()
    model.add(Dense(nn_number, input_dim=input_shape, activation=tf.nn.leaky_relu, kernel_initializer='he_uniform', bias_initializer='zeros'))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))
    for i in range(nn_layer - 1):
        model.add(Dense(nn_number, input_dim=input_shape, activation=tf.nn.leaky_relu, kernel_initializer='he_uniform', bias_initializer='zeros'))
        model.add(BatchNormalization())
        model.add(Dropout(0.1))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss=keras.losses.binary_crossentropy, optimizer=keras.optimizers.Adam(lr=learning_rate), metrics=['accuracy'])
    model.summary()
    model.load_weights("./save_model/simul_final_" + str(nn_number) + "x" + str(nn_layer) + "_sig_20190519_2.h5")
    a = model.predict
    zeros = np.zeros(7)
    criteria = model.predict(zeros.reshape(1, 7))[0][0]

    #Machine, Mask의 영향을 안받는 (reticle flag가 전부 동일 한) 상태에서 모든 Lot을 나열하기 위한 Merge sort 알고리즘
    def merge_sort(list):
        if len(list) <= 1:
            return list
        mid = len(list) // 2
        leftList = list[:mid]
        rightList = list[mid:]
        leftList = merge_sort(leftList)
        rightList = merge_sort(rightList)
        return merge(leftList, rightList)

    #Merge sort를 위한 부분함수
    def merge(left, right):
        result = np.empty((0, 14))
        while len(left) > 0 or len(right) > 0:
            if len(left) > 0 and len(right) > 0:
                if model.predict(np.reshape((left[0][3:10] - right[0][3:10]), (1, input_shape))) >= criteria:
                    result = np.vstack((result, left[0]))
                    left = left[1:]
                else:
                    result = np.vstack((result, right[0]))
                    right = right[1:]
            elif len(left) > 0:
                result = np.vstack((result, left[0]))
                left = left[1:]
            elif len(right) > 0:
                result = np.vstack((result, right[0]))
                right = right[1:]
        return result

    #데이터 읽어오기, 정규화
    data = pd.read_excel('./PHT_EQP_LOT_ARRANGE_INFO_HIST_20190516.xlsx')
    for i in range (1,11):
        data[data['ARR_EQUIPMENT_NAME'] == i] = min_max_normalization(data[data['ARR_EQUIPMENT_NAME']==i])

    #Lot의 Reticle 순서를 제외한 순위 확인
    data_lot = data.copy()
    data_lot['AI_05_RET_EQP_LAST_RET_FLAG'] = 0
    data_lot = data_lot.drop_duplicates(subset =["LOT_ID"])
    data_lot = data_lot.drop(columns = ['ARR_EQUIPMENT_NAME','ARR_BOM_TYPE']).reset_index(drop=True)
    data_lot_index = data_lot.columns.values
    data_lot = np.array(data_lot)
    Lot_order = merge_sort(np.array(data_lot))
    Lot_order = pd.DataFrame(Lot_order,columns = data_lot_index)
    Lot_order = Lot_order['LOT_ID']

    #Machine - Lot  edge 존재유무 테이블 생성 (EDGE_EXIST_TABLE)
    LOT_ID = data['LOT_ID'].drop_duplicates().reset_index(drop=True)
    MACHINE_ID = data['ARR_EQUIPMENT_NAME'].drop_duplicates().reset_index(drop=True)
    EMPTY = np.zeros((len(LOT_ID) * len(MACHINE_ID), 3))
    EDGE_EXIST_TABLE = pd.DataFrame(EMPTY, columns=["LOT_ID", "ARR_EQUIPMENT_NAME", "VALUE"])
    G = nx.from_pandas_edgelist(data, "LOT_ID", "ARR_EQUIPMENT_NAME")
    for i in range(len(LOT_ID)):
        for j in range(len(MACHINE_ID)):
            EDGE_EXIST_TABLE.iloc[len(MACHINE_ID) * i + j, 0] = LOT_ID[i]
            EDGE_EXIST_TABLE.iloc[len(MACHINE_ID) * i + j, 1] = MACHINE_ID[j]
            EDGE_EXIST_TABLE.iloc[len(MACHINE_ID) * i + j, 2] = int(G.has_edge(LOT_ID[i], MACHINE_ID[j]))

    #LOOP IN 이전 EML LOAD 계산 및 Machine list 테이블 생성
    data = data.sort_values(['LOT_ID','ARR_BOM_TYPE']).reset_index(drop=True)
    data['LOT_MACHINE_COUNT'] = data.groupby('LOT_ID')['LOT_ID'].transform('count')
    data['REAL_TIME'] = data['ST']*data['LOT_QUANTITY']/data['LOT_MACHINE_COUNT']
    data['ASSIGNING_LOAD'] = data.groupby('ARR_EQUIPMENT_NAME')['REAL_TIME'].transform('sum')
    data['ASSIGNED_LOAD'] = data['ST']*data['LOT_QUANTITY']
    data['RESULT'] = 0
    data['LOOP'] = 0
    data.to_excel("./data.xlsx")
    machine_drop_duplicates = data.drop_duplicates(subset =["ARR_EQUIPMENT_NAME"])
    machine = machine_drop_duplicates["ARR_EQUIPMENT_NAME"].values
    eml_load = machine_drop_duplicates["ASSIGNING_LOAD"].values
    machine_list = pd.DataFrame(np.zeros((len(machine),5)), columns = ["ARR_EQUIPMENT_NAME", 'eml_load','mask',"ASSIGNING_LOAD","ASSIGNED_LOAD"])
    machine_list['ARR_EQUIPMENT_NAME'] = machine
    machine_list["ASSIGNING_LOAD"] = eml_load
    machine_list = machine_list.sort_values(["ARR_EQUIPMENT_NAME"], ascending=[True])
    machine_list["eml_load"] = machine_list['ASSIGNING_LOAD'] + machine_list['ASSIGNED_LOAD']
    data.to_excel("./input_before.xlsx")
    machine_list['mask'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    #MACHINE - LOT 데이터를 이용한 COMPETING SET 생성
    machine_lot = dict()
    for i in (machine_list['ARR_EQUIPMENT_NAME']):
        machine_lot[i] = data[data['ARR_EQUIPMENT_NAME'] == i]
        machine_lot[i] = machine_lot[i].reset_index(drop=True)

    #LOOP IN을 위한 변수 생성
    zeros = np.zeros(7)
    criteria = model.predict(zeros.reshape(1, 7))[0][0]
    TOTAL_RESULT = pd.DataFrame()
    finish_machine = pd.DataFrame()
    loop = 0

    competing_set = dict()
    new_index = ["LOT_ID","ARR_EQUIPMENT_NAME",'ARR_BOM_TYPE','AI_01_FIXED_FLAG',"AI_02_EML_LOAD",'AI_03_QTIME_WARN_OVER_FLAG','AI_04_STEPSEQ_COMMENT','AI_05_RET_EQP_LAST_RET_FLAG','AI_06_LOT_PRIORITY',"AI_07_LOT_ESTIMATE_END_TIME",'AI_08_LPST_DATE',"AI_09_LOT_END_TIME",'LOT_QUANTITY','ST','COUNT','REAL_TIME']

    #Machine, Reticle을 제외한 Lot의 우선순위 테이블과 Machine, Reticle 관련정보 결합
    for i in (machine_list['ARR_EQUIPMENT_NAME']):
        competing_set[i] = pd.merge(Lot_order,data[data['ARR_EQUIPMENT_NAME']==i],on = "LOT_ID",how = "left")
        competing_set[i]["AI_05_RET_EQP_LAST_RET_FLAG"] =  0
        competing_set[i] = competing_set[i].dropna()
        competing_set[i] = competing_set[i][new_index].reset_index(drop=True)
        print(i,"\t",competing_set[i]['REAL_TIME'].sum())

    #스케줄 시작
    SCHEDULE_TIME = 10 * 4
    while machine_list['ASSIGNED_LOAD'].min() <= 60*SCHEDULE_TIME:
        #스케줄 시간을 초과한 Machine 데이터 삭제
        finish_machine = finish_machine.append(machine_list[machine_list['ASSIGNED_LOAD']>=60*SCHEDULE_TIME])
        machine_list = machine_list[machine_list['ASSIGNED_LOAD']<=60*SCHEDULE_TIME]
        machine_list = machine_list.reset_index(drop=True)
        loop +=1
        assigned_lot = pd.DataFrame()
        #각각 Reticle별 Lot 우선순위 테이블 생성
        reticle_competing_set = dict()
        for i in (machine_list['ARR_EQUIPMENT_NAME']):
            reticle_competing_set[i] = competing_set[i]
            reticle_competing_set[i] = reticle_competing_set[i].drop_duplicates(subset =['ARR_BOM_TYPE'])
            reticle_competing_set[i]['AI_05_RET_EQP_LAST_RET_FLAG'] = (machine_list[machine_list['ARR_EQUIPMENT_NAME'] ==i]['mask'].values[0] ==reticle_competing_set[i]['ARR_BOM_TYPE'].values).astype(int)
        #Machine의 모든 Reticle 가운데 가장 좋은 LOT 선택
        for i in (machine_list['ARR_EQUIPMENT_NAME']):
            competing_lot_set = reticle_competing_set[i]
            competing_lot_set = np.array(competing_lot_set)
            total_lot = len(competing_lot_set)
            target_lot = competing_lot_set[0]
            l = 0
            if total_lot >= 2:
                for j in range(1, total_lot):
                    competing_lot = competing_lot_set[j]
                    input_data = target_lot[5:12] - competing_lot[5:12]
                    result = model.predict(np.reshape(input_data,(1,input_shape)))
                    if abs(input_data).sum() != 0:
                        if result < 0.5:
                            target_lot = competing_lot
                            l = j
                assigned_lot = assigned_lot.append(reticle_competing_set[i][l:l+1])

        #Lot이 여러개의 Machine에 할당될 수 있을 경우 EML_LOAD기준으로 할당할 Machine 선택
        assigned_lot = pd.merge(assigned_lot,machine_list, on ='ARR_EQUIPMENT_NAME')
        assigned_lot = assigned_lot.sort_values(["eml_load"], ascending=[True])
        assigned_lot = assigned_lot.drop_duplicates(['LOT_ID'], keep='first').reset_index(drop=True)
        print(machine_list)
        assigned_lot_number = len(assigned_lot)
        print(assigned_lot)

        #EML Load가 비교적 높은 Machine 가운데 할당이 이루어 질 수 있는 Machine을 선별
        #(현재 할당 대상인 Machine보다 낮은 EML Load를 가진 Machine에서 할당하려고 하는 Lot을 할당할 수 없으면 할당 진행)
        for p in reversed(range(assigned_lot_number)):
            cum_score = 0
            temp_machine = assigned_lot.iloc[p,1]
            target_machine_index = assigned_lot[assigned_lot["ARR_EQUIPMENT_NAME"]==temp_machine].index[0]
            target_machine = assigned_lot['ARR_EQUIPMENT_NAME'][:target_machine_index]
            number_of_target_machine = len(target_machine)
            for q in range(number_of_target_machine):
                LOT_ID_TEMP = assigned_lot.iloc[p,0]
                MACHINE_ID_TEMP = target_machine.iloc[q]
                cum_score += EDGE_EXIST_TABLE[(EDGE_EXIST_TABLE["LOT_ID"] ==LOT_ID_TEMP) & (EDGE_EXIST_TABLE["ARR_EQUIPMENT_NAME"] == MACHINE_ID_TEMP)]["VALUE"].values
            if cum_score > 0 :
                assigned_lot = assigned_lot.drop([p])
        assigned_lot['ASSIGNED_LOAD'] = assigned_lot['ST'] * assigned_lot['LOT_QUANTITY']

        #할당 결과 종합
        assigned_lot_ID = assigned_lot['LOT_ID'].reset_index(drop=True)
        assigned_lot_character = assigned_lot[['ARR_EQUIPMENT_NAME','ARR_BOM_TYPE', 'ASSIGNED_LOAD']]
        assigned_lot_character.columns = ['ARR_EQUIPMENT_NAME','ARR_BOM_TYPE', 'ASSIGNED_LOAD_x']
        assigned_lot['LOOP'] = loop
        TOTAL_RESULT = TOTAL_RESULT.append(assigned_lot)
        assigned_machine_list = pd.merge(machine_list,assigned_lot_character,how = "left",on = ['ARR_EQUIPMENT_NAME'])
        assigned_machine_list = assigned_machine_list.dropna()
        #새로운 LOT 할당 결과 입력 및 COLUMN 값 업데이트
        assigned_machine_list['mask'] = assigned_machine_list['ARR_BOM_TYPE']
        assigned_machine_list['ASSIGNED_LOAD'] += 10*assigned_machine_list['ASSIGNED_LOAD_x']
        assigned_machine_list = assigned_machine_list.drop(columns = ['ARR_BOM_TYPE','ASSIGNED_LOAD_x'])
        machine_list = machine_list.append(assigned_machine_list)
        machine_list = machine_list.drop_duplicates(['ARR_EQUIPMENT_NAME'], keep='last').sort_values('ARR_EQUIPMENT_NAME',ascending=True).reset_index(drop=True)
        for i in (machine_list['ARR_EQUIPMENT_NAME']):
            for j in range(len(assigned_lot_ID)):
                competing_set[i] = competing_set[i][competing_set[i].LOT_ID != assigned_lot_ID[j]]
                competing_set[i] = competing_set[i].reset_index(drop=True)
            new_assigning_load = competing_set[i]['REAL_TIME'].sum()
            machine_list['ASSIGNING_LOAD'][i-1:i] = new_assigning_load
            machine_lot[i] =machine_lot[i].reset_index(drop=True)
        machine_list['eml_load'] = machine_list['ASSIGNING_LOAD'] + machine_list['ASSIGNED_LOAD']
        machine_list = machine_list.sort_values('eml_load',ascending=True).reset_index(drop = True)

    TOTAL_RESULT = TOTAL_RESULT.sort_values(['ARR_EQUIPMENT_NAME',"LOOP"],ascending=True).reset_index(drop=True)
    finish_machine = finish_machine.sort_values(['ARR_EQUIPMENT_NAME'],ascending=True).reset_index(drop =True)
    TOTAL_RESULT.to_csv('./assigned_result.csv')
    print(TOTAL_RESULT)
    print(finish_machine)
    print(machine_list)

start_time = time.time()
Assigne_start()
print(time.time()-start_time)



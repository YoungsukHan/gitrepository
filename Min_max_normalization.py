import pandas as pd
import numpy as np
import copy

#출력옵션
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
np.set_printoptions(edgeitems=1000,infstr='inf',linewidth=1000, nanstr='nan', precision=10, suppress=False, threshold=20, formatter=None)

def data_preprocessing(d):
    #데이터 불러오기, 데이터 값 date형식으로 변경
    data = pd.read_csv('./data/20190519/JSM_InputData_20190519_T1_'+str(d)+'.csv')
    data = data.drop(columns=['ARR_EQUIPMENT_NAME','LOT_ID','AI_01_FIXED_FLAG','AI_02_EML_LOAD','AI_06_LOT_PRIORITY','AI_10_ARR_EQUIPMENT_NAME','AI_11_LOT_ID', 'AI_12_SCHED_STEPSEQ','AI_13_ARR_BOM_TYPE','ARR_BOM_TYPE','Unnamed: 0'])
    data['AI_07_LOT_ESTIMATE_END_TIME'] = pd.to_datetime(data['AI_07_LOT_ESTIMATE_END_TIME'])
    data['AI_08_LPST_DATE'] = pd.to_datetime(data['AI_08_LPST_DATE'])
    data['AI_09_LOT_END_TIME'] = pd.to_datetime(data['AI_09_LOT_END_TIME'])
    data['AI_07_LOT_ESTIMATE_END_TIME'] = (data['AI_07_LOT_ESTIMATE_END_TIME'] - np.datetime64('1910-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    data['AI_08_LPST_DATE'] = (data['AI_08_LPST_DATE'] - np.datetime64('1910-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    data['AI_09_LOT_END_TIME'] = (data['AI_09_LOT_END_TIME'] - np.datetime64('1910-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    max_schedule = int(data['SCHEDULE_SEQ'].max())
    min_schedule = int(data['SCHEDULE_SEQ'].min())
    #각각의 competing set별로 정규화를 진행
    for i in range(min_schedule,max_schedule+1):
        data2 = data[data['SCHEDULE_SEQ']==i]
        data5 = copy.deepcopy(data2)
        max_loop = int(data5['COMPETE_SEQ'].max())
        for j in range(1,max_loop+1):
            data3 = data5[data5['COMPETE_SEQ'] == j]
            data4 = copy.deepcopy(data3)
            #각각 정규화가 필요한 column 정규화
            if data4['AI_03_1_LOT_PRIORITY'].min() == data4['AI_03_1_LOT_PRIORITY'].max():
                if data4['AI_03_1_LOT_PRIORITY'].min()  ==0 :
                    data4['AI_03_1_LOT_PRIORITY'] = 0
                else:
                    data4['AI_03_1_LOT_PRIORITY'] /= data4['AI_03_1_LOT_PRIORITY'].max()
            else:
                data4['AI_03_1_LOT_PRIORITY'] = (data4['AI_03_1_LOT_PRIORITY'] - data4['AI_03_1_LOT_PRIORITY'].min()) / (data4['AI_03_1_LOT_PRIORITY'].max() - data4['AI_03_1_LOT_PRIORITY'].min())

            if data4['AI_07_LOT_ESTIMATE_END_TIME'].min() == data4['AI_07_LOT_ESTIMATE_END_TIME'].max():
                if data4['AI_07_LOT_ESTIMATE_END_TIME'].min()  ==0 :
                    data4['AI_07_LOT_ESTIMATE_END_TIME'] = 0
                else:
                    data4['AI_07_LOT_ESTIMATE_END_TIME'] /= data4['AI_07_LOT_ESTIMATE_END_TIME'].max()
            else:
                data4['AI_07_LOT_ESTIMATE_END_TIME'] = (data4['AI_07_LOT_ESTIMATE_END_TIME'] - data4['AI_07_LOT_ESTIMATE_END_TIME'].min()) / (data4['AI_07_LOT_ESTIMATE_END_TIME'].max() - data4['AI_07_LOT_ESTIMATE_END_TIME'].min())

            if data4['AI_08_LPST_DATE'].min() == data4['AI_08_LPST_DATE'].max():
                if data4['AI_08_LPST_DATE'].min()  ==0 :
                    data4['AI_08_LPST_DATE'] = 0
                else:
                    data4['AI_08_LPST_DATE'] /= data4['AI_08_LPST_DATE'].max()
            else:
                data4['AI_08_LPST_DATE'] = (data4['AI_08_LPST_DATE'] - data4['AI_08_LPST_DATE'].min()) / (data4['AI_08_LPST_DATE'].max() - data4['AI_08_LPST_DATE'].min())

            if data4['AI_09_LOT_END_TIME'].min() == data4['AI_09_LOT_END_TIME'].max():
                if data4['AI_09_LOT_END_TIME'].min()  ==0 :
                    data4['AI_09_LOT_END_TIME'] = 0
                else:
                    data4['AI_09_LOT_END_TIME'] /= data4['AI_09_LOT_END_TIME'].max()
            else:
                data4['AI_09_LOT_END_TIME'] = (data4['AI_09_LOT_END_TIME'] - data4['AI_09_LOT_END_TIME'].min()) / (data4['AI_09_LOT_END_TIME'].max() - data4['AI_09_LOT_END_TIME'].min())
            data5[data5['COMPETE_SEQ'] == j] = data4
        data[data['SCHEDULE_SEQ'] == i] = data5

    #동률이 발생했을 경우를 대비한 score function
    data['score_function'] = 10000000 * data['AI_03_QTIME_WARN_OVER_FLAG'] + 1000000 * (10 - data['AI_03_1_LOT_PRIORITY']) + 100000 * data['AI_04_STEPSEQ_COMMENT'] + 10000 * data['AI_05_RET_EQP_LAST_RET_FLAG'] + 1000 * (1 - data['AI_07_LOT_ESTIMATE_END_TIME']) + 100 * (1 - data['AI_08_LPST_DATE']) + 10 * (1 - data['AI_09_LOT_END_TIME'])
    max_schedule = int(data['SCHEDULE_SEQ'].max())
    min_schedule = int(data['SCHEDULE_SEQ'].min())
    start_lot = 0
    end_lot = 0
    #동률이 발생했을 때를 대비하여 학습에 방해가되는 할당된 Lot과 동률을 이루는 값 제거
    for i in range(min_schedule, max_schedule + 1):
        data2 = data[data['SCHEDULE_SEQ'] == i]
        data5 = copy.deepcopy(data2)
        min_loop = int(data5['COMPETE_SEQ'].min())
        max_loop = int(data5['COMPETE_SEQ'].max())
        for j in range(min_loop, max_loop + 1):
            data3 = data5[data5['COMPETE_SEQ'] == j]
            data4 = copy.deepcopy(data3)
            max_score = data4['score_function'].max()
            number_of_job =len(data4)
            end_lot += number_of_job
            for k in range(start_lot, end_lot):
                if data4['score_function'][k] == max_score and data4['RESULT'][k] != 1:
                    data4 = data4.drop([k])
            data5[data5['COMPETE_SEQ'] == j] = data4
            start_lot += number_of_job
        data[data['SCHEDULE_SEQ'] == i] = data5
    #전체 Competing set의 LOOP 순서 생성
    data = data.dropna()
    data['loop_total'] =10000000000000000* data['SCHEDULE_SEQ'] +1000000000000* data['COMPETE_SEQ']
    data['loop_rank'] = data['loop_total'].rank(method='dense')
    data = data.drop(columns = ["score_function","ASSGINED_SEQ", "LOOP_SEQ", "COMPETE_SEQ", "SCHEDULE_SEQ"])
    data = data.reset_index(drop=True)
    data = pd.DataFrame(data ,columns = ["AI_03_QTIME_WARN_OVER_FLAG", "AI_03_1_LOT_PRIORITY", "AI_04_STEPSEQ_COMMENT",'AI_05_RET_EQP_LAST_RET_FLAG', 'AI_07_LOT_ESTIMATE_END_TIME','AI_08_LPST_DATE','AI_09_LOT_END_TIME',  "RESULT","loop_rank" ])
    return data

#실제로 할당된 작업(A)와 할당되지 않은 작업(B)의 차이값으로 데이터를 변환
def data_loop_diff(d):
    #데이터 정규화 및 기준 COLUMN 생성
    data = data_preprocessing(d)
    min_group = int(data['loop_rank'].min())
    max_group = int(data['loop_rank'].max())
    start_numb = 0
    end_numb = 0
    datas = pd.DataFrame(columns = ["AI_03_QTIME_WARN_OVER_FLAG", "AI_03_1_LOT_PRIORITY", "AI_04_STEPSEQ_COMMENT",'AI_05_RET_EQP_LAST_RET_FLAG', 'AI_07_LOT_ESTIMATE_END_TIME','AI_08_LPST_DATE','AI_09_LOT_END_TIME',  "RESULT"])
    #Competing set별로 할당된작업(A)과 할당되지 않은 작업(B)의  A-B의 DATA에 대해여 Y값을 1로 라벨링,  B-A의 DATA에 대하여 Y값을 0으로 라벨링
    for i in range(min_group,max_group+1):
        data_i_group = data[data['loop_rank']==i]
        number_of_lot = len(data_i_group)
        end_numb +=number_of_lot
        assigned_job = data_i_group[data_i_group['RESULT']==1].values[0][0:8]
        data_temp = data_i_group[data_i_group['RESULT']==0]
        data_1 = data_temp.iloc[:,0:8] - assigned_job
        data_2 = assigned_job - data_temp.iloc[:,0:8]
        datas = datas.append(data_1)
        datas = datas.append(data_2)
        start_numb += number_of_lot
    datas['RESULT'].loc[(datas['RESULT']==-1)] =0
    datas = datas.reset_index(drop=True)
    datas.to_excel("./test_test.xlsx")
    return datas

data_loop_diff(1)
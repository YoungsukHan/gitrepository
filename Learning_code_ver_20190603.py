import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import keras
from keras.models import Sequential
from keras.layers import Dense,BatchNormalization, Dropout
from keras.callbacks import EarlyStopping
import time
import tensorflow as tf

#출력 관련 옵션
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
np.set_printoptions(edgeitems=1000,infstr='inf',linewidth=1000, nanstr='nan', precision=10, suppress=False, threshold=1000, formatter=None)

#신경망 size 설정
nn_number = 128
nn_layer = 5

def simul_JSM():
    #신경망 생성 및 hyper parameters 설정
    epochs = 2000
    batch_size = 10000
    input_shape = 7
    model = Sequential()
    model.add(Dense(nn_number, input_dim=input_shape, activation=tf.nn.leaky_relu,kernel_initializer='he_uniform', bias_initializer='zeros'))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))
    for i in range(nn_layer-1):
        model.add(Dense(nn_number, activation=tf.nn.leaky_relu,kernel_initializer='he_uniform', bias_initializer='zeros'))
        model.add(BatchNormalization())
        model.add(Dropout(0.1))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss=keras.losses.binary_crossentropy, optimizer='Adam', metrics=['accuracy'])
    model.summary()

    #학습 데이터 불러오기 및 학습에 알맞은 데이터로 변환
    data = pd.read_csv('./total_data_drop.csv')
    data = data.drop(columns = "Unnamed: 0")
    data = data.reset_index(drop=True)
    data = data.sample(frac=1)
    data = np.array(data)
    x_columns = input_shape
    X = data[:, :x_columns]
    Y = data[:, x_columns:x_columns + 1]
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    x_train = x_train.reshape(x_train.shape[0], x_columns)
    x_test = x_test.reshape(x_test.shape[0], x_columns)
    y_train = y_train.reshape(y_train.shape[0], 1)
    y_test = y_test.reshape(y_test.shape[0], 1)
    early_stop = EarlyStopping(monitor='val_loss', patience=5, mode='min')

    #학습 진행
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs,callbacks= [early_stop], validation_split=0.2, shuffle=True, verbose=2)
    score = model.evaluate(x_test, y_test, verbose=0)
    print(' - test_loss:', score[0], ' - test_acc:', score[1])
    model.save("./save_model/simul_final_"+str(nn_number)+"x"+str(nn_layer)+"_sig_20190519_3.h5")


#학습결과 시뮬레이션
def simul_test():
    input_shape = 7
    model = Sequential()
    model.add(Dense(nn_number, input_dim=input_shape, activation=tf.nn.leaky_relu,kernel_initializer='he_uniform', bias_initializer='zeros'))
    model.add(BatchNormalization())
    model.add(Dropout(0.1))
    for i in range(nn_layer-1):
        model.add(Dense(nn_number, activation=tf.nn.leaky_relu,kernel_initializer='he_uniform', bias_initializer='zeros'))
        model.add(BatchNormalization())
        model.add(Dropout(0.1))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss=keras.losses.binary_crossentropy, optimizer="Adam", metrics=['accuracy'])
    model.summary()
    model.load_weights("./save_model/simul_final_" + str(nn_number) + "x" + str(nn_layer) + "_sig_20190519_3.h5")
    a = model.predict
    #각각의 스케줄별로 테스트진행
    for h in range(70,105):
        print(h)
        #데이터 불러오기 및 Loop에 필요한 값 생성
        data = pd.read_csv('./tester/JSM_InputData_20190519_T1_'+str(h)+'.csv')
        data = data.drop(columns = "Unnamed: 0")
        data = data.sample(frac=1)
        data = data.sort_values(["RESULT"], ascending=[False])
        data = data.sort_values(["loop_rank"], ascending=[True])
        data = data.reset_index(drop=True)
        data['result_predict'] = 0
        max_loop = int(data['loop_rank'].max())
        min_loop = int(data['loop_rank'].min())
        data = np.array(data)
        lot_numb = 0
        zeros = np.zeros(7)
        criteria = model.predict(zeros.reshape(1,7))[0][0]
        start_time = time.time()
        #각각의 Competing set 가운데 할당할 작업 선정
        for i in range(min_loop,max_loop+1):
            competing_set = data[data[:,9]==i]
            total_lot = len(competing_set)
            target_lot = competing_set[0]
            l=0
            time_sum = 0
            for j in range(1,total_lot):
                competing_lot = competing_set[j]
                input_data = np.reshape(target_lot[0:input_shape] - competing_lot[0:input_shape],(1,input_shape))
                temp_time = time.time()
                result = model.predict(input_data)
                temp_time_2 = time.time()-temp_time
                time_sum +=temp_time_2
                #input_data = 0일경우  8번째 column (기준정보외 임의로 생성해준 정보값으로 스케줄 데이터상으로 할당된 이력이 있을경우1 아닐경우0)
                if abs(input_data).sum() == 0:
                    if competing_lot[7] == 1:
                        target_lot = competing_lot
                        l = j
                #새로운 competing_lot이 더욱 좋은 Lot일 경우 할당할 Target Lot을 변경
                else:
                    if result< criteria:
                        target_lot = competing_lot
                        l = j
            data[lot_numb + l,10] = 1
            lot_numb  += total_lot
        print(time.time() - start_time)
        #데이터 저장
        df = pd.DataFrame(data,columns = ["AI_03_QTIME_WARN_OVER_FLAG", "AI_03_1_LOT_PRIORITY", "AI_04_STEPSEQ_COMMENT",'AI_05_RET_EQP_LAST_RET_FLAG', 'AI_07_LOT_ESTIMATE_END_TIME','AI_08_LPST_DATE','AI_09_LOT_END_TIME', "AI_10_LOT_ORDER", "RESULT","loop_rank","RESULT_pred" ] )
        df.to_excel("./result/20190519_final_"+str(nn_number)+"x"+str(nn_layer)+"_"+str(h)+"_3.xlsx")

simul_JSM()
simul_test()



import numpy as np
from sklearn.model_selection import GridSearchCV, ParameterGrid
from keras.models import Sequential
from keras.layers import Dense, Dropout, advanced_activations
from keras.wrappers.scikit_learn import KerasRegressor
import pandas as pd
import random
from sklearn.preprocessing import MinMaxScaler

# 데이터 입력시 model에 적합한 dataframe 생성
def mk_model_data(file_directory, random_seed=245):
    ########### 디렉토리설정 및 원본 파일 불러오기###############
    # directory data
    # dir_rwdata = "C://Users//"

    # raw data
    rwdata = pd.read_csv(file_directory)
    # rwdata = pd.read_csv(dir_rwdata + 'original_data_0901.csv')
    # print(rwdata)


    ##################### train test spilit ################
    # test train 추출을 위한 random number 생성
    games = 2182

    random.seed(random_seed)
    ran_number = random.sample(range(1, games), k=games-1)
    type(ran_number)
    test_number = ran_number[0:int(games * 0.3)]
    train_number = ran_number[int(games * 0.3):]
    # len(train_number)

    # test , train data.frame
    train_data = rwdata[rwdata['race'].isin(train_number)]
    test_data = rwdata[rwdata['race'].isin(test_number)]
    # print(train_data)



    ############# 변수 #################
    # 모든 변수
    all_columns = list(rwdata.columns)
    # categorical 변수
    cat_variables = ['name', 'sex', 'rcDist']

    # 모델외 변수
    not_variables = ['race', 'rcDate', 'rcNo', 'hrNo', 'ona', 'ord']

    # target 변수
    # dep_variables =['OnA']
    dep_variables = ['rcTime']

    # numeric 변수
    num_variables = [x for x in all_columns if x not in not_variables]
    num_variables = [x for x in num_variables if x not in cat_variables]
    num_variables = [x for x in num_variables if x not in dep_variables]

    # model에 사용 안되는 변수
    not_in_x_variables = not_variables + dep_variables

    # print(not_in_x_variables)


    ##############Data pre-processing ####################
    # dummy 변수 생성
    def categoricalToDummies(df, varName):
        result = pd.get_dummies(df[varName], prefix=varName)
        colnames = list(result.columns)
        for j in colnames:
            df[j] = result[j]
        del df[varName]
        return df

    # Scaling numeric 변수
    # test
    scale_test_data = test_data.copy()
    scaler = MinMaxScaler()
    scaler.fit(scale_test_data[num_variables])
    scale_test_data[num_variables] = scaler.transform(scale_test_data[num_variables])

    # train
    scale_train_data = train_data.copy()
    scaler = MinMaxScaler()
    scaler.fit(scale_test_data[num_variables])
    scale_train_data[num_variables] = scaler.transform(scale_train_data[num_variables])

    # dummy variable
    # test
    for var in cat_variables:
        model_test_data = categoricalToDummies(scale_test_data.copy(), var)
    # Y = data['OnA']
    # X = data.drop('OnA', axis=1)

    Y_test = model_test_data['rcTime']
    X_test = model_test_data.drop(not_in_x_variables, axis=1)

    # train
    for var in cat_variables:
        model_train_data = categoricalToDummies(scale_train_data.copy(), var)
    # Y = data['OnA']
    # X = data.drop('OnA', axis=1)

    Y_train = model_train_data['rcTime']
    X_train = model_train_data.drop(not_in_x_variables, axis=1)

    return rwdata, train_data, test_data, scale_test_data, scale_train_data, model_test_data, model_train_data, Y_test, X_test, Y_train, X_train


def mk_model_data2(file_directory, random_seed=245):
    ########### 디렉토리설정 및 원본 파일 불러오기###############
    # directory data
    # dir_rwdata = "C://Users//"

    # raw data
    rwdata = pd.read_csv(file_directory)
    # rwdata = pd.read_csv(dir_rwdata + 'original_data_0901.csv')
    # print(rwdata)


    ##################### train test spilit ################
    # test train 추출을 위한 random number 생성
    games = 2182

    random.seed(random_seed)
    ran_number = random.sample(range(1, games), k=games-1)
    type(ran_number)
    test_number = ran_number[0:int(games * 0.3)]
    train_number = ran_number[int(games * 0.3):]
    # len(train_number)

    # test , train data.frame
    train_data = rwdata[rwdata['race'].isin(train_number)]
    test_data = rwdata[rwdata['race'].isin(test_number)]
    # print(train_data)



    ############# 변수 #################
    # 모든 변수
    all_columns = list(rwdata.columns)
    # # categorical 변수
    # cat_variables = ['name', 'sex', 'rcDist']
    #
    # # 모델외 변수
    not_variables = ['race', 'rcDate', 'rcNo', 'chulNo', 'ord']

    # target 변수
    dep_variables = ['rcTime']

    # numeric 변수
    num_variables = [x for x in all_columns if x not in not_variables]
    # num_variables = [x for x in num_variables if x not in cat_variables]
    num_variables = [x for x in num_variables if x not in dep_variables]

    # model에 사용 안되는 변수
    not_in_x_variables = not_variables + dep_variables

    # print(not_in_x_variables)


    ##############Data pre-processing ####################
    # dummy 변수 생성


    # Scaling numeric 변수
    # test
    scale_test_data = test_data.copy()
    scaler = MinMaxScaler()
    scaler.fit(scale_test_data[num_variables])
    scale_test_data[num_variables] = scaler.transform(scale_test_data[num_variables])

    # train
    scale_train_data = train_data.copy()
    scaler = MinMaxScaler()
    scaler.fit(scale_test_data[num_variables])
    scale_train_data[num_variables] = scaler.transform(scale_train_data[num_variables])

    # dummy variable
    # test
    # for var in cat_variables:
    #     model_test_data = categoricalToDummies(scale_test_data.copy(), var)
    # Y = data['OnA']
    # X = data.drop('OnA', axis=1)

    Y_test = scale_test_data['rcTime']
    X_test = scale_test_data.drop(not_in_x_variables, axis=1)

    # train
    # for var in cat_variables:
    #     model_train_data = categoricalToDummies(scale_train_data.copy(), var)
    # Y = data['OnA']
    # X = data.drop('OnA', axis=1)

    Y_train = scale_train_data['rcTime']
    X_train = scale_train_data.drop(not_in_x_variables, axis=1)

    return rwdata, train_data, test_data, scale_test_data, scale_train_data,Y_test, X_test, Y_train, X_train



# predict한 값을 1,0으로 dataframe에 추가
def making_ona(one_race_dataframe):
    top3 = one_race_dataframe.sort_values(by='rcTime').sort_values(by='ona', ascending=False)[0:3]
    top3['ona_predict'] = 1
    not_top3 = one_race_dataframe.sort_values(by='rcTime').sort_values(by='ona', ascending=False)[3:]
    not_top3['ona_predict'] = 0
    result = pd.concat([top3, not_top3], axis=0)
    #     print(top3)
    #     print(not_top3)
    return result

def making_ona2(one_race_dataframe):
    one_race_dataframe['pred_rank'] = one_race_dataframe.groupby(by='race')['pred'].rank(method = "dense",ascending=True)
    # one_race_dataframe['pred_ona'] = np.zeros(one_race_dataframe.shape[0])
    one_race_dataframe['pred_ona'] = [1 if x < 4 else 0 for x in one_race_dataframe['pred_rank']]
    #     print(top3)
    #     print(not_top3)


# Output rctime 1,0으로 convert
def labeling_ona(prd_rctime):
    prd_rctime = pd.Series(prd_rctime)
    result = []
    for i in range(0, len(prd_rctime)):
        try:
            if prd_rctime.rank(method='first')[i] < 4:
                result.append(1)
            else:
                print("ayo")
                result.append(0)
        except:
            print("vec")
            result.append(0)
    return result


# 각 race마다 predict (맞췄을 경우 1, 못 맞췄을 경우 0)
def predict_ona(race_num,  model_data):
    if list(model_data[model_data['race'] == race_num]['ord']) == list(model_data[model_data['race'] == race_num]['pred_ona']):
        return 1
    else:
        return 0

def dnn_model(activation='relu', kernel_initializer='uniform', neurons_1=30, neurons_2=10, neurons_3=3,neurons_4 = 4, dropout_rate = 0.5):

    # create model
    model = Sequential()
    model.add(Dense(neurons_1, input_dim=46, kernel_initializer=kernel_initializer, activation='selu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(neurons_2, input_dim=neurons_1, kernel_initializer=kernel_initializer, activation='selu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(neurons_3, input_dim=neurons_2, kernel_initializer=kernel_initializer, activation='selu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(neurons_4, input_dim=neurons_3, kernel_initializer=kernel_initializer, activation='selu'))
    model.add(Dropout(dropout_rate))
    model.add(Dense(1, kernel_initializer=kernel_initializer))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])

    return model

if __name__ =='__main__':
    seed = 1111

    # dropout_rate = 0.2

    np.random.seed(seed)
    rwdata, train_data, test_data, scale_test_data, scale_train_data, Y_test, X_test, Y_train, X_train= mk_model_data2("./sam_data.csv")

    param_grid = {
        'neurons_1' : [30,60],
        'neurons_2' : [20,30,40],
        'neurons_3': [7,10,15],
        'neurons_4': [3, 5],
    }

    # X_train = X_train.reset_index(drop=True)
    # Y_train = Y_train.reset_index(drop=True)
    params_list =[]
    accuracy_list = []
    for params in ParameterGrid(param_grid):

        model = KerasRegressor(build_fn=dnn_model, epochs=200, verbose=0)
        model.set_params(**params)
        model.fit(X_train.values, Y_train.values)
        pred  = model.predict(X_test.values)
        test_data["pred"] = pred
        making_ona2(test_data)
        result = []
        v_list=list(set(test_data['race'].values))
        for y in v_list:
            result.append(predict_ona(y,test_data))
        accuracy = sum(result)/len(result)*100
        print("%s with: %f" % (params, accuracy))
        params["accuracy"] = accuracy

        params_list.append(params)

    df = pd.DataFrame(params_list)
    df.to_csv("./result_set_deeper_selu_dropout.csv")

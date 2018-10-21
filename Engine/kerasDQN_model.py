import os
import datetime
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten, Concatenate, BatchNormalization 
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
from keras.losses import mean_squared_error

def buildModel():
    board_input = Input((12, 12, 2))
    action_input = Input((2,3))

    x = Conv2D(12, 2, input_shape=(12, 12, 2))(board_input)
    x = Activation("relu")(x)
    x = Conv2D(12, 2)(board_input)
    x = Activation("relu")(x)
    x = MaxPooling2D(pool_size=(2,2))(x)

    x = Conv2D(24, 3)(board_input)
    x = Activation("relu")(x)
    x = MaxPooling2D(pool_size=(2,2))(x)

    x = Flatten()(x)
    x = Dense(1024, activation="relu")(x)
    y = Flatten()(action_input)
    y = Dense(1024, activation="relu")(y)
    x = Concatenate(-1)([x, y])
    x = Dense(512, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dense(128, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dropout(2.0)(x)
    
    output = Dense(1, activation="tanh")(x)
    
    model = Model(inputs=[board_input,action_input],outputs=output)
    return model

def train(model, x_train, y_train, val_x, val_y, max_epochs):
    timestamp = datetime.datetime.now()

    cp_dir = "./checkpoint".format(timestamp)
    if not os.path.exists(cp_dir):
        os.makedirs(cp_dir)
    cp_filepath = os.path.join(cp_dir, "model_params.h5")
    cb_mc = ModelCheckpoint(filepath=cp_filepath, monitor="val_loss", period=1, save_best_only=True)

    #cb_es = EarlyStopping(monitor="val_loss", patience=patience)

    tb_log_dir = "./tensorboard/{:%Y%m%d_%H%M%S}".format(timestamp)
    cb_tb = TensorBoard(log_dir=tb_log_dir)

    model.fit(
        x=x_train,
        y=y_train,
        #epochs=max_epochs,
        verbose=2,
        validation_data=(val_x, val_y),
        callbacks=[cb_mc, cb_tb])

def Evaluate(model, img, intention): #行動の評価値を算出
    img = np.array(img).reshape(-1,12,12,2)
    intention = np.array(intention).reshape(-1,2,3)
    return model.predict([img, intention], verbose=0)
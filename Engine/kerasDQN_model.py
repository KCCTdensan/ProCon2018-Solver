import os
import datatime
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Conv2D, MaxPooling2D, Activation, Flatten
from keras.callbacks import TensorBoard, Modelcheckpoint, EarlyStopping
from keras.losses import mean_squared_error

def buildModel():
    board_input = Input(shape = [14, 14, 3])
    action_input = Input(shape = [3,2])
    x = Conv2D(14, 3)(board_input)
    x = Activation("relu")(x)
    x = Conv2D(14, 3)(board_input)
    x = Activation("relu")(x)
    x = MaxPooling2D(pool_size=(2,2))(x)

    x = Conv2D(28, 3)(board_input)
    x = Activation("relu")(x)
    x = MaxPooling2D(pool_size=(2,2))(x)

    x = Flatten()(x)
    x = Dense(1024, activation="relu")(x)
    x = Dropout(2.0)(x)
    
    output = Dense(6, activation="softmax")(x)
    
    model = Model(inputs=[board_input,action_input],outputs=output)
    return model

def train(model, x_train, y_train, val_dataflow, max_epochs, patience):
    timestamp = datetime.datetime.now()

    cp_dir = "./checkpoint/{:%Y%m%d_%H%M%S}".format(timestamp)
    if not os.path.exists(cp_dir):
        os.makedirs(cp_dir)
    cp_filepath = os.path.join(cp_dir, "model_{epoch:06d}.h5")
    cb_mc = ModelCheckpoint(filepath=cp_filepath, monitor="val_loss", period=1, save_best_only=True)

    cb_es = EarlyStopping(monitor="val_loss", patience=patience)

    tb_log_dir = "./tensorboard/{:%Y%m%d_%H%M%S}".format(timestamp)
    cb_tb = TensorBoard(log_dir=tb_log_dir)

    model.fit(
        x=x_train,
        y=y_train,
        epochs=max_epochs,
        verbose=2,
        validation_data=(val_x, val_y),
        callbacks=[cb_mc, cb_es, cb_tb])

def Evaluate(self, img, Intention): #行動の評価値を算出
    return predict([img, Intention], verbose=1)
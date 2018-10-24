import os
import datetime
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Conv2D, Activation, Flatten, Concatenate, BatchNormalization 
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
from keras.optimizers import Adam
from keras.losses import mean_squared_error

def buildModel():
    input = Input((10, 12, 12))

    x = Conv2D(12, 2, padding="same", data_format="channels_first", input_shape=(10, 12, 12))(input)
    x = Activation("relu")(x)
    x = Conv2D(12, 2, padding="same")(x)
    x = Activation("relu")(x)
    x = Conv2D(24, 3, padding="same")(x)
    x = Activation("relu")(x)
    x = Flatten()(x)

    x = Dense(1024, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dense(512, activation="relu")(x)
    x = BatchNormalization()(x)
    x = Dense(256, activation="relu")(x)
    x = BatchNormalization()(x)
    #x = Dropout(2.0)(x)

    output = Dense(81, activation="relu")(x)
    
    model = Model(inputs=input, outputs=output)
    #model.summary()
    model.compile(
            loss="categorical_crossentropy",
            optimizer=Adam(lr=0.0001),
            metrics=["accuracy"]
            )
    return model

def train(model, x_train, y_train, val_x, val_y, epochs):
    timestamp = datetime.datetime.now()

    cp_dir = "./checkpoint/{:%Y%m%d_%H%M%S}".format(timestamp)
    if not os.path.exists(cp_dir):
        os.makedirs(cp_dir)
    cp_filepath = os.path.join(cp_dir, "model_{epoch:06d}.h5")
    cb_mc = ModelCheckpoint(filepath=cp_filepath, monitor="val_loss", period=1, save_best_only=True)

    #cb_es = EarlyStopping(monitor="val_loss")

    tb_log_dir = "./tensorboard/{:%Y%m%d_%H%M%S}".format(timestamp)
    cb_tb = TensorBoard(log_dir=tb_log_dir)

    x_train = x_train.reshape(-1, 10, 12, 12).astype("float32")/16.0
    y_train = y_train.reshape(-1, 81).astype("float32")/2.0

    val_x = val_x.reshape(-1, 10, 12, 12).astype("float32")/16.0
    val_y = val_y.reshape(-1, 81).astype("float32")/2.0
    
    train_Dataflow=trainDataGenerator(x_train, y_train, 100)
    val_Dataflow=trainDataGenerator(val_x, val_y, 100)

    model.fit_generator(
        train_Dataflow,
        steps_per_epoch=1000,
        epochs=epochs,
        callbacks=[cb_mc, cb_tb],
        validation_data=val_Dataflow,
        validation_steps=100,
        shuffle=True
        )

def Evaluate(model, img): #行動の評価値を算出
    img = np.array(img).reshape(-1,10,12,12).astype("float32")/16.0
    return model.predict(img, verbose=0)

def trainDataGenerator(x_train, y_train, batch_size):
    while True:
        yield trainDataCreater(x_train, y_train, batch_size)

def trainDataCreater(x_train, y_train, batch_size):
    offsets = np.random.randint(len(x_train), size=batch_size)
    batch_x = np.stack(x_train[offset] for offset in offsets)
    batch_y = np.stack(y_train[offset] for offset in offsets)
    return batch_x, batch_y

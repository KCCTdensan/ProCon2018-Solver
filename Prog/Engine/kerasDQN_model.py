import os
import datetime
import numpy as np
from keras.models import Model
from keras.layers import Input, Dense, Dropout, Conv2D, Activation, Flatten, Concatenate, BatchNormalization 
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
from keras.optimizers import Adam
from keras.losses import mean_squared_error

def buildModel():
	input = Input(( 12, 12, 10))

	x = Conv2D(240, 3, padding="same", input_shape=(12, 12, 10))(input)
	x = BatchNormalization()(x) 
	x = Activation("relu")(x)
	x = Conv2D(240, 3, padding="same")(x)
	x = BatchNormalization()(x)
	x = Activation("relu")(x)
	x = Conv2D(240, 3, padding="same")(x)
	x = BatchNormalization()(x)
	x = Activation("relu")(x)
	x = Conv2D(240, 3, padding="same")(x)
	x = BatchNormalization()(x)
	x = Activation("relu")(x)
	x = Conv2D(240, 3, padding="same")(x)
	x = BatchNormalization()(x)
	x = Activation("relu")(x)
	x = Conv2D(240, 3, padding="same")(x)
	x = BatchNormalization()(x)
	x = Activation("relu")(x)
	x = Conv2D(240, 3, padding="same")(x)
	x = BatchNormalization()(x)
	x = Activation("relu")(x)
	x = Flatten()(x)

	x = Dense(1024, activation="relu")(x)
	x = BatchNormalization()(x)
	x = Dense(512, activation="relu")(x)
	x = BatchNormalization()(x)
	x = Dropout(0.25)(x)
	x = Dense(256, activation="relu")(x)
	x = BatchNormalization()(x)
	x = Dropout(0.5)(x)
	
	y1 = Dense(128, activation="relu")(x)
	output1 = Dense(81, activation="softmax", name="intention")(y1)
	y2 = Dense(128, activation="relu")(x)
	output2 = Dense(1, activation="sigmoid", name="Evalue")(y2)
	
	model = Model(inputs=input, outputs=[output1,output2])
	#model.summary()
	model.compile(
			loss={"intention":"categorical_crossentropy",
				"Evalue":"binary_crossentropy"},
			optimizer=Adam(),
			metrics=["accuracy"]
			)
	return model

def train(model, x_train, y_train1, y_train2, val_x, val_y1, val_y2, epochs):
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
	x_train = x_train.transpose(0,2,3,1)
	y_train1 = y_train1.reshape(-1, 81).astype("float32")
	y_train2 = y_train2.reshape(-1,1)
	val_x = val_x.reshape(-1, 10, 12, 12).astype("float32")/16.0
	val_x = val_x.transpose(0,2,3,1)
	val_y1 = val_y1.reshape(-1, 81).astype("float32")
	val_y2 = val_y2.reshape(-1,1)
	
	train_Dataflow=trainDataGenerator(x_train, y_train1, y_train2, 100)
	val_Dataflow=trainDataGenerator(val_x, val_y1, val_y2, 100)

	model.fit_generator(
		train_Dataflow,
		steps_per_epoch=1000,
		epochs=epochs,
		callbacks=[cb_mc, cb_tb],
		validation_data=val_Dataflow,
		validation_steps=100,
		)

def predict(model, img): #方策、行動の評価値を算出
	img = np.array(img).reshape(-1,10,12,12).astype("float32")/16.0
	img = img.transpose(0,2,3,1)
	return model.predict(img, verbose=0)

def trainDataGenerator(x_train, y_train1, y_train2, batch_size):
	while True:
		yield trainDataCreater(x_train, y_train1, y_train2, batch_size)

def trainDataCreater(x_train, y_train1, y_train2, batch_size):
	offsets = np.random.randint(len(x_train), size=batch_size)
	batch_x = np.stack(x_train[offset] for offset in offsets)
	batch_y1 = np.stack(y_train1[offset] for offset in offsets)
	batch_y2 = np.stack(y_train2[offset] for offset in offsets)
	batch_y11 = np.zeros((len(batch_y1),9), "float32")
	batch_y12 = np.zeros((len(batch_y1),9), "float32")
	return batch_x, [batch_y1, batch_y2]

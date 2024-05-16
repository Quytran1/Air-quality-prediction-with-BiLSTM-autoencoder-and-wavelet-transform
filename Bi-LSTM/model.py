from numpy import array
from keras.models import Sequential
from keras.layers import LSTM, Bidirectional
from keras.layers import Dense
from keras.layers import RepeatVector, Dropout
from keras.layers import TimeDistributed, BatchNormalization, Input, Attention, Concatenate
from keras.utils import plot_model
import keras

def build_lstm_autoencoder_model(input_shape):
    model = Sequential()
    model.add(Bidirectional(LSTM(units = 32,activation='relu'), input_shape=input_shape))
    model.add(RepeatVector(input_shape[1]))
    model.add(Bidirectional(LSTM(units = 32, activation='relu')))
    model.add(Dense(8, activation='softmax'))
    return model

def train_model(model, X_train, y_train, lr, epochs, batch_size):
    optimizer = keras.optimizers.Adam(learning_rate=lr)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    return model
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
import numpy as np
import os

# dimensions of our images.
img_width, img_height = 150, 150

package_directory               = os.path.dirname(os.path.abspath(__file__))
top_model_weights_path          = os.path.join(package_directory, 'output/bottleneck_fc_model.h5')
train_data_dir                  = os.path.join(package_directory, '../../../datasets/gender-data/train')
validation_data_dir             = os.path.join(package_directory, '../../../datasets/gender-data/train')
bottleneck_feature_train_dir    = os.path.join(package_directory, 'output/bottleneck_features_train.npy')
bottleneck_feature_val_dir      = os.path.join(package_directory, 'output/bottleneck_features_validation.npy')

nb_train_samples = 20
nb_validation_samples = 8
epochs = 50
batch_size = 2


def save_bottleneck_features():
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_train = model.predict_generator(
        generator, nb_train_samples // batch_size)
    np.save(bottleneck_feature_train_dir,
            bottleneck_features_train)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_validation = model.predict_generator(
        generator, nb_validation_samples // batch_size)
    np.save(bottleneck_feature_val_dir,
            bottleneck_features_validation)


def train_top_model():
    train_data = np.load(bottleneck_feature_train_dir)
    train_labels = np.array([0] * int((nb_train_samples / 2)) + [1] * int((nb_train_samples / 2)))

    validation_data = np.load(bottleneck_feature_val_dir)
    validation_labels = np.array([0] * int((nb_validation_samples / 2)) + [1] * int((nb_validation_samples / 2)))

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels))
    model.save_weights(top_model_weights_path)


save_bottleneck_features()
train_top_model()

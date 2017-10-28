from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential, Model
from keras.layers import Dropout, Flatten, Dense
from keras import applications, optimizers
import numpy as np
import os

# dimensions of our images.
img_width, img_height = 150, 150

package_directory               = os.path.dirname(os.path.abspath(__file__))
train_data_dir                  = os.path.join(package_directory, '../../../datasets/ethnicity-data/train')
validation_data_dir             = os.path.join(package_directory, '../../../datasets/ethnicity-data/val')
tuned_model_path                = os.path.join(package_directory, 'output/tuned_model.h5')

nb_train_samples = 50
nb_validation_samples = 20
epochs = 20
batch_size = 5

datagen = ImageDataGenerator(rescale=1. / 255)

# build the VGG16 network
base_model = applications.VGG16(include_top=False, weights='imagenet')

generator = datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode=None,
    shuffle=False)
bottleneck_features_train = base_model.predict_generator(
    generator, nb_train_samples // batch_size)

generator = datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode=None,
    shuffle=False)
bottleneck_features_validation = base_model.predict_generator(
    generator, nb_validation_samples // batch_size)

train_data = bottleneck_features_train
train_labels = np.array([0] * int((nb_train_samples / 2)) + [1] * int((nb_train_samples / 2)))

validation_data = bottleneck_features_validation
validation_labels = np.array([0] * int((nb_validation_samples / 2)) + [1] * int((nb_validation_samples / 2)))

base_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=(150,150,3))

top_model = Sequential()
top_model.add(Flatten(input_shape=train_data.shape[1:]))
top_model.add(Dense(256, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(1, activation='sigmoid'))

top_model.compile(optimizer='rmsprop',
              loss='binary_crossentropy', metrics=['accuracy'])

top_model.fit(train_data, train_labels,
          epochs=epochs,
          batch_size=batch_size,
          validation_data=(validation_data, validation_labels))

# add the model on top of the convolutional base
# model.add(top_model)
model = Model(inputs=base_model.input, outputs=top_model(base_model.output))

# set the first 15 layers (up to the last conv block)
# to non-trainable (weights will not be updated)
for layer in model.layers[:15]:
    layer.trainable = False

# compile the model with a SGD/momentum optimizer
# and a very slow learning rate.
model.compile(loss='binary_crossentropy',
              optimizer=optimizers.SGD(lr=1e-4, momentum=0.9),
              metrics=['accuracy'])

# prepare data augmentation configuration
train_datagen = ImageDataGenerator(
    rescale= 1./255,
    rotation_range = 40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='binary')

model.summary()

# fine-tune the model
model.fit_generator(
    train_generator,
    steps_per_epoch=nb_train_samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=nb_validation_samples // batch_size,
    verbose=2)

model.save(tuned_model_path)

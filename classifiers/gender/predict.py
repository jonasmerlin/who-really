import numpy as np
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras.utils.np_utils import to_categorical
import math
import os

package_directory       = os.path.dirname(os.path.abspath(__file__))
top_model_weights_path  = os.path.join(package_directory, 'bottleneck_fc_model.h5')
class_indices_path      = os.path.join(package_directory, 'class_indices.npy')

def classify(image_path):
    # load the class_indices saved in the earlier step
    class_dictionary = np.load(class_indices_path).item()

    num_classes = len(class_dictionary)

    print("[INFO] loading and preprocessing image...")
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)

    # important! otherwise the predictions will be '0'
    image = image / 255

    image = np.expand_dims(image, axis=0)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    # get the bottleneck prediction from the pre-trained VGG16 model
    bottleneck_prediction = model.predict(image)

    # build top model
    model = Sequential()
    model.add(Flatten(input_shape=bottleneck_prediction.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='sigmoid'))

    model.load_weights(top_model_weights_path)

    # use the bottleneck prediction on the top model to get the final
    # classification
    class_predicted = model.predict_classes(bottleneck_prediction)

    probabilities = model.predict_proba(bottleneck_prediction)

    inID = class_predicted[0]

    inv_map = {v: k for k, v in class_dictionary.items()}

    label = inv_map[inID]

    # get the prediction label
    print("Image ID: {}, Label: {}".format(inID, label))
    return label

# import keras
# from keras import applications
# from keras.preprocessing.image import ImageDataGenerator
# from keras import optimizers
# from keras.models import Sequential
# from keras.models import Model
# from keras.layers import Dropout, Flatten, Dense
# from keras.applications.vgg16 import preprocess_input
# from keras.preprocessing import image as kimage
# import numpy as np
# import os

# tuned_model_weights_path = os.path.join(os.path.dirname(__file__), 'tuned_model.h5')

# # path to the model weights files.

# # build the VGG16 network
# base_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=(150,150,3))
# print('Model loaded.')

# # build a classifier model to put on top of the convolutional model
# top_model = Sequential()
# top_model.add(Flatten(input_shape=base_model.output_shape[1:]))
# top_model.add(Dense(256, activation='relu'))
# top_model.add(Dropout(0.5))
# top_model.add(Dense(1, activation='sigmoid'))

# # add the model on top of the convolutional base
# # model.add(top_model)
# model = Model(inputs=base_model.input, outputs=top_model(base_model.output))
# # model = base_model.add(top_model)

# model.load_weights(tuned_model_weights_path)

# def classify(img_path):

# 	img = kimage.load_img(img_path, target_size=(150, 150))
# 	x = kimage.img_to_array(img)
# 	x = np.expand_dims(x, axis=0)
# 	x = preprocess_input(x)

# #	print(keras.utils.np_utils.to_categorical(model.predict(x)))
# 	return model.predict(x)


# Alternativ:

# from keras.models import load_model
# import numpy as np
# import os

# tuned_model_path = os.path.join(os.path.dirname(__file__), 'tuned_model.h5')

# model = model.load_model(tuned_model_path)

# def classify(img_path):

# 	img = kimage.load_img(img_path, target_size=(150, 150))
# 	x = kimage.img_to_array(img)
# 	x = np.expand_dims(x, axis=0)
# 	x = preprocess_input(x)

# 	return model.predict(x)
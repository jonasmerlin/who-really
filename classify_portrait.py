import classifiers
import os

def classify_portrait(portrait_path):
    predictions = {}
    for module in classifiers.modules:
        prediction = module.classify(os.path.abspath(portrait_path))
        print(prediction)
        predictions[module.__package__.replace('classifiers.', '')] = prediction
    return predictions

import classifiers
from arguments import set_up_arguments
import os

args = set_up_arguments()

def classify_portrait(portrait_path):
    predictions = {}
    for module in classifiers.modules:
        prediction = module.classify(os.path.abspath(portrait_path))
        print(prediction)
        predictions[module.__package__.replace('classifiers.', '')] = prediction
    return predictions

if __name__ == '__main__':
    classify_portrait(args.portrait)

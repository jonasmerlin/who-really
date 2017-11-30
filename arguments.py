# This module sets up the arguments and parses the arguments provided

import argparse

def set_up_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("portrait", help="the portrait you want to classify")

    return parser.parse_args()


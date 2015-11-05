__author__ = 'Sebastian.Law'

# Currently the data is pickled as a dict of the form 'SEAT': [text1, text2, ...]

import pickle
import files


def load(file_name=files.pickle_file):
    file = open(file_name, 'rb')
    data = pickle.load(file)
    return data


def dump(data, file_name=files.pickle_file):
    file = open(file_name, 'wb')
    pickle.dump(data, file)
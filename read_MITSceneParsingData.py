__author__ = 'charlie'
import numpy as np
import os
import os.path as osp
import random
from six.moves import cPickle as pickle
from tensorflow.python.platform import gfile
import glob

import TensorflowUtils as utils

# DATA_URL = 'http://sceneparsing.csail.mit.edu/data/ADEChallengeData2016.zip'
#DATA_URL = 'http://data.csail.mit.edu/places/ADEchallenge/ADEChallengeData2016.zip'


def read_dataset(data_dir):
#    pickle_filename = "MITSceneParsing.pickle"
#    pickle_filepath = os.path.join(data_dir, pickle_filename)
#    if not os.path.exists(pickle_filepath):
#        utils.maybe_download_and_extract(data_dir, DATA_URL, is_zipfile=True)
#        SceneParsing_folder = os.path.splitext(DATA_URL.split("/")[-1])[0]
#        result = create_image_lists(os.path.join(data_dir, SceneParsing_folder))
#        print ("Pickling ...")
#        with open(pickle_filepath, 'wb') as f:
#            pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)
#    else:
#        print ("Found pickle file!")

    pickle_filename = osp.basename(data_dir)+'.pickle'
    pickle_filepath = os.path.join(data_dir, pickle_filename)
    if not os.path.exists(pickle_filepath):
        result = create_image_lists(data_dir)
        print ("Pickling ...")
        with open(pickle_filepath, 'wb') as f:
            pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)
    else:
        print ("Found pickle file!")

     
    with open(pickle_filepath, 'rb') as f:
        result = pickle.load(f)
        training_records = result['training']
        validation_records = result['validation']
        del result

    return training_records, validation_records


def create_image_lists(data_dir):
    directories = ['training', 'validation']
    image_list = {}

    for directory in directories:
        file_list = []
        image_list[directory] = []
        file_glob = osp.join(data_dir, "images", directory, '*.' + 'jpg')
        file_list.extend(glob.glob(file_glob))

        if not file_list:
            print('No files found')
        else:
            for f in file_list:
                filename = osp.basename(f).replace('.jpg','')
                annotation_file = osp.join(data_dir, "annotations", directory, filename) + '.png'
                if osp.exists(annotation_file):
                    record = {'image': f, 'annotation': annotation_file, 'filename': filename}
                    image_list[directory].append(record)
                else:
                    print("Annotation file not found for %s - Skipping" % filename)

        random.shuffle(image_list[directory])
        no_of_images = len(image_list[directory])
        print ('No. of %s files: %d' % (directory, no_of_images))

    return image_list


if __name__ == '__main__':
    results=read_dataset(r'E:\work\01-Myproject\imag_division\FCN.tensorflow-master\Data_zoo\STEM')

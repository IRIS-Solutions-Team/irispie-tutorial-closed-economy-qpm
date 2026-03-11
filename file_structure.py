r"""
Files and folders
"""


import os


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILES_DIR = os.path.join(THIS_DIR, "data_files", )
PICKLE_FILES_DIR = os.path.join(THIS_DIR, "pickle_files", )

MODEL_PICKLE_FILE = os.path.join(PICKLE_FILES_DIR, "model.pkl", )
PARAMETERS_FILE = os.path.join(DATA_FILES_DIR, "parameters.json", )
FILTER_DATA_FILE = os.path.join(DATA_FILES_DIR, "filter_data.csv", )


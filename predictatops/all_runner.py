##### import from other modules
"""
The all_runner.py module of predictatops executes all the "<name>_runner.py" modules of predictatops in the following sequence:


- configurationplusfiles_runner.py = establishes configuration, input data, & output variables.
- checkdata_runner.py = finds what curves & tops are available for use in the input dataset.
- load_runner.py = loads the well curves and tops.
- split_runner.py = splits the wells into train & test portions.
- wellsKNN_runner.py = finds the nearest neighbors of each well and creates some features.
- features_runner.py = creates the rest of the features.
- balance_runner.py = throws away instances of common classes & duplicates uncommon classes.
- trainclasses_runner.py = trains the dataset using XGBoost algorithm.
- predictionclasses_runner.py = uses the trained model to predict stratigraphic tops.

The fetch_demo_data.py script is executed due to default configuration in the configurationplusfiles_runner.py module.

The plot_runner.py module, which generates plots some of the results, is not run by all_runner.py as plot.py and plot_runner.py are more for evaluation of results and not used in every run.

"""

from os import system

# system('python file.py')
from configurationplusfiles_runner import input_data_inst, config, output_data_inst

from checkdata_runner import checkdata_path_results

import load_runner

import split_runner

import wellsKNN_runner

import features_runner

import balance_runner

import trainclasses_runner

import predictionclasses_runner


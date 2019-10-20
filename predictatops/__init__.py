# -*- coding: utf-8 -*-

"""
The __init__ module doesn't contain any code, just a description of predictatops.

Predictatops is a python package for stratigraphic top prediction
-----------------------------------------------------------------

Predictatops modules are designed to be run in a sequence, one step after another.

Each step has two ways to run it.
---------------------------------

For example, there is load.py, which has all the functions to load data, and then there is load_runner.py, which leverages load.py, configuration set in the configurationplusfiles.py module, and some sensible defaults to execute the entire loading step without any more work on the user's part.

Depending on your needs, you might use write your own code that leverages load.py or you might just run load_runner.py as a executable script.

As mentioned above, Predictatops modules are run in a sequence. An example sequence is below.

- fetch_demo_data.py = fetches demo dataset for predicting top Mcmurray.
- configurationplusfiles_runner.py = establishes configuration, input data, & output variables.
- checkdata_runner.py = finds what curves & tops are available for use in the input dataset.
- load_runner.py = loads the well curves and tops.
- split_runner.py = splits the wells into train & test portions.
- wellsKNN_runner.py = finds the nearest neighbors of each well and creates some features.
- features_runner.py = creates the rest of the features.
- balance_runner.py = throws away instances of common classes & duplicates uncommon classes.
- trainclasses_runner.py = trains the dataset using XGBoost algorithm.
- predictionclasses_runner.py = uses the trained model to predict stratigraphic tops.
- plot_runner.py = plots some of the results in map form.

Running this full sequence is also packaged into the predictatops.all_runner module.

"""

__author__ = """Justin Gosses"""
__email__ = "jgosses82@gmail.com"
__version__ = "0.0.3"



print("run from __init__.py in source folder for this package")

# import fetch_demo_data
# import main
# import configurationplusfiles
# import configurationplusfiles_runner
# import checkdata
# import checkdata_runner
# import load
# import load_runner
# import split
# import split_runner
# import wellsKNN
# import wellsKNN_runner
# import features
# import features_runner
# import balance
# import balance_runner
# import trainclasses
# import trainclasses_runner
# import predictionclasses
# import predictionclasses_runner
# import plot
# import plot_runner

functions and classes
=====================

This section is partially autodocumented. You can find a link to the the completely autodocumented functions and classes page at :ref:`modindex`

Modules in rough order of use are defined below:

.. contents:: 
   :depth: 2

The __init__.py module
-----------------------
.. automodule:: predictatops.__init__
    :members:

The “main” module
----------------------------
.. automodule:: predictatops.main
    :members:

The “fetch_demo_data” module
----------------------------
.. automodule:: predictatops.fetch_demo_data
    :members:

The “all_runner” module
----------------------------
.. automodule:: predictatops.all_runner
    :members:

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

The “configurationplusfiles” module
----------------------------
.. automodule:: predictatops.configurationplusfiles
    :members:

s
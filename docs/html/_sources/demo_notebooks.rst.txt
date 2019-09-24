Demo notebooks
==============
.. _demo_notebooks-label:

These notebooks give examples of how to run different parts of predictatops's sequence of steps. 

To a large extent the notebooks either run modules with the "_runner" ending in their name that directly execute code or they mirror the code execution patterns in the "_runner" modules.

1. The notebook `Example_Every_Step_Via_HighLevel_Runner_Scripts_v1.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_Every_Step_Via_HighLevel_Runner_Scripts_v1.ipynb>`_. covers:

Running the high-level runner modules for each step one by one. This does the whole pipeline from data load, data evaluation, data processing, feature creation, model training, to prediction.

- fetch_demo_data.py

- configurationplusfiles_runner.py

- checkdata_runner.py

- load_runner.py

- split_runner.py

- wellsKNN_runner.py

- features_runner.py

- balance_runner.py

- trainclasses_runner.py

- predictionclasses_runner.py

-----------------------------------------

NOTE: The following notebooks don't use "_runner" modules. Code is imported from predictatops and more code written in the notebooks themselves expresses how and when to execute that code.


2. The notebook `Example_firstSteps_modules_fetchdata_configuration_checkdata.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_firstSteps_modules_fetchdata_configuration_checkdata.ipynb/>`_. Covers the initial data load, data evaluation, and configuration. Specifically it covers the modules:

- fetch_demo_data.py
    - Gets the data into the data folder from the demo folder in the repository.

- configurationplusfiles.py
    - Instantiates the class objects that contain information on how to run the rest of the program as it applies to input files, output files, and general configuration.

- checkdata.py
    - Helps to find out which wells have the tops and curves you need or the inverse to find out which curves you have if you want a certain number of wells in your data population.

3. This notebook TBD

- load.py
    - Loads the data from wells identified in the checkdata.py step above.

- split.py
    - Splits the data from the load.py step into train and test groups.

4. The notebook `Example_module_wellsKNN_v1.ipynb
https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_module_wellsKNN_v1.ipynb/>`_. covers:

- wellsKNN.py
    - Uses well location to identify wells next to one another up to X number of neighbors.

5. The notebook `Example_module_balance_v1.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_module_balance_v1.ipynb/>`_.  covers:

- balance.py
    - balancing the populations of classes, or labels, associated with each depth point in each well for training, so there are roughly equal number of classes.

6. The notebook `Example_module_features_and_balance.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_module_features_and_balance.ipynb/>`_. covers:

- features.py
    - creates features not already created in wellsKNN.py

- balance.py
    - balancing the populations of classes, or labels, associated with each depth point in each well for training, so there are roughly equal number of classes.

7. The notebook `Example_module_trainclasses_v2.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_module_trainclasses_v2.ipynb/>`_.  covers:

- trainclasses.py
    - training the model

8. The notebook `Example_module_predictionclasses_v1.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_module_predictionclasses_v1.ipynb/>`_.  covers:

- predictionclasses.py
    - making the top prediction

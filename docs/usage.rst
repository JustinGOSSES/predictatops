=====
Usage
=====

-------------
How to use predictatops in a project:
-------------
This uses Conda, so you might have to install that first. 

In a terminal type the following commands - 
=============
These first steps are duplicated here from the installation section:
Clone the predictatops repository first as we don't have have it PyPy yet::

    git clone https://github.com/JustinGOSSES/predictatops.git

CD into the the folder::

    cd predictatops

Create the conda environment with all the dependencies from the environment.yml at the top level folder::

    conda env create -f environment.yml

Activate that conda environment::

    source activate predictatops


Now we're into the actual usuage part.

Change directories to the predictatops source folder inside of the top-level Predictatops::

    cd predictatops

Run the script to fetch the demo data and put it in the data folder::

    Python fetch_demo_data.py 

Run the all_runner script to run all the code in one go::

    Python all_runner.py

What this runs
=============
This will run all the code using the demo dataset and default configuration, which predicts the top McMurray surface. It takes about 1.5 hours on a 2015 MacBook Pro.

Changing how it runs via configuration instructions
=============
Results should be in the results folder or whatever output folder is set as the base output folder via configurationplusfiles.py
This method of running assumes you're using all the default input, configuration, and output settings for the demo dataset. If you aren't interested in that, you'll need to change those via the configurationplusfiles.py file.


=====
More complicated ways to run
=====
    
There are three ways to run the code all the way through at three different levels of abstraction. 

(1.) You can run one python script that does everything based on configuration. This is the all_runner.py used above.

(2.) You can call each major step via a python file, examples of how to do that have _runner on the end, like load_runner.py or features_runner.py. 

(3.) You can also import functions from the python file for each step and call them from within your own code.


Running with more control or different code swapped in
=============

If you want the most control, you can import the functions in the python files for each of those major steps and call those functions within your own code. This is method 3 above. This will let you more easily swap in and out new parts and interrogate itermediate results. Notebooks below give some examples on how to do this.

Note: these jupyter notebooks are still in progress. 

Demo notebooks to examine
=============
1. The notebook `Example_firstSteps_modules_fetchdata_configuration_checkdata.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_firstSteps_modules_fetchdata_configuration_checkdata.ipynb/>`_. covers:

- fetch_demo_data.py
    - Gets the data into the data folder from the demo folder in the repository.

- configurationplusfiles.py
    - Instantiates the class objects that contain information on how to run the rest of the program as it applies to input files, output files, and general configuration.

- checkdata.py
    - Helps to find out which wells have the tops and curves you need or the inverse to find out which curves you have if you want a certain number of wells in your data population.

2. The notebook TBD

- load.py
    - Loads the data from wells identified in the checkdata.py step above.

- split.py
    - Splits the data from the load.py step into train and test groups.

3. The notebook TBD

- wellsKNN.py
    - Uses well location to identify wells next to one another up to X number of neighbors.

4. The notebook `Example_module_balance_v1.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_module_balance_v1.ipynb/>`_.  covers:

- balance.py
    - balancing the populations of classes, or labels, associated with each depth point in each well for training, so there are roughly equal number of classes.

5. The notebook `Example_module_features_and_balance.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_module_features_and_balance.ipynb/>`_. covers:

- features.py
    - creates features not already created in wellsKNN.py

- balance.py
    - balancing the populations of classes, or labels, associated with each depth point in each well for training, so there are roughly equal number of classes.

6. The notebook `Example_module_trainclasses_v2.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_module_trainclasses_v2.ipynb/>`_.  covers:

- trainclasses.py
    - training the model

7. The notebook `Example_module_predictionclasses_v1.ipynb
<https://github.com/JustinGOSSES/predictatops/blob/master/demo/Example_module_predictionclasses_v1.ipynb/>`_.  covers:

- predictionclasses.py
    - making the top prediction


=============
If you use your own dataset, some code features you might need to change
=============
This code assumes all wells to be in the same file format, LAS.

The load_all_wells_in() function in load.py does a slight transformation to the UWI names as the UWI uses / in places and - in others. Please look at this function and your datasets to figure out if it applies to your data. You may need to modify this piece of code for your own purposes.

There is an assumption that the picks text file includes a quality column. If there isn't, fake one with everything as equally quality at value of 1.
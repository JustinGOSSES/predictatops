=====
Usage
=====


Quick High-level Description of Code Project Architecture
=============

A pipeline
----------
Predictatops is a pipeline. It consists of a series of steps. 

The steps include things like fetch the demo data, load data, train, etc. 

The code for each step was written with the assumption that people, including the authors, 
would want to throw out parts and substitute in new or different code while keeping the
other code the same. It was also written with the idea that sometimes you'd want to just 
call an entire step via a single command and other times you'd want to call things incrementally
sub-step by sub-step.

Modules that hold functions vs. modules that will execute code.
--------------------------------------------------------------
If you look at the modules in Predicatops, you'll noticed there are pairs of modules where one member
of a pair has the same name but '_runner' affixed to its end, for example load.py & load_runner.py.
Load.py contains only functions and class definitions. It doesn't execute any code by itself.
load_runner.py calls functions and classes from load.py and then executes them. Any Python module
with '_runner' on the end is basically a single module you can call to run all the functions in the
module without '_runner' on the end.

Changing how the code is run via configuration or code changes
============================
    
There are three ways to run the code all the way through at three different levels of abstraction. 

(1.) You can run one python script that does everything based on configuration. This is the all_runner.py used above.

(2.) You can call each major step via a python file, examples of how to do that have _runner on the end, like load_runner.py or features_runner.py. 

(3.) You can also import functions from the python file for each step and call them from within your own code.


Running the Pipeline Using Only High-Level "_runner" Modules
------------------------------------------------------------
You can combine all the '_runner.py' modules one after another to run through the whole Predictatops
sequence quite simply. The major modules necessary to run the Predicatops pipline are listed below. 
These are called in the same sequence below in the all_runner.py module.

- *fetch_demo_data.py* = fetches demo dataset for predicting top Mcmurray.

- *configurationplusfiles_runner.py* = establishes configuration, input data, & output variables.

- *checkdata_runner.py* = finds what curves & tops are available for use in the input dataset.

- *load_runner.py* = loads the well curves and tops.

- *split_runner.py* = splits the wells into train & test portions.

- *wellsKNN_runner.py* = finds the nearest neighbors of each well and creates some features.

- *features_runner.py* = creates the rest of the features.

- *balance_runner.py* = throws away instances of common classes & duplicates uncommon classes.

- *trainclasses_runner.py* = trains the dataset using XGBoost algorithm.

- *predictionclasses_runner.py* = uses the trained model to predict stratigraphic tops.

The '_runner' modules know how to execute the modules without '_runner' based on a combination
of sensible defaults defined in the '_runner' files & choices established in the
configurationplusfiles_runner.py module.


How install predictatops and run the demo dataset straight through in shortest way possibe:
===========================================================================================
This uses Conda, so you might have to install that first. 

In a terminal type the following commands - 
---------------------------------------------
Note: These first steps are duplicated here from the installation section:
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

So what does all the code above actually do? 

This will run all the code using the demo dataset and default configuration, which predicts the top McMurray surface. It takes about 1.5 hours on a 2015 MacBook Pro.



Changing how it runs via configuration instructions
=============

You can change how the code runs without writing any code but changing the configurationplusfiles.py. 

Items that can be changed by configuration include:

- Inputs: Where data is coming in from. Information about the incoming data that might vary from one dataset to another.

- Output: where intermediate and final data is stored and how it is named.

- Configuration: Variations in how the code is run. Variations in naming conventions of well log curves. Many other variables and assumptions that predictatops uses.

You can see what all is possible to change via configuration by looking at the documentation for the configurationplusfiles.py
file in the `functions-and-classes
<functions_and_classes.html>`_. section or reading the `actual python file.
<"https://github.com/JustinGOSSES/predictatops/blob/master/predictatops/configurationplusfiles.py">`_.

Running with more control or different code swapped in
------------------------------------------------------

If you want the most control, you can import the functions in the python files for each of those major steps and call those functions within your own code. This is method 3 above. This will let you more easily swap in and out new parts and interrogate itermediate results. Notebooks below give some examples on how to do this.

Note: these jupyter notebooks are still in progress. 

`demo_notebooks_section
<demo_notebooks.html>`_.


If you use your own dataset, some code features you might need to change
========================================================================
1. This code assumes all wells to be in the same file format, LAS.

2. The load_all_wells_in() function in load.py does a slight transformation to the UWI names as the UWI uses / in places and - in others. Please look at this function and your datasets to figure out if it applies to your data. You may need to modify this piece of code for your own purposes.

3. The code has an assumption that the picks text file includes a quality column. If there isn't, fake one with everything as equally quality at value of 1.
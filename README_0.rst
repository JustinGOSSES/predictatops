==============
predictatops
==============

--------------
Code for stratigraphic pick prediction via supervised machine-learning
--------------

.. image:: Yale-Peabody-Triceratops-004Trp.png
   :width: 512pt

`MIT License
<https://github.com/JustinGOSSES/predictatops/blob/master/LICENSE/>`_.


This repository has a https://zenodo.org/record/2642860 but be aware the repository on github is ahead of the DOI'd version.

This code is the subject of an `abstract
<https://github.com/JustinGOSSES/predictatops/blob/master/AAPG_Abstract_2019ACE.md
/>`_. 

Development was in `this repo, MannvilleGroup_Strat_Hackathon
<https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon.html/>`_. but is now moving here as the code gets cleaned and modulized. This project is under active development. Significant portions of the code still only exist on MannvilleGroup_Strat_Hackathon repo at this time.


# YOU MAY WISH TO REFER TO THE README.md here -> https://github.com/JustinGOSSES/predictatops.html instead of README_0.rst for the time being as it is more complete.


[these are in progress]

.. image:: https://img.shields.io/pypi/v/predictatops.svg
        :target: https://pypi.python.org/pypi/predictatops
        :alt: PyPi Status

.. image:: https://img.shields.io/travis/JustinGOSSES/predictatops.svg
        :target: https://travis-ci.org/JustinGOSSES/predictatops
        :alt: Travis Status

.. image:: https://readthedocs.org/projects/predictatops/badge/?version=latest
        :target: https://predictatops.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/JustinGOSSES/predictatops/shield.svg
     :target: https://pyup.io/repos/github/JustinGOSSES/predictatops/
     :alt: Updates

* Documentation: https://predictatops.readthedocs.io. <- well, eventually, until then look in docs folder and readme.md



Philosophy
-------

In human-generated stratigraphic correlations there is often talk of lithostratigraphy vs. chronostratigraphy. We propose there is a weak analogy between lithostratigraphy and chronostratigraphy and different methods of computer assisted stratigraphy. 

Historically, many papers that attempted to use code to correlate well logs either assumed there was a mathematical or pattern basis for stratigraphic surfaces that can be teased out of individual logs or one could measured differences in curve patterns between neighboring wells. These workflows share some characteristics with lithostratigraphy in terms of their reliance of matching curve shapes and assumption that changes in lithology are equivelant to stratigraphy, at least at distances equal or greater than well to well distances. 

In contrast, chronostratigraphy assumes lithology can equate to facies belts that can fluctuate gradually in space over time resulting in two wells having similar lithology patterns in different time packages. Traditional chronostratigraphy relies on models of how facies belts should change in space when not otherwise constrained by biostratigraphy, chemostratigraphy, or radiometric dating. 

Instead of relying on stratigraphic models, this project proposes known picks can define spatial distribution of, and variance of, well log curve patterns that are then used to predict picks in new wells. This project attempts to focus on creating programatic features and operations that mimic the low level observations of a human geologist and progressively build into higher order clustering of patterns occuring across many wells that would have been done by a human geologist.

Datasets
-------
The default demo dataset used is a collection of over 2000 wells made public by the Alberta Geological Survey's Alberta Energy Regulator. To quote their webpage, "In 1986, Alberta Geological Survey began a project to map the McMurray Formation and the overlying Wabiskaw Member of the Clearwater Formation in the Athabasca Oil Sands Area. The data that accompany this report are one of the most significant products of the project and will hopefully facilitate future development of the oil sands." It includes well log curves as LAS files and tops in txt files and xls files. There is a word doc and a text file that describes the files and associated metadata. 

_Wynne, D.A., Attalla, M., Berezniuk, T., Brulotte, M., Cotterill, D.K., Strobl, R. and Wightman, D. (1995): Athabasca Oil Sands data McMurray/Wabiskaw oil sands deposit - electronic data; Alberta Research Council, ARC/AGS Special Report 6._

Please go to the links below for more information and the dataset:

Report for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands Deposit http://ags.aer.ca/document/OFR/OFR_1994_14.PDF

Electronic data for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands Deposit http://ags.aer.ca/publications/SPE_006.html Data is also in the repo folder: SPE_006_originalData of the original repo for this project https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/tree/master/SPE_006_originalData

In the metadata file https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/blob/master/SPE_006_originalData/Metadata/SPE_006.txt -> SPE_006.txt. the dataset is described as `Access Constraints: Public` and `Use Constraints: Credit to originator/source required. Commercial reproduction not allowed.`

_The Latitude and longitude of the wells is not in the original dataset. https://github.com/dalide -> @dalide used the Alberta Geological Society's UWI conversion tool to find lat/longs for each of the well UWIs. A CSV with the coordinates of each well's location can be found https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/blob/master/well_lat_lng.csv . These were then used to find each well's nearest neighbors.

Please note that there are a few misformed .LAS files in the full dataset, so the code in this repository skips those.

If for some reason the well data is not found at the links above, you should be able to find it https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/tree/master/SPE_006_originalData


Architecture and Abstraction
-------
Although very much a work in progress, I've tried to organize things such that the whole process doesn't have to be done at once and intermediate work can be easily saved to file and the work started at a later date. This was done running the full sequence of tasks to completion can take several hours, and I typically had less time than that to work on this project. I suspect others will have time limits as well.

This project is made up of a series of self-contained tasks done in series. The results from one task can be optionally saved to file and then reloaded into memory at a later time before starting the next task. Also, a task can be run x different ways and results saved in x different files which are then used x different times by the later steps.

In terms of how much the code is abstracted into higher level actions vs small lower level actions, I'm trying to enable two levels of abstraction. At one level, individual arguments are supplied to functions by the users who then calls those functions, potentially in a Jupyter Notebook. Many functions are called for each task. I'm also trying to enable a higher order way of working in which all arguments are configuration options set in configuration files before any code runs. This gives less visability into what is happening, but allows one to set up a bunch of different configuration variables, write a script to run all of them through to completion in the cloud, walk away, come back hours later, and evaluate what options work better for their particular datasets.  


**Code Tasks**

The code is broken into individual Tasks. 
Mandetory ones will have (m). Option ones denoted by a (o). 

- (m) [main] Main.py function. Used for some utilities leveraged across multiple steps.
- (o) [fetch_demo_data.py] The full example dataset is quite large, so it is kept in a separate folder that won't be added to PyPy (eventually this will be there maybe). Instead, we fetch it once via this script, which leverages Pooch.
- (m) [configurationplusfiles] Sets input path, configuration, and output path variables used by the Predictatops
- (o) [checkdata] Counts combinations of available tops and curves to help users figure out what wells can be used.
- (m) [load] Loads LAS files based on a well list constructed in the checkdata step.
- (m) [split] Splits the wells from load into train or test wells and assigns labels. Need to do before feature creation due to some features using neighboring wells. You don't want to use test well information when creating features for training.
- (m) [wellsKNN] Find K nearest neighbors for each well. Creates features based on neighbor relationships.
- (m) [features] Create additioal features.
- (m) [balance] Deal with imbalanced class distribution by duplicating some rows and taking out very common varieties.
- (m) [trainclasses] Machine learning 1: Model training
- (m) [predictionclasses] Go from trained model from trainclasses.py to predicted classes at each depth point.
- (o) [traintops] Secondary Machine learning 2 that takes results of class prediction and uses a secondary machine learning model to predict the top based on regression. : Inference
- (o) [predictiontops] Uses models in traintops and predict the top through regression & and a limited set of features instead of heuristic set of rules.
- (o) [plot] Map & plot results.
- (o) [uncertainty] Potential places for functions for calculating uncertainty predictions and plotting ranges.

Each task has at least one .py file with low level functions and another higher level .py file that calls those functions, often with the same name but _runner appended. 

An example is `load.py` and `load_runner.py`. 

The higher level .py file imports the results of configurationplusfiles.py to get variables for configuration, input file locations, and output saved files locations. It also calls the functions in the lower level .py file. The lower level .py files hold functions, nothing is run by them when the file is run. For example, in a command line `python3 load.py` won't do anything. `python3 load_runner.py` will execute code. 

Alternatively to using the higher level .py files, just the lower level .py files can be called and work of the _runner files done in the cells of a jupyter notebook.

I've followed this breakdown as I wanted to both train together things like configurationplusfiles_runner.py load_runner.py and split_runner.py easily while also easily ignoring them altogether as different methods are substituted. The goal was to allow code to be swapped out easily without having to keep track of much as the code is still rapidly changing while also be able to set up different trials to run in sequence. 

Folder Structures
-------
- **predictatops** = These are the source files. I.E. the actual code.
- **Data** = Where the data input goes. 
- **Demo** = I'll put some .py files and Jupyter Notebooks here that demo how to run the code.
- **Docs** = Documentation will go here, eventaully.
- **Results** = Intermediate and final results will be written by default to directories and files inside this directory as established in the output function of configurationplusfiles.py.
- **Tests** = Place to put code the runs tests.


Credits
-------
Original hackathon participants: 
`Justin Gosses
<https://github.com/JustinGOSSES/>`_.

`Licheng Zhange
<https://github.com/dalide/>`_.

`https://github.com/jazzskier<https://github.com/jazzskier/>`_.


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
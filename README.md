# StratPickSupML

A series of modules for various steps involved in a stratigraphic pick supervised machine-learning prediction.

Development was in this repo: <a href="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon">MannvilleGroup_Strat_Hackathon</a> but is now moving here as the code gets cleaned and modulized. This project is under active development. Significant portions of the code still only exist on MannvilleGroup_Strat_Hackathon repo at this time.

This code is the subject of an <a href="https://github.com/JustinGOSSES/StratPickSupML/blob/master/AAPG_Abstract_2019ACE.md">abstract</a> submitted to the AAPG ACE convention in 2019.


[![DOI](https://zenodo.org/badge/151658252.svg)](https://zenodo.org/badge/latestdoi/151658252)


Philosophy
-------

In human-generated stratigraphic correlations there is often talk of lithostratigraphy vs. chronostratigraphy. We propose there is a weak analogy between lithostratigraphy and chronostratigraphy and different methods of computer assisted stratigraphy. 

Historically, many papers that attempted to use code to correlate well logs either assumed there was a mathematical or pattern basis for stratigraphic surfaces that can be teased out of individual logs or one could measured differences in curve patterns between neighboring wells. These workflows share some characteristics with lithostratigraphy in terms of their reliance of matching curve shapes and assumption that changes in lithology are equivelant to stratigraphy, at least at distances equal or greater than well to well distances. 

In contrast, chronostratigraphy assumes lithology can equate to facies belts that can fluctuate gradually in space over time resulting in two wells having similar lithology patterns in different time packages. Traditional chronostratigraphy relies on models of how facies belts should change in space when not otherwise constrained by biostratigraphy, chemostratigraphy, or radiometric dating. 

Instead of relying on stratigraphic models, this project proposes known picks can define spatial distribution of, and variance of, well log curve patterns that are then used to predict picks in new wells. This project attempts to focus on creating programatic features and operations that mimic the low level observations of a human geologist and progressively build into higher order clustering of patterns occuring across many wells that would have been done by a human geologist.

Datasets
-------

Report for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands Deposit http://ags.aer.ca/document/OFR/OFR_1994_14.PDF

Electronic data for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands Deposit http://ags.aer.ca/publications/SPE_006.html Data is also in the repo folder: SPE_006_originalData

@dalide used the Alberta Geological Society's UWI conversion tool to find lat/longs for each of the well UWIs. These were then used to find each well's nearest neighbors as demonstrated in this notebook.


Architecture / Abstraction
-------
Although very much a work in progress, I've tried to organize things such that the whole process doesn't have to be done at once and intermediate work can be easily saved to file and the work started at a later date. This was done running an experiment to completion can take several hours, and I typically had less time than that to work on it. I suspect others will as well.

This project is made up of a series of self-contained tasks done in series. The results from one task can be optionally saved to file and then reloaded into memory at a later time before starting the next task. Also, a task can be run x different ways and results saved in x different files which are then used x different times by the later steps.

In terms of how much the code is abstracted into higher level actions vs small lower level actions, I'm trying to enable two levels of abstraction. At one level, individual arguments are supplied to functions by the users who then calls those functions, potentially in a Jupyter Notebook. Many functions are called for each task. I'm also trying to enable a higher order way of working in which all arguments are configuration options set in configuration files before any code runs. This gives less visability into what is happening, but allows one to set up a bunch of different configuration variables, write a script to run all of them through to completion in the cloud, walk away, come back hours later, and evaluate what options work better for their particular datasets.  

### Code Tasks
The code is broken into individual Tasks. 
Mandetory ones will have (m). Option ones denoted by a (o). 

(o) Figure out what wells can be used based on presence or lack of tops and well curves
(m) Load LAS files & restrict based on presence of tops and well curves
(m) Find K nearest neighbors for each well.
(m) Create features
(m) Machine learning 1: Model training
(m) Machine learning 2: Inference, modeling part 2, inference 2, and scoring
(o) Map results
(o) Evaluate results of machine-learning
(o) Explore features and alternative feature creation though UMAP and other visualizations techniques.

Each task has at least one, sometimes more than one .py file with low level functions and another higher level .py file that calls those functions. The higher level .py file refers to a configuration file, input data sources file, and output dataset file. Alternatively, the higher level .py file(s) can be replace with functions called in a notebook environment.

Status
-------
Most of the work is still in <a href="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon">the old repository</a>, but it is progressively being moved here in a simplified form.

Credits
-------

#### Contributors
<a href="https://github.com/JustinGOSSES">Justin Gosses</a>, <a href="https://github.com/dalide">Licheng Zhang</a>, <a href="https://github.com/jazzskier">jazzskier</a>



#### Key Dependencies
This package was created with <a href="https://github.com/audreyr/cookiecutter">Cookiecutter</a> and the <a href="https://github.com/audreyr/cookiecutter-pypackage">`audreyr/cookiecutter-pypackage`_</a> project template.

Libraries used for working with well logs include: <a href="https://github.com/kinverarity1/lasio">Lasio</a> & <a href="https://github.com/search?q=welly">Welly</a>.

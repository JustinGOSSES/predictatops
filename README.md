# Predictatops

<table>
<tbody>
<tr class="odd">
<td>Code for stratigraphic pick prediction via supervised machine-learning</td>
</tr>
<tr class="even">
<td><hr /></td>
</tr>
<tr class="odd">
<td><p><img src="Yale-Peabody-Triceratops-004Trp.png" alt="image" /></p></td>
</tr>
<tr class="even">
<td><blockquote>
<dl>
<dt>width</dt>
<dd><p>512pt</p>
</dd>
</dl>
</blockquote></td>
</tr>
<tr class="odd">
<td>`MIT License</td>
</tr>
<tr class="even">
<td><p>&lt;<a href="https://github.com/JustinGOSSES/predictatops/blob/master/LICENSE/" class="uri">https://github.com/JustinGOSSES/predictatops/blob/master/LICENSE/</a>&gt;`_.</p></td>
</tr>
<tr class="odd">
<td><p>This repository has a <a href="https://zenodo.org/record/2642860" class="uri">https://zenodo.org/record/2642860</a> but be aware the repository on github is ahead of the DOI'd version.</p></td>
</tr>
<tr class="even">
<td>This code is the subject of an `abstract</td>
</tr>
<tr class="odd">
<td>&lt;<a href="https://github.com/JustinGOSSES/predictatops/blob/master/AAPG_Abstract_2019ACE.md" class="uri">https://github.com/JustinGOSSES/predictatops/blob/master/AAPG_Abstract_2019ACE.md</a></td>
</tr>
<tr class="even">
<td>/&gt;_. for a talk</td>
</tr>
<tr class="odd">
<td><p>&lt;<a href="https://www.abstractsonline.com/pp8/#!/6795/presentation/3405/" class="uri">https://www.abstractsonline.com/pp8/#!/6795/presentation/3405/</a>&gt;`_. that will be given at AAPG ACE 2019.</p></td>
</tr>
<tr class="even">
<td>Development was in `this repo, MannvilleGroup_Strat_Hackathon</td>
</tr>
<tr class="odd">
<td><p>&lt;<a href="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon.html/" class="uri">https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon.html/</a>&gt;`_. but is now moving here as the code gets cleaned and modulized. This project is under active development. A few portions of the code still only exist on MannvilleGroup_Strat_Hackathon repo at this time. This is a nights and weekend side project, but will continue to be developed by the main developer.</p></td>
</tr>
<tr class="even">
<td><p>[these are in progress]</p></td>
</tr>
<tr class="odd">
<td><p><img src="https://img.shields.io/pypi/v/predictatops.svg" alt="image" /></p></td>
</tr>
<tr class="even">
<td><blockquote>
<dl>
<dt>target</dt>
<dd><p><a href="https://pypi.python.org/pypi/predictatops" class="uri">https://pypi.python.org/pypi/predictatops</a></p>
</dd>
</dl>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<dl>
<dt>alt</dt>
<dd><p>PyPi Status</p>
</dd>
</dl>
</blockquote></td>
</tr>
<tr class="even">
<td><p><img src="https://img.shields.io/travis/JustinGOSSES/predictatops.svg" alt="image" /></p></td>
</tr>
<tr class="odd">
<td><blockquote>
<dl>
<dt>target</dt>
<dd><p><a href="https://travis-ci.org/JustinGOSSES/predictatops" class="uri">https://travis-ci.org/JustinGOSSES/predictatops</a></p>
</dd>
</dl>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<dl>
<dt>alt</dt>
<dd><p>Travis Status</p>
</dd>
</dl>
</blockquote></td>
</tr>
<tr class="odd">
<td><p><img src="https://readthedocs.org/projects/predictatops/badge/?version=latest" alt="image" /></p></td>
</tr>
<tr class="even">
<td><blockquote>
<dl>
<dt>target</dt>
<dd><p><a href="https://predictatops.readthedocs.io/en/latest/?badge=latest" class="uri">https://predictatops.readthedocs.io/en/latest/?badge=latest</a></p>
</dd>
</dl>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<dl>
<dt>alt</dt>
<dd><p>Documentation Status</p>
</dd>
</dl>
</blockquote></td>
</tr>
<tr class="even">
<td><p><img src="https://pyup.io/repos/github/JustinGOSSES/predictatops/shield.svg" alt="image" /></p></td>
</tr>
<tr class="odd">
<td><blockquote>
<dl>
<dt>target</dt>
<dd><p><a href="https://pyup.io/repos/github/JustinGOSSES/predictatops/" class="uri">https://pyup.io/repos/github/JustinGOSSES/predictatops/</a></p>
</dd>
</dl>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<dl>
<dt>alt</dt>
<dd><p>Updates</p>
</dd>
</dl>
</blockquote></td>
</tr>
<tr class="odd">
<td>========</td>
</tr>
<tr class="even">
<td>Docs</td>
</tr>
<tr class="odd">
<td>========</td>
</tr>
<tr class="even">
<td>Can be found `here</td>
</tr>
<tr class="odd">
<td><p>&lt;<a href="https://justingosses.github.io/predictatops/html/index.html/" class="uri">https://justingosses.github.io/predictatops/html/index.html/</a>&gt;`_..</p></td>
</tr>
<tr class="even">
<td>==============</td>
</tr>
<tr class="odd">
<td>Philosophy</td>
</tr>
</tbody>
</table>

In human-generated stratigraphic correlations there is often talk of
lithostratigraphy vs. chronostratigraphy. We propose there is a weak
analogy between lithostratigraphy and chronostratigraphy and different
methods of computer assisted stratigraphy.

Historically, many papers that attempted to use code to correlate well
logs either assumed there was a mathematical or pattern basis for
stratigraphic surfaces that can be teased out of individual logs or one
could measured differences in curve patterns between neighboring wells.
These workflows share some characteristics with lithostratigraphy in
terms of their reliance of matching curve shapes and assumption that
changes in lithology are equivelant to stratigraphy, at least at
distances equal or greater than well to well distances.

In contrast, chronostratigraphy assumes lithology can equate to facies
belts that can fluctuate gradually in space over time resulting in two
wells having similar lithology patterns in different time packages.
Traditional chronostratigraphy relies on models of how facies belts
should change in space when not otherwise constrained by
biostratigraphy, chemostratigraphy, or radiometric dating.

Instead of relying on stratigraphic models, this project proposes known
picks can define spatial distribution of, and variance of, well log
curve patterns that are then used to predict picks in new wells. This
project attempts to focus on creating programatic features and
operations that mimic the low level observations of a human geologist
and progressively build into higher order clustering of patterns
occuring across many wells that would have been done by a human
geologist.

# Datasets

The default demo dataset used is a collection of over 2000 wells made
public by the Alberta Geological Survey's Alberta Energy Regulator. To
quote their webpage, "In 1986, Alberta Geological Survey began a project
to map the McMurray Formation and the overlying Wabiskaw Member of the
Clearwater Formation in the Athabasca Oil Sands Area. The data that
accompany this report are one of the most significant products of the
project and will hopefully facilitate future development of the oil
sands." It includes well log curves as LAS files and tops in txt files
and xls files. There is a word doc and a text file that describes the
files and associated metadata.

\_Wynne, D.A., Attalla, M., Berezniuk, T., Brulotte, M., Cotterill,
D.K., Strobl, R. and Wightman, D. (1995): Athabasca Oil Sands data
McMurray/Wabiskaw oil sands deposit - electronic data; Alberta Research
Council, ARC/AGS Special Report 6.\_

Please go to the links below for more information and the dataset:

Report for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands Deposit
<http://ags.aer.ca/document/OFR/OFR_1994_14.PDF>

Electronic data for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands
Deposit <http://ags.aer.ca/publications/SPE_006.html> Data is also in
the repo folder: SPE\_006\_originalData of the original repo for this
project
<https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/tree/master/SPE_006_originalData>

In the metadata file
<https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/blob/master/SPE_006_originalData/Metadata/SPE_006.txt>
-\> SPE\_006.txt. the dataset is described as Access Constraints: Public
and Use Constraints: Credit to originator/source required. Commercial
reproduction not allowed.

\_The Latitude and longitude of the wells is not in the original
dataset. <https://github.com/dalide> -\> @dalide used the Alberta
Geological Society's UWI conversion tool to find lat/longs for each of
the well UWIs. A CSV with the coordinates of each well's location can be
found
<https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/blob/master/well_lat_lng.csv>
. These were then used to find each well's nearest neighbors.

Please note that there are a few misformed .LAS files in the full
dataset, so the code in this repository skips those.

If for some reason the well data is not found at the links above, you
should be able to find it
<https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/tree/master/SPE_006_originalData>

<table>
<thead>
<tr class="header">
<th>Architecture and Abstraction</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Although very much a work in progress, I've tried to organize things such that the whole process doesn't have to be done at once and intermediate work can be easily saved to file and the work started at a later date. This was done running the full sequence of tasks to completion can take several hours, and I typically had less time than that to work on this project. I suspect others will have time limits as well.</p></td>
</tr>
<tr class="even">
<td><p>This project is made up of a series of self-contained tasks done in series. The results from one task can be optionally saved to file and then reloaded into memory at a later time before starting the next task. Also, a task can be run x different ways and results saved in x different files which are then used x different times by the later steps.</p></td>
</tr>
<tr class="odd">
<td><p>In terms of how much the code is abstracted into higher level actions vs small lower level actions, I'm trying to enable two levels of abstraction. At one level, individual arguments are supplied to functions by the users who then calls those functions, potentially in a Jupyter Notebook. Many functions are called for each task. I'm also trying to enable a higher order way of working in which all arguments are configuration options set in configuration files before any code runs. This gives less visability into what is happening, but allows one to set up a bunch of different configuration variables, write a script to run all of them through to completion in the cloud, walk away, come back hours later, and evaluate what options work better for their particular datasets.</p></td>
</tr>
<tr class="even">
<td><p><strong>Code Tasks</strong></p></td>
</tr>
<tr class="odd">
<td>The code is broken into individual Tasks.</td>
</tr>
<tr class="even">
<td><p>Mandetory ones will have (m). Option ones denoted by a (o).</p></td>
</tr>
<tr class="odd">
<td>- (m) [main] Main.py function. Used for some utilities leveraged across multiple steps.</td>
</tr>
<tr class="even">
<td>- (o) [fetch_demo_data.py] The full example dataset is quite large, so it is kept in a separate folder that won't be added to PyPy (eventually this will be there maybe). Instead, we fetch it once via this script, which leverages Pooch.</td>
</tr>
<tr class="odd">
<td>- (m) [configurationplusfiles] Sets input path, configuration, and output path variables used by the Predictatops</td>
</tr>
<tr class="even">
<td>- (o) [checkdata] Counts combinations of available tops and curves to help users figure out what wells can be used.</td>
</tr>
<tr class="odd">
<td>- (m) [load] Loads LAS files based on a well list constructed in the checkdata step.</td>
</tr>
<tr class="even">
<td>- (m) [split] Splits the wells from load into train or test wells and assigns labels. Need to do before feature creation due to some features using neighboring wells. You don't want to use test well information when creating features for training.</td>
</tr>
<tr class="odd">
<td>- (m) [wellsKNN] Find K nearest neighbors for each well. Creates features based on neighbor relationships.</td>
</tr>
<tr class="even">
<td>- (m) [features] Create additioal features.</td>
</tr>
<tr class="odd">
<td>- (m) [balance] Deal with imbalanced class distribution by duplicating some rows and taking out very common varieties.</td>
</tr>
<tr class="even">
<td>- (m) [trainclasses] Machine learning 1: Model training</td>
</tr>
<tr class="odd">
<td>- (m) [predictionclasses] Go from trained model from trainclasses.py to predicted classes at each depth point.</td>
</tr>
<tr class="even">
<td>- (o) [traintops] Secondary Machine learning 2 that takes results of class prediction and uses a secondary machine learning model to predict the top based on regression. : Inference</td>
</tr>
<tr class="odd">
<td>- (o) [predictiontops] Uses models in traintops and predict the top through regression &amp; and a limited set of features instead of heuristic set of rules.</td>
</tr>
<tr class="even">
<td>- (o) [plot] Map &amp; plot results.</td>
</tr>
<tr class="odd">
<td><ul>
<li><ol start="15" type="a">
<li>[uncertainty] Potential places for functions for calculating uncertainty predictions and plotting ranges.</li>
</ol></li>
</ul></td>
</tr>
<tr class="even">
<td><p>Each task has at least one .py file with low level functions and another higher level .py file that calls those functions, often with the same name but _runner appended.</p></td>
</tr>
<tr class="odd">
<td><p>An example is load.py and load_runner.py.</p></td>
</tr>
<tr class="even">
<td><p>The higher level .py file imports the results of configurationplusfiles.py to get variables for configuration, input file locations, and output saved files locations. It also calls the functions in the lower level .py file. The lower level .py files hold functions, nothing is run by them when the file is run. For example, in a command line python3 load.py won't do anything. python3 load_runner.py will execute code.</p></td>
</tr>
<tr class="odd">
<td><p>Alternatively to using the higher level .py files, just the lower level .py files can be called and work of the _runner files done in the cells of a jupyter notebook.</p></td>
</tr>
<tr class="even">
<td><p>I've followed this breakdown as I wanted to both train together things like configurationplusfiles_runner.py load_runner.py and split_runner.py easily while also easily ignoring them altogether as different methods are substituted. The goal was to allow code to be swapped out easily without having to keep track of much as the code is still rapidly changing while also be able to set up different trials to run in sequence.</p></td>
</tr>
<tr class="odd">
<td>Folder Structures</td>
</tr>
<tr class="even">
<td>-------</td>
</tr>
<tr class="odd">
<td>- <strong>predictatops</strong> = These are the source files. I.E. the actual code.</td>
</tr>
<tr class="even">
<td>- <strong>Data</strong> = Where the data input goes.</td>
</tr>
<tr class="odd">
<td>- <strong>Demo</strong> = I'll put some .py files and Jupyter Notebooks here that demo how to run the code.</td>
</tr>
<tr class="even">
<td>- <strong>Docs</strong> = Documentation will go here, eventaully.</td>
</tr>
<tr class="odd">
<td>- <strong>Results</strong> = Intermediate and final results will be written by default to directories and files inside this directory as established in the output function of configurationplusfiles.py.</td>
</tr>
<tr class="even">
<td><ul>
<li><strong>Tests</strong> = Place to put code the runs tests.</li>
</ul></td>
</tr>
<tr class="odd">
<td>==============</td>
</tr>
<tr class="even">
<td>Credits</td>
</tr>
</tbody>
</table>

Please see credits in the docs
[here](https://justingosses.github.io/predictatops/html/authors.html).

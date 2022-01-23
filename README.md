# predictatops

_Code for stratigraphic pick prediction via supervised machine-learning_


<a title="Triceratops logo based on MathKnight based on photo by Nicholas R. Longrich and Daniel J. Field [CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0)], via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:Yale-Peabody-Triceratops-004Trp.png"><img width="512" alt="Yale-Peabody-Triceratops-004Trp" src="docs/Yale-Peabody-Triceratops-004Trp.png"></a>


[![DOI](https://zenodo.org/badge/151658252.svg)](https://zenodo.org/badge/latestdoi/151658252)

<a href="https://github.com/JustinGOSSES/predictatops/blob/master/LICENSE">![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)</a>

<b>Status</b>: Runs and ready for others to try. This code project is most useful as a working proof-of-concept. It is not optimized to be used in a plug-n-play or as a dependency. Updated to v0.0.4-alpha October 26th, 2019. Updates to dependencies are done but not frequently.
<i>NOTE: Running in a standard google colab notebook may fail during model training due to memory requirements exceeding the default initial amount of RAM.</i>

#### Current best RMSE on Top McMurray surface is 6.6 meters.

Related Content
-------
The <b><a href="https://justingosses.github.io/predictatops/html/index.html">docs</a></b> provide information additional to this README.

This code is the subject of an <b><a href="https://github.com/JustinGOSSES/predictatops/blob/master/AAPG_Abstract_2019ACE.md">abstract</a></b> submitted to the AAPG ACE convention in 2019. 

The <b><a href="https://github.com/JustinGOSSES/predictatops/blob/master/docs/ACE2019_Gosses_theme8_StratigraphicTopML_201905018_submitted.pdf">slides</a></b> I presented at AAPG ACE 2019 are available in PDF form. They give an introduction to the theory and thought process behind Predictatops.

Development was in this repo: <a href="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon">MannvilleGroup_Strat_Hackathon</a> but is now moving here as the code gets cleaned and modulized. This project is under active development. A few portions of the code still only exist on MannvilleGroup_Strat_Hackathon repo at this time. This is a nights and weekend side project, but will continue to be developed by the main developer.

A more non-coder friendly description of the work can be found in <a href="http://justingosses.com/predictatops/">this</a> blog post. 

Philosophy
-------

In human-generated stratigraphic correlations there is often talk of lithostratigraphy vs. chronostratigraphy. We propose there is a weak analogy between lithostratigraphy and chronostratigraphy and the different methods of computer assisted stratigraphy. Some of the past efforts, which work very well under certain circumstances, are similar to lithostratigraphy in terms of what they accomplish. They match curve patterns between neighboring wells and rely on the assumption that changes in lithology ~ curve shapes are equivelant to stratigraphy.

Other papers attempt to use code to correlate well logs assuming there was a mathematical or pattern basis for stratigraphic surfaces that can be teased out of individual logs. Although there are recent papers that seem to do better with this type of approach, no code was released, the earlier ones seem to have problems that at least in part were related to their assumption that stratigraphic changes had similar expression across large spatial areas.

In contrast to lithostratigraphy, chronostratigraphy assumes lithology equates to facies belts that can fluctuate gradually in space over time, and are not correlated with time. Two wells with similar lithology patterns can be in different time packages. Traditional chronostratigraphy relies on models of how facies belts should change in space when not otherwise constrained by biostratigraphy, chemostratigraphy, or radiometric dating. 

Instead of relying on stratigraphic models, this project proposes known picks can define spatial distribution of, and variance of, well log curve patterns that are then used to predict picks in new wells. This project attempts to focus on creating programatic features and operations that mimic the low level observations of a human geologist and progressively build into higher order clustering of patterns occuring across many wells that would have been done by a human geologist.

Datasets
-------
The default demo dataset used is a collection of over 2000 wells made public by the Alberta Geological Survey's Alberta Energy Regulator. To quote their webpage, "In 1986, Alberta Geological Survey began a project to map the McMurray Formation and the overlying Wabiskaw Member of the Clearwater Formation in the Athabasca Oil Sands Area. The data that accompany this report are one of the most significant products of the project and will hopefully facilitate future development of the oil sands." It includes well log curves as LAS files and tops in txt files and xls files. There is a word doc and a text file that describes the files and associated metadata. 

_Wynne, D.A., Attalla, M., Berezniuk, T., Brulotte, M., Cotterill, D.K., Strobl, R. and Wightman, D. (1995): Athabasca Oil Sands data McMurray/Wabiskaw oil sands deposit - electronic data; Alberta Research Council, ARC/AGS Special Report 6._

Please go to the links below for more information and the dataset:

Report for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands Deposit http://ags.aer.ca/document/OFR/OFR_1994_14.PDF

Electronic data for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands Deposit http://ags.aer.ca/publications/SPE_006.html Data is also in the repo folder: SPE_006_originalData of the original repo for this project <a href="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/tree/master/SPE_006_originalData">here.</a>

In the metadata file <a href="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/blob/master/SPE_006_originalData/Metadata/SPE_006.txt">SPE_006.txt</a> the dataset is described as `Access Constraints: Public` and `Use Constraints: Credit to originator/source required. Commercial reproduction not allowed.`

_The Latitude and longitude of the wells is not in the original dataset._ <a href="https://github.com/dalide">@dalide<a> used the Alberta Geological Society's UWI conversion tool to find lat/longs for each of the well UWIs. A CSV with the coordinates of each well's location can be found <a href="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/blob/master/well_lat_lng.csv">here.</a> These were then used to find each well's nearest neighbors.

Please note that there are a few misformed .LAS files in the full dataset, so the code in this repository skips those.

If for some reason the well data is not found at the links above, you should be able to find it <a href="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/tree/master/SPE_006_originalData">here.</a>


Architecture and Abstraction
-------
PLEASE REFER TO THE SECTION <a href="https://justingosses.github.io/predictatops/html/readme.html#architecture-and-abstraction">Architecture and Abstraction</a> in the DOCs. Information is provided on code architecture, tasks, and folder organization.


GettingStarted
-------
See the <a href="https://justingosses.github.io/predictatops/html/usage.html">Usage</a> and the <a href="https://justingosses.github.io/predictatops/html/installation.html">Installation</a> sections of the docs.


Credits
-------
There's a theme here. Check the <a href="https://justingosses.github.io/predictatops/html/authors.html">docs</a>.

______________________________
## Status

The root mean squared error for the Top McMurray surface is down to ~7 meters (with a handful of wells identified as too difficult to predict, -8% depending on settings). 

#### Distribution of Absolute Error in Test Portion of Dataset for Top McMurray Surface in Meters. 
Y-axis is number of picks in each bin, and X-axis is distance predicted pick is off from human-generated pick.
<img src="docs/images/Histogram_Error_predictatops_6.6_vA.png"
     alt="image of current_errors_TopMcMr_20190517"
     style="float: left; margin-right: 25px;" />

Current algorithm used is XGBoost.

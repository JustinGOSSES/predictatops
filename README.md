# StratPickSupML

A series of modules for various steps involved in a stratigraphic pick supervised machine-learning prediction.

Development was in this repo: <a href="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon">MannvilleGroup_Strat_Hackathon</a> but is now moving here as the code gets cleaned and modulized. This project is under active development. Significant portions of the code still only exist on MannvilleGroup_Strat_Hackathon repo at this time.

This code is the subject of an <a href="https://github.com/JustinGOSSES/StratPickSupML/blob/master/AAPG_Abstract_2019ACE.md">abstract</a> submitted to the AAPG ACE convention in 2019.


[![DOI](https://zenodo.org/badge/151658252.svg)](https://zenodo.org/badge/latestdoi/151658252)


Philosophy
-------

In human-generated stratigraphic correlations there is often talk of lithostratigraphy vs. chronostratigraphy. We propose there is a weak analogy between lithostratigraphy and chronostratigraphy and different methods of computer assisted stratigraphy. 

Historically, many papers that attempted to use code to correlate well logs either assumed there was a mathematical or pattern basis for stratigraphic surfaces that can be teased out of individual logs or one could measured differences in curve patterns between neighboring wells. These workflows share some characteristics with lithostratigraphy in terms of their reliance of matching curve shapes and assumption that changes in lithology are equivelant to stratigraphy, at least at distances equal or greater than well to well distances. 

In contrast, chronostratigraphy assumes lithology can equate to facies belts that can fluctuate gradually in space over time resulting in two wells having similar lithology patterns in different time packages. Traditional chronostratigraphy relies on models of how facies belts should change in space when not otherwise constrained by biostratigraphy, chemostratigraphy, or radiometric dating. Instead of relying on stratigraphic models, this project proposes known picks can define spatial distribution of, and variance of, well log curve patterns that are then used to predict picks in new wells. This project attempts to focus on creating programatic features and operations that mimic the low level observations of a human geologist and progressively build into higher order clustering of patterns occuring across many wells that would have been done by a human geologist.

Datasets
-------

Report for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands Deposit http://ags.aer.ca/document/OFR/OFR_1994_14.PDF

Electronic data for Athabasca Oil Sands Data McMurray/Wabiskaw Oil Sands Deposit http://ags.aer.ca/publications/SPE_006.html Data is also in the repo folder: SPE_006_originalData

@dalide used the Alberta Geological Society's UWI conversion tool to find lat/longs for each of the well UWIs. These were then used to find each well's nearest neighbors as demonstrated in this notebook.

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

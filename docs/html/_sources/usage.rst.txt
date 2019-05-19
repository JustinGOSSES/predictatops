=====
Usage
=====

-------------
How to use predictatops in a project:
-------------
This uses Conda, so you might have to install that first. 

In a terminal type the following commands - 
=============

Clone the predictatops repository first as we don't have have it PyPy yet::

    git clone https://github.com/JustinGOSSES/predictatops.git

CD into the the folder::

    cd predictatops

Create the conda environment with all the dependencies from the environment.yml at the top level folder::

    conda env create -f environment.yml

Activate that conda environment::

    source activate predictatops

Change directories to the predictatops source folder inside of the top-level Predictatops::

    cd predictatops

Run the script to fetch the demo data and put it in the data folder::

    Python fetch_demo_data.py 

Run the all_runner script to run all the code in one go::

    Python all_runner.py

What this runs
=============
This will run all the code using the demo dataset and default configuration, which predicts the top McMurray surface. It takes about an hour on a 2015 MacBook Pro.


Changing how it runs
=============
Results should be in the results folder or whatever output folder is set as the base output folder via configurationplusfiles.py
This method of running assumes you're using all the default input, configuration, and output settings for the demo dataset. If you aren't interested in that, you'll need to change those via the configurationplusfiles.py file.
    
Running with more control or different code swapped in
=============
There will be jupyter notebooks showing other examples of how to run Predictatops in the demo directory, at some point soon. In addition to running the code in one go, you can also run it by major steps like (check data, load, split, etc.) or use the functions base directly and call every function with your own code. This lets you more earily swap in and out new parts and interrogate itermedia results. I'll include some examples of that soon as well. 


Code features that might require changing for different datasets
=============
Requires all wells to be in the same file format, LAS.

The load_all_wells_in() function in load.py does a slight transformation to the UWI names as the UWI uses / in places and - in others. Please look at this function and your datasets to figure out if it applies to your data. You may need to modify this piece of code for your own purposes.

There is an assumption that the picks text file includes a quality column. If there isn't, fake one with everything as equally quality at value of
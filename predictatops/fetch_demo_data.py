# -*- coding: utf-8 -*-

##### import statements #####

"""
Module mypackage/datasets.py
"""
import pooch

# Get the version string from your project. You have one of these, right?
#from . import version


# Create a new friend to manage your sample data storage
GOODBOY = pooch.create(
    # Folder where the data will be stored. For a sensible default, use the default
    # cache folder for your OS.
    #path=pooch.os_cache("mypackage_test"),
    #path=pooch.os_cache("mypackage_test"),
    path="../data/",
    # Base URL of the remote data store. Will call .format on this string to insert
    # the version (see below).  https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/tree/master/SPE_006_originalData
    base_url="https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/raw/{version}/SPE_006_originalData/",
    # Pooches are versioned so that you can use multiple versions of a package
    # simultaneously. Use PEP440 compliant version number. The version will be
    # appended to the path.
    version='0.0.1',
    # If a version as a "+XX.XXXXX" suffix, we'll assume that this is a dev version
    # and replace the version with this string.
    version_dev="master",
    # An environment variable that overwrites the path.
    env="../data",
    # The cache file registry. A dictionary with all files managed by this pooch.
    # Keys are the file names (relative to *base_url*) and values are their
    # respective SHA256 hashes. Files will be downloaded automatically when needed
    # (see fetch_gravity_data). 1414057d0c5235b0ed13103c72c864ddfd34a0c8
    # https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/tree/85c39ac7c27c28e4b6df776e23b69afbecd30443/SPE_006_originalData
    registry={"OilSandsDB/WELLS.xls": "2520ace4bdab0762b4d587760f684bc5223fe3b759f98eee6af59a4442450144"}
    #registry={"SPE_006_originalData": "83f3be338d6fa42eeadf60466c716e4370fe8723682c187d214a054bd695880a"}
)
# You can also load the registry from a file. Each line contains a file name and
# it's sha256 hash separated by a space. This makes it easier to manage large
# numbers of data files. The registry file should be in the same directory as this
# module.

#GOODBOY.load_registry("registry.txt")


# Define functions that your users can call to get back some sample data in memory
def fetch_gravity_data():
    """
    Load some sample gravity data to use in your docs.
    """
    # Fetch the path to a file in the local storae. If it's not there, we'll
    # download it.
    fname = GOODBOY.fetch("OilSandsDB/WELLS.xls")
    # Load it with numpy/pandas/etc
    data = ...
    return data

fetch_gravity_data()
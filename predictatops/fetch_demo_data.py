##coding: utf-8 -*-

"""
   The fetch_data_data.py script is used to fetch the demo data using the pooch data fetching library. This is the only module that executes on being run but doesn't has a "_runner" ending to its name.
   
   Alternatively, you can use your own data in a top-level "data" directory and skip using this script entirely.

   The script imports pooch, then fetches the demo dataset from: "https://github.com/JustinGOSSES/predictatops/raw/{version}/demo/mannville_demo_data/".
   That link is defined in the registry.txt file. Pooch is used to create a GOODBYE object instance, which then exectures the fetching using the fetch_mannville_data() function in this python file.

   NOTE: This was changed since version 1 to pull in a single zip file and unzip it as that's faster than pulling in each file unzipped individually!
"""


##### import statements #####
import pooch
import os
from zipfile import ZipFile

# Get the version string from your project. You have one of these, right?
# from . import version

data_path = "../data/Mannville_input_data/"

# Create a new friend to manage your sample data storage
GOODBOY = pooch.create(
    # Folder where the data will be stored. For a sensible default, use the default
    # cache folder for your OS.
    # path=pooch.os_cache("mypackage_test"),
    # path=pooch.os_cache("mypackage_test"),
    path=data_path,
    # Base URL of the remote data store. Will call .format on this string to insert
    # https://github.com/JustinGOSSES/predictatops/
    # the version (see below).  https://github.com/JustinGOSSES/MannvilleGroup_Strat_Hackathon/tree/master/SPE_006_originalData
    #base_url="https://github.com/JustinGOSSES/predictatops/raw/{version}/demo/mannville_demo_data/",
    base_url="https://github.com/JustinGOSSES/predictatops/raw/{version}/demo/",
    # Pooches are versioned so that you can use multiple versions of a package
    # simultaneously. Use PEP440 compliant version number. The version will be
    # appended to the path.
    #version="v0.0.0-alpha",
    version="v0.0.3-alpha",
    # If a version as a "+XX.XXXXX" suffix, we'll assume that this is a dev version
    # and replace the version with this string.
    version_dev="master",
    # An environment variable that overwrites the path.
    env=data_path,
    # The cache file registry. A dictionary with all files managed by this pooch.
    # Keys are the file names (relative to *base_url*) and values are their
    # respective SHA256 hashes. Files will be downloaded automatically when needed
    # (see fetch_gravity_data).  1414057d0c5235b0ed13103c72c864ddfd34a0c8
    # registry={"OilSandsDB/LITHOLOGY_DIC.TXT": "83f3be338d6fa42eeadf60466c716e4370fe8723682c187d214a054bd695880a"}
)
# You can also load the registry from a file. Each line contains a file name and
# it's sha256 hash separated by a space. This makes it easier to manage large
# numbers of data files. The registry file should be in the same directory as this
# module.

#GOODBOY.load_registry("./registry.txt")
GOODBOY.load_registry(os.path.join(os.path.dirname(__file__),"registry_zip.txt"))

# Define functions that your users can call to get back some sample data in memory
def fetch_mannville_data():
    """
   Loads all required Mannville Group data and metadata for demo data. 
   Fetches the path to a file in the local storae. If it's not there, we'll
   download it.

   Parameters
   ----------
   none: none
    It does not take any parameters but it assumes there is a registry.txt in the same directory that has in it the name hash and location of the file to load.


   Returns
   -------
   ...: ellipses
    Returns nothing but three dots which reads as ellipses in Python. It does, however, write files to the data or whatever directory is given above in goodboy instance, which is created in fetch_demo_data.py by the pooch.create() call.
   """

    with open(os.path.join(os.path.dirname(__file__),"registry_zip.txt")) as f:
        lines = f.readlines()
    for line in lines:
        firstname = line.split(" ")[0]
        GOODBOY.fetch(firstname)
    data = ...
    
    return data


fetch_mannville_data()
# ZipFile.extractall("../data/Mannville_input_data/mannville_demo_data.zip")

with ZipFile("../data/Mannville_input_data/v0.0.3-alpha/mannville_demo_data.zip", 'r') as zip_ref:
    zip_ref.extractall("../data/Mannville_input_data/v0.0.3-alpha/")
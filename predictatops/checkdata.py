# -*- coding: utf-8 -*-

##### import statements
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt

#%matplotlib inline
import welly
from welly import Well
import lasio
import glob
import pickle
import math
import os

# env = %env


##### import from other modules
from configurationplusfiles import *


##### Classes
class TopsAvailable:
    """
    Class that uses the configuration class and data_inpunt class objects and additional 
    user input to find out the number of wells of those available that have the tops we want.

    Parameters
    ----------
    input_data_obj:object
         An object instantiated from the input class in configurationplusfile.py that contains attributes we'll call in this function.
    configuration_obj:object
         An object instantiated from the config class in configurationplusfile.py that contains attributes we'll call in this function.


    Attributes
    ----------
    input : object
        Example is input_data_obj imported from configurationplusfiles.py 
    config : object
        Example is configuration_obj imported from configurationplusfiles.py  
    picks_df_noNullPicks : dataframe
        Default is "nothing here yet, run take_out_wells_with_no_tops or set_picks_df_noNullPicks"
    wells_wAny_tops__list : dataframe
        Default is "nothing here yet"
    wells_with_all_given_tops : dataframe
        Default is None. It will be populated in function below within this class
    new_wells_with_all_given_tops : list
        Default is None. It will be populated by convertSiteIDListToUWIList() function in this class.

    Return
    ------
    none: none
        This class contains various functions that returns things but it itself does not return anything.

    """

    def __init__(self, input_data_obj, configuration_obj):
        """
        Initiates this class with two inputs, input_data_obj & configuration_obj.
        Several other attributes are initially None or strings like "nothing here yet" that are later populated by the functions below.      
        """
        #### intermediate files and paths
        self.input = input_data_obj
        self.config = configuration_obj
        ####
        self.picks_df_noNullPicks = "nothing here yet, run take_out_wells_with_no_tops or set_picks_df_noNullPicks"
        self.wells_wAny_tops__list = "nothing here yet"
        self.wells_with_all_given_tops = (
            None
        )  # populated in function below within this class
        self.new_wells_with_all_given_tops = None  # populated by

    def find_unique_tops_list(self):
        """
        Takes the input and config objects used as parameters to intiate this class and 
        Returns a list of available tops across all the wells.
        """
        unique_tops_list = self.input.picks_df[
            self.config.get_top_name_col_in_picks_df()
        ].unique()
        print(": unique_tops_list", unique_tops_list)
        return unique_tops_list

    def get_must_have_tops(self):
        """
        Uses the must have tops defined in the config object provided on intiation of this class object and returns the must have tops in the config object.
        """
        return self.config.get_must_have_tops__list()
        # print("must have top list is: ",must_have_curves_in_list)

    def take_out_wells_with_no_tops(self):
        """
        function is defined to take in a picks_df and 
        exclude any wells that have no picks or are flagged as very bad quality.
        THIS FUNCTION ASSUMES SOME STRUCTURES THAT MIGHT NOT EXIST IN YOUR PROJECT
        It populates this class object's attribute of self.picks_df_noNullPicks with noZeroPicks[noZeroPicks.Quality != -1] which should take out the rows with no picks.
        """
        #### THIS FUNCTION ASSUMES SOME STRUCTURES THAT MIGHT NOT EXIST IN YOUR PROJECT
        #### YOU MAY HAVE TO DO THIS A DIFFERENT WAY
        print(
            "THIS FUNCTION ASSUMES SOME STRUCTURES THAT MIGHT NOT EXIST IN YOUR PROJECT. It should work find with Mannville default data"
        )
        #### produces dataframe with no picks that have a value of zero
        noZeroPicks = self.input.picks_df[self.input.picks_df.Pick != 0]
        #### produces dataframe that doesn't have any picks with a quality of negative one, meaning not to be trusted or present
        noNullPicks = noZeroPicks[noZeroPicks.Quality != -1]
        self.picks_df_noNullPicks = noNullPicks

    def get_picks_df_noNullPicks(self):
        """
        Function that returns self.picks_df_noNullPicks. The picks dataframe with null pick rows removed.
        """
        return self.picks_df_noNullPicks

    #### THIS ONE NEEDS EDITING AS IT REQUIRES ARGUMENTS THAT MAY NOT BE NEEDED LIKE THIS????????
    def set_picks_df_noNullPicks(self, picks_df_noNullPicks):
        """
        Sets the self.picks_df_noNullPicks given picks_df_noNullPicks after making sure the input argument is a dataframe type.
        """
        if str(type(picks_df_noNullPicks)) == "<class 'pandas.core.frame.DataFrame'>":
            self.picks_df_noNullPicks = picks_df_noNullPicks
            print("set picks_df_noNullPicks attribute as ", picks_df_noNullPicks)
        else:
            raise ValueError("Argument picks_df_noNullPicks should be type dataframe")

    def get_df_of_top_counts_in_picks_df(self):
        """Uses class attributes already established to return a dataframe of how many non-zero and non-null picks exist for each top name."""
        #### produces dataframe of horID and counts of non-zero,non-null picks
        pick_counts = self.picks_df_noNullPicks.groupby(
            self.config.get_top_name_col_in_picks_df()
        )[self.config.siteID_col_in_picks_df].count()
        return pick_counts

    def get_df_wells_with_any_top(self):
        """Returns dataframe of wells with any sort of pick"""
        #### The total number of wells with any sort of pick is:
        self.wells_wAny_tops__list = self.picks_df_noNullPicks[
            self.config.siteID_col_in_picks_df
        ].unique()
        return self.wells_wAny_tops__list

    def get_number_wells_with_any_top(self):
        """Returns the total number of wells with any sort of pick"""
        if type(self.wells_wAny_tops__list) == str:
            self.get_df_wells_with_any_top()
            if type(self.wells_wAny_tops__list) == str:
                raise ValueError(
                    "expected self.wells_wAny_tops__list to be array but is type str, please run get_df_wells_with_any_top function"
                )
            else:
                return len(self.wells_wAny_tops__list)
        else:
            return len(self.wells_wAny_tops__list)

    def findWellsThatHaveCertainTop(self, top, quality_items_to_skip__list):
        """
        #### Takes in top
        #### Returns a list of wells with the given top
        """

        # print(top)
        if self.wells_wAny_tops__list == "nothing here yet":
            print(
                "self.wells_wAny_tops__list has not been populated properly yet. I'll run take_out_wells_with_no_tops() & get_df_wells_with_any_top"
            )
            self.take_out_wells_with_no_tops()
            print("test")
            self.get_df_wells_with_any_top()
            print("test2")
            # raise ValueError("self.wells_wAny_tops__list has not been populated properly yet. I'll run take_out_wells_with_no_tops() & get_df_wells_with_any_top()")

        else:
            picks = self.picks_df_noNullPicks
            Quality = self.config.get_quality_col_name_in_picks_df()
            HorID = self.config.get_top_name_col_in_picks_df()
            SitID = self.config.get_siteID_col_in_picks_df()
            Pick = self.config.get_picks_depth_col_in_picks_df()
            #####   g
            for item in quality_items_to_skip__list:
                # print("Quality = ",Quality)
                # print("picks type",type(picks),"and picks = ",picks)
                picks = picks[picks[Quality] != item]
            rows_with_picks = picks
            # rows_with_picks = picks[picks.Quality != 0]
            # rows_with_picks = rows_with_picks[rows_with_picks.Quality != -1]
            # print(rows_with_picks[0:4])\

            test = rows_with_picks.loc[rows_with_picks[HorID] == top]
            test[Pick].replace("", np.nan, inplace=True)
            # print(test)
            rows_with_that_top = list(
                rows_with_picks.loc[rows_with_picks[HorID] == top]
                .dropna()[SitID]
                .unique()
            )
            # print("before return",rows_with_that_top)
            return rows_with_that_top

    def findWellsWithAllTopsGive(self):
        """
        #### Takes in a list of tops
        #### Returns a list of wells that include all of those tops. If only one top occurs, well is not included
        """
        tops = self.config.get_must_have_tops__list()
        quality_items_to_skip__list = self.config.get_quality_items_to_skip__list()

        #
        list_of_wells_with_tops = []
        for top in tops:
            list_of_wells_with_tops.append(
                self.findWellsThatHaveCertainTop(top, quality_items_to_skip__list)
            )
        # print(len(list_of_wells_with_tops))
        if len(list_of_wells_with_tops) == 0:
            raise ValueError(
                "nothing in list_of_wells_with_tops, there should be at least one item! Something bad happened."
            )
        elif len(list_of_wells_with_tops) == 1:
            print(
                "returning list of wells names that have the required tops. The length of list is :",
                len(list_of_wells_with_tops[0]),
                " If this number is too small, consider changing the required tops in the configuration object.",
            )
            self.wells_with_all_given_tops = list_of_wells_with_tops
            return list_of_wells_with_tops[0]
        else:
            for eachlist in list_of_wells_with_tops[1:]:
                list_of_wells_with_tops = list(
                    set(list_of_wells_with_tops[0]).intersection(eachlist)
                )
            print(
                "returning list of wells names that have the required tops. The length of list is :",
                len(list_of_wells_with_tops),
                " If this number is too small, consider changing the required tops in the configuration object.",
            )
            self.wells_with_all_given_tops = list_of_wells_with_tops
            return list_of_wells_with_tops
            # list_of_wells_with_tops =list(set(list_of_wells_with_tops[0]).intersection(list_of_wells_with_tops[1]))

    def convertSiteIDListToUWIList(self):
        """
        Converts the list of wells by to list of wells by UWI. May not work well if your data is structured differently, so look at the actual code.
        """
        if self.input.wells_df is not None:
            wells = self.input.load_wells_file()
        else:
            wells = self.input.wells_df
        if self.wells_with_all_given_tops is not None:
            wells_with_all_given_tops = self.findWellsWithAllTopsGive()
        else:
            wells_with_all_given_tops = self.wells_with_all_given_tops

        new_wells = wells.set_index("SitID").T.to_dict("list")
        for key in new_wells:
            new_wells[key].append(new_wells[key][1].replace("/", "-") + ".LAS")
            #         print("new_wells",new_wells)
            #         print(len(new_wells))

        new_wells_with_all_given_tops = []
        for well in wells_with_all_given_tops:
            new_wells_with_all_given_tops.append(new_wells[well][2])
        self.new_wells_with_all_given_tops = new_wells_with_all_given_tops
        return new_wells_with_all_given_tops

    def run_all(self):
        """
        Runs all the functions in this class at once with default values from config object inputted at class object initiation.
        Returns list of wells_with_all_given_tops_by_uwi
        """
        unique_tops = self.find_unique_tops_list()
        print("The list of unique tops is: ", unique_tops)
        print(
            "The list of required tops from the configuration object that was used as an argument are: ",
            self.get_must_have_tops(),
        )
        print("This will, of course, exclude wells with no tops.")
        self.take_out_wells_with_no_tops()
        print("The counts for each top in the dataset are: ")
        top_counts = self.get_df_of_top_counts_in_picks_df()
        print(top_counts)
        print(
            "and the total number of wells with any tops is: ",
            self.get_number_wells_with_any_top(),
        )
        self.wells_with_all_given_tops = self.findWellsWithAllTopsGive()
        print(
            "The length of the list with all the names of the wells that have the required tops"
            + str(self.get_must_have_tops())
            + "is: ",
            len(self.wells_with_all_given_tops),
            " and it will be what is returned",
        )
        wells_with_all_given_tops_by_uwi = self.convertSiteIDListToUWIList()

        return wells_with_all_given_tops_by_uwi


class CurvesAvailable:
    """
    Class that uses the configuration class and data_inpunt class objects and additional 
    user input to find out the number of wells of those available that have the tops we want.
    """

    def __init__(self, input_data_obj, configuration_obj):
        """doc string goes here"""
        #### intermediate files and paths
        self.input = input_data_obj
        self.config = configuration_obj
        ####
        # self.full_well_path = self.input.las_path+'*'+self.input.well_format
        self.objectOfCurves = None  # populates from findAllCurvesInGivenWells()
        self.countsOfCurvesObj = None  # populates from _____ function
        self.onlyPlentifulCurvesArray = (
            None
        )  # populates from getCurvesInMinNumberOfWells
        self.wellsWithWantedCurves = (
            None
        )  # populates from findWellsWithCertainCurves(self)
        # self.picks_df_noNullPicks = "nothing here yet, run take_out_wells_with_no_tops or set_picks_df_noNullPicks"
        # self.wells_wAny_tops__list = "nothing here yet"
        #### self.config.threshold_returnCurvesThatArePresentInThisManyWells = 2000
        #### self.input.las_folder_path
        #### self.input.well_format

    def findAllCurvesInGivenWells(self):
        """ say what it does here"""
        objectOfCurves = {}
        las_folder_path = self.input.las_folder_path
        well_format = self.input.well_format
        path = las_folder_path + "*" + well_format
        print("loading all wells in the path = ", path)
        for fn in glob.glob(path):
            las = lasio.read(fn, ignore_data=True)
            mnemonics = [c.mnemonic for c in las.curves]
            fnShort = fn.replace(las_folder_path, "")
            objectOfCurves[fnShort] = mnemonics
        # print(fn + '\n\t' + '\n\t'.join(mnemonics))
        self.objectOfCurves = objectOfCurves
        return objectOfCurves

    def countsOfCurves(self):
        """ say what it does here"""
        if self.objectOfCurves == None:
            self.findAllCurvesInGivenWells()
        else:
            pass
        listOfListOfCurves = self.objectOfCurves.values()
        startList = []
        for listI in listOfListOfCurves:
            startList = startList + listI
        uniq_CurvesList = set(startList)
        countsOfCurvesObj = {}
        for eachCurve in uniq_CurvesList:
            countsOfCurvesObj[eachCurve] = startList.count(eachCurve)
        print("counts of curves are: ", countsOfCurvesObj)
        self.countsOfCurvesObj = countsOfCurvesObj
        return countsOfCurvesObj

    def getCurvesInMinNumberOfWells(self):
        """ say what it does here"""
        minNumberCurves = (
            self.config.threshold_returnCurvesThatArePresentInThisManyWells
        )
        countsOfCurves = self.countsOfCurvesObj
        #### Takes in a minmum number of wells that need to have specific curves and an object where keys are curve names and values is the count of that curves across all wells.
        #### Returns an array of curve names that are found in at least the given number of wells.
        curvePlusCountArray = countsOfCurves.items()
        onlyPlentifulCurvesArray = []
        for curve in curvePlusCountArray:
            if curve[1] > minNumberCurves:
                onlyPlentifulCurvesArray.append(curve[0])
        self.onlyPlentifulCurvesArray = onlyPlentifulCurvesArray
        return onlyPlentifulCurvesArray

    def findWellsWithCertainCurves(self):
        """
        Function takes in an object with keys that are well names and values that are all curves in that well 
        and as the second argument an array of plentiful curves expected to be in every well
        Function returns an array of wells that have the specified curves in the second argument.
        """
        ######## Check if none, if none run appropriate function, if not use it,
        if self.onlyPlentifulCurvesArray == None:
            print(
                "self.onlyPlentifulCurvesArray was not populated yet so getCurvesInMinNumberOfWells() will be ran"
            )
            self.getCurvesInMinNumberOfWells()
            print("self.onlyPlentifulCurvesArray is now", self.onlyPlentifulCurvesArray)
        else:
            pass
        plentifulCurves = self.onlyPlentifulCurvesArray

        ######## Check if none, if none run appropriate function, if not use it,
        if self.countsOfCurvesObj == None:
            print(
                "self.countsOfCurvesObj was not populated yet so countsOfCurves()) will be ran"
            )
            self.countsOfCurves()
            print("self.countsOfCurvesObj is now", self.countsOfCurvesObj)
        else:
            pass
        objectOfCurves = self.objectOfCurves
        #######
        wellsWithWantedCurves = []
        print(type(plentifulCurves))
        print("plentifulCurves is:", plentifulCurves)
        print(type(objectOfCurves))
        print("objectOfCurves is: ", objectOfCurves)
        for eachWell in objectOfCurves.keys():
            print(eachWell)
            if set(plentifulCurves).issubset(objectOfCurves[eachWell]):
                wellsWithWantedCurves.append(eachWell)
        ######## Initiate THIS !!!!!
        self.wellsWithWantedCurves = wellsWithWantedCurves
        return wellsWithWantedCurves

    def run_all(self):
        """
        runs all included functions and returns a ____ of wells with the requested log curves
        """
        countsOfCurves = self.countsOfCurves()
        objectOfCurves = self.findAllCurvesInGivenWells()
        onlyPlentifulCurvesArray = self.getCurvesInMinNumberOfWells()
        wellsWithWantedCurves = self.findWellsWithCertainCurves()
        all_results_obj = {
            "countsOfCurves": countsOfCurves,
            "objectOfCurves": objectOfCurves,
            "onlyPlentifulCurvesArray": onlyPlentifulCurvesArray,
            "wellsWithWantedCurves": wellsWithWantedCurves,
        }
        print(
            "returning an object with 4 parts, each a piece of information that helps determine how many log curves are availabe in how many logs "
        )
        return all_results_obj


##### Functions not in class objects
def findWellsWithCertainCurves(objectOfCurves, plentifulCurves):
    """
    #### Function takes in an object with keys that are well names and values that are all curves in that well and as the second argument an array of plentiful curves expected to be in every well
    #### Function returns an array of wells that have the specified curves in the second argument.
    """

    wellsWithWantedCurves = []
    for eachWell in objectOfCurves.keys():
        if set(plentifulCurves).issubset(objectOfCurves[eachWell]):
            wellsWithWantedCurves.append(eachWell)
    return wellsWithWantedCurves


def getCurvesListWithDifferentCurveName(originalCurveList, origCurve, newCurve):
    """
    Takes in list of curves, curve name to be replaced, and curve name to replace with.
    Returns a list with the orginal and new curve names switched in the given curve list
    """

    plentifulCurves_wDEPTH = originalCurveList.copy()
    try:
        plentifulCurves_wDEPTH.remove(origCurve)
        plentifulCurves_wDEPTH.append(newCurve)
    except:
        print(
            "did not find ",
            origCurve,
            " when attempting to replace it with ",
            newCurve,
            " in the getCurvesListWithDifferentCurveName function",
        )
    return plentifulCurves_wDEPTH


def findWellsWithGivenTopsCurves(
    wells, wells_with_all_given_tops, wellsWithNeededCurvesList_real
):
    """
    NOTE: THIS FUNCTION MAY NOT BE USED DUE TO OTHER CHANGES IN THE CODE.
    It was created to deal with wanting to find the intersection of a list of wells with SITEID only and a list of wells with UWI only.
    """
    new_wells = wells.set_index("SitID").T.to_dict("list")
    # print("new_wells",new_wells[0])
    for key in new_wells:
        new_wells[key].append(new_wells[key][1].replace("/", "-") + ".LAS")
    print("new_wells", new_wells)
    print(len(new_wells))
    new_wells_with_all_given_tops = []
    for well in wells_with_all_given_tops:
        print("well in wells_with_all_given_tops:", well)
        new_wells_with_all_given_tops.append(new_wells[well][2])
    return list(
        set(new_wells_with_all_given_tops).intersection(wellsWithNeededCurvesList_real)
    )

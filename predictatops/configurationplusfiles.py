# -*- coding: utf-8 -*-
"""

The configurationplusfiles.py module sets up three objects from class functions. 

- input_data() establishes where data is loaded from.
- configuration() establishes various configuration variables used in the rest of the code.
- output_data() establishes where data is written to. 

These are intended to be changed by the configurationplusfiles_runner.py module.

"""

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


##### import from other modules


##### Classes
class input_data:
    """
    A class object that holds paths and other information related to input data such as log files location, top files, well information files, etc.
    
    Parameters
        ----------
        picks_file_path: str
            A string for the file path to the file with all the pick names and depths.
        picks_delimiter_str: str
            The delimiter of the file that has all the picks.
        path_to_logs_str: str
            The path to the directory with all the well logs.
    
    """

    def __init__(self, picks_file_path, picks_delimiter_str, path_to_logs_str):
        #### Default initiation = ('../../../SPE_006_originalData/OilSandsDB/PICKS.TXT','\t','../../../SPE_006_originalData/OilSandsDB/Logs/*.LAS')
        #### Only things that are mandatory on initiation are below
        self.data_directory = "../data/Mannville_input_data/v0.0.3-alpha/"
        self.picks_file_path = (
            picks_file_path
        )  #### example = '../../../SPE_006_originalData/OilSandsDB/PICKS.TXT'
        self.picks_delimiter_str = picks_delimiter_str  #### example = '\t'
        self.picks_df = pd.read_csv(picks_file_path, delimiter=picks_delimiter_str)
        self.picks_dic = self.data_directory + "OilSandsDB/PICKS.TXT"
        self.picks_dic_file_path_delimiter = "\t"
        self.logs_path_to_folder = (
            path_to_logs_str
        )  #### example = '../../../SPE_006_originalData/OilSandsDB/Logs/*.LAS'
        #### non-mandatory attributes, defaults should work for the example dataset. Can be changed with set functions below
        self.wells_file_path = self.data_directory + "OilSandsDB/WELLS.TXT"
        self.wells_file_path_delimiter = "\t"

        self.gis_file_path = self.data_directory + "well_lat_lng.csv"
        self.gis_file_path_delimiter = ","
        self.gis_lat_col = "lat"
        self.gis_long_col = "lng"
        # wells_wTopsCuves_toLoad = 'WellNamesWithGivenTopsCurves_defaultFileName.pkl'
        #### for logs
        self.las_folder_path = self.data_directory + "OilSandsDB/Logs/"
        self.well_format = ".LAS"
        #### Technically optional but often used.
        #### GIS file is mandatory if you want to use information from nearby wells or well's general location.
        self.wells_df = None
        self.gis_df = None

    def load_wells_file(self):
        """ load wells file into pandas dataframe """
        self.wells_df = pd.read_csv(
            self.wells_file_path, delimiter=self.wells_file_path_delimiter
        )
        return self.wells_df

    def load_gis_file(self):
        """ load wells file into pandas dataframe """
        self.gis_df = pd.read_csv(
            self.gis_file_path, delimiter=self.gis_file_path_delimiter
        )
        return self.gis_df

    def set_wells_file_path(self, wells_file_path_str, wells_file_delimiter):
        """ set wells file path as attribute of object and returns wells data frame using load_well_file. Can be txt, tsv, or csv"""
        self.wells_file_path = wells_file_path_str
        self.wells_file_path_delimiter = wells_file_delimiter
        return self.load_wells_file()

    def set_gis_file_path(self, gis_file_path_str, gis_file_path_delimiter):
        """ set wells file path as attribute of object and returns wells data frame using load_well_file. Can be txt, tsv, or csv"""
        self.gis_file_path = gis_file_path_str
        self.gis_file_path_delimiter = gis_file_path_delimiter
        return self.load_gis_file()


class configuration:
    """
    A class to keep configuration variables you might change between runs. That is why it has a large number of attributes listed below.

    Types of information information stored in here would mandetory curves or mandatory tops, column names, name of the top you're trying to predict, etc.
    The object created by this class is used throughout Predictatops, so many modules reimport it. 

    Be careful to not change something in one module close your code, start up later working with the next module and except your changes to persis unless you saved them or wrote them into the configurationplusfiles_runner.py file.
    
    Parameters
    ----------
    none:none
        None.
       

    Attributes
    ----------
    csv_of_well_names_wTopsCuves__name : str
        csv_of_well_names_wTopsCuves__name
    csv_of_well_names_wTopCurves__path : str
        csv_of_well_names_wTopsCuves__name
    must_have_curves_list : list
        An array of strings that are curve names like ['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT']
    curve_windows_for_rolling_features : list
        Array of integers like [5,7,11,21]
    must_have_tops__list : list
        An array of tops list that could be integers or strings like [13000,14000]
    target_top : str
        A string or integer like 1300
    top_under_target : str
        A string or interger that is a top name and is the name of a top under the top you want to predict such as 14000
    top_name_col_in_picks_df : str
        The top name as it appears in the picks dataframe 
    siteID_col_in_picks_df : str
        The string for the siteID column in the picks dataframe like 'SitID'
    UWI : str
        The string for the UWI column like "UWI"
    DEPTH_col_in_featureCreation : str
        The string for the depth column like "DEPT"
    HorID_name_col_in_picks_df : str
         The string for the horizon ID column like "HorID"
    quality_col_name_in_picks_df : str
        The string for the quality of the pick column like "Quality"
    picks_depth_col_in_picks_df : str 
        The string for the pick column name like 'Pick'
    col_topTarget_Depth_predBy_NN1thick : str
        The string for the top target depth predicted by nearest neighbor thickess like 'topTarget_Depth_predBy_NN1thick'
    quality_items_to_skip__list : str
        The array of the integers for the quality of wells to optionally skip as not good quality picks. An example is [-1,0]
    test : str
        Honestly forget what this is come back and find out but is should be "test0"
    pick_class_str : str
        String for the top taget pick prediction column like 'TopTarget_Pick_pred'
    threshold_returnCurvesThatArePresentInThisManyWells : int
        The integer for the number of wells a curve has to be present in to be kept for example 2000
    max_numb_wells_to_load : int
        Max number of wells to load out of all the wells in the directory with wells. This is used for when you're testing. Example is 1000000
    split_traintest_percent : float
        The percent in 0 to 1 terms for train vs. split. You give the percent to keep. example is 0.8
    kdtree_leaf : int
        Levels of kdtree? default is 2
    kdtree_k : int
        Integer for number of neighbors or K in k nearest neighbor code for finding nearby wells for each well. Default is 8
    rebalanceClassZeroMultiplier : int
        When rebalancing class zero. The number of instances of class zero is duplicated by this times. Default is 100
    rebalanceClass95Multiplier : int
        When rebalancing class zero. The number of instances of class 95 is duplicated by this times. Default is 40
    NN1_topTarget_DEPTH : str
        The string used in the column that holds the depth of the top in the first nearest neighbor training well. For example 'NN1_topTarget_DEPTH'
    NN1_TopHelper_DEPTH : str
        Helper depth for calculations for NN1_topTarget_DEPTH. Example is "NN1_TopHelper_DEPTH"
    trainOrTest : str
        String for column that holds string of either train or test. Example is 'trainOrTest'
    colsToNotTurnToFloats : list
        List of columsn to not turn to floads during feature creation. Examples is ['UWI', 'SitID', 'trainOrTest','Neighbors_Obj']
    zonesAroundTops : object
        An object of class lables and depths around top to create those classes in. Example is {"100":[0],"95":[-0.5,0.5],"60":[-5,0.5],"70":[0.5,5],"0":[]} #### NOTE: The code in createFeat_withinZoneOfKnownPick(df,config) function in features.py current ASSUMES only 5 zone labels
    columns_to_not_trainOn_andNotCurves : list
        List of strings for names of columns to not train on and are not curves. Example is  ['FromBotWell','FromTopWel''rowsToEdge','lat','lng',  'SitID','TopHelper_HorID','TopTarget_HorID','TopHelper_DEPTH','diff_Top_Depth_Real_v_predBy_NN1thick','diff_TopTarget_DEPTH_v_rowDEPT','diff_TopHelper_DEPTH_v_rowDEPT','class_DistFrPick_TopHelper','NewWell','LastBitWell','TopWellDept','BotWellDept','WellThickness','rowsToEdge','closTopBotDist','closerToBotOrTop','Neighbors_Obj']
    columns_to_not_trainOn_andAreCurves : list
        list of strings for columns to not train on that are curves. Example is  ['RHOB','SP','CALI','COND','DELT','DENS','DPHI:1','DPHI:2','DT','GR:1','GR:2','IL','ILD:1','ILD:2','ILM','LITH','LLD','LLS','PHID','PHIN','RESD','RT','SFL','SFLU','SN','SNP','Sp']
    columns_to_use_as_labels : list
        List of strings for columns to use as labels. Examples are= ['class_DistFrPick_TopTarget','UWI','trainOrTest','TopTarget_DEPTH']

    """

    def __init__(self):
        #### intermediate files and paths
        self.csv_of_well_names_wTopsCuves__name = ""
        self.csv_of_well_names_wTopCurves__path = "."
        #### Choices
        self.must_have_curves_list = [""]  # ['ILD', 'NPHI', 'GR', 'DPHI', 'DEPT']
        self.curve_windows_for_rolling_features = [5, 7, 11, 21]
        self.must_have_tops__list = [13000, 14000]
        self.target_top = 13000
        self.top_under_target = 14000
        #### Column string names
        self.top_name_col_in_picks_df = ""
        self.siteID_col_in_picks_df = "SitID"
        self.UWI = "UWI"
        self.DEPTH_col_in_featureCreation = "DEPT"
        self.HorID_name_col_in_picks_df = "HorID"
        self.quality_col_name_in_picks_df = "Quality"
        self.picks_depth_col_in_picks_df = "Pick"
        self.col_topTarget_Depth_predBy_NN1thick = "topTarget_Depth_predBy_NN1thick"
        self.quality_items_to_skip__list = [-1, 0]
        self.test = "test0"
        self.pick_class_str = "TopTarget_Pick_pred"
        self.threshold_returnCurvesThatArePresentInThisManyWells = 2000
        self.max_numb_wells_to_load = 1000000
        self.split_traintest_percent = 0.8
        self.kdtree_leaf = 2
        self.kdtree_k = 8
        self.rebalanceClassZeroMultiplier = 100
        self.rebalanceClass95Multiplier = 40
        self.NN1_topTarget_DEPTH = "NN1_topTarget_DEPTH"
        self.NN1_TopHelper_DEPTH = "NN1_TopHelper_DEPTH"
        self.trainOrTest = "trainOrTest"
        self.colsToNotTurnToFloats = ["UWI", "SitID", "trainOrTest", "Neighbors_Obj"]
        self.zonesAroundTops = {
            "100": [0],
            "95": [-0.5, 0.5],
            "60": [-5, 0.5],
            "70": [0.5, 5],
            "0": [],
        }  #### NOTE: The code in createFeat_withinZoneOfKnownPick(df,config) function in features.py current ASSUMES only 5 zone labels
        self.columns_to_not_trainOn_andNotCurves = [
            "FromBotWell",
            "FromTopWel" "rowsToEdge",
            "lat",
            "lng",
            "SitID",
            "TopHelper_HorID",
            "TopTarget_HorID",
            "TopHelper_DEPTH",
            "diff_Top_Depth_Real_v_predBy_NN1thick",
            "diff_TopTarget_DEPTH_v_rowDEPT",
            "diff_TopHelper_DEPTH_v_rowDEPT",
            "class_DistFrPick_TopHelper",
            "NewWell",
            "LastBitWell",
            "TopWellDept",
            "BotWellDept",
            "WellThickness",
            "rowsToEdge",
            "closTopBotDist",
            "closerToBotOrTop",
            "Neighbors_Obj",
        ]
        self.columns_to_not_trainOn_andAreCurves = [
            "RHOB",
            "SP",
            "CALI",
            "COND",
            "DELT",
            "DENS",
            "DPHI:1",
            "DPHI:2",
            "DT",
            "GR:1",
            "GR:2",
            "IL",
            "ILD:1",
            "ILD:2",
            "ILM",
            "LITH",
            "LLD",
            "LLS",
            "PHID",
            "PHIN",
            "RESD",
            "RT",
            "SFL",
            "SFLU",
            "SN",
            "SNP",
            "Sp",
        ]
        self.columns_to_use_as_labels = [
            "class_DistFrPick_TopTarget",
            "UWI",
            "trainOrTest",
            "TopTarget_DEPTH",
        ]
        # self.results_path = "../results"
        # self.availableData_path = "availableData"

    #### only keep wells that have these curves
    def set_must_have_curves(self, must_have_curves_in_list):
        """doc string goes here"""
        self.must_have_curves_list = must_have_curves_in_list
        print("must have curve list is: ", must_have_curves_in_list)

    def get_must_have_curves(self, must_have_curves_in_list):
        """doc string goes here"""
        return self.must_have_curves_list

    #### only keep wells that have these tops
    def set_must_have_tops__list(self, must_have_tops__list):
        # [13000,14000]
        self.must_have_tops__list = must_have_tops__list
        print("set must_have_tops_list as: ", self.must_have_tops__list)

    def get_must_have_tops__list(self):
        # [13000,14000]
        return self.must_have_tops__list

    def set_quality_items_to_skip__list(self, quality_items_to_skip__list):
        self.quality_items_to_skip__list = quality_items_to_skip__list
        print("set quality_items_to_skip__list as: ", quality_items_to_skip__list)

    def get_quality_items_to_skip__list(self):
        return self.quality_items_to_skip__list

    #### column names in picks_df
    def set_top_name_col_in_picks_df(self, top_name_col_in_picks_df__str):
        self.top_name_col_in_picks_df = top_name_col_in_picks_df__str
        print(" set self.top_name_col_in_picks_df as: ", top_name_col_in_picks_df__str)

    def set_siteID_col_in_picks_df(self, sitID__str):
        self.siteID_col_in_picks_df = sitID__str
        print(" set siteID_col_in_picks_df as: ", self.siteID_col_in_picks_df)

    def get_siteID_col_in_picks_df(self):
        return self.siteID_col_in_picks_df

    def get_top_name_col_in_picks_df(self):
        return self.top_name_col_in_picks_df

    def set_quality_col_name_in_picks_df(self, Quality__str):
        self.quality_col_name_in_picks_df = Quality__str

    def get_quality_col_name_in_picks_df(self):
        return self.quality_col_name_in_picks_df

    def set_picks_depth_col_in_picks_df(self, picks_depth_col_in_picks_df):
        self.picks_depth_col_in_picks_df = picks_depth_col_in_picks_df

    def get_picks_depth_col_in_picks_df(self):
        return self.picks_depth_col_in_picks_df


class output_data:
    """
    A class to keep information related to where output files are saved and naming conventions. 
    
    This class can also makes all the directories for intermediate result files via its make_all_directories() function.
    
    Types of information information stored in here would all the intermediate output file paths as you run different functions and modules of Predictatops.
    
    The object created by this class is used throughout Predictatops, so many modules reimport it. 
    
    Be careful to not change something in one module close your code, start up later working with the next module and except your changes to persis unless you saved them or wrote them into the configurationplusfiles_runner.py file.
    

    Parameters
    ----------
    none:none
        None.
       

    Attributes
    ----------
    default_results_file_format : str = ".h5"
        A base path for all results. Example is '../results/'
    path_checkData : str
        A path string for the checkData directory. Example is 'checkData'
    path_load : str
        A path string for the load directory. Example is 'load'
    path_split : str
        A path string for the split directory. Example is 'split'
    path_wellsKNN : str
        A path string for the wellsKNN directory. Example is 'wellsKNN'
    path_features : str
        A path string for the features directory. Example is 'features'
    path_balance : str
        A path string for the balance directory. Example is 'balance'
    path_trainclasses : str
        A path string for the trainclasses directory. Example is 'trainclasses'
    path_prediction :str
        A path string for the prediction directory. Example is 'prediction'
    path_evaluate : str
        A path string for the evaluation directory. Example is 'evaluate'
    path_map : str
        A path string for the map directory. Example is 'map'
    path_plot : str
        A path string for the plot directory. Example is 'plot
    loaded_results_wells_df : str
        A path string for the loaded wells with top curves dataframe. Example is "loaded_wells_wTopsCurves"
    split_results_wells_df : str
        A path string for the loaded wells with top curves and splited dataframe. Example is "wells_wTopsCurvesSplits"
    wellsKNN_results_wells_df : str
        A path string for the loaded wells with top curves splitted and with KNN features dataframe. Example is "wells_wTopsCurvesSplitsKNN"
    features_results_wells_df : str
        A path string for the loaded wells with top curves splitted with KNN features and main features from features.py module dataframe. Example is "wells_wTopsCurvesSplitsKNNFeatures"
    balance_results_wells_df : str
        A path string for the loaded wells with top curves splitted and with KNN features and features from features.py and rebalanced classes dataframe. Example is "wells_wTopsCurvesSplitsKNNFeaturesBalance"
    trainclasses_results_model : str
        A path string for the trained model. Example is "model_trainclasses_wTopsCurvesSplitsKNNFeaturesBalance"
    
    
    """

    def __init__(self):
        #### paths to directories to store itermediate and final results
        self.default_results_file_format = ".h5"
        self.base_path_for_all_results = "../results/"
        self.path_checkData = "checkData"
        self.path_load = "load"
        self.path_split = "split"
        self.path_wellsKNN = "wellsKNN"
        self.path_features = "features"
        self.path_balance = "balance"
        self.path_trainclasses = "trainclasses"
        self.path_prediction = "prediction"
        self.path_evaluate = "evaluate"
        self.path_map = "map"
        #### IF YOU ADD ANOTHER DIRECTORY TO THE ONES ABOVE, ADD IT TO THE LIST IN make_all_directories(self) FUNCTION !!! ####
        self.loaded_results_wells_df = "loaded_wells_wTopsCurves"
        self.split_results_wells_df = "wells_wTopsCurvesSplits"
        self.wellsKNN_results_wells_df = "wells_wTopsCurvesSplitsKNN"
        self.features_results_wells_df = "wells_wTopsCurvesSplitsKNNFeatures"
        self.balance_results_wells_df = "wells_wTopsCurvesSplitsKNNFeaturesBalance"
        self.trainclasses_results_model = (
            "model_trainclasses_wTopsCurvesSplitsKNNFeaturesBalance"
        )

    def make_all_directories(self):
        """
        A function that makes all the directories defined in the attributes of the output_data() class init function.
        Examples of directories made include: [self.path_checkData,self.path_load,self.path_split,self.path_wellsKNN,self.path_features,
        self.path_balance,self.path_trainclasses,self.path_prediction,self.path_evaluate,self.path_map]
        

        Parameters
        ----------
        none:none
            None.

        Return
        ------
        none: none
            The function does not return anything though it does print all the directories it creates, whether they already exist, and the base results directory created by running this function.
        """
        print("making base folder for results in:", self.base_path_for_all_results)
        list_of_sub_directories = [
            self.path_checkData,
            self.path_load,
            self.path_split,
            self.path_wellsKNN,
            self.path_features,
            self.path_balance,
            self.path_trainclasses,
            self.path_prediction,
            self.path_evaluate,
            self.path_map,
        ]
        if not os.path.exists(self.base_path_for_all_results):
            os.makedirs(self.base_path_for_all_results)
            try:
                os.makedirs(self.base_path_for_all_results)
            except OSError as e:
                print(e.errno)
                # if e.errno != errno.EEXIST:
                #     raise
        else:
            print(
                "base_path directory already exists,",
                self.base_path_for_all_results,
                " so not creating it again. This may or may not be what you intended, so just flagging it.",
            )
        for sub_dir in list_of_sub_directories:
            if not os.path.exists(self.base_path_for_all_results + "/" + sub_dir):
                os.makedirs(self.base_path_for_all_results + "/" + sub_dir)
                try:
                    os.makedirs(self.base_path_for_all_results + "/" + sub_dir)
                except OSError as e:
                    print(e.errno)
                    # if e.errno != errno.EEXIST:
                    #     raise
            else:
                print(
                    "directory ",
                    sub_dir,
                    " already exists so not making it again in make_all_directories function of configurationplusfiles.py",
                )
        print(
            "made directories for each step in the process. They should be in : ",
            self.base_path_for_all_results,
        )

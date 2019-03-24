# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
# %matplotlib inline
import welly
from welly import Well
import lasio
import glob

"""Main module."""

def printHello():
    print("hello 5s")

class AvailableData:
    def __init__(self, path_to_wells, path_to_tops):
        self.path_to_wells = path_to_wells
        self.path_to_tops = path_to_tops
        self.path_to_locations = "."
        self.curves_must_have = []
        self.tops_must_have = []
        self.min_number_wells_with_required_attributes = 0
        self.picks_df = []
        self.wells_df = []
        self.locations_df = []
        self.wells_that_failed_to_load = []

    def load_picks_df(self):
    	"""
    	doc string goes here
    	"""
        # print("test")
    	picks = pd.read_csv("./data/SPE_006_originalData/OilSandsDB/PICKS.TXT",delimiter='\t')
    	self.picks_df = picks
        # return picks

    def load_wells_df():
    	"""
    	doc string goes here
    	"""
    	# wells = pd.read_csv(self.path_to_wells)
    	# self.path_to_wells = wells
        # print("nothing here yet")

    def load_locations_df(self,locations_path):
    	"""
    	doc string goes here
    	"""
        self.path_to_locations = locations_path
    	gis = pd.read_csv(locations_path)
        self.locations_df = gis
        print('well location data from path '+locations_path+' has been added to the self.locations_df')
    	return 'gis'

    def load_picks_wells(self,locations_path):
    	"""
    	doc string goes here
    	"""
    	load_picks_df(self)
    	load_wells_df(self)
    	print('Loaded picks, wells, but not a locations dataframe. Acess picks df via strat.AvailableData.picks_df')

    def load_picks_wells_locations(self,locations_path):
    	"""
    	doc string goes here
    	"""
    	load_picks_df(self)
    	load_wells_df(self)
    	load_locations_df(self,locations_path)
    	print('Loaded picks, wells, and locations dataframe. Acess picks df via strat.AvailableData.picks_df')

    def count_curves(self,df,curves_col_str,UWI_str):
    	"""
    	doc string goes here
    	"""
    	return curves_counts

    def count_tops(self,df,picks_col_str,UWI_str):
    	"""
    	doc string goes here
    	"""
    	pick_counts = df.groupby(picks_col_str)[UWI_str].count()
    	return picks_counts

    def set_curves_must_have(self, curves_array):
    	"""
    	doc string goes here
    	"""
        # self.curves_must_have = curves_array

    def set_min_number_wells_with_required_attributes(self, min_number):
    	"""
    	doc string goes here
    	"""
        # self.min_number_wells_with_required_attributes = min_number

    def get_wells_with_top(self, top_str):
    	"""
    	doc string goes here
    	"""
        # return well_list_top_plus_curves

    def get_wells_with_tops_and_curves(self, tops_array,curves_array):
    	"""
    	First argument should be array of tops. If one top, put that one top in an array. Second argument should be array of curves.
    	If one curve is a suitable replacement for another curve, that pair or triplet should be an array instead of a string.
    	For example, ["RESD",["GR","GR1","GR2"],"ILD"]
    	Function should return a series that is a well list where each well contains the required tops and curves.
    	"""
        # return well_list_top_plus_curves


def PrintTest():
    print("test")
    return "test"

# class DemoData:
# 	"""
# 	Returns paths to demo data from Mannville Group in Alberta, Canada.
# 	"""
#     def __init__(self, path_to_wells, path_to_tops):
#         self.path_to_wells = "."
#         self.path_to_tops = "."
#         self.path_to_tops_dictionary = "."
#         self.path_to_locations = "."
#         self.data_info = [{"name":"","Data from location":"","Link to original data":"","Link to report on data":"","Description":""}]
#         self.wells_format = "LAS 2.0"
#         self.location_formation = ""
#         self.tops_format = ""
    
class LoadNMerge():
	"""
	Load all the original data into a single dataframe for further work
	"""

class FindNeighbors():
	"""
	Find the depth of given tops in K nearest neighbors using location coordinates and tops dataset
	"""

class CreatesFeatures():
	"""
	doc string
	"""

class SplitTrainTest():
	"""
	doc string
	"""

class Rebalance():
	"""
	doc string
	"""

class ML1():
	"""
	doc string
	"""

class ML2():
	"""
	doc string
	"""

class EvaluateML():
	"""
	doc string
	"""

class Map():
	"""
	doc string
	"""

class UmapHelper():
	"""
	doc string
	"""

class Pipelines():
	"""
	doc string
	"""

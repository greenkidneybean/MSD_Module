"""
This module is used to convert a .txt file containing a variable number of 8x12
arrays, each representing an MSD 96-well plate.

An "msd_96" object must be created to initiate this module. Input variables are
called to create a project file tree in the current working directory.

A given .txt file is then split into individual plates, and for each plate
array a .csv and plot are created.
"""

import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

print ("msd_module imported!")
#class

class msd_96:
    """
    The "msd_96()" initiates the creation or a project file tree
    """
    def __init__(self):
        date = input('Input date (e.g. yymmdd): ')
        self.date = date

        project_name = input('Input project name (e.g. my_project): ')
        self.project_name = project_name

        main_project_folder = (date) + '_' + (project_name)
        self.main_project_folder = main_project_folder

        graph_folder_name = str(date) + '_Graphs'
        graph_path = (main_project_folder) + '/' + (graph_folder_name)
        self.graph_path = graph_path

        csv_folder_name = str(date) + '_Plates'
        csv_path = (main_project_folder) + '/' + (csv_folder_name)
        self.csv_path = csv_path

        #create folder tree in current working directory
        os.mkdir(main_project_folder)
        os.mkdir(graph_path)
        os.mkdir(csv_path)

        #Dilution series automatically created as the following:
        self.dilution = [5, 2.5, 1.25, 0.625, 0.3125, 0.15625, 0.078125, 0.0390625]

    def create_df(self, filename): #creates working dataframe in pandas
        """
        Creates a working Pandas DataFrame object from an appended MSD 96-well
        .txt file
        """
        open = pd.read_table(filename, header=1)
        df = pd.DataFrame(open)
        df = df.dropna(axis=0)
        i = list(range(0, len(df)))
        df.index = i
        df.columns = ['Rows', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12']
        self.df = df
        print ('df created!')
    def create_dilution(self, starting_conc,dilution_fold,number_of_dilutions):
        """
        Creates a serial dilution series based upon the starting concentration,
        dilution fold, and number of dilutions
        """
        i = 0
        dilution = []
        while i < number_of_dilutions:
            dilution.append(starting_conc)
            starting_conc = starting_conc/dilution_fold
            i += 1
        self.dilution = dilution
    def split_plates(self):
        i = 0
        p = 1
        r = 0
        for i in range(len(self.df)):
            if i % 8 == 0:
                avg_plate = pd.DataFrame()
                c = 1
                for i in range(6):
                    column = self.df.iloc[r:r+8,c:c+2]
                    avg_plate[i+1] = column.mean(axis=1)
                    c += 2
                    i += 1
                avg_plate.insert(0,'dilution', self.dilution)
                avg_plate.insert(0, 'row', self.df.iloc[r:r+8, 0:1])
                csv_file_name = 'PlateAvg_' + str(p) + '.csv'
                csv_file_path = (self.csv_path) + '/' + (csv_file_name)
                avg_plate.to_csv(csv_file_path)
                graph = avg_plate.set_index('dilution')
                #graph2 = graph.drop(['row'], 1)
                print ('Plate#_' + str(p))
                print (avg_plate)
                #print (graph2.plot.line())
                print (graph.plot.line())
                graph_file_name = 'PlateAvg_' + str(p) + '.png'
                graph_file_path = (self.graph_path) + '/' + (graph_file_name)
                plt.savefig(graph_file_path)
                r += 8
                p += 1

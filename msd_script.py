#!/usr/local/bin/python
print ('\nmsd_script starting\n')
#imports

import numpy as np
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import argparse

#argparse arguments

parser = argparse.ArgumentParser(description=
    'This script is designed to convert a given MSD appended .txt file and\
    break it down into the individual plates, with an output of a .csv file\
    and .png graph averaging column duplicates.')
parser.add_argument('txtfile', help='MSD appended .txt file to be converted')
parser.add_argument('date', help='date of project in the format yymmdd (e.g. 160504)')
parser.add_argument('project_name', help='title of the project being created')
args = parser.parse_args()

#creation of folder tree

#create project folder
project_title = (args.date) + '_' + (args.project_name)
os.mkdir(project_title)
#.csv file folder
csv_folder_name = (args.date) + '_Plates'
csv_folder_path = (project_title) + '/' + (csv_folder_name)
os.mkdir(csv_folder_path)
#graph folder
graph_folder_name = (args.date) + '_Graphs'
graph_folder_path = (project_title) + '/' + (graph_folder_name)
os.mkdir(graph_folder_path)

#preset dilution series
dilution = [5, 2.5, 1.25, 0.625, 0.3125, 0.15625, 0.078125, 0.0390625]

open = pd.read_table(args.txtfile, header=1)
df = pd.DataFrame(open)
df = df.dropna(axis=0)
i = list(range(0, len(df)))
df.index = i
df.columns = ['Rows', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12']

#split txtfile into individual 8x12 plates
i = 0 #cycle counter
p = 1 #plate counter
r = 0 #row counter
for i in range(len(df)):
    if i % 8 == 0:
        plate = pd.DataFrame()
        plate = df.iloc[i:i+8,0:13]
        plate.insert(0,'dilution', dilution)
        csv_plate_name = 'Plate_' + str(p) + '.csv'
        csv_plate_path = (csv_folder_path) + '/' + (csv_plate_name)
        plate.to_csv(csv_plate_path)
        print (('Plate#_') + str(p) + ('.csv file created!'))
        r += 8
        p += 1
print ('All plates successfully written to .csv files \n')

#split txtfile into individual 8x12 plates, average columns, create graph and
#file for each averaged plate
i = 0 #cycle counter
p = 1 #plate counter
r = 0 #row counter
for i in range(len(df)):
    if i % 8 == 0:
        avg_plate = pd.DataFrame()
        c = 1 #column counter
        for i in range(6):
            column = df.iloc[r:r+8,c:c+2]
            avg_plate[i+1] = column.mean(axis=1)
            c += 2
            i += 1
        avg_plate.insert(0,'dilution', dilution)
        csv_file_name = 'PlateAvg_' + str(p) + '.csv'
        csv_file_path = (csv_folder_path) + '/' + (csv_file_name)
        avg_plate.to_csv(csv_file_path)
        graph = avg_plate.set_index('dilution')
        plt.title('PlateAvg_' + str(p))
        #print ('Plate#_' + str(p))
        #print (avg_plate)
        #print (graph.plot.line())
        graph_file_name = 'PlateAvg_' + str(p) + '.png'
        graph_file_path = (graph_folder_path) + '/' + (graph_file_name)
        plt.savefig(graph_file_path)
        print (('PlateAvg_') + str(p) + (' .csv and .png created!'))
        r += 8
        p += 1
print ('All plates successfully averaged and written to .csv and .pgn files!')
print ('\nmds_script finished\n')

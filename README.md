# MSD_Module
Python based module to extract 8x12 data arrays from an MSD output .txt file

This module was created for a class project, though improvements are ongoing.

The purpose of this module is to easily extract raw data from a MesoScaleDiscovery (MSD) Sector Imager 2400 .txt file to create both .csv files of each 8x12 array and an image of the standard curves.

Input: .txt file
Output: (1) Project file tree, (2) .csv files for each 8x12 array of data, (3) .tiff standard curve images

Each 8x12 array represents a 96-well plate that contains an 8-step serial dilution of 6 antibodies in duplicates (12 columns).  I use the .csv files in the application Prism for further statistical analysis.  The graph created for each plate is a quick and dirty way of visualizing each 8x12 array.

Future Aims:
- Spring Cleaning: Sheild your eyes, this code is pretty ugly (hopefully not for too long)
- More Functions: Planty of functions can be added to this module, such as apply antibody names to column titles to specific arrays
- XML Prism File: There's no backend API for Prism to conduct statistical analysis, but a XML file written to a Prism template is the next best thing 

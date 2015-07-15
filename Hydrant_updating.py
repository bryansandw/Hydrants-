# This is the folder that the hydrant pdfs that were converted to txt are located in
folder = r'C:\Users\erentschlar\Desktop\FakeHydrants'

# file that the hydrant outputs is being written into 
# currently appending the existing file this is intended to be a record of what hydrants have been processed
out = r'C:\Users\erentschlar\Desktop\Hydrants.txt'
out1 = open(out, 'a')

# These could be used if you would like to create a new file or overwrite an old file instead of appending to an existing file
# header = 'Date	Flow Hydrant	Pilot Reading	Pitot Reading	Static	Static Hydrant	Residuals	Static_2	Grease1	Paint1	Type	Height	Manufacture Date \n'
# out1.write(header)

# these are where all of the text files in the folder will be referenced
txt_files = []

# Find only the txt files in folder, this will keep the hydrant pdf forms from being processed unnecessarily 
import os, glob
path = folder
for infile in glob.glob( os.path.join(path, '*.txt') ):
        #print("current file is: " + infile) # to check that it is finding them
        txt_files.append(infile)   
#print txt_files # to check that they were all in the list

# Hydro_list will be a list of the hydrants sored as lists, this will allow the information to be accessed by the surch cursor later
hydro_list = []
# The label_list will contain all of the hydrant labels that are in hydro_list, this will allow the code to correctly identify the index of the hydrant
label_list = []
# list1 is the same as the header information, it isn't really nessisary, but without it helps keep the indexing in order
list1 = ['Date','Flow Hydrant','Pilot Reading','Pitot Reading','Static','Static Hydrant','Residuals','Static_2','Grease1','Paint1','Type','Height','Manufacture Date']
hydro_list.append(list1)
# item is index 1, which is the 'Flow Hydrant' which is the same as the hydrant Label
item = list1[1]
label_list.append(item)

# 
for txt in txt_files:
    with open(txt, 'r') as f:
        next(f)
        for str in f:    
            print str
            out1.write(str)
            list = str.split('\t')
            hydro_list.append(list)
            # The labels sould be in A##-###-AA format
            hydro_label = list[1]
            if len(hydro_label) > 10:
                continue
            elif len(hydro_label) > 7:
                label_list.append(hydro_label.upper())
            elif len(hydro_label) == 7:
                hydro_label = hydro_label.upper() + "-FH"
                label_list.append(hydro_label)
            else:
                continue
out1.close()

#################################################################################################
# This is where the ShapeFile will be proccessed with the data that was collected from the PDFs #
#################################################################################################

import arcpy 

hydrants = arcpy.UpdateCursor('Hydrant_Copy')  # path to hydrants shapefile to be updated

# iterate through the features in the shapefile looking for hydrants that in the pdfs
for hydrant in hydrants:
    if hydrant.LABEL in label_list:
        print hydrant.LABEL
        index = label_list.index(hydrant.LABEL)
        # print index # to check that the index was correct
        
        # Defining the hydrant values that will be used to update the shapefile 
        # need to check if they have null values or are wrong data type
        hydrant.FLOW_DATE = hydro_list[index][0] #Should never be null, self fills 
        hydrant.PITOT_PSI = hydro_list[index][2]
        hydrant.PITOT_GPM = hydro_list[index][3]
        hydrant.STATIC_PSI = hydro_list[index][4]
        hydrant.STATIC_HYD = hydro_list[index][5]
        hydrant.RESID_PSI = hydro_list[index][6]
        hydrant.ST_HYD_PSI = hydro_list[index][7]
        
        # not to update shapefile
        #Greased = hydro_list[index][8] 
        #Painted = hydro_list[index][9]
		
        # for updating shapefile 
        if hydro_list[index][8] == 'Yes':
            hydrant.Greased = hydro_list[index][0]
        else:
            pass
        if hydro_list[index][9] == 'Yes':
            hydrant.Painted = hydro_list[index][0]
        else:
            pass
		
        
        # probably wont use these since they are only for new hydrants... what to do with new... 
        Model = hydro_list[index][10]
        HGHT = hydro_list[index][11]
        Manuf_Date = hydro_list[index][12]

		
        print "date: " + hydrant.FLOW_DATE + "    PSI: " + hydrant.PITOT_PSI + "    GPM: " + hydrant.PITOT_GPM + "    Date Greased: " + hydrant.Greased + "    Date Painted: " + hydrant.Painted
        hydrants.updateRow(hydrant)
    else:
        continue
del hydrant,hydrants

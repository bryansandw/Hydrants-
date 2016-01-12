#############################################################################
# Name: Elizabeth Rentschlar                                                #
# Purpose:                                                                  #
# Created: 5/15/15                                                          #
# Copyright: (c) City of Bryan                                              #
# ArcGIS Version: 10.2.2                                                    #
# Python Version: 2.7                                                       #
#############################################################################

import arcpy

# Attempt to create a code to fill the valve fields that are dependent on
# other information within the map

valves = r'C:\Users\erentschlar\Desktop\ToDelete\valve.shp'
rows = arcpy.SearchCursor(valves)
vrows = arcpy.SearchCursor("WATER_VALVES")
mapGrid = r'G:\4_LAYERS\IMAGERY\GRID_INDEX\MAP GRID.lyr'
grid_list = []
number_list = []
label_list = []
#x_list = []
#y_list = []
type_valve = ["AIR RELIEF", "BLOW-OFF", "BUTTERFLY", "GATE"]
label_valve = ["AR", "BO", "VL", "VL"]

list_of_grids = ['V07','V08','V09','U06','U07','U08','U09','U10','T06','T07',
    'T08','T09','T10','T11','S07','S08','S09','S10','S11','S12','R08','R09',
    'R10','R11','R12','Q08','Q09','Q10','Q11','Q12','Q13','Q14','P07','P08',
    'P09','P10','P11','P12','P13','P14','O07','O08','O09','O10','O11','O12',
    'O13','O14','N07','N08','N09','N10','N11','N12','N13','N14','M07','M08',
    'M09','M10','M11','M12','L04','L05','L07','L08','L09','L10','L11','K04',
    'K05','K07','K08','K09','K10','K11','J04','J05','J06','J07','J09','I05',
    'I06']	
list_of_valve = ["AR", "BO", "VL"]

list_of_list = []
for grid in list_of_grids:
    new_list = [[], [], []]
    list_of_list.append(new_list)	
	
#print list_of_list

#compiles lists of all the numbers present in 
for vrow in vrows:
    item = vrow.GRID_ID 
    number = vrow.NUMBER
    label_id = vrow.LABEL_ID

    if item != ' ':
        num = int(number)	
	    #finds the list that is associated with the grid and valve to put the
	    #number in 
        x = list_of_grids.index(item)
        y = list_of_valve.index(label_id)
        
        list_of_list[x][y].append(num)
        #print list_of_list[x][y]
    else:
        pass
del vrows
print "f1 worked"

#rows = arcpy.SearchCursor(valves)
#rows = arcpy.SearchCursor("sde.GIS_ADMIN.COB_WATER_VALVES")


# create a list of the values that will later be placed in the valve fields
for row in rows:
    item = row.GRID_ID 
    number = row.NUMBER
    label_id = row.LABEL_ID
    ctype = row.COMP_TYPE
    fid = row.FID
    #x_coord = row.X_COORD
    #y_coord = row.Y_COORD
	
    expression = '"FID" = ' + str(fid) 
    	
	
    if item == ' ':
        # need to iterate through the valves that do not have grid ids, then 
        # have to select the grid map grid by location, thereby finding the 
        # grid id that will be use to update the valve fields
        valve = arcpy.SelectLayerByAttribute_management("valve","NEW_SELECTION", expression)
        this = arcpy.SelectLayerByLocation_management('MAP GRID', "INTERSECT",valve)
        thisIS = arcpy.SearchCursor(this)
        for IS in thisIS:
            grid = IS.GRID_ID
        grid_list.append(grid)
        
		# the user will need to manually input the COMP_TYPE and the code uses 
		# a dictionary to determine what the Label id should be
        label = label_valve[type_valve.index(ctype)]
        label_list.append(label)

		
		#checking my code
        print "This is the yes grid " + grid 
        
        #  pulls the max number and adds 1 for the grid and valve type       
        x = list_of_grids.index(grid)
        y = list_of_valve.index(label)
        
        list_max = max(list_of_list[x][y])
        new_number = list_max + 1
        number_list.append(new_number)
		
		
		#Deleteing varables in to loop just in case
        del label
        del grid
        del thisIS
        #del ID
        #del gID
    else:
        print "This is the no item " + item 
        grid_list.append(item)
        label_list.append(label_id)
        number_list.append(number)

del rows
print grid_list
print label_list
print number_list


#This is where the fields are updated 
expression2 = '"GRID_ID" = ' + "'*'"
arcpy.SelectLayerByAttribute_management("valve","NEW_SELECTION", expression2)
features = arcpy.UpdateCursor(valves)
i = 0
for feature in features:
    grid_id = grid_list[i]
    label_id2 = label_list[i]
    # get the number in the right format 
    number2 = number_list[i]
    if number2 < 10:
        number3 = '00' + str(number2)
    elif number2 < 100:
        number3 = '0' + str(number2)
    else:
        number3 =  str(number2)
    feature.LABEL_ID = label_id2
    feature.GRID_ID = grid_id
    feature.NUMBER = number3
    feature.LABEL = feature.GRID_ID + '-' + feature.NUMBER + '-' + feature.LABEL_ID
    print feature.LABEL
    features.updateRow(feature)
    i = i + 1
del features
del grid_list
del label_list
del number_list
	

# Hydrants
A python script for use in ArcMap to update the the hydrant shapefile with data that was exported from Adobe PDFs.

The paths are currently hard coded. 

# How to use a script to update the hydrants feature with the data from the hydrant flow forms pdfs. 
There are two active steps that the user will need to perform, running the javascript in Adobe and the python script in ArcMap.

# Adobe:
To run the JavaScript the user must have Acrobat on their computer.
The first time the user does this they will need to set the tool up in acrobat:
  1.	In the upper right hand corner of a document click on tools.  This will open a table of contents of the tool types available in Acrobat.  
  2.	Select the Action Wizard drop down.  
  3.	Create a New Action.  
  4.	On the left select More Tools and Execute JavaScript.  It should appear on the right side of the window. 
  5.	Click on Specify Setting.  This will open a pop up window where the JavaScript should be input.  The JavaScript:

//To be located in a folder level Action Wizard in Adobe Acrobat for Hydrant Flow Report forms
var FileName_str = this.documentFileName.slice(0, this.documentFileName.indexOf("."));
var aFields = ["Date", "Flow Hydrant", "Pilot Reading", "Pitot Reading", "Static", "Static Hydrant", "Residuals", "Static_2", "Grease1", "Paint1", "Type", "Height", "Manufacture Date"];
this.exportAsText(true, aFields, FileName_str + '.txt');

  6.	Click ok to close the window.
  7.	Unselect Prompt User.
  8.	On the top of the right side click on the folder icon and navigate to the folder that the hydrant pdfs are or will be stored in while being processed.
  9.	Clicking Save will prompt you to Name the Action and provide a description of the action.  You can name it whatever you like, mine is “Hydrants” and “Use to pre-process the pdf data into a format that is usable for python. 
  10.	The tool will now be accessible under the Action Wizard drop down for you to use.
For the JavaScript to work there can be no documents of a type other than pdf in the folder.  When the JavaScript finishes running there will txt files with the same names as the pdfs in the hydrant folder that was processed.  

# ArcMap:
To run the python script you will first need to open the Hydrant mxd. If you do not already have the python window open in ArcMap open it by toggling the python window button.  

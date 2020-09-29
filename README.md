# RenameSequence
My own sequence renaming tool in Nuke
Here's a screenshot of how it looks like: 
![Image of Yaktocat](https://user-images.githubusercontent.com/44877614/94612148-8c0cee00-0257-11eb-88db-a0fecc274554.png)


How To Install:

Put the two files and the icon file into your user .nuke folder

How To Use:

You will see a Rename tool icon on the menubar, go into it, click on the Rename Sequence while selecting a node to see the hot boxes appear.

The source file name displays in the source area into three setions: file name, delimiter and padding. 

File name is the name of the sequence, you can add or change version number here.
Delimiter is symbol used to seperate the sequence name and the frame number.
Padding shows how many digits in the frame number. It's shown in the form of "#" or "%01d", if you have 3 digits frame number it will be "###" or "%03d".

You can change these three parts of the sequence name by modifying the text in the Destination are.
Default input is set the same as the source file.

Click on Preview to make sure the destination file name is correct before running.

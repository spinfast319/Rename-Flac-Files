# Rename-Flac-Files
### This python script loops through a directory and looks for files that are flac, when it finds them it uses the Vorbis tags to rename the file to a specific format.

It has two different templates that can be used, and someone could easily tweak the code to make the format whatever it is they prefer. The two formats that come set up are:

```
Track Number - Title.flac
Track Number - Artist - Title.flac
```
If there are multi-disc files all in one folder rather than a sub-folder it will append a _Disc Number_ in front of the _Track Number_ so the tracks are ordered correctly. It also will add leading zeroes to single digit numbers which do not have them and will replace illegal windows characters with alternatives. It logs both the original and new name of all the tracks it changes in a log file. 

It can handle albums with artwork folders or multiple disc folders in them. It can also handle specials characters. It has been tested and works in both Ubuntu Linux and Windows 10. You will need to install the mutagen library with pip for it to work.

You may want to run the [Find Missing Tags Script](https://github.com/spinfast319/Find-Missing-Tags) prior to running this one to make sure all the albums have the needed tags before you try and rename them.

## Install and set up
1) Clone this script where you want to run it.

2) Install [mutagen](https://pypi.org/project/mutagen/) with pip. (_note: on some systems it might be pip3_) 

to install it:

```
pip install mutagen
```

3) Edit the script where it says _Set your directories here_ to set up or specify two directories you will be using. Write them as absolute paths for:

    A. The directory where the albums you want to examine for missing tags are stored  
    B. The directory to store the log files the script creates  

4) Edit the script where it says _Set your file name template here_ to specify which pattern you want the files to be renamed in 

    A. If you want your tracks to be _Track Number - Title.flac_ leave this value set to 1  
    B. If you want your tracks to be _Track Number - Artist - Title.flac_ set this value to 2

5) Use your terminal to navigate to the directory the script is in and run the script from the command line.  When it finishes it will output how many tracks were renamed.

```
Rename-Flac-Files.py
```

_note: on linux and mac you will likely need to type "python3 Rename-Flac-Files.py"_  
_note 2: you can run the script from anywhere if you provide the full path to it_

The script will also create a log listing all the tracks it renamed and include the original name and the new name.  

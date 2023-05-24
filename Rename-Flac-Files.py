#!/usr/bin/env python3

# Rename Files
# author: hypermodified
# This python script loops through a directory and looks for files that are flac, when it finds them it uses the Vorbis tags to rename the file to a specific format.
# This has only been tested to work with flac files.
# It can handle albums with artwork folders or multiple disc folders in them. It can also handle specials characters.
# It has been tested and works in both Ubuntu Linux and Windows 10.

# Before running this script install the dependencies
# pip install mutagen

# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import datetime  # Imports functionality that lets you make timestamps
import mutagen  # Imports functionality to get metadata from music files

import origin_script_library as osl  # Imports common code used across all origin scripts

#  Set your directories here
album_directory = "M:\PROCESS"  # Which directory do you want to start with?
log_directory = "M:\PROCESS-LOGS\Logs"  # Which directory do you want the log in?

# Set your file name template here
# 1 will rewrite the tracks to Track Number - Title
# 2 will rewrite the track to Track Number - Artist - Title
file_template = 1

# Establishes the counters for completed albums and missing origin files
count = 0
total_count = 0

# A function to log events
def log_outcomes(directory, log_name, message, log_list):
    global log_directory

    script_name = "Rename Files"
    today = datetime.datetime.now()
    log_name = f"{log_name}.txt"
    album_name = directory.split(os.sep)
    album_name = album_name[-1]
    log_path = os.path.join(log_directory, log_name)
    with open(log_path, "a", encoding="utf-8") as log_name:
        log_name.write(f"--{today:%b, %d %Y} at {today:%H:%M:%S} from the {script_name}.\n")
        log_name.write(f"The album folder {album_name} {message}.\n")
        log_name.write("\n".join(map(str, log_list)))
        log_name.write(f"\nAlbum location: {directory}\n")
        log_name.write(" \n")
        log_name.close()


# A function that writes a summary of what the script did at the end of the process
def summary_text():
    global count
    global total_count

    print("")
    print(f"This script renamed {count} tracks after searching through {total_count} folders.")


#  A function to replace illegal characters in the windows operating system
#  For other operating systems you could tweak this for their illegal characters
def cleanFilename(file_name):
    if not file_name:
        return ""
    badchar1 = '"'
    badchar2 = "?"
    badchar3 = ":"
    badchar4 = "*"
    badchar5 = "|"
    badchar6 = "<"
    badchar7 = ">"
    badchar8 = "\\"
    badchar9 = "/"
    for c in badchar1:
        file_name = file_name.replace(c, "＂")
    for c in badchar2:
        file_name = file_name.replace(c, "？")
    for c in badchar3:
        file_name = file_name.replace(c, "：")
    for c in badchar4:
        file_name = file_name.replace(c, "＊")
    for c in badchar5:
        file_name = file_name.replace(c, "｜")
    for c in badchar6:
        file_name = file_name.replace(c, "＜")
    for c in badchar7:
        file_name = file_name.replace(c, "＞")
    for c in badchar8:
        file_name = file_name.replace(c, "＼")
    for c in badchar9:
        file_name = file_name.replace(c, "／")
    return file_name


"""# Keeping this function in case i want to refactor the next one and use ideas from it
# A function to remove any null values from track numbers
def clean_track_number(track_number):
    each_char = list(track_number)
    clean_track = []
    for i in each_char:
        try:
            int(i)
            clean_track.append(i)
        except:
            print("Bad Character Found")
            continue
    track_number = ''.join(clean_track)
    return track_number"""

# A function to remove any null values from strings
def clean_string_null(string_to_clean):
    each_char = list(string_to_clean)
    clean_track = []
    for i in each_char:
        if i == "\x00":
            print("--Bad character removed")
        else:
            clean_track.append(i)
    clean_string = "".join(clean_track)
    return clean_string


# A function to add a leading zero if it is missing, avoiding vinyl names
def add_leading_zero(track_number):
    each_char = list(track_number)
    num_list = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    if each_char[0] in num_list:
        track_number_length = len(track_number)
        # Add leading zero to track if the zero is missing
        if track_number_length == 1:
            track_number = "".join(["0", track_number])
            print("--Leading zero added.")
            return track_number
        else:
            return track_number
    else:
        return track_number

# A function to remove the / symbol and anything following it from track numbers
def remove_slash(track_number):
    if '/' in track_number:
        return track_number.split('/')[0]
    else:
        return track_number
        


# A function to check if there are more than one discs worth of tracks in one folder
def multidisc_check(directory):
    print("--Checking if multi-disc.")
    disc_number_set = set()

    # Loop through the directory and check if there is more than one disc number
    for fname in os.listdir(directory):
        if fname.lower().endswith(".flac"):
            meta_data = mutagen.File(fname)
            if "discnumber" in meta_data:
                disc_number = meta_data["discnumber"][0]
                disc_number_set.add(disc_number)

    disc_number_set_length = len(disc_number_set)
    if disc_number_set_length > 1:
        return True
    else:
        return False


# A function to write a new file name based on the metadata of the track
def rename_file(directory, multidisc_status):
    global count
    global file_template

    print("--Renaming files.")
    # Clear the list so the log captures just this albums tracks
    rename_list = []

    # Loop through the directory and rename flac files
    for fname in os.listdir(directory):
        if fname.lower().endswith(".flac"):
            meta_data = mutagen.File(fname)
            print(f"--Old Name: {fname}")
            # log old name
            rename_list.append(f"--Old Name: {fname}")

            # clean null characters out of track number, artist and title strings
            # set variables
            track_number = meta_data["TRACKNUMBER"][0]
            artist = meta_data["ARTIST"][0]
            title = meta_data["TITLE"][0]
            if multidisc_status == True:
                disc_number = disc_number = meta_data["DISCNUMBER"][0]
            # clean variables
            track_number = clean_string_null(track_number)
            artist = clean_string_null(artist)
            title = clean_string_null(title)
            if multidisc_status == True:
                disc_number = clean_string_null(disc_number)
                
            # reformat track numbers that are formatted 01/12 to 01 
            track_number = remove_slash(track_number)
            if multidisc_status == True:
                disc_number = remove_slash(disc_number)    
                
            # add leading zero to track if needed
            track_number = add_leading_zero(track_number)
            if multidisc_status == True:
                disc_number = add_leading_zero(disc_number)    

            # Write clean and formatted track number as new metadata to track
            meta_data["TRACKNUMBER"] = track_number
            meta_data["ARTIST"] = artist
            meta_data["TITLE"] = title
            if multidisc_status == True:
                meta_data["DISCNUMBER"] = disc_number
            meta_data.save()

            # Set new name using file template
            if multidisc_status == False:
                if file_template == 1:
                    new_name = f"{meta_data['TRACKNUMBER'][0]} - {meta_data['TITLE'][0]}.flac"
                elif file_template == 2:
                    new_name = f"{meta_data['TRACKNUMBER'][0]} - {meta_data['ARTIST'][0]} - {meta_data['TITLE'][0]}.flac"
            elif multidisc_status == True:
                if file_template == 1:
                    new_name = f"{meta_data['DISCNUMBER'][0]} - {meta_data['TRACKNUMBER'][0]} - {meta_data['TITLE'][0]}.flac"
                elif file_template == 2:
                    new_name = f"{meta_data['DISCNUMBER'][0]} - {meta_data['TRACKNUMBER'][0]} - {meta_data['ARTIST'][0]} - {meta_data['TITLE'][0]}.flac"

            # Clean the filename of any banned characters
            new_name = cleanFilename(new_name)

            print(f"--New Name: {new_name}")
            # log new name
            rename_list.append(f"--New Name: {new_name}")

            # Rename the file
            os.rename(fname, new_name)
            count += 1  # variable will increment every loop iteration

    # figure out how many tracks were renamed
    tracks_renamed = len(rename_list) / 2
    if tracks_renamed != 0:
        print(f"--Tracks Renamed: {tracks_renamed:g}")
    else:
        print(f"--There were no flac in this folder.")
    # log the album the name change
    log_name = "files_renamed"
    log_message = f"had {tracks_renamed:g} files renamed"
    log_list = rename_list
    log_outcomes(directory, log_name, log_message, log_list)
    

# The main function that controls the flow of the script
def main():
    global total_count

    try:
        # intro text
        print("")
        print("Now you see me...")
  
        # Get all the subdirectories of album_directory recursively and store them in a list:
        directories = osl.set_directory(album_directory)

        #  Run a loop that goes into each directory identified in the list and runs the function that renames the files
        for i in directories:
            os.chdir(i)  # Change working Directory
            total_count += 1  # variable will increment every loop iteration
            print("")
            print("Processing files.")
            print(f"Directory: {i}")
            # Check to see if multi-disc processing is needed
            multidisc_status = multidisc_check(i)
            # Rename the files in the directory based on the global template
            rename_file(i, multidisc_status)

    finally:
        # Summary text
        print("")
        print("...now you don't")
        # run summary text function to provide error messages
        summary_text()
        print("")


if __name__ == "__main__":
    main()

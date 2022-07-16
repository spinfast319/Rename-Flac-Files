# Rename Files
# author: hypermodified
# This python script loops through a directory and looks for files that are flac, when it finds them it uses the Vorbis tags to rename the file to a specific format.
# It can handle albums with artwork folders or multiple disc folders in them. It can also handle specials characters.
# It has been tested and works in both Ubuntu Linux and Windows 10.

# Before running this script install the dependencies
# pip install mutagen

# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import shutil  # Imports functionality that lets you copy files and directory
import datetime  # Imports functionality that lets you make timestamps
import mutagen  # Imports functionality to get metadata from music files

#  Set your directories here
album_directory = "M:\Python Test Environment\Albums"  # Which directory do you want to start with?
log_directory = "M:\Python Test Environment\Logs"  # Which directory do you want the log in?

# Set whether you are using nested folders or have all albums in one directory here
# If you have all your ablums in one music directory Music/Album_name then set this value to 1
# If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2
# The default is 1
album_depth = 1

# Set your file name template here
# 1 will rewrite the tracks to Track Number - Title
# 2 will rewrite the track to Track Number - Artist - Title
file_template = 2

# Establishes the counters for completed albums and missing origin files
count = 0
total_count = 0
error_message = 0
tags_missing = 0

# identifies album directory level
path_segments = album_directory.split(os.sep)
segments = len(path_segments)
album_location = segments + album_depth

# A function to log events
def log_outcomes(directory, log_name, message):
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
        log_name.write(f"Album location: {directory}\n")
        log_name.write(" \n")
        log_name.close()


# A function that determines if there is an error
def error_exists(error_type):
    global error_message

    if error_type >= 1:
        error_message += 1  # variable will increment if statement is true
        return "Warning"
    else:
        return "Info"


# A function that writes a summary of what the script did at the end of the process
def summary_text():
    global count
    global total_count
    global error_message
    global tags_missing

    print("")
    print(f"This script renamed {count} tracks from {total_count} albums.")
    print("This script looks for potential missing files or errors. The following messages outline whether any were found.")

    error_status = error_exists(tags_missing)
    print(f"--{error_status}: There were {tags_missing} albums missing either track number, title, artist or album tags. They were moved to the Missing Tags folder.")

    if error_message >= 1:
        print("Check the logs to see any errors.")
    else:
        print("There were no errors.")


# A function to check whether the directory is a an album or a sub-directory
def level_check(directory):
    global total_count
    global album_location

    print("")
    print(directory)
    print("Folder Depth:")
    print(f"--The albums are stored {album_location} folders deep.")

    path_segments = directory.split(os.sep)
    directory_location = len(path_segments)

    print(f"--This folder is {directory_location} folders deep.")

    # Checks to see if a folder is an album or subdirectory by looking at how many segments are in a path
    if album_location == directory_location:
        print("--This is an album.")
        total_count += 1  # variable will increment every loop iteration
        return True
    elif album_location < directory_location:
        print("--This is a sub-directory")
        return False
    elif album_location > directory_location and album_depth == 2:
        print("--This is an artist folder.")
        return False


# A function to check whether a directory has flac and should be checked further
def flac_check(directory):

    # Loop through the directory and see if any file is a flac
    for fname in os.listdir(directory):
        if fname.endswith(".flac"):
            print("--There are flac in this directory.")
            return True
        else:
            print("--There are no flac in this directory.")
            return False


# A function to check the tags of each file and sort it if critical tags are missing
def rename_file(directory, is_album):
    global count
    global file_template

    # Loop through directory and rename flac files
    for fname in os.listdir(directory):
        if fname.endswith(".flac"):
            meta_data = mutagen.File(fname)
            print(f"Old Name: {fname}")
            track_number = meta_data["tracknumber"][0]
            track_number_length = len(track_number)
            # Add leading zero to track if the zero is missing
            if track_number_length == 1:
                track_number = "".join(["0", track_number])
                # Write track number as new metadata to track
                meta_data["tracknumber"] = track_number
                meta_data.save()
            # Set file template
            if file_template == 1:
                new_name = f"{meta_data['tracknumber'][0]} - {meta_data['title'][0]}.flac"
            elif file_template == 2:
                new_name = f"{meta_data['tracknumber'][0]} - {meta_data['artist'][0]} - {meta_data['title'][0]}.flac"
            # Rename the file
            print(f"New Name: {new_name}")
            os.rename(fname, new_name)
            count += 1  # variable will increment every loop iteration


# The main function that controls the flow of the script
def main():

    try:
        # intro text
        print("")
        print("Now you see me...")
        print("")
        print("Part 1: Sorting")

        # Get all the subdirectories of album_directory recursively and store them in a list:
        directories = [os.path.abspath(x[0]) for x in os.walk(album_directory)]
        directories.remove(os.path.abspath(album_directory))  # If you don't want your main directory included

        #  Run a loop that goes into each directory identified in the list and runs the function that sorts the folders
        for i in directories:
            os.chdir(i)  # Change working Directory
            # establish directory level
            is_album = level_check(i)
            # check for flac
            is_flac = flac_check(i)
            # check for meta data and sort
            if is_flac == True:
                rename_file(i, is_album)

    finally:
        # Summary text
        print("")
        print("...now you don't")
        # run summary text function to provide error messages
        summary_text()
        print("")


if __name__ == "__main__":
    main()

# Rename Files
# author: hypermodified
# This python script loops through a directory and looks for files that are flac, when it finds them it uses the Vorbis tags to rename the file to a specific format.
# It can handle albums with artwork folders or multiple disc folders in them. It can also handle specials characters.
# It has been tested and works in both Ubuntu Linux and Windows 10.

# Before running this script install the dependencies
# pip install mutagen

# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import datetime  # Imports functionality that lets you make timestamps
import mutagen  # Imports functionality to get metadata from music files

#  Set your directories here
album_directory = "M:\Python Test Environment\Albums"  # Which directory do you want to start with?
log_directory = "M:\Python Test Environment\Logs"  # Which directory do you want the log in?

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
        log_name.write('\n'.join(map(str, log_list)))
        log_name.write(f"\nAlbum location: {directory}\n")
        log_name.write(" \n")
        log_name.close()


# A function that writes a summary of what the script did at the end of the process
def summary_text():
    global count
    global total_count

    print("")
    print(f"This script renamed {count} tracks after searching through {total_count} folders.")


# A function to check the tags of each file and sort it if critical tags are missing
def rename_file(directory):
    global count
    global file_template

    print("")
    print("Renaming files.")
    print(f"Directory: {directory}")
    #Clear the list so the log captures just this albums tracks
    rename_list = []

    # Loop through the directory and rename flac files
    for fname in os.listdir(directory):
        if fname.endswith(".flac"):
            meta_data = mutagen.File(fname)
            print(f"--Old Name: {fname}")
            # log old name
            rename_list.append(f"--Old Name: {fname}")
            
            #determine whether track needs leading zero by looking at length
            track_number = meta_data["tracknumber"][0]
            track_number_length = len(track_number)
            # Add leading zero to track if the zero is missing
            if track_number_length == 1:
                track_number = "".join(["0", track_number])
                # Write track number as new metadata to track
                meta_data["tracknumber"] = track_number
                meta_data.save()
                
            # Set new name using file template
            if file_template == 1:
                new_name = f"{meta_data['tracknumber'][0]} - {meta_data['title'][0]}.flac"
            elif file_template == 2:
                new_name = f"{meta_data['tracknumber'][0]} - {meta_data['artist'][0]} - {meta_data['title'][0]}.flac"

            print(f"--New Name: {new_name}")
            # log new name
            rename_list.append(f"--New Name: {new_name}")
            
            # Rename the file
            os.rename(fname, new_name)
            count += 1  # variable will increment every loop iteration
    
    #figure out how many tracks were renamed
    tracks_renamed = len(rename_list)/2    
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
        directories = [os.path.abspath(x[0]) for x in os.walk(album_directory)]
        directories.remove(os.path.abspath(album_directory))  # If you don't want your main directory included

        #  Run a loop that goes into each directory identified in the list and runs the function that renames the files
        for i in directories:
            os.chdir(i)  # Change working Directory
            total_count += 1  # variable will increment every loop iteration
            # Rename the files in the directory based on the global template
            rename_file(i)

    finally:
        # Summary text
        print("")
        print("...now you don't")
        # run summary text function to provide error messages
        summary_text()
        print("")


if __name__ == "__main__":
    main()

"""
Overview
     
     This program allows for system tray icons to be animated, like a GIF is playing in
     the system tray. Any png/jpg/jpeg images can be used and displayed.

Recommended usage
     
     The way I use this program is to find a GIF I'd like to display in the tray and then
     follow the steps below to split the GIF into seperate png/jpg files. This method doesn't
     have to be followed and any images can be used (don't have to be frames from a GIF)

     - to convert gif to png/jpg use: http://animizer.net/en/gif-apng-splitter
     - the output frames will have to the names frame-001.png, frame-002.png etc
     - to rename frame-001.png, frame-002.png etc.  to frame-1.png, frame-2.png etc. (which is the required format, notice the file extension IS included in the name) use the following command in the frames directory. Change .png to .jpg/.jpeg in the command if needed.
     - find -name '*.png' | awk 'BEGIN{ a=0 }{ printf "mv \"%s\" %s%d.png\n", $0, "frame-", a++ }' | bash
	 
     ! sometimes the command fails on the first run, if it does fail: delete the output files and run the command again on a copy of the frames

Requirements

     - python-gtk2 package (Ubuntu repo name)
     - python 2
     - an absolute directory path must be given with the -p (--path-to-frames) argument
"""

from sys import exit
import gobject # for callbacks
import gtk
import argparse
import fnmatch # counting number of frames
import os # counting frames in supplied dir

class StatusIconAnimator():
    """
    Allows an icon to be shown in the system tray which changes
    frames over time	
    """

    frame_paths = [] # holds the absolute paths to each frame of the animation
    frame_format = ".png" # defaults to PNG, can also use JPG
    frame_filename_prefix = "frame-"

    frame_time = 300
    num_of_frames = None
    icon = gtk.StatusIcon() # the system tray icon to be used for the animation
    frame_counter = 1

    def __init__(self):
        """
        Initialises all the neccessary variables needed
        to display the frames in the system tray properly and 
        aborts the program if something is wrong
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("-p", "--path-to-frames",  help="The absolute path to the frames. For example: /home/USER/.icons/status_icons/my_frames/ The frames must follow this naming convention: frame-<NUMBER>.<FORMAT>\nWhere <NUMBER> starts at 0 and is incremented by 1 for the next frame and so on. <FORMAT> will default to png if no format is supplied\nFor example a 3 frame PNG sequence should have the filenames: frame-0.png, frame-1.png, frame-2.png")
        parser.add_argument("-f", "--filetype", help="Specify the image format for the frames. Valid options: png, jpg, jpeg. Default is png.")
        parser.add_argument("-t", "--time-per-frame", help="Specify the time for each frame to be shown in milliseconds. Default is 300ms.", type=int)
        parser.add_argument("-b", "--blank-icon", help="Creates a blank icon in the system tray to act as a spacer.", action="store_true")
        args = parser.parse_args()

        if args.blank_icon: # icon is already blank
            return

        if args.path_to_frames == None:
            print("Absolute path to the frames must be specified with the -p option.\nAborting...")
            exit(-1)

        if args.filetype == "jpg":
            self.frame_format = "." + args.filetype
        elif args.filetype == "jpeg":
            self.frame_format = "." + args.filetype
       
        self.num_of_frames = len(fnmatch.filter(os.listdir(args.path_to_frames), self.frame_filename_prefix + "*" + self.frame_format)) # count number of frames in the supplied directory
        if self.num_of_frames == 0:
            print("Error: No suitable frames found in " + args.path_to_frames + "\nAborting...")
            exit(-1)

        if args.time_per_frame:
            self.frame_time = args.time_per_frame
            if self.frame_time < 10:
                print("Warning: A low time per frame value will lead to high CPU usage.")

        frame_path_prefix = args.path_to_frames + self.frame_filename_prefix
        for i in range(1, self.num_of_frames + 1): # setup correct path names
            self.frame_paths.append(frame_path_prefix + str(i) + self.frame_format)

        if self.num_of_frames == 1: # we don't need callbacks if only one frame has been supplied so just set icon and return
            self.icon.set_from_file(self.frame_paths[0])
            return

        gobject.timeout_add(self.frame_time, self.update_frame) # callback from gtk.main()
        return

    def update_frame(self):
        """
        Changes the icons image to the next frame
        when called via the callback
        """
        print("counter: " + str(self.frame_counter))

        if self.frame_counter == self.num_of_frames: # otherwise potential overflow
            self.frame_counter = 0 
		
        self.icon.set_from_file(self.frame_paths[self.frame_counter % self.num_of_frames]) # updates the icon with the next frame. Loops to start if at the last frame

        self.frame_counter += 1
        return True

if __name__=='__main__':
    animator = StatusIconAnimator()
    gtk.main() # main loop

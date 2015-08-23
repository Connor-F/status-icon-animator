"""
Overview

	 - to convert gif to png/jpg use: http://animizer.net/en/gif-apng-splitter
	 - the output frames will have to the names frame-001.png, frame-002.png etc
	 - to rename frame-001.png to frame-1.png (which is the required format) use the following command in the frames directory. Change .png to .jpg/.jpeg in the command if needed.
	 - find -name '*.png' | awk 'BEGIN{ a=0 }{ printf "mv \"%s\" %s%d.png\n", $0, "frame-", a++ }' | bash
	 - sometimes the command fails on the first run, if it does delete the output files and run the command again on a copy of the frames
"""

import gobject # for callbacks
import gtk
import argparse
import fnmatch # for counting number of frames
import os # for counting number of frames

class StatusIconAnimator():
    """
    Allows an icon to be shown in the system tray which changes
    frames over time	
    """

    frame_paths = [] # holds the absolute paths to each frame of the animation
    frame_format = ".png" # defaults to PNG, can also use JPG
    frame_filename_prefix = "frame-"

    frame_time = 300
    num_of_frames = -1
    icon = gtk.StatusIcon() # the system tray icon to be used for the animation
    frame_counter = 0

    def __init__(self):
        """
        Initialises all the neccessary variables needed
        to display the frames in the system tray properly
        """

        parser = argparse.ArgumentParser()
        parser.add_argument("path_to_frames", help="The absolute path to the frames. For example: /home/USER/.icons/status_icons/my_frames/ The frames must follow this naming convention: frame-<NUMBER>.<FORMAT>\nWhere <NUMBER> starts at 0 and is incremented by 1 for the next frame and so on. <FORMAT> will default to png if no format is supplied\nFor example a 3 frame PNG sequence should have the filenames: frame-0.png, frame-1.png, frame-2.png")
        parser.add_argument("-f", "--filetype", help="Specify the image format for the frames. Valid options: png, jpg, jpeg. Default is png.")
        parser.add_argument("-t", "--time-per-frame", help="Specify the time for each frame to be shown in milliseconds. Default is 300ms.", type=int)
        args = parser.parse_args()

        if args.time_per_frame:
            self.frame_time = args.time_per_frame
            if self.frame_time < 10:
                print("Warning: A low time per frame value will lead to high CPU usage")
        if args.filetype == "jpg":
		    self.frame_format = "." + args.filetype
        elif args.filetype == "jpeg":
		    self.frame_format = "." + args.filetype

        frame_path_prefix = args.path_to_frames + self.frame_filename_prefix
        self.num_of_frames = len(fnmatch.filter(os.listdir(args.path_to_frames), self.frame_filename_prefix + "*" + self.frame_format)) # count number of frames in the supplied directory

        for i in range(0, self.num_of_frames): # setup correct path names
            self.frame_paths.append(frame_path_prefix + str(i) + self.frame_format)

        gobject.timeout_add(self.frame_time, self.update_frame) # callback from gtk.main()
        return


    def update_frame(self):
        """
        Changes the icons image to the next frame
        """

        if self.frame_counter == self.num_of_frames: # otherwise potential overflow
		    self.frame_counter = 0 
		
        self.icon.set_from_file(self.frame_paths[self.frame_counter % self.num_of_frames]) # updates the icon with the next frame. Loops to start if at the last frame

        self.frame_counter += 1
        return

if __name__=='__main__':
    animator = StatusIconAnimator()
    gtk.main() # main loop

# automatically count number of frames in supplied path with the correct name/file ext.

import gobject # for callbacks
import gtk
import argparse
import fnmatch # for counting number of frames
import os # for counting number of frames

class StatusIconAnimator():
    frame_paths = [] # holds the absolute paths to each frame of the animation
    frame_format = ".png" # defaults to PNG, can also use JPG
    frame_filename_prefix = "frame-"

    frame_time = 300
    num_of_frames = -1
    icon = gtk.StatusIcon() # the system tray icon to be used for the animation
    frame_counter = 0

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("path_to_frames", help="The absolute path to the frames. For example: /home/USER/.icons/status_icons/my_frames/ The frames must follow this naming convention: frame-<NUMBER>.<FORMAT>\nWhere <NUMBER> starts at 0 and is incremented by 1 for the next frame and so on. <FORMAT> will default to png if no format is supplied\nFor example a 3 frame PNG sequence should have the filenames: frame-0.png, frame-1.png, frame-2.png")
        parser.add_argument("-f", "--filetype", help="Specify the image format for the frames. Valid options: png (default) or jpg")
        parser.add_argument("-t", "--time-per-frame", help="Specify the time for each frame to be shown in milliseconds. Default is 300ms.", type=int)
        args = parser.parse_args()

        if args.time_per_frame:
		    frame_time = args.time_per_frame
        if args.filetype == "jpg":
		    frame_format = "." + args.filetype
        elif args.filetype == "jpeg":
		    frame_format = "." + args.filetype

        frame_path_prefix = args.path_to_frames + self.frame_filename_prefix
# todo regex the wildcard to be any number instead of anything, also maybe make a function to make sure frames are in consecutive order
        self.num_of_frames = len(fnmatch.filter(os.listdir(args.path_to_frames), self.frame_filename_prefix + "*" + self.frame_format)) # count number of frames in the supplied directory

        for i in range(0, self.num_of_frames): # setup correct path names
            self.frame_paths.append(frame_path_prefix + str(i) + self.frame_format)

        gobject.timeout_add(self.frame_time, self.update_frame) # callback from gtk.main()
        return


    def update_frame(self):
        if self.frame_counter == self.num_of_frames: # otherwise potential overflow
		    self.frame_counter = 0 
		
        print("frame_counter: " + str(self.frame_counter) + "     mod: " + str(self.frame_counter % self.num_of_frames))
        self.icon.set_from_file(self.frame_paths[self.frame_counter % self.num_of_frames]) # updates the icon with the next frame. Loops to start if at the last frame

        if self.frame_counter != self.num_of_frames: # now increment
		    self.frame_counter += 1

        return True


if __name__=='__main__':
    animator = StatusIconAnimator()
    gtk.main()

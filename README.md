#GTK Status Icon Animator

- Creates a system tray icon that continually updates its icon according to the supplied frames. Making it appear as if there is an animation in your system tray.
- Single frames can be supplied to create just a static icon. 
- Blank icons can also be created via the `-b` or `--blank-icon` option.
  - Both single frame and blank icons with not refresh the frame and therefore won't waste CPU cycles.

**Example usage**

`python status_icon_animator.py -p /home/USER/.icons/status_icons/my_frames/ -t 400 -f jpg`
Where the `my_frames` directory contains all the jpg images that you'd like to display

**Required arguments**
`-p` or `--path-to-frames` Specify the ABSOLUTE path to the frames. For example: `/home/USER/.icons/status_icons/my_frames/` 
The frames must follow this naming convention: frame-<NUMBER>.<FORMAT> Where <NUMBER> starts at 0 and is incremented by 1 for the next frame and so on. 
<FORMAT> will default to png if no format is supplied
For example a 3 frame PNG sequence should have the filenames: frame-0.png, frame-1.png, frame-2.png 

**Options**
`-t` or `--time-per-frame` Specify the time in milliseconds each frame should be shown in the system tray. Default is 300ms.
`-f` or `--filetype` Specify the filetype of the images to be used. Valid options: png, jpg, jpeg. Default is png.
`-b` or `--blank-icon` This will create a blank icon in the system tray which is useful for creating `spacer` icons.

**Tested with**
- i3 bar
- xfce bar

## i3 bar
![alt tag](http://i.imgur.com/91ZtDHE.gif)

![alt tag](http://i.imgur.com/a71g9Uq.gif)

![alt tag](http://i.imgur.com/zJJGyKV.gif)

## xfce bar
![alt tag](http://i.imgur.com/sDu6ymw.gif)

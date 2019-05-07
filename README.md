# lossless

Typical ways to store data is in form of uncompressed TIFF files or AVIs. These files are, however, unneccesary large.
Here are two ways to store data compressed.

## HDF5

The _de facto_ standard is [hdf5](https://www.hdfgroup.org/solutions/hdf5/).
Using [h5py](https://www.h5py.org/) or [deepdish](https://deepdish.readthedocs.io/en/latest/api_io.html), it is fairly easy to store arbitrary data structures.
More information about compressions on the [PyTables website](http://www.pytables.org/usersguide/optimization.html?highlight=compression).


    import deepdish as dd
    import numpy as np
    
    np.random.seed(42)
    # Random data (e.g. t, z, x, y in 8bit grayscale)
    random_data = (np.random.randn(10, 200, 256, 256) ** 2).astype(np.uint8)
    
    dd.io.save('/path/to/file.h5',
              {'arbitrary_key': random_data},
              compression=('blosc', 4)) # algorithm (str), compression strength (int)
    
    # Uncompressed: 128 MB
    # Compressed: 69 MB

## MP4 using h264

Yes, h264 has a __lossless__ option! Find more information [here](https://trac.ffmpeg.org/wiki/Encode/H.264).
The "complicated" thing is to get it working easily.
The first option is using [imageio](), a standard library for image import/export in Python:

    io.mimwrite("/path/to/file.mp4", 
                ims, # images 
                quality=0, # best, i.e. lossless quality
                codec='libx264rgb', # use the right codec
                pixelformat='rgb24', # and pixel format
                output_params=['-crf', '0']) # Ensure setting crf to 0

The second one is a custom wrapper to FFMPEG that allows more flexibility and control:

    from lossless import LosslessVideoWriter
    
    # Many options that can be set here
    vw = LosslessVideoWriter("file.mp4")
    # mimwrite opens, writes and closes the video
    vw.mimwrite(ims) 

## Comments

If you have any comments, feel free to shoot me an email!

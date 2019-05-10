import subprocess as sp
import numpy as np

class LosslessVideoWriter:
    def __init__(self, 
                 filename, 
                 shape=None, 
                 fps=30, 
                 codec='libx264rgb', 
                 preset='veryslow', 
                 quality='lossless', 
                 FFMPEG_DIR=r"C:\ffmpeg\bin"):
        """VideoWriter using ffmpeg
        
        Parameters
        ----------
        filename : str
            The file to be written, e.g. test.mp4
        shape : tuple (w,h), optional
            the image shape, by default None
        fps : int, optional
            frames per second, by default 30
        codec : str, optional
            codec used by FFMPEG, by default 'libx264rgb'
        preset : str, optional
            mode, e.g. 'ultrafast', by default 'veryslow'
        quality : str or int, optional
            -crf flag of FFMPEG (0-96), by default 'lossless' = 0
        FFMPEG_DIR : str, optional
            FFMPEG bin directory, by default r"C:\ffmpeg\bin"
        """
        
        ### FFMPEG Dependencies ###
        self.FFMPEG_DIR = FFMPEG_DIR
        self.FFMPEG_EXE = FFMPEG_DIR+"\\ffmpeg.exe"

        ### Handler ###
        self.h = None

        ### Settings ###
        self.filename = filename
        self.shape = shape
        self.fps = fps
        self.codec = codec
        self.crf = quality if quality != 'lossless' else 0
        self.preset = preset
        
    def mimwrite(self, ims):
        """Writes multiple images to file (similar to imageio.mimwrite)
        
        Parameters
        ----------
        ims : list or np.ndarray
            Images to be written
        """
        if type(ims) != list and type(ims) != np.ndarray:
            assert False, "provide images as list or ndarray"
        
        if self.shape is None:
            self.shape = ims[0].shape
            
        self.open()
        
        for im in ims:
            self.write(im)
            
        self.close()
        

    def open(self):
        """Opens handler with settings provided
        """
        assert self.shape != None, "provide an image shape!"
        
        command = [self.FFMPEG_EXE,
            '-y', # (optional) overwrite output file if it exists
            '-f', 'rawvideo',
            '-vcodec', 'rawvideo',
            '-s', '{:d}x{:d}'.format(self.shape[1], self.shape[0]), # size of one frame
            '-pix_fmt', 'rgb24',
            '-r', '{}'.format(self.fps), # frames per second
            '-i', '-', # The imput comes from a pipe
            '-an', # Tells FFMPEG not to expect any audio
            '-vcodec', self.codec,
            '-crf', str(self.crf),
            '-preset', self.preset,
            self.filename]

        self.h = sp.Popen(command, 
                        stdout=sp.PIPE, 
                        stdin=sp.PIPE, 
                        stderr=sp.PIPE,
                        bufsize=10**8)

    def write(self, im):
        """Writes image to handler
        
        Parameters
        ----------
        im : ndarray
            the image to be written
        """
        if self.h is None:
            print("No handler open!")
            return

        if type(im) == np.ndarray:
            im = im.tobytes()

        self.h.stdin.write(im)

    def close(self):
        """Closes handler
        """
        if self.h:
            self.h.stdin.close()
            self.h.communicate()
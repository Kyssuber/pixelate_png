import sys
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from PIL import Image

import os
homedir = os.getenv("HOME")

class main_image:
    
    def __init__(self, im_path=None, npixels_x=55, offset=0.35):
        self.im_path = im_path
        
        self.img_only = Image.open(self.im_path)
        self.img_array = np.asarray(self.img_only)

        self.height = np.shape(self.img_array)[0]
        self.width = np.shape(self.img_array)[1]
        
        self.npixels_x = int(npixels_x)
        
        self.offset = float(offset)
        
    def get_scaling_fraction(self):

        if self.height>self.width:
            fraction = self.width/self.height
            return 1, fraction
        elif self.width>self.height:
            fraction = self.height/self.width
            return fraction, 1
        elif self.width==self.height:
            return  1, 1
        else:
            print("I don't know what to tell ye. Your width and height are not numbers.")
            return None
    
    def scale_image(self):
        
        #this function is mine; it helps ensure that pixel cells are square- and not rectangular-shaped
        frac_h, frac_w = self.get_scaling_fraction()

        #resize smoothly down to desired number of pixels for x (55*frac_w) and y (55*frac_h)
        self.img_scaled = self.img_only.resize((int(self.npixels_x*frac_w),int(self.npixels_x*frac_h)), 
                                               resample=Image.Resampling.BILINEAR)
        self.img_scaled_array = np.asarray(self.img_scaled)
        
    def add_grid(self):
     
        self.xticks = []
        self.yticks = []
        self.xlabels = []
        self.ylabels = []
        
        for n in range(np.shape(self.img_scaled_array)[0]):
            plt.axhline(n+self.offset,lw=1,color='black',alpha=0.4)
            if n==0:
                self.yticks.append(n-self.offset)
                self.ylabels.append(n)
            if (n+1)%5==0:
                self.yticks.append(n+self.offset)
                self.ylabels.append(n+1)
                     
        for n in range(np.shape(self.img_scaled_array)[1]):
            plt.axvline(n+self.offset,lw=1,color='black',alpha=0.4)  
            if n==0:
                self.xticks.append(n-self.offset)
                self.xlabels.append(n)
            if (n+1)%5==0:
                self.xticks.append(n+self.offset)
                self.xlabels.append(n+1)        
        
            
    def plot_fig(self, savefig=False):
        im_path_split = self.im_path.split('/')[-1]
        im_name = im_path_split.split('.')
        
        fig, ax = plt.subplots()
        
        #flipping image and changing axis origin --> ensures y-axis increases from bottom to top
        #adapted from https://stackoverflow.com/questions/56916638/invert-the-y-axis-of-an-image-without-flipping-the-image-upside-down
        plt.imshow(np.flipud(self.img_scaled_array), origin='lower')
        self.add_grid()
        
        ax.set_xticks(self.xticks,labels=self.xlabels)
        ax.set_yticks(self.yticks,labels=self.ylabels)  
        
        plt.savefig(f'{homedir}/Desktop/{im_name[0]}_pxd.png',bbox_inches='tight',
                    pad_inches=0.2,dpi=200)
        
        print('Image saved to Desktop.')
        
    def run_all_func(self):
        self.get_scaling_fraction()
        self.scale_image()
        self.plot_fig()
        
        
if __name__ == '__main__':    

    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: %s [-im_path full_path_to_image] [-nx number_of_pixels_along_xaxis_(integer)] [-grid_offset optional_grid_offset_(float)]")
        sys.exit(1)
    
    if '-im_path' in sys.argv:
        p = sys.argv.index('-im_path')
        im_path = str(sys.argv[p+1])
        
    if '-nx' in sys.argv:
        p = sys.argv.index('-nx')
        npixels_x = sys.argv[p+1]
        
    if '-grid_offset' in sys.argv:
        p = sys.argv.index('-grid_offset')
        offset = sys.argv[p+1]
    else:
        offset = 0.5
        
    img_class = main_image(im_path=im_path, npixels_x=npixels_x, offset=offset)
    img_class.run_all_func()
    

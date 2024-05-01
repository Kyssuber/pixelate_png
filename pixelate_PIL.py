import sys
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from PIL import Image, ImageChops
import cv2

import os
homedir = os.getenv("HOME")

class main_image:
    
    def __init__(self, im_path=None, npixels_x=55, offset=0.5, trim=False):
        self.im_path = im_path
        
        self.img_only = Image.open(self.im_path)
        self.img_array = np.asarray(self.img_only)

        self.height = np.shape(self.img_array)[0]
        self.width = np.shape(self.img_array)[1]
        
        self.npixels_x = int(npixels_x)
        self.offset = float(offset)
        self.trim = bool(trim)
        
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
                                               resample=Image.NEAREST)
        self.img_scaled_array = np.asarray(self.img_scaled)  
    
    def trim_image(self):
        bg = Image.new(self.img_only.mode, self.img_only.size, self.img_only.getpixel((0,0)))
        diff = ImageChops.difference(self.img_only, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            self.img_only = self.img_only.crop(bbox)  
            self.img_array = np.asarray(self.img_only)
    
    def add_grid(self,im,axes):
     
        self.xticks = []
        self.yticks = []
        self.xlabels = []
        self.ylabels = []
        
        for n in range(np.shape(im)[0]):
            axes.axhline(n+self.offset,lw=1,color='black',alpha=0.4)
            if n==0:
                self.yticks.append(n-self.offset)
                self.ylabels.append(n)
            if (n+1)%10==0:
                self.yticks.append(n+self.offset)
                self.ylabels.append(n+1)
                     
        for n in range(np.shape(im)[1]):
            axes.axvline(n+self.offset,lw=1,color='black',alpha=0.3)  
            if n==0:
                self.xticks.append(n-self.offset)
                self.xlabels.append(n)
            if (n+1)%10==0:
                self.xticks.append(n+self.offset)
                self.xlabels.append(n+1)         
    
    def plot_fig(self, savefig=False):
        im_path_split = self.im_path.split('/')[-1]
        im_name = im_path_split.split('.')

        titles = ['Unpixelated Image','Pixelated Image']
        
        fig, (ax1,ax2) = plt.subplots(1,2, figsize=(20,10))
        fig.subplots_adjust(wspace=0.1)
        
        ax1.imshow(np.flipud(self.img_array), origin='lower') 
        ax2.imshow(np.flipud(self.img_scaled_array), origin='lower')
        self.add_grid(im=self.img_scaled_array,axes=ax2)
        ax2.set_xticks(self.xticks,labels=self.xlabels)
        ax2.set_yticks(self.yticks,labels=self.ylabels) 
            
        plt.savefig(f'{homedir}/Desktop/{im_name[0]}_pxd.png',bbox_inches='tight',
                    pad_inches=0.2,dpi=200)    
        
        print('Image saved to Desktop.')
    
    
    def run_all_func(self):
        if self.trim:
            self.trim_image()
        self.get_scaling_fraction()
        self.scale_image()
        self.plot_fig()     
        
if __name__ == '__main__':    

    if '-h' in sys.argv or '--help' in sys.argv:
        print("Usage: %s [-im_path full_path_to_image] [-nx number_of_pixels_along_xaxis_(integer)] [-grid_offset optional_grid_offset_(float)] [-trim] [-hide_disclaimer]")
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
    
    if '-trim' in sys.argv:
        trim = True
    else:
        trim = False
        
    if '-hide_disclaimer' in sys.argv:
        hide = True
    else:
        hide = False
        
    img_class = main_image(im_path=im_path, npixels_x=npixels_x, offset=offset, trim=trim)
    img_class.run_all_func()
    
    if not hide:
        print('''

        DISCLAIMER NOTES:

            --- Be sure to use the original image as a reference!

            --- The author does not fully recommend feeding in an already "pixelated" 
                image into the program, as the pixel colors might not be as well-defined as 
                the original image. Rather, use the pixelated image AS the pixelated
                image and draw like the wind (but better and more controlled). 
                
            --- Alternatively, enter the same -nx parameter as the length of the image to 
                effectively add a grid overlay.

            --- Is the quality too...pixelated? Tweak the -nx parameter!

            --- Does the grid appear to be offset? Tweak the -offset parameter! 
                Try small floats first, such as 0.35 or 0.50 (the latter is the default).

            --- If there too much white space about the perimeter? Try the -trim parameter!
                Be aware that -trim works best cases with WHITE SPACE, or with a non-black uniform
                background.
            
            --- Note that -trim also runs before the pixelation process, meaning that -nx is applied
                to anywhere the white space is not. Be sure to adjust syour -nx value accordingly.
              ''')
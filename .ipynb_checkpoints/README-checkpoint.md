### Pixelate PNG or JPG images for pixel art!
##### (or to satisfy your square fixation)
In a terminal window, <br>
`python pixelate_CV2.py -h` <br>
`python pixelate_PIL.py -h` <br>
<br>
Optional args will be printed with brief descriptions. <br>
The two variants of this script reflect whether cv2 or PIL is used for the pixelation process. Both yield marginally different results with respect to outlining and decision-making for finer details/features. <br>
If you have a peculiar interest in generating discolored pixel images, I invite you to try the draft version of the former scripts: <br>
`python pixelate_PIL_bilinear.py -h`, <br>
which, as the label suggests, uses bilinear rather than NEAREST resampling.
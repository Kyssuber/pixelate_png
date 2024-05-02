### Pixelate PNG or JPG images for pixel art!
##### (or to satisfy your square fixation)
In a terminal window, <br>
`python pixelate.py -h` <br>
<br>
Optional args will be printed with brief descriptions. <br>
This script outputs a 2x2 set of panels displaying the original image (upper left), the smoothed pixelated image (upper right), and two variants of a sharper pixelation approach (cv2 -- bottom left; PIL -- bottom right). Each approach of the bottom row yields marginally different results with respect to outlining and decision-making for finer details/features of the original image. <br>
If you have a peculiar interest in generating discolored pixel images, I invite you to try the draft version of the former scripts: <br>
`python pixelate_PIL_bilinear.py -h`, <br>
which, as the label suggests, uses bilinear rather than NEAREST resampling. The idea of bilinear is that the output will generally be smoother, such that transitions from black to white will instead be black to slightly less black to slightly less white to white (usw). Given I was not familiar with this critical information at the time, I added multiple incompetent tricks to eliminate that smoothness characteristic, including a sharpness matrix. If the smoothness intrigues you, then pop off or whatever the younglings utter as slang these days.
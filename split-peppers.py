import numpy as np
import cv2

# still to do:
# auto shrink video to fit perfictly inside the user entered or predetermined screen size
# read the the solidworks .txt file to scrape the screensize info out of it.
# that way all screen editing is done via that text file. 
    
video1 = 'Earth.mov'
video2 = 'chaplin.mp4'
video3 = 'hi.wow'

# put the name of your video in where it says 'Earth.mov' make sure to put single quotes around the file name.
# the video file you want to use should be in the same directory as this python program. 
videoToLoad = cv2.VideoCapture(video1)

# please enter in the screen size you will be using measured in mm
# for ease of use, please enter in the dimentions in as a landscape view as aposed to a portrate view
# eg the largest number becomes the width

entered_width = 145
entered_height = 285

# let's auto correct just incase
if entered_height > entered_width:
    temp_height = entered_width
    temp_width = entered_height

    entered_width = temp_width
    entered_height = temp_height
    
# we will now convert this entered measurement that was in mm to pixels.
screen_height = int(entered_height * 3.7795275591)
screen_width = int(entered_width * 3.7795275591)
    
# This is how this is acomplished.
# How to Convert Millimeter to Pixel (X)
# 1 mm = 3.7795275591 pixel (X)
# 1 pixel (X) = 0.2645833333 mm
# Example: convert 15 mm to pixel (X):
# 15 mm = 15 × 3.7795275591 pixel (X) = 56.6929133858 pixel (X)

def create_blank_image(height,width):
    result = np.zeros(shape = [screen_height, screen_width, 3], dtype = np.uint8)
    return result

def resize(main_source,sub_source):
    mainScale = 4
    height1, width1, channels1 = main_source.shape
    height2, width2, channels2 = sub_source.shape

    temp_height = height2 - height1 / mainScale 
    scale_height = height2 - temp_height

    temp_width = width2 - width1 / mainScale
    scale_width = width2 - temp_width

    #scale_height = scale_width

    result = cv2.resize(sub_source,(int(scale_width),int(scale_height)))
    return result
    
def rotate(source, angle):
    height, width , channels = source.shape
    image_center = (width/2, height/2)

    rotation_source = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_source[0,0]) 
    abs_sin = abs(rotation_source[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_source[0, 2] += bound_w/2 - image_center[0]
    rotation_source[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_source = cv2.warpAffine(source, rotation_source, (bound_w, bound_h))
    return rotated_source

def compsite_upper_image(main_source,pasting_source):
    main_height, main_width, main_channels = main_source.shape
    pasting_height, pasting_width, pasting_channels = pasting_source.shape
    x_offset = int(main_width / 2 - pasting_width / 2)
    y_offset = int(pasting_height / 4)
    main_source[y_offset:y_offset + pasting_source.shape[0], x_offset:x_offset + pasting_source.shape[1]] = pasting_source 
    return main_source

def compsite_lower_image(main_source,pasting_source):
    main_height, main_width, main_channels = main_source.shape
    pasting_height, pasting_width, pasting_channels = pasting_source.shape
    x_offset = int(main_width / 2 - pasting_width / 2)
    y_offset = int(main_height - pasting_height - pasting_height / 4)
    main_source[y_offset:y_offset + pasting_source.shape[0], x_offset:x_offset + pasting_source.shape[1]] = pasting_source 
    return main_source

def compsite_right_image(main_source,pasting_source):
    main_height, main_width, main_channels = main_source.shape
    pasting_height, pasting_width, pasting_channels = pasting_source.shape
    x_offset = int(main_width / 2 + pasting_height/2)
    y_offset = int(main_height / 2 - pasting_height /2 )
    main_source[y_offset:y_offset + pasting_source.shape[0], x_offset:x_offset + pasting_source.shape[1]] = pasting_source 
    return main_source

def compsite_left_image(main_source,pasting_source):
    main_height, main_width, main_channels = main_source.shape
    pasting_height, pasting_width, pasting_channels = pasting_source.shape  
    x_offset = int(main_width / 2 - pasting_height)
    y_offset = int(main_height / 2 - pasting_height /2 )
    
    main_source[y_offset:y_offset + pasting_source.shape[0], x_offset:x_offset + pasting_source.shape[1]] = pasting_source 
    return main_source


while videoToLoad.isOpened():

    sucess, frame = videoToLoad.read()
    if not sucess:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    blank_image = create_blank_image(screen_width,screen_height)

    # let's figure out how to auto resize the video eo fit with in
    # the screen we just generated
    
    resized = resize(blank_image,frame)
    angle90 = rotate(resized,90)
    angle180 = rotate(angle90,90)
    angle270 = rotate(angle180,90)

    composite1 = compsite_upper_image(blank_image,resized)    
    composite2 = compsite_lower_image(composite1,angle180) 
    composite3 = compsite_right_image(composite2,angle90)
    composite4 = compsite_left_image(composite3,angle270)
    
    cv2.imshow("Split Peppers", composite4)

    if cv2.waitKey(1) == ord('q'):
        break
    
videoToLoad.release()
cv2.destroyAllWindows()









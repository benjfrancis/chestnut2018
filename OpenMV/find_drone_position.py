# AprilTags Example
#
# This example shows the power of the OpenMV Cam to detect April Tags
# on the OpenMV Cam M7. The M4 versions cannot detect April Tags.

import sensor, image, time, math, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

# Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

# What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
# a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
# is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
# rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
# reason to use the other tags families just use TAG36H11 which is the default family.

# The AprilTags library outputs the pose information for tags. This is the x/y/z translation and
# x/y/z rotation. The x/y/z rotation is in radians and can be converted to degrees. As for
# translation the units are dimensionless and you must apply a conversion function.

# f_x is the x focal length of the camera. It should be equal to the lens focal length in mm
# divided by the x sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# f_y is the y focal length of the camera. It should be equal to the lens focal length in mm
# divided by the y sensor size in mm times the number of pixels in the image.
# The below values are for the OV7725 camera with a 2.8 mm lens.

# c_x is the image x center position in pixels.
# c_y is the image y center position in pixels.

f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)


#z_ratio = 0.055
#xy_ratio = 0.039
scale_ratio = 4

def degrees(radians):
    return (180 * radians) / math.pi

threshold_index = 0 # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [(30, 100, 15, 127, 15, 127), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0),     # blue
              (30, 100, 15, 127, 15, 127)]  # red taylored to our T-shirt

while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y, families=image.TAG16H5): # defaults to TAG36H11
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

        tag_id = tag.id()

        # Translation units are unknown. Rotation units are in degrees.
        tx = tag.x_translation()*scale_ratio
        ty = tag.y_translation()*scale_ratio
        tz = tag.z_translation()*scale_ratio

        rx = tag.x_rotation()
        ry = tag.y_rotation()
        rz = tag.z_rotation()

        print_args = (tag_id, tx, ty, tz, rx, ry, rz, pyb.millis())
        print("tag,%d,%f,%f,%f,%f,%f,%f,%d\n" % print_args)


    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=10, area_threshold=10, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        player_x = blob.cx()
        player_y = blob.cy()
        img.draw_cross(player_x, player_y)

        print_args = (player_x, player_y, pyb.millis())
        print("player,%d,%d,%d\n" % print_args)

    #print(clock.fps())

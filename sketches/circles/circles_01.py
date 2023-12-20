import argparse
import cv2
import os
import numpy as np
import math
import colorsys

# Set up argument parser
parser = argparse.ArgumentParser(
    description='Create a video of a circle moving horizontally with speed modulated by a sine wave.')
parser.add_argument('--save', action='store_true', help='Save the video to a file')
parser.add_argument('--show', action='store_true', help='Show video as the code executes')
args = parser.parse_args()

# Parameters
width, height = 360, 640  # Video dimensions
radius = 20  # Circle radius

# Function to draw the circle
def draw_circle(frame, x_pos, y_pos, color):
    cv2.circle(frame, (int(x_pos), int(y_pos)), radius, color, -1, lineType=cv2.LINE_AA)
    cv2.circle(frame, (int(x_pos), int(y_pos)), radius, (255, 255, 255), 1, lineType=cv2.LINE_AA)

def generate_phases(num):
    if num <= 0:
        raise ValueError("Number of values (num) must be greater than zero")

    step_size = np.pi / num
    phases_arr = np.arange(0, np.pi, step_size)

    return phases_arr

def generate_angles(num):
    if num <= 0:
        raise ValueError("Number of values (num) must be greater than zero")

    step_size = np.pi / num
    angles_arr = np.arange(0, np.pi, step_size)

    return angles_arr

def generate_hsb_colors(num):
    if num <= 0:
        raise ValueError("Number of colors (num) must be greater than zero")

    hue_step = 1.0 / num  # Divide the hue spectrum into num equal parts
    colors_arr = []

    for i in range(num):
        hue = i * hue_step  # Calculate the hue value
        rgb_color = colorsys.hsv_to_rgb(hue, 1.0, 1.0)  # Convert HSB to RGB
        rgb_color = tuple(int(val * 255) for val in rgb_color)
        colors_arr.append(rgb_color)


    return colors_arr


t = 0
t_scale = 1/360

x_init_pos = width / 2
y_init_pos = height / 2

path_length = width-50
speed = 1

nums = [8]
num_index = 0

# Ensure output directory exists
output_dir = 'outputs'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize the video writer if save argument is provided
if args.save:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    mov_title = "circles_num_" + str(nums[0]) + '.avi'
    out = cv2.VideoWriter(f'{output_dir}/{mov_title}', fourcc, 60.0, (width, height))

# Main loop to create frames and move the circle

while num_index < len(nums):

    num = nums[num_index]
    #The script will run slower since these are being set every single loop need to refactor later
    colors = generate_hsb_colors(num)
    phases = generate_phases(num)
    angles = generate_angles(num)

    # Create a black frame
    frame = np.zeros((height, width, 3), np.uint8)

    i = 0
    while i < len(phases):
        f = 2*np.pi*speed* (t * t_scale)
        if f >= 2*np.pi:
            t = 0
            num_index += 1
            print(num_index)

        step = path_length/2 * np.sin(f + phases[i])

        x_pos = x_init_pos + step * np.cos(np.pi/2 + angles[i])
        y_pos = y_init_pos + step * np.sin(np.pi/2 + angles[i])

        # Draw the circle on the frame
        draw_circle(frame, x_pos, y_pos, colors[i])

        i+=1

    # Display the frame
    if args.show:
        cv2.imshow('Linear Wave Circle Motion', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    # Write the frame to the video if save argument is provided
    if args.save:
        out.write(frame)

    # Increase frame count
    t += 1

# Release everything if job is finished
cv2.destroyAllWindows()
if args.save:
    out.release()
    print('The video was successfully saved.')
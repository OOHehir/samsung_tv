#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Uploads all .jpg images in a directory to a Samsung Frame TV using the SamsungTVWS API. '''

# SEE SOURCE FOR METHODS: https://github.com/NickWaterton/samsung-tv-ws-api/blob/9647fdb8556938b3369ac65f38f15108391c4267/samsungtvws/art.py

import os
import time
from samsungtvws import SamsungTVWS
import sys

BASE_DIRECTORY = "/home/projects/samsung_tv/images"
#IMAGE_DIRECTORY = "home/pictures/Dublin '18"
#IMAGE_DIRECTORY = BASE_DIRECTORY + "/classic_paintings"
IMAGE_DIRECTORY = BASE_DIRECTORY + "/space_pics"
TV_IP_ADDRESS = "192.168.178.28"

# MATTE TYPES (not all matte types work for all images)
# 'none' 'modernthin' 'modern' 'modernwide' 'flexible' 'shadowbox' 'panoramic' 'triptych' 'mix' 'squares'

# MATTE COLORS
# 'black' 'neutral' 'antique' 'warm' 'polar' 'sand' 'seafoam' 'sage' 'burgandy' 'navy' 'apricot' 'byzantine' 'lavender' 'redorange' 'skyblue' 'turquoise'
# (Jon) I tend to prefer 'warm' or 'apricot'

def upload_image(image_path):
    ''' Uploads a single image to the TV. '''
    try:
        # Connect to the TV
        tv = SamsungTVWS(host=TV_IP_ADDRESS)
        art = tv.art()
        api_ver = art.get_api_version()
        if not api_ver:
            print("Can't contact TV, exiting...")
            sys.exit(1)
        else:
            print(f"Connected to TV: {api_ver}")

        if not os.path.exists(image_path):
            print(f"File {image_path} does not exist.")
            sys.exit(1)

        # Read the image
        with open(image_path, "rb") as f:
            image_data = f.read()

        print(f"Now Uploading {image_path}...")
        # Upload the image
        # Sending both `matte` and `portrait_matte` since the image may be landscape or portrait!
        response = art.upload(
            image_data,
            file_type="JPEG",
            matte="flexible_apricot",
            # portrait_matte="flexible_apricot"
        )
        print(f"Uploaded {image_path}: {response}")
        print(f"{time.ctime()}")
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"Error uploading {image_path}: {e}")

def upload_images_in_directory(directory):
    ''' Uploads all .jpg images in a directory to the Frame TV. '''
    files = sorted(
        [filename for filename in os.listdir(directory) if filename.lower().endswith(".jpg")]
    )

    # Loop through sorted filenames
    for filename in files:
        full_path = os.path.join(directory, filename)
        upload_image(full_path)
        # Sleep 2 seconds to let the Frame TV process the image;
        # I found this helps a lot when uploading >25 in sequence
        time.sleep(2)

# Call the function to upload all images
upload_images_in_directory(IMAGE_DIRECTORY)

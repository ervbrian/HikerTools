'''
Name:       HikeTracker.py
Purpose:    Parses gpx files in a given directory, calculates distance and elevation stats and outputs data via CSV file
'''

import os
import multiprocessing
from multiprocessing import Pool
from ParseGPX import ParseGPX
from Hike import Hike


def create_hike_object(gpx_file):
    try:
        hike = Hike(gpx_file)  # initialize Hike object
        soup = ParseGPX.gpx_to_soup(hike.gpx_file)  # Convert XML to BS4 object for further processing
        hike.coordinates = ParseGPX.get_coordinate_list(soup)  # Generate coordinate list from BS4 object
        hike.elev_list = ParseGPX.get_elevation_list(soup)  # Generate elevation/altitude list from BS4 object
        hike.elev_gain, hike.elev_loss = ParseGPX.gen_elevation_stats(hike)  # Calculate elevation details of hike
        hike.distance = ParseGPX.gen_total_distance(hike)  # Calculate total distance of hike
        print('Processing of {} complete!'.format(hike.gpx_file))
    except Exception as e:
        print('Error processing GPX file: ' + str(e))
    return hike


def main():
    # Initialize variables
    initial_dir = os.getcwd()  # Determine current directory (will be used to store output file)
    cpu_count = multiprocessing.cpu_count()  # Used to determine how many concurrent processes to spawn
    gpx_dir = '/Users/ervbrian/Documents/Personal_Files/Hiking/GPX Tracks/'
    output_csv = 'HikeData.csv'
    csv_header = 'Date, Name, GPX File, Elevation Gain (ft), Elevation Loss (ft), Total Distance (mi)\n'
    gpx_file_list = []
    multi_proc = True

    # Change working directory to where GPX files are stored
    if os.path.isdir(gpx_dir) and os.path.exists(gpx_dir):
        os.chdir(gpx_dir)
    else:
        raise Exception('Please verify GPX directory path')

    # Generate list of GPX files to process
    for gpx_file in sorted(os.listdir(gpx_dir)):
        if gpx_file.endswith(".gpx") or gpx_file.endswith(".GPX"):  # Only process gpx files
            gpx_file_list.append(gpx_file)

    print('Found {} GPX files to process ...'.format(len(gpx_file_list)))

    # Process each GPX file and generate a corresponding Hike object
    if multi_proc:
        p = Pool(cpu_count)
        print('Found {} CPU(s) on system. Enabling multiprocessing ...'.format(cpu_count))
        hike_object_list = p.map(create_hike_object, gpx_file_list)
    else:
        hike_object_list = list(map(create_hike_object, gpx_file_list))

    os.chdir(initial_dir)  # Change back to initial directory

    # Generate CSV file containing parsed data
    try:
        with open(str(output_csv), 'w') as f:
            print('Writing data to {} ...'.format(output_csv))
            f.write(csv_header)
            for hike in hike_object_list:
                f.write(hike.ToString())  # Write hike CSV data row
        f.close()
    except Exception as e:
        print('Error writing data to {}: {}'.format(f, e))


if __name__ == "__main__":
    main()

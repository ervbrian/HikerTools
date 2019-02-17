# ----------------------------- #
# Title: PackLoadCalc.py
# Dev: Brian Ervin
# Date: Feb 16, 2019
# ChangeLog: (When, Who, What)
#  2019-02-16, Brian Ervin, Created Version 1.0
#  2019-02-16, Brian Ervin, Updated output_csv() function
#  2019-02-16, Brian Ervin, Updated output_json() function
#  2019-02-17, Brian Ervin, Removed variables used for testing in main()
# ----------------------------- #

"""
Purpose: Calculate pack weight stats based on body weight and trip duration

Usage:
    python PackLoadCalc.py

Steps:
    1) Gather pack weight, body weight and food requirement details
    2) Calculate daily statistics for trip
    3) Output data to JSON and CSV files
    4) Output data plot to PNG file
"""

import json
import sys
import matplotlib.pyplot as plt

def fetch_details():

    """
    Gather details from user interactively

    :return: floating point values to be used in weight calculations
    """

    hike_name = input("Enter name of hike: ")
    base_weight = float(input("Enter pack base weight (lbs): "))
    body_weight = float(input("Enter body weight (lbs): "))
    trip_duration = float(input("Enter trip duration (days): "))
    daily_food = float(input("Enter daily food requirements (lbs): "))

    return hike_name, base_weight, body_weight, trip_duration, daily_food


def calc_daily_load(base_weight, body_weight, trip_duration, daily_food):

    """
    Calculate daily statistics around pack vs body weight per day of trip

    :param base_weight: floating point
    :param body_weight: floating point
    :param trip_duration: floating point
    :param daily_food: floating point
    :return: list object containing dictionaries for each day of trip
    """

    # initialize table and day number variables
    daily_weight_percentage_table = []
    day_num = 1

    # calculate weight stats for each day
    while day_num <= trip_duration:
        food_weight = (daily_food * (trip_duration - day_num))
        total_pack_weight = (base_weight + food_weight)
        pct_body_weight = round((total_pack_weight / body_weight) * 100, 2)

        # consolidate weight stats into dictionary
        day_stats = {'day_num': day_num,
                     'food_weight': food_weight,
                     'total_pack_weight': total_pack_weight,
                     'pct_body_weight': pct_body_weight
                     }

        # append dictionary to table
        daily_weight_percentage_table.append(day_stats)

        # increase day number
        day_num = day_num + 1

    return daily_weight_percentage_table


def output_csv(daily_weight_percentage_table, output_file):

    """
    Write data to CSV file

    :param daily_weight_percentage_table: List of dictionary elements
    :param output_file: string
    :return: None
    """

    # generate csv header
    header = ""
    for key in daily_weight_percentage_table[0].keys():
        header += (key + ',')

    # write csv data to file
    try:
        with open(output_file, "w") as f:
            # write header
            f.write(header + '\n')

            # write table data
            for row in daily_weight_percentage_table:
                for key in row.keys():
                    f.write((str(row[key]) + ','))
                f.write('\n')

            # close file
            f.close()
            print('Successfully wrote data to CSV file...')
    except:
        print("Could not write CSV data to file...")


def output_json(daily_weight_percentage_table, output_file):

    """
    Write data to JSON file

    :param daily_weight_percentage_table: list of dictionary elements
    :param output_file: string
    :return: None
    """

    try:
        with open(output_file, "w") as f:
            f.write(json.dumps(daily_weight_percentage_table, indent=4, sort_keys=True))
            f.close()
            print('Successfully wrote data to JSON file...')
    except:
        print("Could not write JSON data to file...")


def plot_data(daily_weight_percentage_table, hike_name):

    """
    Plot daily pack weight data to graph and store as PNG file

    :param daily_weight_percentage_table: List of dictionary elements
    :param hike_name: string
    :return: None
    """

    # initialize data lists
    day_list = []
    pct_body_weight_list = []
    total_pack_weight_list = []

    # populate data lists
    for i in range(0, len(daily_weight_percentage_table)):
        day_list.append(daily_weight_percentage_table[i]['day_num'])
        pct_body_weight_list.append(daily_weight_percentage_table[i]['pct_body_weight'])
        total_pack_weight_list.append(daily_weight_percentage_table[i]['total_pack_weight'])

    # create plots with pre-defined labels.
    fig, ax = plt.subplots()
    ax.plot(day_list, total_pack_weight_list, 'k', label='Total Pack Weight (Lbs)')
    ax.plot(day_list, pct_body_weight_list, 'k--', label='Pack Weight vs Body Weight (%)')

    # add legend
    ax.legend(loc='upper right', shadow=True, fontsize='medium')

    # label data points
    percentage_annotation = '%'
    for xy in zip(day_list, pct_body_weight_list):
        ax.annotate('%s%s' % (xy[1], percentage_annotation), xy=xy, textcoords='data')

    for xy in zip(day_list, total_pack_weight_list):
        ax.annotate('%s lbs' % xy[1], xy=xy, textcoords='data')

    # label x and y axis
    plt.xlabel('Day of Trip')
    plt.ylabel('Pack Weight | % of Body Weight')

    # label title
    plt.title('{}\nPack Weight Statistics'.format(hike_name))

    # output to file
    fig.savefig(hike_name + '.png')
    print('Successfully plotted data. Output saved to PNG...')


def main():

    # gather details from user
    hike_name, base_weight, body_weight, trip_duration, daily_food = fetch_details()

    # calculate pack weight statistics
    # store in list of dictionary objects
    daily_weight_percentage_table = calc_daily_load(base_weight, body_weight, trip_duration, daily_food)

    # save data to output files
    output_csv(daily_weight_percentage_table, hike_name + '.csv')
    output_json(daily_weight_percentage_table,  hike_name + '.json')
    plot_data(daily_weight_percentage_table, hike_name)


if __name__ == '__main__':
    main()

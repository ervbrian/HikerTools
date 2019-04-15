from bs4 import BeautifulSoup as Soup
from geopy.distance import geodesic


class ParseGPX():

    @staticmethod
    def gpx_to_soup(file):
        """
        Import GPS data from GPX source file.
        Return XML as soup object
        """

        # Open gpx file and construct soup object
        handler = open(file).read()
        return Soup(handler, features="html.parser")

    @staticmethod
    def get_coordinate_list(soup):
        """Generate coordinate list from gpx file"""

        coords = []

        # grab all trkpt objects from gpx file
        for point in soup.findAll('trkpt'):
            coord = (point['lat'], point['lon'])
            coords.append(coord)

        return coords

    @staticmethod
    def get_elevation_list(soup):
        """Generate elevation list from gpx file"""

        elevation_list = []

        # grab all trkpt objects from gpx file
        for point in soup.findAll('ele'):
            elevation_list.append(float(point.text))

        return elevation_list

    @staticmethod
    def gen_elevation_stats(hike):
        """
        Calculate elevation gain based on list of elevation values

        Process:
            Compare each data point and calculate change from previous point

            first iteration  |(i-1)(i)---------------------------|
            second iteration |-(i-1)(i)--------------------------|
            third iteration  |--(i-1)(i)-------------------------|
            ** continue until end of coordinate list **
        """

        elev_gain = 0
        elev_loss = 0

        # Compare each data point to calculate gain/loss
        for i in range(1, len(hike.elev_list)):

            # if current elevation point is less than previous point, then increase total loss
            if hike.elev_list[i] < hike.elev_list[(i - 1)]:
                elev_loss += (hike.elev_list[i] - hike.elev_list[i - 1]) * 3.28084  # meter to foot conversion

            # if current elevation point is greater than previous point, then increase total gain
            elif hike.elev_list[i] > hike.elev_list[(i - 1)]:
                elev_gain += (hike.elev_list[i] - hike.elev_list[i - 1]) * 3.28084  # meter to foot conversion

        return round(elev_gain), round(elev_loss)

    @staticmethod
    def gen_total_distance(hike):
        """
        Calculate total distance based on list of latitude/longitude coordinates

        Process:
            Compare each data point to calculate distance from previous point and add to distance value

            first iteration  |(i-1)(i)---------------------------|
            second iteration |-(i-1)(i)--------------------------|
            third iteration  |--(i-1)(i)-------------------------|
            ** continue until end of coordinate list **
        """

        total_distance = 0

        for i in range(1, len(hike.coordinates)):
            total_distance += geodesic(hike.coordinates[i], hike.coordinates[i - 1]).miles

        return round(total_distance, 2)


class Hike(object):
    """
    Class to store hike details
    """

    def __init__(self, gpx_file):
        self.name = gpx_file.split('.')[0]
        self.gpx_file = gpx_file
        self.date = gpx_file.split('_')[0]
        self.distance = 0
        self.elev_list = []
        self.elev_gain = 0
        self.elev_loss = 0
        self.coordinates = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def gpx_file(self):
        return self.__gpx_file

    @gpx_file.setter
    def gpx_file(self, value):
        self.__gpx_file = value

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, value):
        self.__distance = value

    @property
    def elev_list(self):
        return self.__elev_list

    @elev_list.setter
    def elev_list(self, value):
        self.__elev_list = value

    @property
    def elev_gain(self):
        return self.__elev_gain

    @elev_gain.setter
    def elev_gain(self, value):
        self.__elev_gain = value

    @property
    def elev_loss(self):
        return self.__elev_loss

    @elev_loss.setter
    def elev_loss(self, value):
        self.__elev_loss = value

    @property
    def coordinates(self):
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, value):
        self.__coordinates = value

    def ToString(self):
        """Explicitly returns field data"""
        return self.date + ',' + \
               self.name + ',' + \
               self.gpx_file + ',' + \
               str(self.elev_gain) + ',' + \
               str(self.elev_loss) + ',' + \
               str(self.distance) + '\n'

    def __str__(self):
        """Implictly returns field data"""
        return self.ToString()

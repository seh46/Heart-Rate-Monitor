class HeartRate(object):
    """This class provides information about ECG data.

    __init__ sets the list with ECG data

    Attributes:
        beats (number of heart beats)
        duration (length of ECG reading)
        heartRate (average heart rate over specified interval of ECG reading)
        numBeats (number of heartbeats in ECG reading)
        voltageExtremes (maximum and minimum voltages present in ECG reading)
    """

    def __init__ (self, data_file, interval=0.25):
        """Initialize HeartRate object with data file and interval to measure
        heart rate

        :param data_file: csv file containing rows each with one time and one
        voltage
        :param interval: number value in minutes
        """
        import pandas as pd
        import logging

        self.beats = None
        self.duration = None
        self.mean_hr_bpm = None
        self.num_beats = None
        self.voltage_extremes = None
        self.volts = None
        try:
            self.df = pd.read_csv(data_file, delimiter=',')
            self.df = self.df.fillna(self.df.mean())
        except OSError:
            print('Data file must be located in current directory')
            logging.warning('Data file not found')
            self.df = None

        try:
            self.endval = self.df.iloc[:, 0].tail(n=1)
            if interval/60 > self.endval.iloc[0]:
                raise ValueError
            if type(interval) != int and type(interval) != float:
                raise TypeError
            self.hr_interval = interval
        except ValueError:
            print('Interval must be shorter than duration of input ECG strip')
            logging.warning('Interval longer than duration of data')
            self.hr_interval = None
        except TypeError:
            print('Interval must be a number')
            logging.warning('Interval provided is not numeric')
        self.beat_times()

    def beat_times(self):
        """ Find time of each beat

        :return: list containing timepoint for each beat [float]
        """
        import numpy as np
        import scipy.signal as scs
        import logging
        logging.getLogger().setLevel('DEBUG')

        data_int_size = self.df.iloc[1, 0] - self.df.iloc[0, 0]
        width_min = round(.03/data_int_size, 0)
        width_max = round(0.1/data_int_size, 0)
        volts = self.df.iloc[:, 1]
        self.avg = volts.mean()
        beat_indices = scs.find_peaks_cwt(volts, widths=np.arange(width_min,
                                                                  width_max))
        self.beats = [self.df.iloc[i,0] for i in beat_indices]

    def get_duration(self):
        """ Find duration of input ECG strip

        :return: duration of ECG strip [int]
        """
        import logging

        dur = self.df.iloc[:,0].tail(n=1)
        self.duration = dur[0]
        logging.info('Duration determined with success.')

    def findMeanHR(self):
        """ Find average heart rate over user-specified number of minutes

        :return: integer heart rate in bpm [int]
        """
        import logging

        ints = self.hr_interval/60
        if ints > self.df.iloc[:, 0].tail(n=1):
            ints = self.df.iloc[:, 0].tail(n=1)
        within = self.beats[:, 0] < ints
        number = self.beats[within]
        self.mean_hr_bpm = number*60/ints

    def numBeats(self):
        """ Find number of beats in ECG strip

        :return: number of beats [int]
        """
        self.num_beats = len(self.beats)

    def voltageExtremes(self):
        """ Find extrema of input voltage data

        :return: list containing maximum and minimum voltages [float]
        """
        self.voltage_extremes = []
        x_min = self.df.iloc[:, 1].min()
        x_max = self.df.iloc[:, 1].max()
        self.voltage_extremes = [x_min, x_max]

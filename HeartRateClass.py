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

    def __init__(self, data_file, interval=0.25):
        """Initialize HeartRate object with data file and interval to measure
        heart rate

        :param data_file: csv file containing rows each with one time and one
        voltage
        :param interval: number value in minutes
        """
        import pandas as pd
        import logging
        import os

        self.beats = None
        self.duration = None
        self.mean_hr_bpm = None
        self.num_beats = None
        self.voltage_extremes = None
        self.volts = None
        try:
            self.df = pd.read_csv(data_file, delimiter=',')
            self.df = self.df.fillna(self.df.mean())
            self.filename = os.path.splitext(data_file)[0]
        except OSError:
            print('Data file must be located in current directory')
            logging.warning('Data file not found')
            self.df = None

        try:
            endval = self.df.iloc[:, 0].tail(n=1)
            if interval/60 > endval.iloc[0]:
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
        logging.info("Input data read with success")
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
        beat_indices = scs.find_peaks_cwt(volts, widths=np.arange(width_min,
                                                                  width_max))
        self.beats = [self.df.iloc[i, 0] for i in beat_indices]
        logging.info("Beat times determined")

    def get_duration(self):
        """ Find duration of input ECG strip

        :return: duration of ECG strip [int]
        """
        import logging

        dur = self.df.iloc[:, 0].tail(n=1)
        self.duration = dur
        self.duration = self.duration.iloc[0]
        logging.info("Duration of ECG strip has been determined.")

    def findMeanHR(self):
        """ Find average heart rate over user-specified number of minutes

        :return: integer heart rate in bpm [int]
        """
        import logging

        ints = self.hr_interval*60
        count = 0
        for i in self.beats:
            if i < ints:
                count += 1
        self.mean_hr_bpm = count*60/ints
        logging.info('Mean HR over interval of length %s minutes determined to'
                     ' be %s', ints/60, self.mean_hr_bpm)

    def numBeats(self):
        """ Find number of beats in ECG strip

        :return: number of beats [int]
        """
        import logging

        self.num_beats = len(self.beats)
        logging.info('Number of beats is %s', self.num_beats)

    def voltageExtremes(self):
        """ Find extrema of input voltage data

        :return: list containing maximum and minimum voltages [float]
        """
        import logging

        self.voltage_extremes = []
        x_min = self.df.iloc[:, 1].min()
        x_max = self.df.iloc[:, 1].max()
        self.voltage_extremes = [x_min, x_max]
        logging.info('Voltage extremes are min: %s, and max: %s', x_min, x_max)

    def output_attributes(self):
        import json
        import logging

        self.beat_times()
        self.numBeats()
        self.get_duration()
        self.findMeanHR()
        self.voltageExtremes()

        rounded_beats = [round(elem, 3) for elem in self.beats]
        out_beats = json.dumps(rounded_beats)
        out_number = json.dumps(self.num_beats)
        out_dur = json.dumps(self.duration)
        out_HR = json.dumps(self.mean_hr_bpm)
        out_extremes = json.dumps(self.voltage_extremes)
        all_out = {
            "Beat times": out_beats,
            "Number of beats": out_number,
            "Duration of ECG strip": out_dur,
            "Average heart rate over interval": out_HR,
            "Extrema of voltage readings": out_extremes
        }
        name = self.filename + '.json'
        with open(name, 'w') as outfile:
            json.dump(all_out, outfile)

        logging.info("ECG data attributes successfully written to JSON file")

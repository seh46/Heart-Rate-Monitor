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

    def __init__ (self, data_file):
        import numpy as np
        import pandas as pd

        self.beats = None
        self.duration = None
        self.mean_hr_bpm = None
        self.num_beats = None
        self.voltage_extremes = None
        self.volts = None
        try:
            self.df = pd.read_csv(data_file, delimiter=',')
        except OSError:
            print('Data file must be located in current directory')
            #logging.warning('Data file not found')
            self.df = None

    def beat_times(self):
        import numpy as np
        import pandas as pd
        import scipy.signal as scs

        width_min = round(.03/(self.df.iloc[1, 0] - self.df.iloc[0, 0]), 0)
        width_max = round(0.1/(self.df.iloc[1, 0] - self.df.iloc[0, 0]), 0)
        volts = self.df.iloc[:, 1]
        beat_indices = scs.find_peaks_cwt(volts, widths=np.arange(width_min,width_max))
        self.beats = [self.df.iloc[i,0] for i in beat_indices]

        ## Verify beat times based on beat count
        peak_check = 0.4*self.voltage_extremes[1]
        check_array = pd.DataFrame()
        for i, item in enumerate(range(self.df.shape[0]-1)):
            if self.df.iloc[i, 1] >= peak_check:
                check_array = check_array.append(self.df.iloc[[i]])

        peak_times = []
        for i, item in enumerate(range(1,check_array.shape[0]-2)):
            if check_array.iloc[i, 1]-check_array.iloc[i-1, 1] >= 0 and check_array.iloc[i+1, 1]-check_array.iloc[i, 1] < 0:
                peak_times.append(check_array.iloc[i, 0])

        if len(self.beats) > len(peak_times):
            self.beats = peak_times


    def get_duration(self):
        import numpy as np
        import pandas as pd

        self.duration = self.df.iloc[:,0].tail(n=1)

    #
    # def findMeanHR(self):
    #
    #

    def numBeats(self):

        self.num_beats = len(self.beats)


    def voltageExtremes(self):
        import numpy as np
        import pandas as pd

        self.voltage_extremes = []
        x_min = self.df.iloc[:,1].min()
        x_max = self.df.iloc[:,1].max()

        self.voltage_extremes = [x_min,x_max]


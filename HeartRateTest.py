import HeartRateClass as hrc
import pytest


def test_beattimes():
    from numpy import allclose

    t1 = hrc.HeartRate('test_data1.csv')
    t1.beat_times()
    assert allclose(t1.beats[0:5], [0.214, 1.028, 1.842, 2.631, 3.419],
                    rtol=1e-01)
    t2 = hrc.HeartRate('test_data2.csv')
    t2.beat_times()
    assert allclose(t2.beats[0:5], [0.228, 1.1, 1.975, 2.867, 3.8], rtol=1e-01)
    t3 = hrc.HeartRate('test_data8.csv')
    t3.beat_times()
    assert allclose(t3.beats[0:5], [0.744, 1.569, 2.447, 3.339, 4.208],
                    rtol=1e-01)
    t4 = hrc.HeartRate('test_data28.csv')
    t4.beat_times()
    assert allclose(t4.beats[0:5], [0.214, 1.028, 1.842, 2.631, 3.419],
                    rtol=1e-01, atol=0.1)
    t5 = hrc.HeartRate('test_data31.csv')
    t5.beat_times()
    assert allclose(t5.beats[0:5], [0.043, 0.793, 1.543, 2.293, 3.043],
                    rtol=1e-01, atol=0.1)


def test_get_duration():

    t1 = hrc.HeartRate('test_data1.csv')
    t1.get_duration()
    assert t1.duration == 27.775
    t2 = hrc.HeartRate('test_data2.csv')
    t2.get_duration()
    assert t2.duration == 27.775
    t3 = hrc.HeartRate('test_data8.csv')
    t3.get_duration()
    assert t3.duration == 27.775
    t4 = hrc.HeartRate('test_data28.csv')
    t4.get_duration()
    assert t4.duration == 27.775
    t5 = hrc.HeartRate('test_data31.csv')
    t5.get_duration()
    assert t5.duration == 13.887

def test_findmeanhr():
    from numpy import isclose

    t1 = hrc.HeartRate('test_data1.csv')
    t1.findMeanHR()
    assert t1.mean_hr_bpm == 76
    t2 = hrc.HeartRate('test_data2.csv')
    t2.findMeanHR()
    assert t2.mean_hr_bpm == 68
    t3 = hrc.HeartRate('test_data8.csv')
    t3.findMeanHR()
    assert t3.mean_hr_bpm == 72
    t4 = hrc.HeartRate('test_data28.csv')
    t4.findMeanHR()
    assert t4.mean_hr_bpm == 76
    t5 = hrc.HeartRate('test_data31.csv')
    t5.findMeanHR()
    assert isclose(t5.mean_hr_bpm, 81, atol=1)


def test_numbeats():
    from numpy import isclose

    t1 = hrc.HeartRate('test_data1.csv')
    t1.numBeats()
    assert isclose(t1.num_beats, 34, atol=3)
    t2 = hrc.HeartRate('test_data2.csv')
    t2.numBeats()
    assert isclose(t2.num_beats, 32, atol=15)
    t3 = hrc.HeartRate('test_data8.csv')
    t3.numBeats()
    assert isclose(t3.num_beats, 33, atol=4)
    t4 = hrc.HeartRate('test_data28.csv')
    t4.numBeats()
    assert isclose(t4.num_beats, 35, atol=3)
    t5 = hrc.HeartRate('test_data31.csv')
    t5.numBeats()
    assert isclose(t5.num_beats,19, atol=3)


def test_voltageextremes():

    t1 = hrc.HeartRate('test_data1.csv')
    t1.voltageExtremes()
    assert t1.voltage_extremes == [-0.68, 1.05]
    t2 = hrc.HeartRate('test_data2.csv')
    t2.voltageExtremes()
    assert t2.voltage_extremes == [-0.59, 1.375]
    t3 = hrc.HeartRate('test_data8.csv')
    t3.voltageExtremes()
    assert t3.voltage_extremes == [-3.105, 1.975]
    t4 = hrc.HeartRate('test_data28.csv')
    t4.voltageExtremes()
    assert t4.voltage_extremes == [-0.68, 1.05]
    t5 = hrc.HeartRate('test_data31.csv')
    t5.voltageExtremes()
    assert t5.voltage_extremes == [-0.19375, 0.7875]

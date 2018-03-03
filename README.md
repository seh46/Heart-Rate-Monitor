# Heart-Rate-Monitor

To use this software, create a HeartRate object via the file HeartRateClass.py.
Your input should be of the form:
	objectname = HeartRateClass.HeartRate(datafilename, interval)

	where datafilename is a csv file in the same directory containing rows,
	each with one time point and one voltage measurement
	
	and where interval is an optional argument in minutes, over which to calculate
	a mean heart rate

You may access various attributes of the HeartRate object by calling functions detailed in the
documentation at this link: http://my-heart-rate-monitor.readthedocs.io/en/latest/

You may also call the function output_attributes() in order to generate a JSON file containing
all attributes that can be generated for the object

[![Build Status](https://travis-ci.org/seh46/Heart-Rate-Monitor.svg?branch=master)](https://travis-ci.org/seh46/Heart-Rate-Monitor)

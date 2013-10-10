## Parser for LOCUS log files

This was generated using log files extracted from the [Adafruit](http://www.adafruit.com/) GPS modules.

This parser takes the lazy approach and parses `$PMTKLOX,1` log messages in the order they appear generating a list of Coordinate objects. Log begin `$PMTKLOX,0,43*6E`, log end `$PMTKLOX,2*47`, and other lines are ignored.

The code was cobbled together from reading the [Sample LOCUS Code](http://www.adafruit.com/datasheets/Locus_Sample_Code.zip), [Code from Doug Gilliland](https://github.com/douggilliland/Dougs-Arduino-Stuff/blob/master/Host%20code/parseLOCUS/parseLOCUS.cpp), the [MTK NMEA checksum calculator](http://www.hhhh.org/wiml/proj/nmeaxor.html), [Adafruit's GPS Tutorial](http://learn.adafruit.com/adafruit-ultimate-gps/downloads-and-resources) and a bunch random PDFs found on the internet. It all appears to work for the limited data sets I have used.  Let me know if you see anomalies.

The two examples, `log_to_json.py` and `log_to_kml.py`, parse the sample LOCUS log file and generate JSON and KML output.s

Known problems

 * GPS fix isn't decoded correctly

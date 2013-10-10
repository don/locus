# LOCUS log parser
# (c) 2013 Don Coleman 

import sys
from pprint import pformat
from datetime import datetime

# turn a string of bytes into a byte array
def toByteArray(str):
    bytes = []
    while len(str) > 1:
        byte = str[:2]
        bytes.append(int(byte, 16))
        str = str[2::] 
        
    return bytes

def parseInt(bytes):
    if len(bytes) != 2:
        print >> sys.stderr, "WARNING: expecting 2 bytes got %s" % bytes
    number = ((0xFF & bytes[1]) << 8) | (0xFF & bytes[0])
    return number

def parseLong(bytes):
    if len(bytes) != 4:
        print >> sys.stderr, "WARNING: expecting 4 bytes got %s" % bytes
    number = ((0xFF & bytes[3]) << 24) | ((0xFF & bytes[2]) << 16) | ((0xFF & bytes[1]) << 8) | (0xFF & bytes[0])    
    return number

def parseFloat(bytes):
    longValue = parseLong(bytes)

    # borrowed code from https://github.com/douggilliland/Dougs-Arduino-Stuff/blob/master/Host%20code/parseLOCUS/parseLOCUS.cpp
    exponent = ((longValue >> 23) & 0xff) # float
    exponent -= 127.0
    exponent = pow(2,exponent)
    mantissa = (longValue & 0x7fffff)
    mantissa = 1.0 + (mantissa/8388607.0)
    floatValue = mantissa * exponent
    if ((longValue & 0x80000000) == 0x80000000):
        floatValue = -floatValue
    return floatValue 

def parseLine(line):
    """Returns an array of Coordinates"""
    if line.startswith("$PMTKLOX,1"):
        data, actual_checksum = line.split("*")

        generated_checksum = checksum(data)
        actual_checksum = actual_checksum.strip()

        if generated_checksum != actual_checksum:
            # TODO stop processing?
            print >> sys.stderr, "WARNING: Checksum failed. Expected %s but calculated %s for %s" % (actual_checksum, generated_checksum, line)

        parts = data.split(",")
        
        # remove the first 3 parts - command, type, line_number
        # following this 8 byte hex strings (max 24)
        dataFields = parts[3:]

        # turn the remaining data into a byte array
        bytes = toByteArray("".join(dataFields)) # could call in a loop appending instead of join

        # Slice into chunks based on the record size
        records = []

        chunksize = 16 # Basic logging
        while len(bytes) >= chunksize:

            record = parseBasicRecord(bytes[:chunksize])
            records.append(record)
            bytes = bytes[chunksize::]

        return records

# http://www.hhhh.org/wiml/proj/nmeaxor.html
def checksum(line):
    check = 0

    # XOR all the chars in the line except leading $
    for char in line[1:]:
        check = check ^ ord(char)

    # convert to hex string, remove 0x, 0 pad 
    return hex(check)[2:].upper().zfill(2)

# See "LOCUS logging content.pdf" 
# http://learn.adafruit.com/adafruit-ultimate-gps/downloads-and-resources
#
# Basic Record - 16 bytes
# 0 - 3 timestamp
# 4 fix flag
# 5 - 8 latitude
# 9 - 12 longitude
# 13 - 14 height
def parseBasicRecord(bytes):

    timestamp = parseLong(bytes[0:4])
    # if timestamp > 4290000000: # skip bad values
    #     continue    
        
    date = datetime.fromtimestamp(timestamp)
    fix = bytes[4] # TODO bit flag     unsigned char u1VALID = 0x00;  // 0:NoFix , 1: Fix, 2: DGPS, 6: Estimated
    latitude = parseFloat(bytes[5:9])
    longitude = parseFloat(bytes[9:13])
    height = parseInt(bytes[13:15])

    return Coordinates(date, fix, latitude, longitude, height)

def parseFile(filename):
    f = open(filename, "r")

    coords = []

    for line in f.readlines():
        results = parseLine(line)
        if (results):
            coords += (results)

    return coords
 
# TODO Is Coordinates the right name? Or would it be better to have a
# Position object that contains a TimeStamp and Coordinates?
# Or just replace this class with a dictionary?
class Coordinates:

    def __init__(self, datetime, fix, latitude, longitude, height):
        self.datetime = datetime
        self.fix = fix
        self.latitude = latitude
        self.longitude = longitude
        self.height = height

    def __repr__(self):
        return pformat(self.__dict__)

    # TODO fix formatting
    def __str__(self):
        return """
        datetime: %s
        fix: %s
        latitude: %3.14f
        longitude: %3.14f
        height: %i
        """ % (self.datetime, self.fix, self.latitude, self.longitude, self.height)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
		
if __name__ == "__main__":
    from pprint import pprint
    coords = parseFile("sample.log")

    # remove invalid and print
    coords = [c for c in coords if c.fix < 5]
    pprint(coords)


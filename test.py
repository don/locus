import locus
import unittest
from datetime import datetime

class TestLocusParser(unittest.TestCase):

    def test_toByteArray(self):
        val = locus.toByteArray("FFFF")
        self.assertEqual(val, [255, 255])

        val = locus.toByteArray("000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F")
        self.assertEqual(val, range(32))

        val =locus.toByteArray('DA324F52')
        self.assertEqual(val, [218, 50, 79, 82])

    def test_parseInt(self):
        val = locus.parseInt([0xC, 0x0])
        self.assertEqual(val, 12)

        val = locus.parseInt([255, 255])
        self.assertEqual(val, 65535)

    def test_parseLong(self):
        val = locus.parseLong([218, 50, 79, 82])
        self.assertEqual(val, 1380922074)

    def test_parseFloat(self):
        val = locus.toByteArray("31AD2042")
        self.assertEqual(val, [49, 173, 32, 66])

        val1 = locus.parseFloat(val)
        self.assertEqual(val1, 40.16913320650258)

    def test_checksum(self):
        val = locus.checksum("$PMTK000")
        self.assertEqual(val, '32')

        val = locus.checksum("")
        self.assertEqual(val, '00')

        val = locus.checksum("$PMTKLOX,1,1,0ADE5552,04A58920,42926996,C21D002B,19DE5552,04A78920,42926996,C21D003A,28DE5552,04A78920,42926996,C21D000B,37DE5552,04A98920,42926996,C21E0019,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF")
        self.assertEqual(val, '5B')

    def test_parseBasicRecord(self):
        record = "19DE5552,04A78920,42926996,C21D003A"
        bytes = locus.toByteArray(record.replace(',',''))
        val = locus.parseBasicRecord(bytes)
        expected = locus.Coordinates(datetime(2013, 10, 9, 18, 52, 9), 
            4, 40.13442708664263, -75.20619335248391, 29)

        self.assertEqual(val, expected)

    def test_parseLine(self):
        line = "$PMTKLOX,1,1,0ADE5552,04A58920,42926996,C21D002B*24"
        results = locus.parseLine(line)

        self.assertEqual(len(results), 1)
        val = results[0]

        self.assertEqual(val.datetime, datetime(2013, 10, 9, 18, 51, 54))
        self.assertEqual(val.fix, 4)
        self.assertEqual(val.latitude, 40.13441945724719)
        self.assertEqual(val.longitude, -75.20619335248391)
        self.assertEqual(val.height, 29)

        line = "$PMTKLOX,1,1,0ADE5552,04A58920,42926996,C21D002B,19DE5552,04A78920,42926996,C21D003A,28DE5552,04A78920,42926996,C21D000B,37DE5552,04A98920,42926996,C21E0019,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF,FFFFFFFF*5B"
        results = locus.parseLine(line)

        self.assertEqual(len(results), 6)
        # the first entry should be the same as val from the first test
        self.assertEqual(results[0], val)

if __name__ == '__main__':
    unittest.main()
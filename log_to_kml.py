#!/usr/bin/env python

# Generate KML from a LOCUS log file
# KML template is based on the output from
#    http://learn.adafruit.com/custom/ultimate-gps-parser
#
# usage: python kml.py > example.kml
# open the generated example.kml in Google Earth
#
# (c) 2013 Don Coleman 

import locus

coords = locus.parseFile('sample.log')

# filter out any bad records
coords = [c for c in coords if c.fix > 0 and c.fix < 5] 

# format each coordinate for kml
data = map(lambda c: "%3.14f,%3.14f,%s" % (c.longitude, c.latitude, c.height), coords)

template = """<?xml version="1.0" encoding="UTF-8"?> 
  <kml xmlns="http://www.opengis.net/kml/2.2"> 
   <Document> 
     <name>GPS Path</name> 
     <description>Path parsed from GPS data.</description> 
    <Style id="yellowLineGreenPoly"> 
       <LineStyle> 
         <color>7f00ffff</color> 
         <width>4</width> 
         <gx:labelvisibility>0</gx:labelvisibility> 
       </LineStyle> 
       <PolyStyle> 
         <color>7f00ff00</color> 
       </PolyStyle> 
     </Style> 
     <Placemark> 
       <scale>0</scale> 
       <name>Begin</name> 
       <description>Start GPD Data</description> 
       <styleUrl>#yellowLineGreenPoly</styleUrl> 
       <LineString> 
         <extrude>1</extrude> 
         <tessellate>1</tessellate> 
         <altitudeMode>absolute</altitudeMode> 
         <coordinates>
%s
 		 </coordinates>
       </LineString>
     </Placemark>
   </Document>
 </kml>
"""

print template % "\n".join(data)

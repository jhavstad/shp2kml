#! /usr/bin/env python

import math

def ToWebMercator(lon, lat):
  factor1 = 0.017453292519943295
  factor2 = 6378137.0
  factor3 = 3189068.5

  num = lon * factor1
  x = factor2 * num
  a = lat * factor1

  mercatorLon = x
  mercatorLat = factor3 * math.log((1.0 + math.sin(a)) / (1.0 - math.sin(a)))

  return mercatorLon, mercatorLat

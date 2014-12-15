#! /usr/bin/env python

import os
import kmldom
import shapefile
import sys

import Coordinates
import MapRegions

def isOuterRing(currentPoint, previousPoint):
        if currentPoint[1] > previousPoint[1]:
		if currentPoint[0] > previousPoint[0]:
			return True
		else:
			return False
	else:
		if currentPoint[0] < previousPoint[0]:
			return True
		else:
			return False

def shp2kml(shpFilename, kmlFilename):
	#shpfile_reader = shapefile.Reader(shpFilename)
	#shapes = shpfile_reader.shapes()
	map_regions = MapRegions.getMapRegions(shpFilename)
	factory = kmldom.KmlFactory.GetFactory()
	document = factory.CreateDocument()
	
	sys.stdout.write('Starting')

	for lrr in map_regions.iterkeys():
		sys.stdout.write('+')
		lrr_folder = factory.CreateFolder()
		lrr_folder.set_name(lrr)
		lrr_folder.set_description(map_regions[lrr]['description'])
		for mlra in map_regions[lrr]['mlras']:
			mgeom_mlra = factory.CreateMultiGeometry()

			for shape in map_regions[lrr]['mlras'][mlra]:

				for part in shape.parts:

					coords = factory.CreateCoordinates()
					start_index = part

					end_index = len(shape.points)

					if shape.parts.index(part) < len(shape.parts) - 1:
						end_index = shape.parts[shape.parts.index(part)+1]

					for index in range(start_index, end_index):
						point = shape.points[index]

						mercatorLon, mercatorLat = Coordinates.ToWebMercator(point[0], point[1])
						coords.add_latlng(mercatorLat, mercatorLon)
			
					linear_ring = factory.CreateLinearRing()
					linear_ring.set_altitudemode(0)
					linear_ring.set_tessellate(True)
					linear_ring.set_coordinates(coords)
		
					mgeom_mlra.add_geometry(linear_ring)
					sys.stdout.write('.')

			pmark = factory.CreatePlacemark()
			pmark.set_name(mlra)
			pmark.set_geometry(mgeom_mlra)
			lrr_folder.add_feature(pmark)
			sys.stdout.write('-')

		document.add_feature(lrr_folder)

		sys.stdout.write('*\n')

	
	kml = factory.CreateKml()
	kml.set_feature(document)
	xml = kmldom.SerializePretty(kml)
	fout = open(kmlFilename, 'w')
	fout.write(xml)
	fout.close()
	sys.stdout.write('\n')
		
def main(argv):
	shpFilename = None

	if len(argv) > 1:
		shpFilename = argv[1]

	if shpFilename != None:
		dotIndex = shpFilename.rindex('.')
		kmlFilename = shpFilename[0:dotIndex] + '.kml'
		print('Converting ' + shpFilename + ' to ' + kmlFilename)
		shp2kml(shpFilename, kmlFilename)
		print('All done!')
	else:
		print('No inputs.  Quitting')

if __name__ == '__main__':
	main(sys.argv)


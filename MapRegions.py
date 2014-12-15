import shapefile
import sys

default_filename = 'nrcs/mlra_v42.shp'

def getMapRegions(filename):
  reader = shapefile.Reader(filename)
  records = reader.records()
  shapes = reader.shapes()
  print('Found ' + str(len(shapes)) + ' records in shapefile ' + filename)
  map_regions = dict()
  for i in range(len(shapes)):
    #print('Reading record ' + str(i) + ' in shapefile')
    shape = shapes[i]
    record = records[i]
    lrr = record[3]
    mlra = record[0]
    desc = record[2]
    #print('Current LRR: ' + str(lrr))
    #print('Current MLRA: ' + str(mlra))
    if not lrr in map_regions:
      map_regions[lrr] = dict()
      map_regions[lrr]['description'] = desc
      map_regions[lrr]['mlras'] = dict()
    if not mlra in map_regions[lrr]['mlras']:
      map_regions[lrr]['mlras'][mlra] = list()
    map_regions[lrr]['mlras'][mlra].append(shape)

  return map_regions

def main(argv):
  getMapRegions(default_filename)

if __name__ == "__main__":
  main(sys.argv)

from PIL import Image
import pprint
import random as r

class Path:
  """
  Class that maps a path across our Map object. Keeps track of a
  list of tuples, containing the coordinates that it visits on its
  way across the map, and tracks its elevation change step to step.
  """
  def __init__(self, MapData, position = (0,0)):
    self.coordinates = MapData.coordinates
    self.path = [position]
    self.elevation_change = []
    self.position = position
    print(self.position)
  
  
    

class MapData:
  """
  Class that holds onto information about our map and draws on it.
  """
  def __init__(self, elevation_file):
    self.data = elevation_file
    self.paths = []
    self.coordinates = {}
  
  def assign_coordinates(self, data):
    with open(data) as data:
      raw = data.readlines()
      rows = [row.split()for row in raw]
      for y in range(len(rows)):
        for x in range(len(rows)):
          self.coordinates[(x,y)]=int(rows[y][x])
    self.min_elevation = self.get_min_elevation()
    self.max_elevation = self.get_max_elevation()
          
  def get_max_elevation(self):
    return max(self.coordinates.items(),key=lambda x: x[1])[1]
    
  def get_min_elevation(self):
    return min(self.coordinates.items(),key=lambda x: x[1])[1]
    
  def get_color(self, elevation):
    scale = (elevation - self.min_elevation) / (self.max_elevation - self.min_elevation)
    greyscale = int(255*scale)
    return (greyscale, greyscale, greyscale, 255)
  
  def draw_topo_map(self):
    size = max(self.coordinates)
    print(size)
    self.canvas = Image.new('RGBA',(size[0]+1, size[1]+1))
    for item in self.coordinates.items():
      self.canvas.putpixel(item[0], self.get_color(item[1]))
    self.canvas.save('test.png')
    pass
    
  def forge_random_path(self):
    y_start = r.randrange(max(self.coordinates)[1]+1)
    self.paths.append(Path(self, (0,y_start)))

if __name__ == "__main__":
  new_map = MapData('elevation_small.txt')
  new_map.assign_coordinates(new_map.data)
  # new_map.draw_topo_map()
  new_map.forge_random_path()
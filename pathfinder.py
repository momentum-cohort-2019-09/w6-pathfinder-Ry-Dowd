from PIL import Image
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
    self.max_x = max(self.coordinates)[0]
    self.max_y = max(self.coordinates)[1]
    print(self.position)
    self.walk()
    
  # def valid_steps(self):
  #   current_x = self.position[0] 
  #   current_y = self.position[1]    
    
  def valid_forward_steps(self):
    current_x = self.position[0] 
    current_y = self.position[1]
    
    return[(current_x+1, choice) for choice in range(current_y-1, current_y+2)if (0 <= choice <= self.max_y)]
   
  def choose_step(self, valid_steps):
    current_elevation = self.coordinates[self.position]
    options_dict = {step:(abs(current_elevation-self.coordinates[step])+r.random()) for step in valid_steps}
    choice = min(options_dict.items(), key = lambda x:x[1])
    self.elevation_change.append(int(choice[1]))
    return choice[0]
    
  def take_step(self):
    valid_steps = self.valid_forward_steps()
    self.position = self.choose_step(valid_steps)
    self.path.append(self.position)
    
    
    
  def walk(self):
    while self.position[0] < self.max_x:
      self.take_step()
    else:
      self.total_elevation_change = sum(self.elevation_change)
      print(self.total_elevation_change)
      # print(self.path)
  
  
    

class MapData:
  """
  Class that holds onto information about our map and draws on it.
  """
  def __init__(self, elevation_file):
    self.data = elevation_file
    self.paths = []
    self.coordinates = {}
    self.path_set = set()
  
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
    
  def forge_random_path(self):
    y_start = r.randrange(max(self.coordinates)[1]+1)
    self.paths.append(Path(self, (0, y_start)))
    
  def forge_all_paths(self):
    for y in range(max(self.coordinates)[1]+1):
      self.paths.append(Path(self, (0, y)))
    
    
  def draw_paths(self):
    for path in self.paths:
      for location in path.path:
        self.path_set.add(location)
    for location in self.path_set:
      self.canvas.putpixel(location, (255,0,0,255))
      # print('painting')
    self.canvas.save('test.png')
    
  def draw_best_path(self):
    best_path = min(self.paths, key= lambda path:path.total_elevation_change)
    print(best_path.total_elevation_change)
    print("drawing best path")
    for location in best_path.path:
      self.canvas.putpixel(location, (0,255,0,255))
    self.canvas.save('test.png')

if __name__ == "__main__":
  new_map = MapData('elevation_large.txt')
  new_map.assign_coordinates(new_map.data)
  new_map.draw_topo_map()
  # new_map.forge_random_path()
  new_map.forge_all_paths()
  new_map.draw_paths()
  new_map.draw_best_path()
from PIL import Image
import random as r
# from multiprocessing import Pool
import argparse

class Path:
  """
  Class that maps a path across our Map object. Keeps track of a
  list of tuples, containing the coordinates that it visits on its
  way across the map, and tracks its elevation change step to step.
  """
  def __init__(self, MapData, position, max_x, max_y):
    self.coordinates = MapData.coordinates
    self.path = [position]
    self.elevation_change = []
    self.position = position
    self.elevation = self.coordinates[self.position]
    self.max_x = max_x
    self.max_y = max_y
    self.negative_change = []
    self.walk()
    
    
  def valid_steps(self):
    current_x = self.position[0] 
    current_y = self.position[1]
    valid = [(x,y)for x in range(current_x, current_x +2) for y in range(current_y - 1, current_y + 2) if (0<= x <= self.max_x) & (0<= y <= self.max_y)]
    return [option for option in valid if option not in self.path[-2:]]
    
  def valid_forward_steps(self):
    current_x = self.position[0] 
    current_y = self.position[1]
    
    return[(current_x+1, choice) for choice in range(current_y-1, current_y+2)if (0 <= choice <= self.max_y)]
  
  def choose_downhill(self,options):
    current_elevation = self.coordinates[self.position]
    options_dict = {step:(current_elevation - self.coordinates[step]+r.random()) for step in options}
    choice = min(options_dict.items(), key = lambda x:x[1])
    self.elevation_change.append(int(choice[1]))
    self.elevation = self.coordinates[choice[0]]
    if int(choice[1]) <= 0:
      self.negative_change.append('y')
    return choice[0]
   
  def choose_step(self, options):
    current_elevation = self.coordinates[self.position]
    options_dict = {step:(abs(current_elevation-self.coordinates[step])+r.random()) for step in options}
    choice = min(options_dict.items(), key = lambda x:x[1])
    self.elevation_change.append(int(choice[1]))
    self.elevation = self.coordinates[choice[0]]
    return choice[0]
    
  def take_step(self):
    options = self.valid_forward_steps()
    self.position = self.choose_step(options)
    self.path.append(self.position)
    
  def walk(self):
    while self.position[0] < self.max_x:
      self.take_step()
    else:
      self.total_elevation_change = sum(self.elevation_change)
  
  
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
        for x in range(len(rows[0])):
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
    self.size = max(self.coordinates)
    print(self.size)
    self.canvas = Image.new('RGBA',(self.size[0]+1, self.size[1]+1))
    for item in self.coordinates.items():
      self.canvas.putpixel(item[0], self.get_color(item[1]))
    self.canvas.save('test.png')
    
  def forge_all_paths(self):
    # pool = Pool(processes = 2)
    coords = [(0,y) for y in range(max(self.coordinates)[1]+1)]
    # self.paths = pool.map(self.forge_path, coords)
    self.paths = [self.forge_path(coord) for coord in coords]
  
  def forge_path(self, start):
    return Path(self, start, self.size[0], self.size[1])
      
  def draw_paths(self):
    for path in self.paths:
      for location in path.path:
        self.path_set.add(location)
    for location in self.path_set:
      self.canvas.putpixel(location, (255,0,0,255))
    self.canvas.save('test.png')
    
  def draw_best_path(self):
    best_path = min(self.paths, key= lambda path:path.total_elevation_change)
    # best_path = max(self.paths, key = lambda path: len(path.negative_change))
    print(best_path.total_elevation_change)
    print("drawing best path")
    for location in best_path.path:
      self.canvas.putpixel(location, (0,255,0,255))
    self.canvas.save('test.png')


if __name__ == "__main__":
  # parser = argparse.ArgumentParser()
  
  new_map = MapData('elevation_small.txt')
  new_map.assign_coordinates(new_map.data)
  new_map.draw_topo_map()
  new_map.forge_all_paths()
  new_map.draw_paths()
  new_map.draw_best_path()
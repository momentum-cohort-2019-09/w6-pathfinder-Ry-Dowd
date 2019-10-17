from PIL import Image

blank_image = Image.new('RGBA', (600,600))

class Path:
  def __init__(self, MapData):
    self.terrain = MapData
    self.path = []
    

class MapData:
  """
  Class that holds onto information about our map and draws on it.
  """
  def __init__(self, elevation_file, width, height):
    self.canvas = Image.new('RGBA',(width,height))
    self.data = elevation_file
    self.paths = []
import pygame
import json

class TileSet(object):
	def __init__(self, filename, tile_width, tile_height):
		super(TileSet, self).__init__()
		self.tile_width = tile_width
		self.tile_height = tile_height
		self._load(filename)

	def _load(self, filename):
		self.img = pygame.image.load(filename).convert_alpha()
		self._split_images()

	def _split_images(self):
		width, height = self.img.get_size()
		self.tiles = []
		for tile_y in range(0, height/self.tile_height):
			for tile_x in range(0, width/self.tile_width):
				rect = (
					tile_x * self.tile_width,
					tile_y * self.tile_height,
					self.tile_width,
					self.tile_height)
				self.tiles.append(self.img.subsurface(rect))

class Layer(object):
	def __init__(self, name, data, width, height):
		super(Layer, self).__init__()
		self.name = name
		self.data = data
		self.width = width
		self.height = height
		print("layer '%s' has %d tiles" % (name, len(data)))

class TileMap(object):
	def __init__(self, filename):
		super(TileMap, self).__init__()
		self.filename = filename
		self._parse()

	def _read_input(self):
		f = open(self.filename)
		self._data = json.load(f)
		f.close()

	def _parse(self):
		self._read_input()
		self._tilesets = []
		self._layers = []
		try:
			self.tile_width = self._data["tilewidth"]
			self.tile_height = self._data["tileheight"]
			for tileset in self._data["tilesets"]:
				self._tilesets.append(TileSet(
					tileset["image"],
					self.tile_width,
					self.tile_height))
			for layer in self._data["layers"]:
				self._layers.append(Layer(
					layer["name"],
					layer["data"],
					layer["width"],
					layer["height"]))
		except KeyError as e:
			print("Failed to parse tile map %s" % self.filename)
			raise e

	def draw(self, screen, x, y):
		width, height = screen.get_size()
		for layer in self._layers:
			for tile_y in range(0, height / self.tile_height):
				for tile_x in range(0, width / self.tile_width):
					id_index = tile_x + tile_y * layer.width
					if id_index < 0 or id_index > len(layer.data) - 1:
						continue
					id = layer.data[id_index]
					tile = self._tilesets[0].tiles[id - 1]
					rect = (tile_x * self.tile_width + x,
						tile_y * self.tile_height + y,
						self.tile_width,
						self.tile_height)
					screen.blit(tile, rect)

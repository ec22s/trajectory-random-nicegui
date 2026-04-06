import random
from functools import reduce
from nicegui import ui

POINTS_RANGE = [16, 64]
LAT_RANGE = [33.2, 33.3]
LON_RANGE = [130.1, 130.2]
LINE_COLOR_1 = 'yellow'
LINE_COLOR_2 = 'red'
MAP_URL_1 = 'https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg'
MAP_URL_2 = 'https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png'
MAP_ATTRIBUTION = '<a href="https://maps.gsi.go.jp/development/ichiran.html">国土地理院</a>'
CSS = '''
  .nicegui-content {
    margin: 0;
    padding: 0;
  }
  .leaflet {
    height: 100vh;
    z-index: -1;
  }
  .overlay {
    position: absolute;
    left: 12px;
    top: 96px;
    z-index: 1;
  }
  .icon-button {
    font-size: 10px;
    padding: 0;
    height: 30px;
    width: 30px;
    overflow: hidden;
  }
'''

class Polyline:
  def __init__(self, map):
    self.coordinates = ()
    self.indexes = []
    self.start_index = 0
    self.end_index = None
    self.layer = None
    self.map = map
    self.color = LINE_COLOR_1
    self.random()

  def random(self):
    self.set_coordinates(random_coordinates(
      POINTS_RANGE,
      LAT_RANGE,
      LON_RANGE,
    ))
    self.sew_coordinates()

  def set_coordinates(self, coordinates):
    self.coordinates = coordinates
    self.start_index = 0

  def change_start_point(self):
    candidates = list(range(len(self.coordinates)))
    [candidates.remove(x) for x in (self.start_index, self.end_index)]
    if len(candidates) == 0:
      # TODO: handle unexpected status
      return

    old_start = self.start_index
    old_end = self.end_index
    self.start_index = random.sample(candidates, 1)[0]
    self.sew_coordinates()

  def sew_coordinates(self):
    # 点をsew縫う
    coords = self.coordinates
    total_indexes = set(range(len(coords)))
    if len(total_indexes) == 0:
      # TODO: handle unexpected status
      return

    self.indexes = [self.start_index]

    while True:
      [end_lat, end_lng] = coords[self.indexes[-1]]
      dist_squared_min = None
      nearest_index = None
      for i in (total_indexes - set(self.indexes)):
        [lat, lng] = coords[i]
        dist_squared = (end_lat - lat)**2 + (end_lng - lng)**2
        if dist_squared_min is not None and dist_squared_min < dist_squared:
          continue

        # TODO: 交差した箇所の点を入れ替えたい
        dist_squared_min = dist_squared
        nearest_index = i
      if nearest_index is None:
        # TODO: handle unexpected result
        break

      self.indexes.append(nearest_index)
      if len(self.indexes) == len(total_indexes):
        self.end_index = nearest_index
        break

    self.update()

  def show_points(self):
    ui.notify(self.coordinates)

  def remove(self):
    try:
      self.map.leaflet.remove_layer(self.layer)
    except:
      """do nothing"""

  def update(self):
    self.remove()
    coords = tuple(map(lambda x: self.coordinates[x], self.indexes))
    if len(coords) == 0:
      # TODO: handle unexpected status
      return

    m = self.map.leaflet
    self.layer = m.generic_layer(
      name='polyline', args=[coords, {'color': self.color}]
    )
    m.run_map_method(
      'fitBounds', [[
        reduce(lambda x, y: [min(x[0], y[0]), min(x[1], y[1])], coords),
        reduce(lambda x, y: [max(x[0], y[0]), max(x[1], y[1])], coords)
      ]]
    )

  def toggle_map_style(self):
    if self.map.url == MAP_URL_1:
      self.color = LINE_COLOR_2
      self.map.url = MAP_URL_2
    else:
      self.color = LINE_COLOR_1
      self.map.url = MAP_URL_1
    self.map.toggle_style()
    self.update()

class Map:
  def __init__(self, url):
    self.url = url
    self.leaflet = ui.leaflet(options={'zoomSnap': 0.25}).classes('leaflet')
    self.leaflet.clear_layers()
    self.leaflet.tile_layer(
      url_template=url,
      options={'attribution': MAP_ATTRIBUTION},
    )

  async def initialize(self):
    await self.leaflet.initialized()

  def toggle_style(self):
    self.leaflet.clear_layers()
    self.leaflet.tile_layer(
      url_template=self.url,
      options={'attribution': MAP_ATTRIBUTION},
    )

@ui.page('/')
async def page():
  ui.add_css(CSS)
  m = Map(MAP_URL_1)
  await m.initialize()
  poly = Polyline(m)
  with ui.column().classes('gap-2 overlay'):
    custom_button('map', poly.toggle_map_style, 'Toggle map style')
    custom_button('cached', poly.random, 'Random points')
    custom_button('timeline', poly.change_start_point, 'Random route')
    custom_button('code', poly.show_points, 'Show coordinates')

def custom_button(icon, func, tooltip):
  button = ui.button(color='white', icon=icon, on_click=func).classes('icon-button')
  with button:
    ui.tooltip(tooltip)
  return  button

def random_coordinates(
  points_range,
  lat_range,
  lon_range
):
  return tuple(map(lambda x: [
    random.uniform(lat_range[0], lat_range[1]),
    random.uniform(lon_range[0], lon_range[1])
  ], range(random.randint(points_range[0], points_range[1]))))

ui.run()

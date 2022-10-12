import math

R_MAJOR = 6378137.000
R_MINOR = 6356752.3142
RATIO = R_MINOR / R_MAJOR
ECCENT = math.sqrt(1.0 - (RATIO * RATIO))
COM = 0.5 * ECCENT

DEG2RAD = math.pi / 180.0
RAD2Deg = 180.0 / math.pi
PI_2 = math.pi / 2.0


def rad_to_deg(rad):
  return rad * RAD2Deg


def deg_to_rad(deg):
  return deg * DEG2RAD


def lon_to_x(lon):
  return R_MAJOR * deg_to_rad(lon)


def lat_to_y(lat):
  lat = min(89.5, max(lat, -89.5))
  phi = deg_to_rad(lat)
  sin_phi = math.sin(phi)
  con = ECCENT * sin_phi
  con = math.pow(((1.0 - con) / (1.0 + con)), COM)
  ts = math.tan(0.5 * ((math.pi * 0.5) - phi)) / con

  return 0 - R_MAJOR * math.log(ts)


def x_to_lon(x):
  return rad_to_deg(x) / R_MAJOR


def y_to_lat(y):
  ts = math.exp(-y / R_MAJOR)
  phi = PI_2 - 2 * math.atan(ts)
  d_phi = 1.0
  i = 0
  while (math.fabs(d_phi) > 0.000000001) and (i < 15):
     con = ECCENT * math.sin(phi)
     d_phi = PI_2 - 2 * math.atan(ts * math.pow((1.0 - con) / (1.0 + con), COM)) - phi
     phi += d_phi
     i += 1

  return rad_to_deg(phi)


def coord3857_to4326(x3857, y3857):
  e_value = 2.7182818284
  x = 20037508.34

  lon4326 = (x3857 * 180) / x

  lat4326 = y3857 / (x / 180)
  exponent = (math.pi / 180) * lat4326

  lat4326 = math.atan(math.pow(e_value, exponent))
  lat4326 = lat4326 / (math.pi / 360)
  lat4326 = lat4326 - 90

  return lat4326, lon4326


def coord4326_to3857(lat, lon):
  x = (lon * 20037508.34) / 180
  y = math.log(math.tan(((90 + lat) * math.pi) / 360)) / (math.pi / 180)
  y = (y * 20037508.34) / 180

  return x, y


def lon_to_tile_x(lon, z):
  return int(math.floor((lon + 180.0) / 360.0 * (1 << z)))


def lat_to_tile_y(lat, z):
  return int(math.floor((1 - math.log(math.tan(to_radians(lat)) + 1 / math.cos(to_radians(lat))) / math.pi) / 2 * (1 << z)))


def tile_x_to_lon(x, z):
  return x / (1 << z) * 360.0 - 180


def tile_y_to_lat(y, z):
  n = math.pi - 2.0 * math.pi * y / (1 << z)
  return 180.0 / math.pi * math.atan(0.5 * (math.exp(n) - math.exp(-n)))


def tile_x_to_position_x(x, z):
  lon = tile_x_to_lon(x, z)
  x3857, y3857 = coord4326_to3857(0, lon)
  return x3857


def tile_y_to_position_y(y, z):
  lat = tile_y_to_lat(y, z)
  x3857, y3857 = coord4326_to3857(lat, 0)
  return y3857


def to_radians(val):
  return (math.pi / 180) * val


def position_to_tile(x3857, y3857, zoom):
  lat, lon = position_to_lat_lon(x3857, y3857)
  tile_x = lon_to_tile_x(lon, zoom)
  tile_y = lat_to_tile_y(lat, zoom)
  return tile_x, tile_y, lat, lon


def position_to_lat_lon(x3857, y3857):
  return coord3857_to4326(x3857, y3857)


def lat_lon_to_position(lat, lon):
  return coord4326_to3857(lat, lon)


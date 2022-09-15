import json
import os
import geopandas
from shapely import wkt
from shapely.geometry import LineString, Polygon, MultiPolygon, LinearRing, Point, MultiLineString, MultiPoint

CommonBufferSize = 0.05
CommonSimplifyValue = 0.5


def gdf_to_json(gdf, place_directory, file_name):
    os.makedirs(place_directory, exist_ok=True)

    json_str = gdf.to_json(ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': '))
    json_str.encode('utf8')
    with open(f'{place_directory}/{file_name}.json', 'w', encoding='utf-8') as f:
        f.write(json_str)


def gdf_from_json(directory, file_name):
    path = f'{directory}/{file_name}.json'
    if not os.path.exists(path):
        return None

    return geopandas.GeoDataFrame.from_file(path, encodings='utf-8')


def json_from_json(directory, file_name):
    path = f'{directory}/{file_name}.json'
    if not os.path.exists(path):
        return None

    with open(f'{directory}/{file_name}.json', 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def import_wkt(file_full_path):
    if not os.path.exists(file_full_path):
        return list()

    obj_list = list()
    with open(file_full_path, 'r') as f:
        for line in f:
            current_place = line[:-1]
            obj = wkt.loads(current_place)
            obj_list.append(obj)

    return obj_list


def import_polygon_from_json(directory, file_name, buffer_size=CommonBufferSize):
    gdf = gdf_from_json(directory, f'gdf_{file_name}')
    if gdf is None:
        return list()

    geometry = gdf['geometry']
    polygon_list = list()
    for i in range(len(geometry)):
        it = geometry[i]

        if 0 < buffer_size:
            polygon_list.append(it.buffer(buffer_size))
        else:
            if type(it) == Polygon or type(it) == MultiPolygon:
                polygon_list.append(it)

    return polygon_list


def export_wkt_inner(f, obj, buffer_size, simplify_value):
    if 0 < buffer_size:
        obj = obj.buffer(buffer_size)

    if type(obj) == Polygon or type(obj) == MultiPolygon:
        if 0 < simplify_value:
            obj = obj.simplify(simplify_value)
        if not obj.is_valid:
            obj = obj.buffer(0)

    if type(obj) == MultiPolygon or type(obj) == MultiLineString or type(obj) == MultiPoint:
        for it2 in obj.geoms:
            f.write(f"{it2}\n")
    elif type(obj) == Point or type(obj) == LinearRing or type(obj) == LineString or type(obj) == Polygon:
        f.write(f"{obj}\n")
    else:
        print(f'type({type(obj)}) is not defined')


def export_wkt(directory, file_name, obj, buffer_size=CommonBufferSize, simplify_value=CommonSimplifyValue):
    with open(f'{directory}/{file_name}', 'w') as f:
        if obj is None:
            pass
        elif type(obj) == list:
            for it in obj:
                export_wkt_inner(f, it, buffer_size, simplify_value)
        elif type(obj) == MultiPolygon or type(obj) == MultiLineString or type(obj) == MultiPoint:
            for it in obj.geoms:
                export_wkt_inner(f, it, buffer_size, simplify_value)
        elif type(obj) == Point or type(obj) == LinearRing or type(obj) == LineString or type(obj) == Polygon:
            export_wkt_inner(f, obj, buffer_size, simplify_value)
        else:
            print(f'type({type(obj)}) is not defined')


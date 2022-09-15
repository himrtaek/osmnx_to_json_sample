from shapely.geometry import LineString

import osm_util


def way_polygon_from_json(directory):
    gdf = osm_util.json_from_json(directory, 'gdf_way')
    if gdf is None:
        return list()

    features = gdf.get('features')

    way_polygon_list = way_parsing(features)
    return way_polygon_list


def way_parsing(features):
    way_polygon_list = list()

    for i in range(len(features)):
        buffer_size = 4

        point_list = list()
        for j in range(len(features[i]['geometry']['coordinates'])):
            coord = features[i]['geometry']['coordinates'][j]
            point_list.append(coord)

        if len(point_list) < 2:
            continue

        line_string = LineString(point_list)
        highway_key = features[i]['properties']['highway']

        if 'motorway_link' in highway_key:
            buffer_size = 8
        elif 'trunk_link' in highway_key:
            buffer_size = 8
        elif 'primary_link' in highway_key:
            buffer_size = 8
        elif 'secondary_link' in highway_key:
            buffer_size = 8
        elif 'tertiary_link' in highway_key:
            buffer_size = 8
        elif 'motorway' in highway_key:
            buffer_size = 12
        elif 'trunk' in highway_key:
            buffer_size = 8
        elif 'primary' in highway_key:
            buffer_size = 8
        elif 'secondary' in highway_key:
            buffer_size = 8
        elif 'tertiary' in highway_key:
            buffer_size = 8
        elif 'living_street' in highway_key:
            buffer_size = 8
        elif 'unclassified' in highway_key:
            buffer_size = 4
        elif 'residential' in highway_key:
            buffer_size = 4
        elif 'road' in highway_key:
            buffer_size = 2
        elif 'path' in highway_key:
            buffer_size = 2
        elif 'bridleway' in highway_key:
            buffer_size = 2
        elif 'footway' in highway_key:
            buffer_size = 2
        elif 'service' in highway_key:
            buffer_size = 2
        elif 'pedestrian' in highway_key:
            buffer_size = 2
        elif 'steps' in highway_key:
            buffer_size = 2
        elif 'track' in highway_key:
            buffer_size = 2
        elif 'elevator' in highway_key:
            buffer_size = 2
        elif 'crossing' in highway_key:
            continue
        elif 'corridor' in highway_key:
            continue
        else:
            print(highway_key)

        cap_style = 1
        join_style = 1
        way_polygon = line_string.buffer(buffer_size, cap_style=cap_style, join_style=join_style)
        way_polygon_list.append(way_polygon)

    return way_polygon_list


def main(directory):
    way_polygon_list = way_polygon_from_json(directory)

    # Export
    osm_util.export_wkt(directory, 'Polygons_Way.txt', way_polygon_list)


if __name__ == '__main__':
    Directory = 'Seoul'

    main(Directory)

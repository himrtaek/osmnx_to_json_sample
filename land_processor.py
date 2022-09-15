import shapely.ops

import osm_util


def main(directory):
    # Import
    boundary_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Boundary.txt')
    environment_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Environment.txt')
    way_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Way.txt')

    # Union
    boundary_polygon_union = shapely.ops.unary_union(boundary_polygon_list)
    environment_polygon_union = shapely.ops.unary_union(environment_polygon_list)
    way_polygon_union = shapely.ops.unary_union(way_polygon_list)

    # Land
    land_polygon_union = boundary_polygon_union

    if not (environment_polygon_union is None):
        land_polygon_union = land_polygon_union.difference(environment_polygon_union)

    if not (way_polygon_union is None):
        land_polygon_union = land_polygon_union.difference(way_polygon_union)

    # Export
    osm_util.export_wkt(directory, 'Polygons_Land.txt', land_polygon_union)


if __name__ == '__main__':
    Directory = 'Seoul'

    main(Directory)

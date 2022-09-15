import shapely.ops

import osm_util


def main(directory):
    # Import
    way_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Way.txt')
    natural_boundary_polygon_list = osm_util.import_polygon_from_json(directory, 'boundary')
    natural_water_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_water')
    natural_grass_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_grass')
    natural_garden_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_garden')
    natural_park_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_park')
    natural_wood_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_wood')
    natural_farm_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_farm')

    # Union
    way_polygon_union = shapely.ops.unary_union(way_polygon_list)
    natural_boundary_polygon_union = shapely.ops.unary_union(natural_boundary_polygon_list)
    natural_water_polygon_union = shapely.ops.unary_union(natural_water_polygon_list)
    natural_grass_polygon_union = shapely.ops.unary_union(natural_grass_polygon_list)
    natural_garden_polygon_union = shapely.ops.unary_union(natural_garden_polygon_list)
    natural_park_polygon_union = shapely.ops.unary_union(natural_park_polygon_list)
    natural_wood_polygon_union = shapely.ops.unary_union(natural_wood_polygon_list)
    natural_farm_polygon_union = shapely.ops.unary_union(natural_farm_polygon_list)

    # Intersection
    if not (natural_water_polygon_union is None):
        natural_water_polygon_union = natural_water_polygon_union.intersection(natural_boundary_polygon_union)

    if not (natural_grass_polygon_union is None):
        natural_grass_polygon_union = natural_grass_polygon_union.intersection(natural_boundary_polygon_union)

    if not (natural_garden_polygon_union is None):
        natural_garden_polygon_union = natural_garden_polygon_union.intersection(natural_boundary_polygon_union)

    if not (natural_park_polygon_union is None):
        natural_park_polygon_union = natural_park_polygon_union.intersection(natural_boundary_polygon_union)

    if not (natural_wood_polygon_union is None):
        natural_wood_polygon_union = natural_wood_polygon_union.intersection(natural_boundary_polygon_union)

    if not (natural_farm_polygon_union is None):
        natural_farm_polygon_union = natural_farm_polygon_union.intersection(natural_boundary_polygon_union)

    # Diff Way
    if not (natural_grass_polygon_union is None):
        if not (way_polygon_union is None):
            natural_grass_polygon_union = natural_grass_polygon_union.difference(way_polygon_union)

    if not (natural_garden_polygon_union is None):
        if not (way_polygon_union is None):
            natural_garden_polygon_union = natural_garden_polygon_union.difference(way_polygon_union)

    if not (natural_park_polygon_union is None):
        if not (way_polygon_union is None):
            natural_park_polygon_union = natural_park_polygon_union.difference(way_polygon_union)

    if not (natural_wood_polygon_union is None):
        if not (way_polygon_union is None):
            natural_wood_polygon_union = natural_wood_polygon_union.difference(way_polygon_union)

    if not (natural_farm_polygon_union is None):
        if not (way_polygon_union is None):
            natural_farm_polygon_union = natural_farm_polygon_union.difference(way_polygon_union)

    # Diff Water
    if not (natural_grass_polygon_union is None):
        natural_grass_polygon_union = natural_grass_polygon_union.difference(natural_water_polygon_union)

    if not (natural_garden_polygon_union is None):
        natural_garden_polygon_union = natural_garden_polygon_union.difference(natural_water_polygon_union)

    if not (natural_park_polygon_union is None):
        natural_park_polygon_union = natural_park_polygon_union.difference(natural_water_polygon_union)

    if not (natural_wood_polygon_union is None):
        natural_wood_polygon_union = natural_wood_polygon_union.difference(natural_water_polygon_union)

    if not (natural_farm_polygon_union is None):
        natural_farm_polygon_union = natural_farm_polygon_union.difference(natural_water_polygon_union)

    # Environment Union
    environment_polygon_union = None
    if not (natural_water_polygon_union is None):
        if environment_polygon_union is None:
            environment_polygon_union = natural_water_polygon_union
        else:
            environment_polygon_union = environment_polygon_union.union(natural_water_polygon_union)

    if not (natural_grass_polygon_union is None):
        if environment_polygon_union is None:
            environment_polygon_union = natural_grass_polygon_union
        else:
            environment_polygon_union = environment_polygon_union.union(natural_grass_polygon_union)

    if not (natural_garden_polygon_union is None):
        if environment_polygon_union is None:
            environment_polygon_union = natural_garden_polygon_union
        else:
            environment_polygon_union = environment_polygon_union.union(natural_garden_polygon_union)

    if not (natural_park_polygon_union is None):
        if environment_polygon_union is None:
            environment_polygon_union = natural_park_polygon_union
        else:
            environment_polygon_union = environment_polygon_union.union(natural_park_polygon_union)

    if not (natural_wood_polygon_union is None):
        if environment_polygon_union is None:
            environment_polygon_union = natural_wood_polygon_union
        else:
            environment_polygon_union = environment_polygon_union.union(natural_wood_polygon_union)

    if not (natural_farm_polygon_union is None):
        if environment_polygon_union is None:
            environment_polygon_union = natural_farm_polygon_union
        else:
            environment_polygon_union = environment_polygon_union.union(natural_farm_polygon_union)

    # Export
    osm_util.export_wkt(directory, 'Polygons_Boundary.txt', natural_boundary_polygon_union)
    osm_util.export_wkt(directory, 'Polygons_Environment.txt', environment_polygon_union)
    osm_util.export_wkt(directory, 'Polygons_Water.txt', natural_water_polygon_union)
    osm_util.export_wkt(directory, 'Polygons_Grass.txt', natural_grass_polygon_union)
    osm_util.export_wkt(directory, 'Polygons_Garden.txt', natural_garden_polygon_union)
    osm_util.export_wkt(directory, 'Polygons_Park.txt', natural_park_polygon_union)
    osm_util.export_wkt(directory, 'Polygons_Wood.txt', natural_wood_polygon_union)
    osm_util.export_wkt(directory, 'Polygons_Farm.txt', natural_farm_polygon_union)


if __name__ == '__main__':
    Directory = 'Seoul'

    main(Directory)

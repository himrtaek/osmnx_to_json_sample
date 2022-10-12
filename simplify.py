import sys

import shapely
from shapely.geometry import Polygon

import mercator_projection
import osmnx_util


def convert_to_simple(place_directory, file_name, new_file_name, union=True, split_zoom=0, buffer_size=0.2,
                      simplify_tolerance=0.1):
    if 0 < split_zoom:
        union = True

    polygons = osmnx_util.import_wkt(f"{place_directory}/{file_name}.txt")
    if type(polygons) is Polygon and polygons.is_empty:
        return

    if 0 < len(polygons):
        if union:
            polygons = shapely.ops.unary_union(polygons)
            if not polygons.is_valid:
                print('if not polygons.is_valid:')
                polygons = polygons.buffer(0)

            polygons = polygons.buffer(buffer_size, join_style=2).simplify(simplify_tolerance)
        else:
            polygons_temp = list()
            for it in polygons:
                it_temp = it
                if 0 < buffer_size:
                    it_temp = it_temp.buffer(buffer_size, join_style=2)
                if 0 < simplify_tolerance:
                    it_temp = it_temp.simplify(simplify_tolerance)

                polygons_temp.append(it_temp)

            polygons = polygons_temp

        if type(polygons) is Polygon and polygons.is_empty:
            pass
        elif 0 < split_zoom:
            polygon_split_list = list()
            left_bottom, right_top = osmnx_util.get_lb_rt(polygons)

            it_x = left_bottom[0]
            while it_x <= right_top[0]:
                align_x_next = it_x
                it_y = right_top[1]
                while left_bottom[1] <= it_y:
                    it_lat, it_lon = mercator_projection.position_to_lat_lon(it_x, it_y)
                    x_3857, y_3857 = mercator_projection.coord4326_to3857(it_lat, it_lon)
                    tile_x, tile_y, lat, lon = mercator_projection.position_to_tile(x_3857, y_3857, split_zoom)
                    align_x = mercator_projection.tile_x_to_position_x(tile_x, split_zoom)
                    align_y = mercator_projection.tile_y_to_position_y(tile_y, split_zoom)

                    align_x_next = mercator_projection.tile_x_to_position_x(tile_x + 1, split_zoom)
                    align_y_next = mercator_projection.tile_y_to_position_y(tile_y + 1, split_zoom)

                    tile_box_polygon = Polygon(
                        [(align_x, align_y), (align_x, align_y_next), (align_x_next, align_y_next),
                         (align_x_next, align_y)])

                    polygon_intersection = polygons.intersection(tile_box_polygon)
                    if not polygon_intersection.is_empty:
                        if not polygon_intersection.is_valid:
                            polygon_intersection = polygon_intersection.buffer(0)

                        polygon_split_list.append(polygon_intersection)
                    it_y = align_y_next

                it_x = align_x_next

            polygons = polygon_split_list

    osmnx_util.export_polygon_data(place_directory, f"{new_file_name}.txt", polygons, True)


def main(place_directory):
    convert_to_simple(place_directory, "Polygons_Boundary", "Simple_Polygons_Boundary")

    convert_to_simple(place_directory, "Polygons_Water", "Simple_Polygons_Water", split_zoom=16)
    convert_to_simple(place_directory, "Polygons_Park", "Simple_Polygons_Park", split_zoom=16)
    convert_to_simple(place_directory, "Polygons_Grass", "Simple_Polygons_Grass", split_zoom=16)
    convert_to_simple(place_directory, "Polygons_Garden", "Simple_Polygons_Garden", split_zoom=16)
    convert_to_simple(place_directory, "Polygons_Farm", "Simple_Polygons_Farm", split_zoom=16)
    convert_to_simple(place_directory, "Polygons_Wood", "Simple_Polygons_Wood", split_zoom=16)
    convert_to_simple(place_directory, "Polygons_Land", "Simple_Polygons_Land", split_zoom=16)
    # convert_to_simple(place_directory, "Polygons_Way", "Simple_Polygons_Way", split_zoom=15)


if __name__ == '__main__':
    PlaceDirectory = 'Seoul'
    if 1 < len(sys.argv):
        PlaceDirectory = sys.argv[1]

    main(PlaceDirectory)



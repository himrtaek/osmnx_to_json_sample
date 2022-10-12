
# 낮으면 정밀도 증가, Python/Unity 오류 발생 확률 증가
import math
import os
import sys
import traceback

import shapely
from shapely import wkt
from shapely.geometry import Polygon, MultiPolygon, Point, LinearRing, LineString, MultiLineString, MultiPoint, \
    GeometryCollection
from shapely.ops import unary_union

CommonBufferSize = 0.5
SimplifyValue = 0.5


def to_polygon(obj, buffer=0.000001):
    polygon = None
    list_temp = list()
    if type(obj) is Polygon:
        polygon = obj
    elif type(obj) is MultiPolygon:
        polygon = obj
    elif type(obj) is list:
        for it in obj:
            it_new = to_polygon(it, buffer)
            if not it_new.is_empty:
                list_temp.append(it_new)
    elif type(obj) is GeometryCollection:
        list_temp = list()
        for it in obj.geoms:
            it_new = to_polygon(it, buffer)
            if not it_new.is_empty:
                list_temp.append(it_new)
    else:
        polygon = obj.buffer(buffer)

    if polygon is None:
        if 0 < len(list_temp):
            polygon = shapely.ops.unary_union(list_temp)
        else:
            polygon = Polygon()

    if not polygon.is_valid:
        polygon = polygon.buffer(0)

    return polygon


def get_lb_rt(all_polygon_uni):
    envelope = all_polygon_uni.envelope
    x_list = list()
    y_list = list()
    for it in envelope.exterior.coords:
        x_list.append(it[0])
        y_list.append(it[1])
    left_bottom = [min(x_list), min(y_list)]
    right_top = [max(x_list), max(y_list)]
    return left_bottom, right_top


def intersection_list(intersection_polygon, polygon_list):
    polygon_list_temp = list()
    for it in polygon_list:
        new_polygon = intersection_polygon.intersection(it)
        if not new_polygon.is_empty:
            polygon_list_temp.append(new_polygon)

    return polygon_list_temp


def difference_list(difference_polygon, polygon_list):
    polygon_list_temp = list()
    for it in polygon_list:
        new_polygon = it.difference(difference_polygon)
        if not new_polygon.is_empty:
            if type(new_polygon) is Polygon:
                polygon_list_temp.append(new_polygon)
            elif type(new_polygon) is MultiPolygon:
                for it2 in new_polygon.geoms:
                    polygon_list_temp.append(it2)
            else:
                new_polygon = new_polygon.buffer(0.000001)
                if type(new_polygon) is Polygon:
                    polygon_list_temp.append(new_polygon)
                elif type(new_polygon) is MultiPolygon:
                    for it2 in new_polygon.geoms:
                        polygon_list_temp.append(it2)

    return polygon_list_temp


def intersects_list(polygon_list, polygon):
    for it in polygon_list:
        if it.intersects(polygon):
            return True

    return False


def simple_polygon(poly, d):
    if type(poly) is MultiPolygon:
        polygon_list = list()
        for it in poly.geoms:
            new_it = simple_polygon(it, d)
            polygon_list.append(new_it)

        return shapely.ops.unary_union(polygon_list)

    cf = 1  # cofactor
    simple_poly = poly.buffer(-d, join_style=2).buffer(d * cf, join_style=2)

    if not simple_poly.is_empty:
        if not simple_poly.is_valid:
            simple_poly = simple_poly.buffer(0)

        simple_poly_intersection = simple_poly.intersection(poly)
        simple_poly = simple_poly_intersection

    return simple_poly


def angle_between_points(pos1_x, pos1_y, pos2_x, pos2_y):
    return math.degrees(math.atan2(-(pos1_y - pos2_y), pos1_x - pos2_x)) - 90


def export_data_for(f, it, simplify=False, simplify_value=0):
    # new_it = shapely.geometry.polygon.orient(it)
    # it_str = str(dumps(it, rounding_precision=8))

    # 낮으면 정밀도 증가, Unity 오류 발생 확률 증가
    if simplify:
        it = it.simplify(simplify_value)
        if not it.is_valid:
            print(f"invalid polygon {it.wkt}")
            it = it.buffer(0)

        if not type(it) == Polygon:
            print(f"type(it) is {type(it)}")
            for it2 in it:
                f.write("%s\n" % str(it2))
        else:
            f.write("%s\n" % str(it))
    else:
        f.write("%s\n" % str(it))


def export_data_for_line(f, it):
    # new_it = shapely.geometry.polygon.orient(it)
    # it_str = str(dumps(it, rounding_precision=8))

    # 낮으면 정밀도 증가, Unity 오류 발생 확률 증가
    f.write(f"{it[1]};{str(it[0])};{it[2]};{it[3]}\n")


def polygon_to_list(polygon_uni):
    polygon_list = list()
    if type(polygon_uni) is Polygon:
        polygon_list.append(polygon_uni)
    elif type(polygon_uni) is MultiPolygon:
        for it in polygon_uni.geoms:
            polygon_list.append(it)
    elif type(polygon_uni) is list:
        for it in polygon_uni:
            polygon_list += polygon_to_list(it)
    else:
        print("type(polygon_uni)")

    return polygon_list


def export_polygon_data(place_directory_, filename_, polygon_, split=False, simplify=False, zero_buffer=True, simplify_value=0):
    with open(f'{place_directory_}/{filename_}', 'w') as f:
        if polygon_ is None:
            pass
        elif type(polygon_) == list:
            for it in polygon_:
                if type(it) == Polygon:
                    if not it.is_valid:
                        print(f"invalid polygon {it.wkt}")
                        if zero_buffer:
                            it = it.buffer(0)
                    export_data_for(f, it, simplify, simplify_value)
                elif type(it) == MultiPolygon:
                    for it2 in it.geoms:
                        if not it2.is_valid:
                            print(f"invalid polygon {it2.wkt}")
                            if zero_buffer:
                                it2 = it2.buffer(0)
                        export_data_for(f, it2, simplify, simplify_value)
                elif type(it) == Point or type(it) == LinearRing or type(it) == LineString:
                    f.write("%s\n" % str(it))
                elif type(it) == MultiLineString:
                    for it2 in it.geoms:
                        f.write("%s\n" % str(it2))
                else:
                    print(f'type(it) is {type(it)}')
                    export_data_for_line(f, it)
        elif type(polygon_) == Polygon:
            if not polygon_.is_valid:
                print(f"invalid polygon {polygon_.wkt}")
                if zero_buffer:
                    polygon_ = polygon_.buffer(0)
            if not polygon_.is_empty:
                export_data_for(f, polygon_, simplify, simplify_value)
        else:
            if split:
                if type(polygon_) is MultiPoint:
                    for it in polygon_:
                        f.write("%s\n" % str(it.wkt))
                else:
                    for it in polygon_.geoms:
                        if not it.is_valid:
                            print(f"invalid polygon {it.wkt}")
                            if zero_buffer:
                                it = it.buffer(0)
                        if type(it) is LineString:
                            it = it.buffer(0.001)
                        export_data_for(f, it, simplify, simplify_value)
            else:
                if not polygon_.is_valid:
                    print(f"invalid polygon {polygon_.wkt}")
                    if zero_buffer:
                        polygon_ = polygon_.buffer(0)
                if simplify:
                    f.write("%s\n" % str(polygon_.simplify(SimplifyValue).wkt))
                else:
                    f.write("%s\n" % str(polygon_.wkt))


def export_data(place_directory_, filename_, data_):
    with open(f'{place_directory_}/{filename_}', 'w', encoding='utf-8') as f:
        f.write("%s" % str(data_))


def export_data_list(place_directory_, filename_, data_):
    with open(f'{place_directory_}/{filename_}', 'w', encoding='utf-8') as f:
        for it in data_:
            f.write("%s\n" % str(it))


def import_polygon_uni(filepath):
    polygon_list = import_wkt(filepath)
    if len(polygon_list) <= 0:
        print(f"if len(polygon_list) <= 0: {filepath}")
        return None

    if 1 < len(polygon_list):
        print(f"if 0 < len(polygon_list): {filepath}")
        return None

    return polygon_list[0]


def import_wkt(filepath, null_is_empty=True):
    if not os.path.exists(filepath):
        if null_is_empty:
            return list()
        else:
            return None

    geo_list = list()
    with open(filepath, 'r') as f:
        for line in f:
            current_place = line[:-1]
            geo = wkt.loads(current_place)
            geo_list.append(geo)

    return geo_list


def import_data_list(place_directory_, filename_):
    path = f'{place_directory_}/{filename_}'
    if not os.path.exists(path):
        return list()

    f = open(path, 'r', encoding='utf-8')
    lines = f.read().splitlines()
    f.close()

    return lines


def import_data_list_as_int(place_directory_, filename_):
    path = f'{place_directory_}/{filename_}'
    if not os.path.exists(path):
        return list()

    f = open(path, 'r', encoding='utf-8')
    lines = f.read().splitlines()
    f.close()

    lines_int = list()
    for it in lines:
        lines_int.append(int(it))

    return lines_int


def import_data_list_as_float(place_directory_, filename_):
    path = f'{place_directory_}/{filename_}'
    if not os.path.exists(path):
        return list()

    f = open(path, 'r', encoding='utf-8')
    lines = f.read().splitlines()
    f.close()

    lines_int = list()
    for it in lines:
        lines_int.append(float(it))

    return lines_int


def set_buffer(multi_polygon, buffer=0.1):
    if type(multi_polygon) == Polygon:
        return multi_polygon.buffer(buffer)

    polygon_list = list()
    for it in multi_polygon.geoms:
        if type(it) is LineString:
            polygon_list.append(it.buffer(buffer))
        else:
            polygon_list.append(it.buffer(buffer))

    return unary_union(polygon_list)


def uni_to_polygon_list(uni, min_area=0):
    polygon_list = list()
    for it in uni.geoms:
        if it.area <= min_area:
            continue

        if type(it) is Polygon:
            polygon_list.append(it)
        elif type(it) is MultiPolygon:
            for it2 in it.geoms:
                polygon_list.append(it2)
        else:
            it_buffered = it.buffer(0.000001)
            if type(it_buffered) is Polygon:
                polygon_list.append(it_buffered)
            elif type(it_buffered) is MultiPolygon:
                for it2 in it_buffered.geoms:
                    polygon_list.append(it2)
            else:
                print(f'if type(it_buffered) is {type(it_buffered)}')
                traceback.print_stack(file=sys.stdout)

    return polygon_list


def list_to_polygon_list(uni, min_area=0):
    polygon_list = list()
    for it in uni:
        if it.area <= min_area:
            continue

        if type(it) is Polygon:
            polygon_list.append(it)
        elif type(it) is MultiPolygon:
            for it2 in it.geoms:
                polygon_list.append(it2)
        else:
            it_buffered = it.buffer(0.000001)
            if type(it_buffered) is Polygon:
                polygon_list.append(it_buffered)
            elif type(it_buffered) is MultiPolygon:
                for it2 in it_buffered.geoms:
                    polygon_list.append(it2)
            else:
                print(f'if type(it_buffered) is {type(it_buffered)}')
                traceback.print_stack(file=sys.stdout)

    return polygon_list


def generate_random_seed(seed_string_):
    seed_str = seed_string_
    seed_str_count = len(seed_str)
    if seed_str_count > 4:
        seed_str = seed_str[:4]

    seed_ints = []
    for _str in seed_str:
        seed_ints.append(str(ord(_str) - ord('A') + 1))
    return "".join(seed_ints)

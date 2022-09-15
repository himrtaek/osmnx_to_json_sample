from matplotlib import pyplot as plt

import draw_util
import osm_util


def main(directory):
    boundary_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Boundary.txt')
    # way_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Way.txt')
    water_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Water.txt')
    grass_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Grass.txt')
    garden_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Garden.txt')
    park_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Park.txt')
    wood_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Wood.txt')
    farm_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Farm.txt')
    land_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Land.txt')
    # building_polygon_list = osm_util.import_wkt(f'{directory}/Polygons_Building.txt')

    fig, axs = plt.subplots()

    for it in boundary_polygon_list:
        draw_util.plot_polygon(axs, it, alpha=0.1, fc='grey', linewidth=0.1)

    for it in land_polygon_list:
        draw_util.plot_polygon(axs, it, alpha=0.2, fc='salmon', linewidth=0.1)

    # for it in way_polygon_list:
    #     draw_util.plot_polygon(axs, it, alpha=0.2, fc='yellow', linewidth=0.1)

    for it in water_polygon_list:
        draw_util.plot_polygon(axs, it, alpha=0.2, fc='blue', linewidth=0.1)

    for it in grass_polygon_list:
        draw_util.plot_polygon(axs, it, alpha=0.2, fc='lime', linewidth=0.1)

    for it in garden_polygon_list:
        draw_util.plot_polygon(axs, it, alpha=0.2, fc='lightgreen', linewidth=0.1)

    for it in park_polygon_list:
        draw_util.plot_polygon(axs, it, alpha=0.2, fc='green', linewidth=0.1)

    for it in wood_polygon_list:
        draw_util.plot_polygon(axs, it, alpha=0.2, fc='brown', linewidth=0.1)

    for it in farm_polygon_list:
        draw_util.plot_polygon(axs, it, alpha=0.2, fc='beige', linewidth=0.1)

    # for it in building_polygon_list:
    #     draw_util.plot_polygon(axs, it, alpha=0.2, fc='purple', linewidth=0.1)

    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    Directory = 'Seoul'

    main(Directory)

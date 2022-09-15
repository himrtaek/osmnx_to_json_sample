from matplotlib import pyplot as plt

import draw_util
import osm_util


def main(directory):
    boundary_polygon_list = osm_util.import_polygon_from_json(directory, 'boundary')
    # way_polygon_list = osm_util.import_polygon_from_json(directory, 'way', 8)
    water_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_water')
    grass_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_grass')
    garden_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_garden')
    park_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_park')
    wood_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_wood')
    farm_polygon_list = osm_util.import_polygon_from_json(directory, 'natural_farm')
    # building_polygon_list = osm_util.import_polygon_from_json(directory, 'building')

    fig, axs = plt.subplots()

    for it in boundary_polygon_list:
        draw_util.plot_polygon(axs, it, alpha=0.2, fc='grey', linewidth=0.1)

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

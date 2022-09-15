import os.path
import osmnx
import osm_util


def download_boundary_gdf(place, directory, force):
    path = f'{directory}/gdf_boundary.json'
    if not force and os.path.exists(path):
        return

    gdf = osmnx.geocode_to_gdf(place)
    gdf = gdf.to_crs(epsg=3857)
    osm_util.gdf_to_json(gdf, directory, 'gdf_boundary')


def download_way_gdf(place, directory, force):
    path = f'{directory}/gdf_way.json'
    if not force and os.path.exists(path):
        return

    graph = osmnx.graph_from_place(place, network_type='drive', retain_all=True, truncate_by_edge=True)
    g_projected = osmnx.project_graph(graph)
    g_undirected = g_projected.to_undirected()

    gdf_way = osmnx.graph_to_gdfs(g_undirected, nodes=False, edges=True)
    gdf_way = gdf_way.to_crs(epsg=3857)

    osm_util.gdf_to_json(gdf_way, directory, 'gdf_way')


def download_gdf(place, directory, tag, file_name, force):
    path = f'{directory}/{file_name}.json'
    if not force and os.path.exists(path):
        return

    gdf = osmnx.geometries_from_place(place, tag)
    gdf = gdf.to_crs(epsg=3857)
    osm_util.gdf_to_json(gdf, directory, f'gdf_{file_name}')


def main(place, directory, force):
    download_boundary_gdf(place, directory, force)
    download_way_gdf(place, directory, force)
    download_gdf(place, directory,
                 {'natural': 'water', 'waterway': True},
                 'natural_water', force)
    download_gdf(place, directory,
                 {'natural': 'grassland', 'landuse': 'grass', 'leisure': 'garden'},
                 'natural_grass', force)
    download_gdf(place, directory,
                 {'leisure': 'garden'},
                 'natural_garden', force)
    download_gdf(place, directory,
                 {'leisure': 'park'},
                 'natural_park', force)
    download_gdf(place, directory,
                 {'natural': ['wood', 'wetland'], 'landuse': 'forest'},
                 'natural_wood', force)
    download_gdf(place, directory,
                 {'landuse': 'farmland'},
                 'natural_farm', force)
    # download_gdf(place, directory,
    #              {'building': True},
    #              'building', force)


if __name__ == '__main__':
    Place = 'Seoul'
    Directory = 'Seoul'
    Force = False

    main(Place, Directory, Force)

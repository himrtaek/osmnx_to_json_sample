import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from shapely.geometry import Polygon, MultiPolygon

from osm_util import CommonBufferSize


def plot_polygon(ax, poly, **kwargs):
    if poly.is_empty:
        return

    if type(poly) is MultiPolygon:
        for it in poly.geoms:
            plot_polygon(ax, it, **kwargs)
        return

    poly_temp = poly
    if not type(poly_temp) is Polygon and not type(poly_temp) is MultiPolygon:
        poly_temp = poly_temp.buffer(CommonBufferSize)

    path = Path.make_compound_path(
        Path(np.asarray(poly_temp.exterior.coords)[:, :2]),
        *[Path(np.asarray(ring.coords)[:, :2]) for ring in poly_temp.interiors])

    patch = PathPatch(path, **kwargs)
    collection = PatchCollection([patch], **kwargs)

    ax.add_collection(collection, autolim=True)
    ax.autoscale_view()

    return collection

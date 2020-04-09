from .util import make_location as _make_location
import numpy as np
from warnings import warn
import palettable
from matplotlib.colors import Colormap
from palettable.palette import Palette


def legendgram(f, ax, y, breaks, pal, bins=50, clip=None,
               loc = 'lower left', legend_size=(.27,.2),
               frameon=False, tick_params = None):
    '''
    Add a histogram in a choropleth with colors aligned with map
    ...

    Arguments
    ---------
    f           : Figure
    ax          : AxesSubplot
    y           : ndarray/Series
                  Values to map
    breaks      : list
                  [Optional. Default=ten evenly-spaced percentiles from the 1st to the 99th]
                  Sequence with breaks for each class (i.e. boundary values
                  for colors)
    pal         : palettable colormap or matplotlib colormap
    clip        : tuple
                  [Optional. Default=None] If a tuple, clips the X
                  axis of the histogram to the bounds provided.
    loc         :   string or int
                    valid legend location like that used in matplotlib.pyplot.legend
    legend_size : tuple
                  tuple of floats between 0 and 1 describing the (width,height)
                  of the legend relative to the original frame.
    frameon     : bool (default: False)
                  whether to add a frame to the legendgram
    tick_params : keyword dictionary
                  options to control how the histogram axis gets ticked/labelled.

    Returns
    -------
    axis containing the legendgram.
    '''
    if pal is None and breaks is None:
        pal = palettable.matplotlib.Viridis_10
        k = 10
    if breaks is None:
        breaks = np.percentile(y, q=np.linspace(1,99,num=10))
    k = len(breaks)
    histpos = _make_location(ax, loc, legend_size=legend_size)
    histax = f.add_axes(histpos)
    N, bins, patches = histax.hist(y, bins=bins, color='0.1')
    #---
    if isinstance(pal, Palette):
        assert k == pal.number, "provided number of classes does not match number of colors in palette."
        pl = pal.get_mpl_colormap()
    elif isinstance(pal, Colormap):
        pl = pal
    else:
        raise ValueError("pal needs to be either palettable colormap or matplotlib colormap, got {}".format(type(pal)))
    bucket_breaks = [0]+[np.searchsorted(bins, i) for i in breaks]
    for c in range(k):
        for b in range(bucket_breaks[c], bucket_breaks[c+1]):
            patches[b].set_facecolor(pl(c/k))
    #---
    if clip is not None:
        histax.set_xlim(*clip)
    histax.set_frame_on(frameon)
    histax.get_yaxis().set_visible(False)
    if tick_params is None:
        tick_params = dict()
    tick_params['labelsize'] = tick_params.get('labelsize', 12)
    histax.tick_params(**tick_params)
    return histax

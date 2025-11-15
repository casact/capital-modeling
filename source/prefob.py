# standard set up imports and display functions

from functools import partial
import re
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import display

from aggregate import Distortion, Portfolio, iman_conover, build, make_ceder_netter
from greater_tables import GT


# turn off eg greater_tables warning (appears p. 99 "desired width too small")
warnings.filterwarnings("ignore")

# original function
# def tff(x):
#     """Table float format function."""
#     if np.isnan(x):
#         return ''
#     if x == 0:
#         return '0'
#     elif x == int(x):
#         y = int(x)
#         return f'{y:,d}'
#     if 1e-3 < np.abs(x) < 1e6:
#         return f'{x:,.3f}'
#     else:
#         return f'{x:.3e}'

def tff(x, default_float='{x:,.3f}'):
    """Table float format function."""
    if np.isnan(x):
        return ''
    try:
        y = int(x)
    except:
        y = -9e99
    if x == 0:
        return '0'
    elif x == y:
        return f'{y:,d}'
    # try to pick up 0.1
    try:
        if abs(10 * x - np.round(10 * x, 0)) <= 4 * np.finfo(float).eps:
            return f'{x:.1f}'
    except ValueError:
        pass
    if np.abs(x) < 100:
        return default_float.format(x=x)
    else:
        return f'{x:.1f}'


import matplotlib.pyplot as plt
import matplotlib as mpl


def apply_ggplot2_style(base=8, font="DejaVu Sans", dpi=600):
    """Attempt to harmonize plots with John's R generated ggplot2 style."""
    plt.style.use("default")  # clear any existing style
    mpl.rcParams.update({
        "font.family": font,
        "font.size": base,

        "axes.edgecolor": "black",
        "axes.grid": True,
        "axes.labelsize": base,
        "axes.linewidth": 0.6,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.titlesize": base * 1.2,

        "figure.dpi": dpi,
        "figure.titlesize": base * 1.4,

        "grid.color": "#dddddd",
        "grid.linestyle": "-",
        "grid.linewidth": 0.5,

        "legend.edgecolor": "none",
        "legend.facecolor": "white",
        "legend.fontsize": base * 0.9,
        "legend.framealpha": 1.0,
        "legend.frameon": True,

        "lines.linewidth": 1.0,
        "lines.markersize": 5,

        "savefig.bbox": "tight",

        "xtick.bottom": True,
        "xtick.direction": "out",
        "xtick.labelsize": base * 0.9,
        "xtick.major.width": 0.6,

        "ytick.direction": "out",
        "ytick.labelsize": base * 0.9,
        "ytick.left": True,
        "ytick.major.width": 0.6,
    })


apply_ggplot2_style()


tff4 = partial(tff, default_float='{x:.4f}')

std_args = {
    'max_table_inch_width': 6.5,
    'tikz_scale': 0.8,
    'table_font_pt_size': 12,
    'font_body': 1.0
}


def GT_with_renamer(df, *argv, **kwargs):
    # deal with the total column name problem
    if "total" in df:
        df = df.rename(columns={'total': 'Total'})
    return GT(df, *argv, **kwargs)


# standard formatter
fGT = partial(GT_with_renamer, table_float_format=tff, **std_args)

# four decimals formatter
f4GT = partial(GT_with_renamer, table_float_format=tff4, **std_args)

# add ratio detection
rGT = partial(GT_with_renamer, table_float_format=tff, ratio_cols='all', **std_args)

# narrower format
nGT = partial(GT_with_renamer, table_float_format=tff,  tikz_column_sep=0.25, **std_args)

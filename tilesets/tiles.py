from __future__ import print_function

import cooler.contrib.higlass as cch
import logging
import numpy as np

logger = logging.getLogger(__name__)


def make_tile(zoomLevel, x_pos, y_pos, dset):
    info = dset[1]
    divisor = 2 ** zoomLevel

    start1 = x_pos * info['max_width'] / divisor
    end1 = (x_pos + 1) * info['max_width'] / divisor
    start2 = y_pos * info['max_width'] / divisor
    end2 = (y_pos + 1) * info['max_width'] / divisor

    data = cch.get_data(
        dset[0], zoomLevel, start1, end1 - 1, start2, end2 - 1
    )

    df = data[data['genome_start1'] >= start1]

    binsize = dset[0].attrs[str(zoomLevel)]
    j = (df['genome_start1'].values - start1) // binsize
    i = (df['genome_start2'].values - start2) // binsize

    if 'balanced' in df:
        v = np.nan_to_num(df['balanced'].values)
    else:
        v = np.nan_to_num(df['count'].values)

    out = np.zeros(65536, dtype=np.float32)  # 256^2
    index = (i * 256) + j
    out[index] = v

    return out

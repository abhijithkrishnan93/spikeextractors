from pathlib import Path
import re
from typing import Union

from scipy.spatial.distance import cdist

import numpy as np

from spikeextractors.extractors.matsortingextractor.matsortingextractor import MATSortingExtractor, HAVE_MAT
from spikeextractors.extraction_tools import check_valid_unit_id

PathType = Union[str, Path]


class WCSortingExtractor(MATSortingExtractor):
    extractor_name = "WCSortingExtractor"
    installation_mesg = "To use the MATSortingExtractor install h5py and scipy: \n\n pip install h5py scipy\n\n"  # error message when not installed

    def __init__(self, file_path: PathType, keep_good_only: bool = False):
        super().__init__(file_path)
        cluster_classes = self._getfield("cluster_class")
        classes = cluster_classes[:, 0]
        spike_times = cluster_classes[:, 1]
        par = self._getfield("par")
        sample_rate = par[0, 0][np.where(np.array(par.dtype.names) == 'sr')[0][0]][0][0]

        self.set_sampling_frequency(sample_rate)
        self._unit_ids = np.unique(classes[classes > 0])

        self._spike_trains = {}
        for uid in self._unit_ids:
            mask = (classes == uid)
            self._spike_trains[uid] = np.rint(spike_times[mask]*(sample_rate/1000))


    @check_valid_unit_id
    def get_unit_spike_train(self, unit_id, start_frame=None, end_frame=None):
        start_frame, end_frame = self._cast_start_end_frame(start_frame, end_frame)

        start_frame = start_frame or 0
        end_frame = end_frame or np.infty
        st = self._spike_trains[unit_id]
        return st[(st >= start_frame) & (st < end_frame)]

    def get_unit_ids(self):
        return self._unit_ids.tolist()
from .neobaseextractor import NeoBaseRecordingExtractor, NeoBaseSortingExtractor

try:
    import neo
    HAVE_NEO = True
except ImportError:
    HAVE_NEO = False


class mcsrawRecordingExtractor(NeoBaseRecordingExtractor):
"""
for extracting data from mcs_raw_binary which has a header file using:
recording=mcsrawRecordingExtractor(filename='Data0349/Data0349.raw')
"""

extractor_name='mcsrawRecoding'
  mode='file'
  NeoRawIOClass='RawMCSRawIO'



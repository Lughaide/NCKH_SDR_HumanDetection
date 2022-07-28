"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, vector_size=64, num_subcarrier=10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='CSI Information Extractor',   # will show up in GRC
            in_sig=[(np.complex64, vector_size)],
            out_sig=[(np.float32, vector_size), np.float32]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.num_subcarrier = num_subcarrier

    def work(self, input_items, output_items):
        tagTuple = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tagTuple:
            if (pmt.to_python(tag.key) == 'ofdm_sync_chan_taps'):
                temp = pmt.to_python(tag.value)
                magnitude = abs(temp)
                output_items[0][:] = magnitude
                output_items[1][:] = magnitude[self.num_subcarrier]

        return len(output_items[0])

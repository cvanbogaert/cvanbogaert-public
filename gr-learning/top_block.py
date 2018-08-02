#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Aug  2 14:57:25 2018
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt, QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import osmosdr
import sys
import time
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 16000000
        self.channelizer_decimation = channelizer_decimation = 50
        self.wspr_center_frequency_2 = wspr_center_frequency_2 = 10.1387e6
        self.wspr_center_frequency_1 = wspr_center_frequency_1 = 7.0386e6
        self.wspr_center_frequency_0 = wspr_center_frequency_0 = 14.0956e6
        self.rs_interpolation = rs_interpolation = 3
        self.rs_decimation = rs_decimation = 20
        self.channelizer_samp_rate = channelizer_samp_rate = samp_rate/channelizer_decimation
        self.center_frequency = center_frequency = 8000000
        self.wspr_deviation_2 = wspr_deviation_2 = wspr_center_frequency_2-center_frequency
        self.wspr_deviation_1 = wspr_deviation_1 = wspr_center_frequency_1-center_frequency
        self.wspr_deviation_0 = wspr_deviation_0 = wspr_center_frequency_0-center_frequency
        self.rs_samp_rate = rs_samp_rate = channelizer_samp_rate*rs_interpolation/rs_decimation
        self.rf_gain = rf_gain = 14
        self.if_gain = if_gain = 16
        self.bb_gain = bb_gain = 16
        self.bandpass_transition = bandpass_transition = 2500
        self.bandpass_low = bandpass_low = 200
        self.bandpass_high = bandpass_high = 2500

        ##################################################
        # Blocks
        ##################################################
        self._rf_gain_range = Range(0, 14, 14, 14, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, "rf_gain", "counter_slider", int)
        self.top_layout.addWidget(self._rf_gain_win)
        self._if_gain_range = Range(0, 40, 8, 16, 200)
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, "if_gain", "counter_slider", int)
        self.top_layout.addWidget(self._if_gain_win)
        self._bb_gain_range = Range(0, 62, 2, 16, 200)
        self._bb_gain_win = RangeWidget(self._bb_gain_range, self.set_bb_gain, "bb_gain", "counter_slider", int)
        self.top_layout.addWidget(self._bb_gain_win)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_ccc(
                interpolation=rs_interpolation,
                decimation=rs_decimation,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=rs_interpolation,
                decimation=rs_decimation,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=rs_interpolation,
                decimation=rs_decimation,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'hackrf=0' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.freq_xlating_fft_filter_ccc_0_0_0 = filter.freq_xlating_fft_filter_ccc(channelizer_decimation, (firdes.complex_band_pass(1,samp_rate,-samp_rate/channelizer_decimation/2,samp_rate/channelizer_decimation/2,samp_rate/channelizer_decimation/16)), wspr_deviation_2, samp_rate)
        self.freq_xlating_fft_filter_ccc_0_0_0.set_nthreads(2)
        self.freq_xlating_fft_filter_ccc_0_0_0.declare_sample_delay(0)
        self.freq_xlating_fft_filter_ccc_0_0 = filter.freq_xlating_fft_filter_ccc(channelizer_decimation, (firdes.complex_band_pass(1,samp_rate,-samp_rate/channelizer_decimation/2,samp_rate/channelizer_decimation/2,samp_rate/channelizer_decimation/16)), wspr_deviation_1, samp_rate)
        self.freq_xlating_fft_filter_ccc_0_0.set_nthreads(2)
        self.freq_xlating_fft_filter_ccc_0_0.declare_sample_delay(0)
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(channelizer_decimation, (firdes.complex_band_pass(1,samp_rate,-samp_rate/channelizer_decimation/2,samp_rate/channelizer_decimation/2,samp_rate/channelizer_decimation/16)), wspr_deviation_0, samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(2)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.blocks_complex_to_real_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.band_pass_filter_0_0_0 = filter.fir_filter_ccf(1, firdes.band_pass(
        	1, rs_samp_rate, bandpass_low, bandpass_high, bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_ccf(1, firdes.band_pass(
        	1, rs_samp_rate, bandpass_low, bandpass_high, bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccf(1, firdes.band_pass(
        	1, rs_samp_rate, bandpass_low, bandpass_high, bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0_0_0 = audio.sink(rs_samp_rate, 'virtual_3', False)
        self.audio_sink_0_0 = audio.sink(rs_samp_rate, 'virtual_2', False)
        self.audio_sink_0 = audio.sink(rs_samp_rate, 'virtual_1', False)
        self.analog_agc2_xx_0_0_0 = analog.agc2_cc(0.25, 0.25, (3.0/2000.0), 1.0)
        self.analog_agc2_xx_0_0_0.set_max_gain(0)
        self.analog_agc2_xx_0_0 = analog.agc2_cc(0.25, 0.25, (3.0/2000.0), 1.0)
        self.analog_agc2_xx_0_0.set_max_gain(0)
        self.analog_agc2_xx_0 = analog.agc2_cc(0.25, 0.25, (3.0/2000.0), 1.0)
        self.analog_agc2_xx_0.set_max_gain(0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.analog_agc2_xx_0_0, 0), (self.blocks_complex_to_real_0_0, 0))
        self.connect((self.analog_agc2_xx_0_0_0, 0), (self.blocks_complex_to_real_0_0_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.analog_agc2_xx_0_0, 0))
        self.connect((self.band_pass_filter_0_0_0, 0), (self.analog_agc2_xx_0_0_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.audio_sink_0_0, 0))
        self.connect((self.blocks_complex_to_real_0_0_0, 0), (self.audio_sink_0_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.band_pass_filter_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fft_filter_ccc_0_0_0.set_taps((firdes.complex_band_pass(1,self.samp_rate,-self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/16)))
        self.freq_xlating_fft_filter_ccc_0_0.set_taps((firdes.complex_band_pass(1,self.samp_rate,-self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/16)))
        self.freq_xlating_fft_filter_ccc_0.set_taps((firdes.complex_band_pass(1,self.samp_rate,-self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/16)))
        self.set_channelizer_samp_rate(self.samp_rate/self.channelizer_decimation)

    def get_channelizer_decimation(self):
        return self.channelizer_decimation

    def set_channelizer_decimation(self, channelizer_decimation):
        self.channelizer_decimation = channelizer_decimation
        self.freq_xlating_fft_filter_ccc_0_0_0.set_taps((firdes.complex_band_pass(1,self.samp_rate,-self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/16)))
        self.freq_xlating_fft_filter_ccc_0_0.set_taps((firdes.complex_band_pass(1,self.samp_rate,-self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/16)))
        self.freq_xlating_fft_filter_ccc_0.set_taps((firdes.complex_band_pass(1,self.samp_rate,-self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/2,self.samp_rate/self.channelizer_decimation/16)))
        self.set_channelizer_samp_rate(self.samp_rate/self.channelizer_decimation)

    def get_wspr_center_frequency_2(self):
        return self.wspr_center_frequency_2

    def set_wspr_center_frequency_2(self, wspr_center_frequency_2):
        self.wspr_center_frequency_2 = wspr_center_frequency_2
        self.set_wspr_deviation_2(self.wspr_center_frequency_2-self.center_frequency)

    def get_wspr_center_frequency_1(self):
        return self.wspr_center_frequency_1

    def set_wspr_center_frequency_1(self, wspr_center_frequency_1):
        self.wspr_center_frequency_1 = wspr_center_frequency_1
        self.set_wspr_deviation_1(self.wspr_center_frequency_1-self.center_frequency)

    def get_wspr_center_frequency_0(self):
        return self.wspr_center_frequency_0

    def set_wspr_center_frequency_0(self, wspr_center_frequency_0):
        self.wspr_center_frequency_0 = wspr_center_frequency_0
        self.set_wspr_deviation_0(self.wspr_center_frequency_0-self.center_frequency)

    def get_rs_interpolation(self):
        return self.rs_interpolation

    def set_rs_interpolation(self, rs_interpolation):
        self.rs_interpolation = rs_interpolation
        self.set_rs_samp_rate(self.channelizer_samp_rate*self.rs_interpolation/self.rs_decimation)

    def get_rs_decimation(self):
        return self.rs_decimation

    def set_rs_decimation(self, rs_decimation):
        self.rs_decimation = rs_decimation
        self.set_rs_samp_rate(self.channelizer_samp_rate*self.rs_interpolation/self.rs_decimation)

    def get_channelizer_samp_rate(self):
        return self.channelizer_samp_rate

    def set_channelizer_samp_rate(self, channelizer_samp_rate):
        self.channelizer_samp_rate = channelizer_samp_rate
        self.set_rs_samp_rate(self.channelizer_samp_rate*self.rs_interpolation/self.rs_decimation)

    def get_center_frequency(self):
        return self.center_frequency

    def set_center_frequency(self, center_frequency):
        self.center_frequency = center_frequency
        self.set_wspr_deviation_2(self.wspr_center_frequency_2-self.center_frequency)
        self.set_wspr_deviation_1(self.wspr_center_frequency_1-self.center_frequency)
        self.set_wspr_deviation_0(self.wspr_center_frequency_0-self.center_frequency)
        self.osmosdr_source_0.set_center_freq(self.center_frequency, 0)

    def get_wspr_deviation_2(self):
        return self.wspr_deviation_2

    def set_wspr_deviation_2(self, wspr_deviation_2):
        self.wspr_deviation_2 = wspr_deviation_2
        self.freq_xlating_fft_filter_ccc_0_0_0.set_center_freq(self.wspr_deviation_2)

    def get_wspr_deviation_1(self):
        return self.wspr_deviation_1

    def set_wspr_deviation_1(self, wspr_deviation_1):
        self.wspr_deviation_1 = wspr_deviation_1
        self.freq_xlating_fft_filter_ccc_0_0.set_center_freq(self.wspr_deviation_1)

    def get_wspr_deviation_0(self):
        return self.wspr_deviation_0

    def set_wspr_deviation_0(self, wspr_deviation_0):
        self.wspr_deviation_0 = wspr_deviation_0
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.wspr_deviation_0)

    def get_rs_samp_rate(self):
        return self.rs_samp_rate

    def set_rs_samp_rate(self, rs_samp_rate):
        self.rs_samp_rate = rs_samp_rate
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)

    def get_bandpass_transition(self):
        return self.bandpass_transition

    def set_bandpass_transition(self, bandpass_transition):
        self.bandpass_transition = bandpass_transition
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))

    def get_bandpass_low(self):
        return self.bandpass_low

    def set_bandpass_low(self, bandpass_low):
        self.bandpass_low = bandpass_low
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))

    def get_bandpass_high(self):
        return self.bandpass_high

    def set_bandpass_high(self, bandpass_high):
        self.bandpass_high = bandpass_high
        self.band_pass_filter_0_0_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.rs_samp_rate, self.bandpass_low, self.bandpass_high, self.bandpass_transition, firdes.WIN_HAMMING, 6.76))


def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()

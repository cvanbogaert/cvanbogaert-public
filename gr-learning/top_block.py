#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NBFM Receiver
# Generated: Tue Jul 31 15:30:32 2018
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

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import osmosdr
import sip
import sys
import time
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NBFM Receiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NBFM Receiver")
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
        self.tuner_center_frequency = tuner_center_frequency = 162475000
        self.squelch_level = squelch_level = 0
        self.samp_rate = samp_rate = 8000000
        self.interpolation = interpolation = 3
        self.deviation = deviation = 500000
        self.decimation_2 = decimation_2 = 5
        self.decimation = decimation = 50
        self.audio_rate = audio_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self._tuner_center_frequency_range = Range(0, 6000000000, 2500, 162475000, 200)
        self._tuner_center_frequency_win = RangeWidget(self._tuner_center_frequency_range, self.set_tuner_center_frequency, 'Frequency', "counter_slider", float)
        self.top_layout.addWidget(self._tuner_center_frequency_win)
        self._squelch_level_range = Range(-100000, 100000, 1, 0, 200)
        self._squelch_level_win = RangeWidget(self._squelch_level_range, self.set_squelch_level, 'Squelch', "counter_slider", float)
        self.top_layout.addWidget(self._squelch_level_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=interpolation,
                decimation=decimation_2,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_1_0_0 = qtgui.waterfall_sink_f(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	audio_rate, #bw
        	"Audio", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_1_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_1_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_1_0_0.disable_legend()

        if "float" == "float" or "float" == "msg_float":
          self.qtgui_waterfall_sink_x_1_0_0.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_1_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_1_0_0_win)
        self.qtgui_waterfall_sink_x_1_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate*interpolation/decimation/decimation_2, #bw
        	"Post Resampler", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_1_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_1_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_1_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_1_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_1_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_1_0_win)
        self.qtgui_waterfall_sink_x_1 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate/decimation, #bw
        	"Post Filter", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_1.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_1.enable_grid(False)
        self.qtgui_waterfall_sink_x_1.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_1.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_1.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_1.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_1.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_1.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_1_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_1_win)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	tuner_center_frequency-deviation, #fc
        	samp_rate, #bw
        	"Input Waterfall", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'hackrf=0' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(tuner_center_frequency-deviation, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(decimation, (firdes.complex_band_pass(1,samp_rate,-samp_rate/decimation/2,samp_rate/decimation/2,samp_rate/decimation/16)), deviation, samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(2)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.audio_sink_0 = audio.sink(audio_rate, '', True)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=samp_rate*3/decimation/decimation_2,
        	tau=75e-6,
        	max_dev=5e3,
          )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.qtgui_waterfall_sink_x_1_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.qtgui_waterfall_sink_x_1, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.qtgui_waterfall_sink_x_1_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tuner_center_frequency(self):
        return self.tuner_center_frequency

    def set_tuner_center_frequency(self, tuner_center_frequency):
        self.tuner_center_frequency = tuner_center_frequency
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.tuner_center_frequency-self.deviation, self.samp_rate)
        self.osmosdr_source_0.set_center_freq(self.tuner_center_frequency-self.deviation, 0)

    def get_squelch_level(self):
        return self.squelch_level

    def set_squelch_level(self, squelch_level):
        self.squelch_level = squelch_level

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_waterfall_sink_x_1_0.set_frequency_range(0, self.samp_rate*self.interpolation/self.decimation/self.decimation_2)
        self.qtgui_waterfall_sink_x_1.set_frequency_range(0, self.samp_rate/self.decimation)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.tuner_center_frequency-self.deviation, self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_taps((firdes.complex_band_pass(1,self.samp_rate,-self.samp_rate/self.decimation/2,self.samp_rate/self.decimation/2,self.samp_rate/self.decimation/16)))

    def get_interpolation(self):
        return self.interpolation

    def set_interpolation(self, interpolation):
        self.interpolation = interpolation
        self.qtgui_waterfall_sink_x_1_0.set_frequency_range(0, self.samp_rate*self.interpolation/self.decimation/self.decimation_2)

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.tuner_center_frequency-self.deviation, self.samp_rate)
        self.osmosdr_source_0.set_center_freq(self.tuner_center_frequency-self.deviation, 0)
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.deviation)

    def get_decimation_2(self):
        return self.decimation_2

    def set_decimation_2(self, decimation_2):
        self.decimation_2 = decimation_2
        self.qtgui_waterfall_sink_x_1_0.set_frequency_range(0, self.samp_rate*self.interpolation/self.decimation/self.decimation_2)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.qtgui_waterfall_sink_x_1_0.set_frequency_range(0, self.samp_rate*self.interpolation/self.decimation/self.decimation_2)
        self.qtgui_waterfall_sink_x_1.set_frequency_range(0, self.samp_rate/self.decimation)
        self.freq_xlating_fft_filter_ccc_0.set_taps((firdes.complex_band_pass(1,self.samp_rate,-self.samp_rate/self.decimation/2,self.samp_rate/self.decimation/2,self.samp_rate/self.decimation/16)))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.qtgui_waterfall_sink_x_1_0_0.set_frequency_range(0, self.audio_rate)


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

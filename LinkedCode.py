import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.MixerComponent import MixerComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.InputControlElement import *
from _Framework.EncoderElement import EncoderElement
from _Framework.SliderElement import SliderElement

CHAN = 0
MIXER_TRACKS = 8
MIXER_SELECT_NOTES = (38, 39, 40, 41, 42. 43, 44, 45)
MIXER_VOLUME_CCS = (4, 8, 12, 16, 20, 24, 28, 32)
MIXER_PAN_CCS = (3, 7, 11, 15, 19, 23, 27, 31)
MIXER_SEND_A_CCS = (2, 6, 10, 14, 18, 22, 26, 30)
MIXER_SEND_B_CCS = (1, 5, 9, 13, 17, 21, 25, 29)
SESSION_TRACKS = 8
SESSION_SCENES = 1

# Factory Reset
FactoryReset = (0xf0, 0x00, 0x01, 0x61, 0x04, 0x06, 0xf7)
# Button Channel Map - 45 buttons, map all to channel 0
ButtonChannelMap = (0xf0, 0x00, 0x01, 0x61, 0x04, 0x13, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, 0xf7)
# Encoder Channel Map - 32 encoders, map all to channel 0
EncChannels = (0xf7, 0x00, 0x01, 0x61, 0x04, 0x14, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, CHAN, 0xf7)

class LinkedCode(ControlSurface):
	def __init__(self, c_instance):
		ControlSurface.__init__(self, c_instance)
		self._reset()
		# turn off rebuild MIDI map until after setup
		self.set_suppress_rebuild_requests(True)
		self._setup_mixer_control()
		self._setup_transport_control()
		self._setup_session_control()
		self.set_suppress_rebuild_requests(False)
		self.log_message("LinkedCode init done")

	def _reset():
		self._send_midi(FactoryReset)
		self._send_midi(ButtonChannelMap)
		self._send_midi(EncoderChannelMap)

	def _setup_mixer_control():
		# FIXME why is mixer a global?
		global mixer
		# MixerComponent(num_tracks, num_returns, ...)
		mixer = MixerComponent(MIXER_TRACKS, 0, with_eqs = True, with_filters = False)
		mixer.set_track_offset(0)
		for i in range(MIXER_TRACKS):
			mixer.channel_strip(i).set_select_button(ButtonElement(True, MIDI_NOTE_TYPE, CHAN, MIXER_SELECT_NOTES[i]))
			mixer.channel_strip(i).set_volume_control(SliderElement(MIDI_CC_TYPE, CHAN, MIXER_VOLUME_CCS[i]))
			mixer.channel_strip(i).set_pan_control(EncoderElement(MIDI_CC_TYPE, CHAN, MIXER_PAN_CCS[i], Live.MidiMap.MapMode.absolute))
			mixer.channel_strip(i).set_send_controls((EncoderElement(MIDI_CC_TYPE, CHAN, MIXER_SEND_A_CCS, Live.MidiMap.MapMode.absolute), EncoderElement(MIDI_CC_TYPE, CHAN, MIXER_SEND_B_CCS, Live.MidiMap.MapMode.absolute)))

	def _setup_transport_control():

	def _setup_session_control():
		global session
		session = SessionComponent(SESSION_TRACKS, SESSION_SCENES)
		session.name = "Session_Control"
		session.set_mixer(mixer)

#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT
from asyncio.tasks import sleep

class LedDisplayEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(LedDisplayEmulatorTask, self).__init__(
			name = ConfigConst.LED_ACTUATOR_NAME,
			typeID = ConfigConst.LED_DISPLAY_ACTUATOR_TYPE,
			simpleName = "LedDisplay")
		
		useEmulator = ConfigUtil().getBoolean(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SENSE_HAT_KEY)
		self.sh = SenseHAT(emulate = useEmulator)

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		if self.sh.screen:
			msg = self.getSimpleName() + " ON: " + str(stateData) + "C"
			self.sh.screen.scroll_text(msg)
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to write.")
			return -1
		
	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		if self.sh.screen:
			msg = self.getSimpleName() + " OFF"
			self.sh.screen.scroll_text(msg)
			
			sleep(5)
			
			self.sh.screen.clear()
			return 0
		else:
			logging.warning("No SenseHAT LED screen instance to write.")
			return -1
	
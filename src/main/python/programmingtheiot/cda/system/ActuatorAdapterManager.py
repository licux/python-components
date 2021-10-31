#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask

class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self):
		configUtil = ConfigUtil()
		self.useEmulator = configUtil.getBoolean(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_EMULATOR_KEY)
		self.locationID = configUtil.getProperty(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		self.dataMsgListener = None
		
		self.humidifierActuator = None
		self.hvacActuator = None
		
		if self.useEmulator:
			logging.info("Use Emulator...")
		elif not self.useEmulator:
			logging.info("Use Simulator...")
			self.humidifierActuator = HumidifierActuatorSimTask()
			self.hvacActuator = HvacActuatorSimTask()
		

	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		if data and not data.isResponseFlagEnabled():
			if data.getLocationID() is self.locationID:
				logging.info("Processing actuator command for loc ID %s.", str(data.getLocationID()))
				
				aType = data.getTypeID()
				responseData = None
				if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE:
					responseData = self.humidifierActuator.updateActuator(data)
				elif aType == ConfigConst.HVAC_ACTUATOR_TYPE:
					responseData = self.hvacActuator.updateActuator(data)
				elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE:
					responseData = self.ledDisplayEmulator.updateActuator(data)
				else:
					logging.warning("No valid actuator type: %s", data.getTypeID())

				if responseData:
					if self.dataMsgListener:
						self.dataMsgListener.handleActuatorCommandResponse(responseData)
					return True
			else:
				logging.warning("Invalid loc ID match: %s", str(self.locationID))
		else:
			logging.warning("Invalid actuator msg. Response or null. Ignoring.")
			
		return False
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener:
			self.dataMsgListener = listener

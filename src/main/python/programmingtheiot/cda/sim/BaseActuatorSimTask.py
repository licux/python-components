#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, name = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
		self.name = name
		self.typeID = typeID
		self.simpleName = simpleName
		
		self.lastKnownCommand = ConfigConst.DEFAULT_COMMAND
		self.lastKnownValue = ConfigConst.DEFAULT_VAL
		
	def getLatestActuatorResponse(self) -> ActuatorData:
		"""
		This can return the current ActuatorData response instance or a copy.
		"""
		pass
	
	def getSimpleName(self) -> str:
		return self.simpleName
	
	def updateActuator(self, data: ActuatorData) -> bool:
		"""
		NOTE: If 'data' is valid, the actuator-specific work can be delegated
		as follows:
		 - if command is ON: call self._activateActuator()
		 - if command is OFF: call self._deactivateActuator()
		
		Both of these methods will have a generic implementation (logging only) within
		this base class, although the sub-class may override if preferable.
		"""
		if data and self.typeID == data.getTypeID():
			statusCode = ConfigConst.DEFAULT_STATUS
			
			currentCommand = data.getCommand()
			currentVal = data.getValue()
			if currentCommand is self.lastKnownCommand and currentVal == self.lastKnownValue:
				logging.debug("New actuator command is repeat of current state. Ignoring: %s", str(currentCommand) + ", " + str(currentVal))
			else:
				if currentCommand == ConfigConst.COMMAND_ON:
					logging.info("Activating actuator...")
					statusCode = self._activateActuator(val = currentVal, stateData = data.getStateData())
				elif currentCommand == ConfigConst.COMMAND_OFF:
					logging.info("Deactivating actuator...")
					statusCode = self._deactivateActuator(val = currentVal, stateData = data.getStateData())
				else:
					logging.warning("ActuatorData command is unkonwn. Ignorign: %s", str(currentCommand))
					statusCode = -1
			
			self.lastKnownCommand = currentCommand
			self.lastKnonwValue = currentVal
			
			actuatorResponse = ActuatorData()
			actuatorResponse.updateData(data)
			actuatorResponse.setStateData(statusCode)
			actuatorResponse.setAsResponse()	
			
			return actuatorResponse
		return None
		
	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Implement basic logging. Actuator-specific functionality should be implemented by sub-class.
		
		@param val The actuation activation value to process.
		@param stateData The string state data to use in processing the command.
		"""
		msg = "\n*******"
		msg = msg + "\n* O N *"
		msg = msg + "\n*******"
		msg = msg + "\n" + self.simpleName + " VALUE -> " + str(val) + "\n======="
		logging.info("Simulating %s actuator ON: %s", self.name, msg)
		
		return 0
		
	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		"""
		Implement basic logging. Actuator-specific functionality should be implemented by sub-class.
		
		@param val The actuation activation value to process.
		@param stateData The string state data to use in processing the command.
		"""
		msg = "\n*******"
		msg = msg + "\n* OFF *"
		msg = msg + "\n*******"
		msg = msg + "\n" + self.simpleName + " VALUE -> " + str(val) + "\n======="
		logging.info("Simulating %s actuator OFF: %s", self.name, msg)
		
		return 0
		
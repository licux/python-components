#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData
from pickle import NONE
from lib2to3.fixer_util import Comma

class ActuatorData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
		super(ActuatorData, self).__init__(name = name, typeID = typeID, d = d)
		
		self.command = ConfigConst.DEFAULT_COMMAND
		self.value = ConfigConst.DEFAULT_VAL
		self.stateData = NONE

	
	def getCommand(self) -> int:
		return self.command
	
	def getStateData(self) -> str:
		return self.stateData
	
	def getValue(self) -> float:
		return self.value
	
	def isResponseFlagEnabled(self) -> bool:
		return False
	
	def setCommand(self, command: int):
		self.command = command
	
	def setAsResponse(self):
		pass
		
	def setStateData(self, stateData: str):
		self.stateData = stateData
	
	def setValue(self, val: float):
		self.value = val
		self.updateTimeStamp()
		
	def _handleUpdateData(self, data):
		if data and isinstance(data, ActuatorData):
			self.value = data.getValue()
			self.command = data.getCommand()
			self.stateData = data.getStateData()
	
	def __str__(self):
		return BaseIotData.__str__(self) + ",value=" + str(self.value)
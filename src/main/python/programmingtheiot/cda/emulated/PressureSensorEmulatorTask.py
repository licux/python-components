#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

from pisense import SenseHAT
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

class PressureSensorEmulatorTask(BaseSensorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, dataSet = None):
		super(PressureSensorEmulatorTask, self).__init__(
			name = ConfigConst.PRESSURE_SENSOR_NAME,
			typeID = ConfigConst.PRESSURE_SENSOR_TYPE,
			minVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
			maxVal = SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
		
		useEmulator = ConfigUtil().getBoolean(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_SENSE_HAT_KEY)
		self.sh = SenseHAT(emulate = useEmulator)
	
	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(name = self.getName(), typeID = self.getTypeID())
		sensorVal = self.sh.environ.pressure
		
		sensorData.setValue(sensorVal)
		self.latestSensorData = sensorData
		return sensorData

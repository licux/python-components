#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import logging
import json
# from json import JSONEncoder
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, encodeToUtf8 = False):
		pass
	
	def actuatorDataToJson(self, actuatorData, flag = False):
		if not actuatorData:
			logging.warning("ActuatorData is null. Ignoring conversion to JSON.")
			return None
		
		logging.debug("Encoding ActuatorData to JSON [pre] -->" + str(actuatorData))
		jsonData = self._generateJsonData(actuatorData)
		logging.debug("Encoding ActuatorData to JSON [post] -->" + str(jsonData))
		
		return jsonData
	
	def sensorDataToJson(self, sensorData):
		if not sensorData:
			logging.warning("SensorData is null. Ignoring conversion to JSON.")
			return None
		
		logging.debug("Encoding SensorData to JSON [pre] -->" + str(sensorData))
		jsonData = self._generateJsonData(sensorData)
		logging.debug("Encoding SensorData to JSON [post] -->" + str(jsonData))
		
		return jsonData

	def systemPerformanceDataToJson(self, sysPerfData):
		if not sysPerfData:
			logging.warning("SystemPerformanceData is null. Ignoring conversion to JSON.")
			return None
		
		logging.debug("Encoding SystemPerformanceData to JSON [pre] -->" + str(sysPerfData))
		jsonData = self._generateJsonData(sysPerfData)
		logging.debug("Encoding SystemPerformanceData to JSON [post] -->" + str(jsonData))
		
		return jsonData
	
	def jsonToActuatorData(self, jsonData):
		if not jsonData:
			logging.warning("JSON data is empty or null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDirectory(jsonData)
		ad = ActuatorData()
		self._updateIotData(jsonStruct, ad)
		
		return ad
	
	def jsonToSensorData(self, jsonData):
		if not jsonData:
			logging.warning("JSON data is empty or null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDirectory(jsonData)
		sd = SensorData()
		self._updateIotData(jsonStruct, sd)
		
		return sd
	
	def jsonToSystemPerformanceData(self, jsonData):
		if not jsonData:
			logging.warning("JSON data is empty or null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDirectory(jsonData)
		sd = SystemPerformanceData()
		self._updateIotData(jsonStruct, sd)
		
		return sd
	
	def _generateJsonData(self, obj) -> str:
		return json.dumps(obj, indent = 4, cls = JsonDataEncoder)
	
	def _formatDataAndLoadDirectory(self, jsonData: str) -> dict:
		jsonData = jsonData.replace("\'", "\"",).replace("False", "false").replace("True", "true")
		
		jsonStruct = json.loads(jsonData)
		return jsonStruct
	
	def _updateIotData(self, jsonStruct, obj):
		varStruct = vars(obj)
		for key in jsonStruct:
			if key in varStruct:
				setattr(obj, key, jsonStruct[key])
			else:
				logging.warn("JSON data key not mappable to object: %s", key)
	
class JsonDataEncoder(json.JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""
	def default(self, o):
		if isinstance(o, bytes):
			return o.decode('utf-8')
		return o.__dict__
	
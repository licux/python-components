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

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask
from pickle import NONE

class SensorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		configUtil = ConfigUtil()
		
		self.pollRate = configUtil.getInteger(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.POLL_CYCLES_KEY, defaultVal = ConfigConst.DEFAULT_POLL_CYCLES)
		self.useEmulator = configUtil.getBoolean(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.ENABLE_EMULATOR_KEY)
		self.locationID = configUtil.getProperty(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.DEVICE_LOCATION_ID_KEY, defaultVal = ConfigConst.NOT_SET)
		
		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
		
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
		
		self.dataMsgListener = None
		
		self.dataGenarator = SensorDataGenerator()
		self.tempAdapter = None
		self.pressureAdapter = None
		self.humidityAdapter = None

		if self.useEmulator:
			logging.info("Use Emulator...")
			tempModule = import_module('programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask', 'TemperatureSensorEmulatorTask')
			teClazz = getattr(tempModule, 'TemperatureSensorEmulatorTask')
			self.tempAdapter = teClazz()
			pressureModule = import_module('programmingtheiot.cda.emulated.PressureSensorEmulatorTask', 'PressureSensorEmulatorTask')
			prClazz = getattr(pressureModule, 'PressureSensorEmulatorTask')
			self.pressureAdapter = prClazz()
			humudityModule = import_module('programmingtheiot.cda.emulated.HumiditySensorEmulatorTask', 'HumiditySensorEmulatorTask')
			huClazz = getattr(humudityModule, 'HumiditySensorEmulatorTask')
			self.humidityAdapter = huClazz()
		elif not self.useEmulator:
			logging.info("Use Simulator...")
			
			tempFloor = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
			tempCeiling = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.TEMP_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
			tempData = self.dataGenarator.generateDailyIndoorTemperatureDataSet(minValue= tempFloor, maxValue = tempCeiling, useSeconds= False)
			
			pressureFloor = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
			pressureCeiling = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.PRESSURE_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
			pressureData = self.dataGenarator.generateDailyEnvironmentPressureDataSet(minValue= pressureFloor, maxValue = pressureCeiling, useSeconds= False)
			
			humidityFloor = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_FLOOR_KEY, defaultVal = SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
			humidityCeiling = configUtil.getFloat(section = ConfigConst.CONSTRAINED_DEVICE, key = ConfigConst.HUMIDITY_SIM_CEILING_KEY, defaultVal = SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
			humidityData = self.dataGenarator.generateDailyEnvironmentHumidityDataSet(minValue= humidityFloor, maxValue = humidityCeiling, useSeconds= False)
			
			self.tempAdapter = TemperatureSensorSimTask(tempData)
			self.pressureAdapter = PressureSensorSimTask(pressureData)
			self.humidityAdapter = HumiditySensorSimTask(humidityData)

	def handleTelemetry(self):
		humidityData = self.humidityAdapter.generateTelemetry()
		pressureData = self.pressureAdapter.generateTelemetry()
		tempData = self.tempAdapter.generateTelemetry()
		
		humidityData.setLocationID(self.locationID)
		pressureData.setLocationID(self.locationID)
		tempData.setLocationID(self.locationID)
		
		logging.info("Generated humidity data: " + str(humidityData))
		logging.info("Generated pressure data: " + str(pressureData))
		logging.info("Generated temperature data: " + str(tempData))
		
		if self.dataMsgListener:
			self.dataMsgListener.handleSensorMessage(humidityData)
			self.dataMsgListener.handleSensorMessage(pressureData)
			self.dataMsgListener.handleSensorMessage(tempData)
		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener:
			self.dataMsgListener = listener
	
	def startManager(self):
		logging.info("Started SensorAdapterManager.")
		
		if not self.scheduler.running:
			self.scheduler.start()
		else:
			logging.warning("SensorAdapterManager shecduler already started.")
		
	def stopManager(self):
		logging.info("Stopped SensorAdapterManager.")
		
		try:
			self.scheduler.shutdown()
		except:
			logging.warning("SensorAdapterManager scheduler already stopped.")
#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import socket
import traceback

# use aiocoap as CoAP library
import asyncio
from aiocoap import *

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil

from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient
from test.support import resource


class CoapClientConnector(IRequestResponseClient):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		self.config = ConfigUtil()
		self.dataMsgListener = dataMsgListener
		self.enableConfirmedMsgs = False
		self.coapClient = None
		
		self.observeRequests = {}
		
		self.host = self.config.getProperty(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
		self.port = self.config.getInteger(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_COAP_PORT)
		
		self.uriPath = "coap://" + self.host + ":" + str(self.port) + "/"
		logging.info("\tHost:Port: %s:%s", self.host, str(self.port))
		
		try:
			tmpHost = socket.gethostbyname(self.host)
			if tmpHost:
				self.host = tmpHost
				self._initClient()
			else:
				logging.error("Can't resolve host: " + self.host)
		except socket.gaierror:
			logging.info("Failed to resolve host: " + self.host)
		
	
	def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		logging.info("Called sendDiscoverRequest().")
		

	def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		if resource or name:
			resourcePath = self._createResourcePath(resource, name)
			logging.debug("Issuing DELETE to path: " + resourcePath)
			
			asyncio.get_event_loop().run_until_complete(self._handleDeleteRequest(resourcePath = resourcePath, enableCON = enableCON))
		else:
			logging.warning("Can't issue DELETE - no path or path list provided.")

	def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
  # logging.info("Called sendGetRequest().")
		if resource or name:
			resourcePath = self._createResourcePath(resource, name)
			logging.debug("Issuing GET to path: " + resourcePath)
			
			asyncio.get_event_loop().run_until_complete(self._handleGetRequest(resourcePath = resourcePath, enableCON = enableCON))
		else:
			logging.warning("Can't issue GET - no path or path list provided.")

	def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		if resource or name:
			resourcePath = self._createResourcePath(resource, name)
			logging.debug("Issuing POST to path: " + resourcePath)
			
			asyncio.get_event_loop().run_until_complete(self._handlePostRequest(resourcePath = resourcePath, payload = payload, enableCON = enableCON))
		else:
			logging.warning("Can't issue POST - not path or path list provided.")

	def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		if resource or name:
			resourcePath = self._createResourcePath(resource, name)
			logging.debug("Issuing PUT to path: " + resourcePath)
			
			asyncio.get_event_loop().run_until_complete(self._handlePutRequest(resourcePath = resourcePath, payload = payload, enableCON = enableCON))
		else:
			logging.warning("Can't issue PUT - not path or path list provided.")

	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		if listener:
			self.dataMsgListener = listener

	def startObserver(self, resource: ResourceNameEnum = None, name: str = None, ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
		logging.info("Called startObserver().")
		if resource or name:
			resourcePath = self._createResourcePath(resource, name)
			
			asyncio.get_event_loop().run_until_complete(asyncio.ensure_future(self._handleStartObserveRequest(resourcePath)))
		else:
			logging.warning("Can't issue OBSERVE - GET - no path or provided.")
								

	def stopObserver(self, resource: ResourceNameEnum = None, name: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		logging.info("Called stopObserver().")
		if resource or name:
			resourcePath = self._createResourcePath(resource, name)
			
			asyncio.get_event_loop().run_until_complete(self._handleStopObserveRequest(resourcePath))
		else:
			logging.warning("Can't cancel OBSERVE - GET - no path provided.")
	
	def _createResourcePath(self, resource: ResourceNameEnum = None, name: str = None):
		resourcePath = ""
		hasResource = False
		if resource:
			resourcePath = resourcePath + resource.value
			hasResource = True
		
		if name:
			if hasResource:
				resourcePath = resourcePath + "/"
			resourcePath = resourcePath + name
		
		return self.uriPath + resourcePath
			
	def _initClient(self):
		asyncio.get_event_loop().run_until_complete(self._initClientContext())
		
	async def _initClientContext(self):
		try:
			logging.info("Creating CoAP client for URI path: " + self.uriPath)
			self.coapClient = await Context.create_client_context()
			
			logging.info("Client context created. Will invoke resources at: " + self.uriPath)
		except Exception as e:
			# Obviously, this is  a craitaical failure
			logging.error("Failed ato create CoAP client to URI path: " + self.uriPath)
			traceback.print_exception(type(e), e, e.__traceback__)
	
	async def _handleStartObserveRequest(self, resourcePath: str = None, ignoreErr: bool = False):
		msg = Message(code = GET, uri = resourcePath, observe = 0)
		req = self.coapClient.request(msg)
		
		# TODO: track which resources are under observation
		self.observeRequests[resourcePath] = req
		
		try:
			# end the initial request
			responseData = await req.response
			# TODO: validate response first
			self._onGetResponse(responseData)
			
			# wait for each observed update
			async for responseData in req.observation:
				# TODO: validate response first
				self._onGetResponse(responseData)
				
				req.observation.cancel()
				break;
		except Exception as e:
			# TODO: for debugging, you may want to optionally include the stack trace
			logging.warning("Failed to execute OBSERVE - GET. Recovering...")
			traceback.print_exception(type(e), e, e.__traceback__)		

	async def _handleStopObserveRequest(self, resourcePath: str = None, ignoreErr: bool = False):
		if resourcePath in self.observeRequests:
			logging.info("Handle stop observe invoked: " + resourcePath)
			try:
				observeRequest = self.observeRequests[resourcePath]
				observeRequest.observation.cance()
			except Exception as e:
				if not ignoreErr:
					logging.warning("Failed to cancel OBSERVE - GET: " + resourcePath)
			
			try:
				del self.observeRequests[resourcePath]
			except Exception as e:
				if not ignoreErr:
					logging.warning("Failed to remove observable from list: " + resourcePath)
		else:
			logging.warning("Resource not currently under observation. Ignoring: " + resourcePath)
	
	def _onGetResponse(self, data):
		logging.info(data)

	async def _handleGetRequest(self, resourcePath: str = None, enableCON: bool = False):
		try:
			msgType = NON
			if enableCON:
				msgType = CON
			
			msg = Message(mtype = msgType, code = GET, uri = resourcePath)
			
			req = self.coapClient.request(msg)
			responseData = await req.response
			
			# TODO; process the response data
		
		except Exception as e:
			# TODO: for debugging, you may want to optionally include the stack trace
			logging.warning("Failed to praocess GET request for path: " + resourcePath)
			traceback.print_exception(type(e), e, e.__traceback__)
	
	async def _handleDeleteRequest(self, resourcePath: str = None, enableCON: bool = False):
		try:
			msgType = NON
			if enableCON:
				msgType = CON
			
			msg = Message(mtype = msgType, code = DELETE, uri = resourcePath)
			
			req = self.coapClient.request(msg)
			responseData = await req.response
			
			# TODO; process the response data
		
		except Exception as e:
			# TODO: for debugging, you may want to optionally include the stack trace
			logging.warning("Failed to praocess DELETE request for path: " + resourcePath)
			traceback.print_exception(type(e), e, e.__traceback__)

	async def _handlePostRequest(self, resourcePath: str = None, payload: str = None, enableCON: bool = False):
		try:
			msgType = NON
			if enableCON:
				msgType = CON
				
			payloadBytes = b''
			
			#decide which encoding to use - this can also be loaded from the configuration file but must also align to the server
			if payload:
				payloadBytes = payload.encode('utf-8')
			
			msg = Message(mtype = msgType, payload = payloadBytes, code = POST, uri = resourcePath)
			
			req = self.coapClient.request(msg)
			responseData = await req.response
			
			# TODO: process the response data
			
		except Exception as e:
			# TODO: for debugging, you may want to optionally include the stack trace
			logging.warning("Failed to praocess POST request for path: " + resourcePath)
			traceback.print_exception(type(e), e, e.__traceback__)
		
	async def _handlePutRequest(self, resourcePath: str = None, payload: str = None, enableCON: bool = False):
		try:
			msgType = NON
			if enableCON:
				msgType = CON
				
			payloadBytes = b''
			
			#decide which encoding to use - this can also be loaded from the configuration file but must also align to the server
			if payload:
				payloadBytes = payload.encode('utf-8')
			
			msg = Message(mtype = msgType, payload = payloadBytes, code = PUT, uri = resourcePath)
			
			req = self.coapClient.request(msg)
			responseData = await req.response
			
			# TODO: process the response data
			
		except Exception as e:
			# TODO: for debugging, you may want to optionally include the stack trace
			logging.warning("Failed to praocess PUT request for path: " + resourcePath)
			traceback.print_exception(type(e), e, e.__traceback__)
		
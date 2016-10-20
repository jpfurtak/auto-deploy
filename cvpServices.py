# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
'''
@Copyright: 2015 Arista Networks, Inc.
Arista Networks, Inc. Confidential and Proprietary.

CvpServices script is used for making request to the Cvp web-serves.
These requests comprise of  addition, modification, deletion and retrieval of
Cvp instance.

It contains 2 classes
   CvpError -- Handles exceptions
   CvpService -- Handles requests
'''
import requests
import json
import urllib
import errorCodes

DEFAULT_USER = "cvpadmin"
DEFAULT_PASSWORD = "cvpadmin"

class CvpError( Exception ):
   '''CvpError is a class for containing the exception information and passing that
   exception information upwards to the application layer

   Public methods:
      __str__()

   Instance variables:
      message -- information corresponding to the error code in response
      value -- error code value provided in response to HTTP/HTTPs requests
      errorCode -- Arista version of error code corresponding above value
   '''

   message = {}
   message[ 0 ] = errorCodes.NO_ERROR_CODE
   message[ 1 ] = errorCodes.UNKNOWN_ERROR_CODE
   message[ 2 ] = errorCodes.UNKNOWN_REQUEST_RESPONSE
   message[ 2002 ] = errorCodes.INVALID_IMAGE_BUNDLE_NAME
   message[ 3002 ] = errorCodes.INVALID_CONTAINER_NAME
   message[ 4001 ] = errorCodes.DEVICE_ALREADY_EXISTS
   message[ 4002 ] = errorCodes.DEVICE_LOGIN_UNAUTHORISED
   message[ 4003 ] = errorCodes.DEVICE_INVALID_LOGIN_CREDENTIALS
   message[ 4005 ] = errorCodes.DEVICE_CONNECTION_ATTEMPT_FAILURE
   message[ 5001 ] = errorCodes.INVALID_IMAGE_NAME
   message[ 112498 ] = errorCodes.INVALID_LOGIN_CREDENTIALS
   message[ 121500 ] = errorCodes.IMAGE_BUNDLE_CVP_RUNTIME_EXCEPTION
   message[ 122401 ] = errorCodes.USER_UNAUTHORISED
   message[ 122502 ] = errorCodes.IMAGE_BUNDLE_DATABASE_CONNECTION_FAILURE
   message[ 122504 ] = errorCodes.DATABASE_ACCESS_FAILURE
   message[ 122514 ] = errorCodes.CONTAINER_ALREADY_EXIST
   message[ 122515 ] = errorCodes.ENTITY_ALREADY_EXISTS
   message[ 122518 ] = errorCodes.IMAGE_BUNDLE_ALREADY_EXIST
   message[ 122519 ] = errorCodes.CANNOT_DELETE_IMAGE_BUNDLE
   message[ 122701 ] = errorCodes.JSON_STRING_AS_BEAN_CLASS
   message[ 131500 ] = errorCodes.CONFIG_CVP_RUNTIME_EXCEPTION
   message[ 132502 ] = errorCodes.CONFIG_DATABASE_ACCESS_FAILURE
   message[ 132506 ] = errorCodes.CONFIG_UPDATE_FAILURE
   message[ 132518 ] = errorCodes.CONFIGLET_ALREADY_EXIST
   message[ 132801 ] = errorCodes.INVALID_CONFIGLET_NAME
   message[ 142500 ] = errorCodes.INVALID_TASK_ID

   def __init__( self, errCode ):
      '''Constructor for the CvpError class'''

      super( CvpError, self ).__init__()
      self.value = int( errCode )
      if self.value not in CvpError.message:
         self.value = 1
      self.errorCode = CvpError.message[ self.value ]

   def __str__( self ):
      '''returns string value of the object'''
      return str( self.errorCode )

class CvpService( object ):
   '''CvpService class is responsible for hitting endpoints of the Cvp web-server
   for retrieving, updating, adding and deleting state of Cvp

   Public methods:
      authenticate(  username, password )
      getConfigletsInfo()
      imageBundleAppliedContainers(imageBundleName )
      searchContainer( containerName )
      imageBundleAppliedDevices( imageBundleName )
      addImage( imageName )
      downloadImage( imageName, imageId, filePath )
      firstLoginDefaultPasswordReset( newPassword, emaildId )
      getInventory()
      configAppliedContainers( configletName )
      configAppliedDevices ( configletName )
      retrieveInventory()
      getImagesInfo()
      addConfiglet( configletName, configletContent )
      getConfigletByName( configletName )
      updateConfiglet( configletName, configletContent, configletKey )
      deleteConfiglet( configletName, configletKey )
      saveImageBundle( imageBundleName, imageBundleCertified, imageInfoList )
      getImageBundleByName( imageBundleName )
      updateImageBundle( imageBundleName, imageBundleCertified, imageInfoList,
          imageBundleKey )
      addToInventory( deviceIpAddress, parentContainerName, parentContainerId )
      saveInventory()
      retryAddToInventory( deviceKey, deviceIpAddress, username, password )
      executeTask( taskId )
      getTasks()
      getImageBundles()
      deleteImageBundle( imageBundleKey, imageBundleName )
      deleteDuplicateDevice( tempDeviceId )
      deleteContainer(  containerName, containerKey, parentContainerName,
         parentKey )
      deleteDevice( deviceKey, parentContainerName, containerKey )
      applyConfigToDevice( deviceIpAddress, deviceFqdn, deviceKey,
         configNameList, configKeyList )
      applyConfigToContainer( containerName, containerKey, configNameList,
         configKeyList )
      removeConfigFromContainer( containerName, containerKey, configNameList,
         configKeyList )
      addContainer( containerName, containerParentName, parentContainerId )
      applyImageBundleToDevice( deviceKey, deviceFqdn, imageBundleName,
         imageBundleKey )
      applyImageBundleToContainer( containerName, containerKey,imageBundleName,
         imageBundleKey )
      deviceComplianceCheck( deviceConfigIdList, deviceMacAddress )
      changeContainerName( oldName, newName, containerKey )

   Instance variables:
      self.port -- Port where Http/Https request made to web server
      self.url -- denotes the host sub-part of the URL
      self.headers -- headers required for the Http/Https requests
      self.hostname -- name of the host
      self.cookies -- cookies of the session establised
   '''
   def __init__( self, hostname, ssl=False, port=80 ):
      '''Constructer for the CvpService class

      Arguments:
         hostname -- name of the host ( type : String )
         SSL -- secured socket layer ( type : boolean )
         port -- port number (type : int )
      '''
      self.hostname = hostname
      self.port = port
      self.cookies = None
      if ssl == True:
         self.url = 'https://%s:%d' % ( self.hostname, self.port )
      else:
         self.url = 'http://%s:%d' % ( self.hostname, self.port )
      self.headers = { 'Accept' : 'application/json',
            'Content-Type' : 'application/json' }

   def doRequest( self, method, url, *args, **kwargs ):
      '''Issues an Http request

      Arguments:
         method -- Http method
         url -- endpoint of the request
         *args --  multiple arguments passed
         **kwargs -- multiple arguments passed that need to be handled using name

      Returns:
         response -- Json response from the endpoint

      Raises:
         CvpError -- If response is not json or response contains error code
                     If parameter data structures are incorrect
      '''
      if not 'cookies' in kwargs:
         kwargs[ 'cookies' ] = self.cookies
      response = method( url, *args, **kwargs )
      if not response.ok:
         raise CvpError( 2 )
      if 'errorCode' in response.text:
         errorCode = response.json().get( 'errorCode', 0 )
         raise CvpError( errorCode )
      return response.json()

   def _authenticationRequest( self, method, url, *args, **kwargs ):
      '''Issues an Http request for authentication

      Arguments:
         method -- Http method
         url -- endpoint of the request
         *args -- multiple arguments passed
         **kwargs -- multiple arguments passed that need to be handled using name

      Returns:
         response -- Information of the established session
                     (cookies, session_id etc.)

      Raises:
         CvpError -- If response contains error code or response is not json
                     If parameter data structures are incorrect
      '''
      response = method( url, *args, **kwargs )
      if not response.ok:
         raise CvpError( 2 )
      if 'errorCode' in response.text:
         errorCode = response.json().get( 'errorCode', 0 )
         raise CvpError( errorCode )
      return response

   def getConfigletsInfo( self ):
      '''Retrieves information of all configlets.

      Arguments: None

      Returns:
         configlets[ 'data' ] -- List of configlets with details
                                 ( type : List of Dict )

      Raises: None
      '''
      configlets = self.doRequest( requests.get,
            '%s/web/configlet/getConfiglets.do?startIndex=%d&endIndex=%d'
                  % ( self.url, 0, 0 ) )
      return configlets[ 'data' ]

   def deviceComplianceCheck( self, deviceConfigIdList, deviceMacAddress ):
      ''' Runs compliance check on the device. Finds differences in
      designed configuration according to Cvp application and actual
      running configuration on the device.

      Arguments:
         deviceConfigIdList -- Configlet Id list of configlets applied to device
                               as per the Designed configuration
         deviceMacAddress -- Mac address of the device

      Returns:
         complianceReport -- Information about the compliance check of the
                             device.
      Raises:
         CvpError -- If device Mac-Address is invalid
                     If parameter data structures are incorrect
      '''

      data = { 'netElementId' : deviceMacAddress,
            'configIdList' : deviceConfigIdList }

      complianceReport = self.doRequest( requests.post,
            '%s/web/ztp/runConfigSync.do' % self.url, data=json.dumps( data ),
            cookies=self.cookies )
      return complianceReport

   def authenticate( self, username, password ):
      '''Authentication with the web server

      Arguments:
         username -- login username ( type : String )
         password -- login password ( type : String )

      Returns: None

      Raises:
         CvpError -- If username and password combination is invalid
                     If parameter data structures are incorrect
      '''
      authData = { 'userId' : username, 'password' : password }
      authentication =  self._authenticationRequest( requests.post,
            '%s/web/login/authenticate.do' % self.url, data=json.dumps( authData ),
            headers=self.headers )
      self.cookies = authentication.cookies
      self.headers[ 'APP_SESSION_ID' ] = authentication.json()[ 'sessionId' ]

   def imageBundleAppliedContainers( self, imageBundleName ):
      '''Retrieves containers to which the image bundle is applied to.
      Warning -- Method deosn't check existence of the image bundle

      Arguments:
         imageBundleName -- name of the image bundle ( type : String )

      Returns:
         containers[ 'data' ] -- List of containers ( type : List of Dict )

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      containers = self.doRequest( requests.get,
            '%s/web/image/getImageBundleAppliedContainers.do?'
            'imageName=%s&startIndex=%d&endIndex=%d&queryparam=null'
            %( self.url, imageBundleName, 0, 0 ) )
      return containers[ 'data' ]

   def changeContainerName( self, oldName, newName, containerKey ):
      '''Changes the container name from old container name to
      the new name

      Arguments:
         oldName -- original name of the container
         containerKey -- unique Id associated with the container
         newName -- desired new name of the container

      Returns: None

      Raises:
         CvpError -- If the oldName is invalid
         CvpError -- If containerKey is invalid
      '''
      data = [ { "info" : "Container " + newName + " renamed from " + oldName,
         "infoPreview" : "Container " + newName + " renamed from " + oldName,
         "action" : "update",
         "nodeType" : "container",
         "nodeId" : containerKey,
         "toId" : "",
         "fromId" : "",
         "nodeName" : newName,
         "fromName" : "",
         "toName" : "",
         "toIdType" : "container",
         "oldNodeName" : oldName } ]
      self.doRequest( requests.post,
            '%s/web/ztp/addTempAction.do?format=topology&queryParam=&nodeId=%s' %
            ( self.url, containerKey ), data=json.dumps( data ),
            cookies=self.cookies )
      self._saveTopology( [] )

   def searchContainer( self, containerName ):
      '''Retrieves information about a container

      Arguments:
         containerName -- name of the container ( type : String )

      Returns:
         container[ 'data' ] -- Complete information about the container
                                ( type : Dict )

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      container = self.doRequest( requests.get,
            '%s/web/inventory/add/searchContainers.do?queryparam=%s&startIndex=%d'
            '&endIndex=%d' %(self.url, containerName, 0, 0 ) )
      return container[ 'data' ]

   def imageBundleAppliedDevices( self, imageBundleName):
      '''Retrieves devices to which the image bundle is applied to.
      Warning -- Method deosn't check existence of the image bundle

      Arguments:
         imagebundleName -- name of the image bundle ( type : String )

      Returns:
         devices[ 'data' ] -- List of devices ( type : List of Dict )

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      devices = self.doRequest( requests.get,
            '%s/web/image/getImageBundleAppliedDevices.do?'
            'imageName=%s&startIndex=%d&endIndex=%d&queryparam=null'
            % (self.url, imageBundleName, 0, 0) )
      return devices[ 'data' ]

   def addImage( self, imageName ):
      '''Add image to Cvp instance
      Warning -- image file with imageName as file should exist

      Argument:
         imageName -- name of the image ( type : String )

      Raises:
         Assertion Error -- If imageName is not of type string
         FileNotFoundError -- If image file doesn't exist

      Returns:
         imageInfo -- information of image added to the cvp instance
      '''
      assert isinstance( imageName, str )
      image = open( imageName, 'r' )
      imageInfo = self.doRequest( requests.post,
            '%s/web/image/addImage.do' % self.url, files={ 'file' : image } )
      return imageInfo

   def downloadImage( self, imageName, imageId, filePath='' ):
      '''Download the image file from Cvp Instance and stores at corresponding
      file path or current directory

      Arguments:
         imageName -- name of image (type : string )
         imageId -- unique Id assigned to the image ( type : string )
         filePath -- storage path in the local system (optional)( type : string )

      Raises:
         Http 500 -- If the imageId is invalid
         IOERROR -- If invalid file path is provided

      Returns None
      '''
      fileName = filePath + imageName
      URL =  '%s/web/services/image/getImagebyId/%s' % ( self.url, imageId )
      imageSWI = urllib.URLopener()
      imageSWI.retrieve( URL, fileName )

   def firstLoginDefaultPasswordReset( self,  newPassword, emailId ):
      '''Reset the password for the first login into the Cvp Web-UI
      Warning -- Method doesn;t check the validity of emailID

      Arguments:
         newPassword -- new password for password reset ( type : String )
         emailId -- emailId assigned to the user ( type : String )

      Returns:
         None

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      data = { "userId" : DEFAULT_USER,
            "oldPassword" : DEFAULT_PASSWORD,
            "currentPassword" : newPassword,
            "email" : emailId}
      self.doRequest( requests.post, '%s/web/login/changePassword.do'
            % self.url, data=json.dumps( data ) )

   def getInventory( self ):
      '''Retrieve information about devices provisioned by the Cvo instance

      Arguments: None

      Returns:
         inventory[ 'netElementList' ] -- List of information of all devices
         ( type : List of Dict )
         inventory[ 'containerList' ] -- Information of parent container of devices
         ( type : List of Dict )

      Raises: None
      '''
      inventory = self.doRequest( requests.get,
            '%s/web/inventory/getInventory.do?queryparam=.&startIndex=%d'
            '&endIndex=%d' % ( self.url, 0, 0 ), cookies=self.cookies )
      return ( inventory[ 'netElementList' ], inventory[ 'containerList' ] )

   def configAppliedContainers( self, configletName ):
      '''Retrieves containers to which the configlet is applied to.
      Warning -- Method deosn't check existence of the configlet

      Arguments:
         configletName -- name of the configlet ( type : String )

      Returns:
         containers[ 'data' ] -- List of container to which configlet is applied
         ( type : List of Dict )

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      containers = self.doRequest( requests.get,
            '%s/web/configlet/getAppliedContainers.do?configletName=%s'
            '&startIndex=%d&endIndex=%d&queryparam=null'
            % ( self.url, configletName, 0, 0 ) )
      return containers[ 'data' ]

   def configAppliedDevices( self, configletName ):
      '''Retrieves devices to which the configlet is applied to.
      Warning -- Method deosn't check existence of the configlet

      Arguments:
         configletName -- name of the configlet ( type : String )

      Returns:
         devices[ 'data' ] -- List of devices to which configlet is applied
         ( type : List of Dict )

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      devices = self.doRequest( requests.get,
            '%s/web/configlet/getAppliedDevices.do?configletName=%s'
            '&startIndex=%d&endIndex=%d&queryparam=null'
            % ( self.url, configletName, 0, 0 ) )
      return devices[ 'data' ]

   def retrieveInventory( self ):
      '''Retrieves information about containers and temporary devices present
      in Cvp inventory

      Arguments: None

      Returns:
         inventory[ 'containers' ] -- complete information of all containers
         ( type : List of Dict )
         inventory[ 'tempNetElement' ] -- List of information of all temporary
                                          devices (type : List of Dict )

      Raises: None
      '''
      inventory = self.doRequest(requests.get,
            '%s/web/inventory/add/retrieveInventory.do?startIndex=%d&endIndex=%d'
            %(self.url, 0, 0) )
      return (inventory[ 'containers' ], inventory[ 'tempNetElement' ] )

   def getImagesInfo( self ):
      '''Get information about all the images

      Arguments:None

      Returns:
         images[ 'data' ] -- List of details of all the images
                             ( type : List of Dict )

      Raises: None
      '''
      images = self.doRequest( requests.get,
            '%s/web/image/getImages.do?queryparam=&startIndex=%d&endIndex=%d'
            % ( self.url, 0, 0 ) )
      return images[ 'data' ]

   def addConfiglet( self, configletName, configletContent ):
      '''Add configlet to Cvp inventory

      Arguments:
         configletName -- name of the configlet ( type : String )
         configletContent -- content of the configlet ( type : String )

      Returns: None

      Raises:
         CvpError -- If configlet with same name already exists
                     If parameter data structures are incorrect
      '''
      configlet = { 'config' : configletContent,
            'name' : configletName }
      self.doRequest( requests.post,
            '%s/web/configlet/addConfiglet.do' % self.url,
            data=json.dumps( configlet ) )

   def getConfigletByName( self, configName ):
      '''Get information about configlet

      Arguments:
         configName -- name of the configlet ( type : String )

      Returns:
         configlet -- information about the configlet ( type : Dict )

      Raises:
         CvpError -- If configlet name is invalid
                     If parameter data structures are incorrect
      '''
      configlet = self.doRequest( requests.get,
            '%s/web/configlet/getConfigletByName.do?name=%s'
            % ( self.url, configName ) )
      return configlet

   def updateConfiglet( self, configletName, configletContent, configletKey ):
      '''Update configlet information

      Arguments:
         configletName -- name of configlet( type : String )
         configletContent -- content of the configlet ( type : String )
         configletKey -- key assigned to the configlet ( type : String )

      Returns: None

      Raises:
         CvpError -- If configlet key is invalid
                     If parameter data structures are incorrect
      '''
      configlet = { 'config' : configletContent,
            'name' : configletName ,
            'key' : configletKey }
      self.doRequest( requests.post,
            '%s/web/configlet/updateConfiglet.do' % ( self.url ),
            data=json.dumps( configlet ) )

   def deleteConfiglet( self, configletName, configletKey ):
      '''Removes the configlet from Cvp instance

      Arguments:
         configletName -- name of the configlet ( type : String )
         configletKey -- Key assigned to the configlet ( type : String )

      Returns: None

      Raises:
         CvpError -- If the configlet key is invalid
                     If parameter data structures are incorrect
      '''
      configlet = [ { 'key' : configletKey, 'name' : configletName } ]
      self.doRequest( requests.post,
            '%s/web/configlet/deleteConfiglet.do' % self.url,
            data=json.dumps( configlet ) )

   def saveImageBundle( self, imageBundleName, imageBundleCertified,
         imageInfoList ):
      '''Add image bundle to Cvp instance.

      Arguments:
         imageBundleName -- Name of image Bundle ( type : String )
         imageBundleCertified -- image bundle certified ( type : String )
         imageInfoList -- details of images present in image bundle
                          ( type : List of Dict )

      Returns: None

      Raises:
         CvpError -- If image bundle name is invalid
                     If image details are invalid
                     If parameter data structures are incorrect
      '''
      data = { 'name' : imageBundleName,
            'isCertifiedImage' : str( imageBundleCertified ).lower(),
            'images' : imageInfoList }
      self.doRequest( requests.post,
            '%s/web/image/saveImageBundle.do' % self.url,
            data=json.dumps( data ) )

   def getImageBundleByName( self, imageBundleName ):
      '''Returns image bundle informations

      Arguments:
         imageBundleName -- Name of the Image bundle ( type : String )

      Returns:
         imageBundle -- Complete information about the imagebundle ( type : Dict )

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''
      imageBundle = self.doRequest( requests.get,
            '%s/web/image/getImageBundleByName.do?name=%s'
            % ( self.url, imageBundleName ) )
      return imageBundle

   def updateImageBundle( self, imageBundleName, imageBundleCertified,
         imageInfoList, imageBundleKey ):
      '''Update image bundle information.

      Arguments:
         imageBundleName -- Name of image Bundle ( type : String )
         imageBundleCertified -- image bundle certified
                                 ( type : String )( value: true/false )
         imageInfoList -- details of images present in image bundle
                          ( type : List of dict )
         imageBundleKey -- key assigned to image bundle ( type : String )

      Returns: None

      Raises:
         CvpError -- If image bundle name or key are invalid
                     If information of image to be mapped to image bundle is invalid
                     If parameter data structures are incorrect
      '''
      data = { 'name' : imageBundleName,
            'isCertifiedImage' : str( imageBundleCertified ).lower(),
            'images' : imageInfoList,
            'id' : imageBundleKey }
      self.doRequest( requests.post,
            '%s/web/image/updateImageBundle.do' % ( self.url ),
            data=json.dumps( data ) )

   def addToInventory( self, deviceIpAddress, parentContainerName,
         parentContainerId ):
      '''Add device to the Cvp inventory. Warning -- Method doesn't check the
      existance of the parent container

      Arguments:
         deviceIpAddress -- ip address of the device to be added ( type : String )
         parentContainerName -- name of parent container ( type : String )
         parentContainerId -- Id of parent container ( type : String )

      Returns: None

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''

      data = [ { 'containerName' : parentContainerName,
         'containerId' : parentContainerId,
         'containerType' : 'Existing',
         'ipAddress' : deviceIpAddress,
         'containerList' : [] }  ]
      self.doRequest(requests.post,
            '%s/web/inventory/add/addToInventory.do?startIndex=%d&endIndex=%d'
            % ( self.url, 0, 0 ), data=json.dumps( data ) )

   def saveInventory( self ):
      '''Saves the current CVP inventory state

      Arguments: None

      Returns: None

      Raises: None
      '''

      self.doRequest( requests.post,
            '%s/web/inventory/add/saveInventory.do' % ( self.url ) )

   def retryAddToInventory( self, deviceKey, deviceIpAddress, username,
         password ):
      '''Retry addition of device to Cvp inventory

      Arguments:
         deviceKey -- mac address of the device ( type : String )
         deviceIpAddress -- ip address assigned to the device ( type : String )
         username -- username for device login ( type : String )
         password -- password for corresponding username ( type : String )

      Returns: None

      Raises:
         CvpError -- If device  key is invalid
                     If parameter data structures are incorrect
      '''
      loginData = { "key" : deviceKey, "ipAddress" : deviceIpAddress,
            "userName" : username, "password" : password }
      self.doRequest( requests.post,
            '%s/web/inventory/add/retryAddDeviceToInventory.do' %( self.url ),
            data=json.dumps( loginData ) )

   def _saveTopology( self, data ):
      '''Schedule tasks for many operations like configlet and image bundle
      mapping/removal to/from device or container, addition/deletion of containers,
      deletion of device.

      Arguments:
         data -- Information required for scheduling tasks

      Raises:
         CvpError -- If incorrect data is used to schedule tasks
      '''
      self.doRequest( requests.post,
            '%s/web/ztp/saveTopology.do' % ( self.url ),
            data=json.dumps( data ) )

   def executeTask( self, taskId ):
      '''Execute particular task in Cvp instance

      Argument:
         taskId -- Work order Id of the task ( type : int )

      Returns: None

      Raises:
         CvpError -- If work order Id of task is invalid
                     If parameter data structures are incorrect
      '''
      self.doRequest( requests.post,
            '%s/web/workflow/executeTask.do' % ( self.url ),
            data=json.dumps( taskId ) )

   def getTasks( self ):
      '''Retrieve information about all the tasks in Cvp Instance

      Arguments: None

      Returns:
         tasks[ 'data' ] -- List of details of tasks ( type: dict of dict )

      Raises: None
      '''
      tasks = self.doRequest( requests.get,
            '%s/web/workflow/getTasks.do?queryparam=&startIndex=%d&endIndex=%d'
            % (self.url, 0, 0) )
      return tasks[ 'data' ]

   def getImageBundles( self ):
      '''Get all details of all image bundles from Cvp instance

      Arguments: None

      Returns:
         imageBundles[ 'data' ] -- List of details of image bundles
                                   ( type: dict of dict )

      Raises: None
      '''

      imageBundles = self.doRequest( requests.get,
            '%s/web/image/getImageBundles.do?queryparam=&startIndex=%d&endIndex=%d'
            % ( self.url, 0, 0 ) )
      return imageBundles[ 'data' ]

   def deleteImageBundle( self, imageBundleKey, imageBundleName ):
      '''Delete image bundle from Cvp instance

      Argument:
         imageBundleKey -- unique key assigned to image bundle ( type : String )
         imageBundleName -- name of the image bundle ( type : String )

      Returns: None

      Raises:
         CvpError -- If image bundle key is invalid
                     If image bundle is applied to any entity
                     If parameter data structures are incorrect
      '''

      data = [ { 'key' : imageBundleKey, 'name' : imageBundleName } ]
      self.doRequest( requests.post,
            '%s/web/image/deleteImageBundles.do' % self.url,
            data=json.dumps( data ) )

   def deleteDuplicateDevice( self, tempDeviceId ):
      '''Delete duplicate device from Cvp. Warning -- Method doesn't check
      presence of actual device corresponding to the tempDeviceId

      Argument:
         tempDeviceId -- temporary Id assigned to device ( type : String )

      Returns:
         None

      Raises:
         CvpError -- If parameter data structures are inconsistent
      '''

      self.doRequest( requests.get,
            '%s/web/inventory/add/deleteFromInventory.do?netElementId=%s'
            % ( self.url, tempDeviceId ) )

   def deleteContainer( self, containerName, containerKey, parentContainerName,
         parentKey ):
      '''Delete container from Cvp inventory. Warning -- doesn't check
      existance of the parent containers

      Arguments:
         containerName -- name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         parentContainerName -- parent container name (type: string)
         parentKey -- unique key assigned to parent container (type: string)

      Returns:
         None

      Raises:
         CvpError -- If container key is invalid
                     If parameter data structures are incorrect
      '''

      data = [ { "id" : 1,
         "info" : "Container " + containerName + " deleted",
         "action" : "delete",
         "nodeType" : "container",
         "nodeId" : containerKey,
         "toId" : "",
         "fromId" : parentKey,
         "nodeName" : containerName,
         "fromName" : parentContainerName,
         "toName" : "",
         "childTasks" : [],
         "parentTask" : "" } ]
      self._saveTopology( data )

   def deleteDevice( self, deviceKey, parentContainerName, containerKey ):
      '''Delete the device from Cvp inventory
      Warning -- doesn't check the existence of the parent container

      Arguments:
         deviceKey -- mac address of the device (type: string)
         parentContainerName -- name of parent container of device (type: string)
         containerKey -- Key assigned to parent container (type: string)

      Returns: None

      Raises:
         CvpError -- If device key is invalid
                     If parameter data structures are incorrect
      '''
      data = [ { "id" : 1,
         "info" : "Device Remove: undefined - To be Removed from"
         "Container"  + parentContainerName,
         "infoPreview" : "<b>Device Remove: undefined<b> - To be Removed "
         "from Container" + parentContainerName,
         "note" : "",
         "action" : "remove",
         "nodeType" : "netelement",
         "nodeId" : deviceKey,
         "toId" : "",
         "fromId" : containerKey,
         "fromName" : parentContainerName,
         "toName" : "",
         "childTasks" : [],
         "parentTask" : "" } ]
      self._saveTopology( data )

   def applyConfigToDevice( self, deviceIpAddress, deviceFqdn, deviceKey,
         configNameList, configKeyList  ):
      '''Applies configlets to device. Warning -- Method doesn't check existence of
      configlets

      Arguments:
         deviceIpAddress -- Ip address of the device (type: string)
         deviceFqdn -- Fully qualified domain name for device (type: string)
         deviceKey -- mac address of the device (type: string)
         configNameList -- List of name of configlets to be applied
                           (type: List of string)
         configKeyList -- Keys of configlets to be applied (type: List of string)

      Returns: None

      Raises:
         CvpError -- If device ip key is invalid
                     If parameter data structures are incorrect
      '''

      data = [ { "id" : 1,
         "info" : "Configlet Assign: to Device" + deviceFqdn +
         " \nCurrent ManagementIP:" + deviceIpAddress +
         "  \nTarget ManagementIP",
         "infoPreview" : "<b>Configlet Assign:</b> to Device" + deviceFqdn,
         "note" : "",
         "action" : "associate",
         "nodeType" : "configlet",
         "nodeId" : "",
         "configletList" : configKeyList,
         "configletNamesList" : configNameList,
         "ignoreConfigletList" : [],
         "ignoreConfigletNamesList" : [],
         "toId" : deviceKey,
         "toIdType" : "netelement",
         "fromId" : "",
         "nodeName" : "",
         "fromName" : "",
         "toName" : deviceKey,
         "childTasks" :[],
         "parentTask" : "",
         "nodeIpAddress" : deviceIpAddress,
         "nodeTargetIpAddress" : "" } ]
      self._saveTopology( data )

   def applyConfigToContainer( self, containerName, containerKey, configNameList,
         configKeyList ):
      '''Applies configlets to container. Warning -- Method doesn't check existence
      of container and the configlets

      Arguments:
         containerName --name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         configNameList -- List of name of configlets to be applied
         (type: List of Strings)
         configKeyList -- Keys of configlets to be applied (type: List of Strings)

      Returns: None

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''

      data = [ { "id" : 1,
         "info" : "Configlet Assign: to container " + containerName,
         "infoPreview" : "<b>Configlet Assign:</b> to container " + containerName +
         "\nCurrent ManagementIP : undefined\nTarget ManagementIPundefined",
         "note" : "",
         "action" : "associate",
         "nodeType" : "configlet",
         "nodeId" : "",
         "configletList" : configKeyList,
         "configletNamesList" : configNameList,
         "ignoreConfigletList" : [],
         "ignoreConfigletNamesList" : [],
         "toId" : containerKey,
         "toIdType" : "container",
         "fromId" : "",
         "nodeName" : "",
         "fromName" : "",
         "toName" : containerName,
         "childTasks" : [],
         "parentTask" : "" } ]
      self._saveTopology( data )

   def removeConfigFromContainer( self, containerName, containerKey, configNameList,
         configKeyList ):
      '''Remove configlets assigned to container. Warning -- Method doesn't check
      existence of configlets and containers

      Arguments:
         containerName --name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         configNameList -- List of name of configlets to be removed
         (type: List of Strings)
         configKeyList -- Keys of configlets to be removed (type: List of Strings)

      Returns: None

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''

      data =   [ { "id" : 1,
         "info" : "Configlet Assign: to container " + containerName,
         "infoPreview" : "<b>Configlet Assign:</b> to container " + containerName
         + "Current ManagementIP : undefined\nTarget ManagementIPundefined",
         "note" : "",
         "action" : "associate",
         "nodeType" : "configlet",
         "nodeId" : '',
         "configletList" : [],
         "configletNamesList" : [],
         "ignoreConfigletList": configKeyList,
         "ignoreConfigletNamesList" : configNameList,
         "toId" : containerKey,
         "toIdType" : "container",
         "fromId" : '',
         "nodeName" : '',
         "fromName" : '',
         "toName" : containerName,
         "childTasks" : [],
         "parentTask" : "" } ]
      self._saveTopology( data )

   def addContainer( self, containerName, containerParentName,
         parentContainerId ):
      '''Adds container to Cvp inventory

      Arguments:
         containerName -- name of container (type: string)
         containerParentName -- name of the parent container (type: string)
         parentContainerId -- Id of parent container (type: string)

      Returns: None

      Raises:
         CvpError -- If container with same name already exists,
                     If Parent Id is invalid
                     If parameter data structures are incorrect
      '''

      data = [ { "id" : 1,
         "info" : "Container " + containerName + " created",
         "infoPreview" : "Container " + containerName + " created",
         "note" : "",
         "action" : "add",
         "nodeType" : "container",
         "nodeId" : "New_container1",
         "toId" : parentContainerId,
         "fromId" : "",
         "nodeName" : containerName,
         "fromName" : "",
         "toName" : containerParentName,
         "childTasks" : [],
         "parentTask" : "" } ]
      self._saveTopology( data )

   def applyImageBundleToDevice( self, deviceKey, deviceFqdn, imageBundleName,
         imageBundleKey ):
      '''Applies image bundle to devices. Warning -- Method doesn't check existence
      of image bundle

      Arguments:
         deviceKey -- mac address of device (type: string)
         deviceFqdn -- Fully qualified domain name for device (type: string)
         imageBundleName -- name of image bundle (type: string)
         imageBundleKey -- unique key assigned to image bundle (type: string)

      Returns: None

      Raises:
         CvpError -- If device key is invalid,
                     If parameter data structures are incorrect
      '''

      data = [ { "id" : 1,
         "info" : "Image Bundle Assign:" + imageBundleName + " - To be "
         "assigned to Device " + deviceFqdn,
         "infoPreview" : "<b>Image Bundle Assign:</b>" +
         imageBundleName + " - To be assigned to Device" + deviceFqdn,
         "note" : "",
         "action" : "associate",
         "nodeType" : "imagebundle",
         "nodeId" : imageBundleKey,
         "toId" : deviceKey,
         "toIdType" : "netelement",
         "fromId" : "",
         "nodeName" : imageBundleName,
         "fromName" : "",
         "toName" : deviceFqdn,
         "childTasks" : [],
         "parentTask" : "" } ]
      self._saveTopology( data )

   def applyImageBundleToContainer( self, containerName, containerKey,
         imageBundleName, imageBundleKey ):
      '''Applies image bundle to a container. Warning -- Method doesn't check
      existence of container and image bundle

      Arguments:
         containerName -- name of the container (type: string)
         containerKey -- unique key assigned to container (type: string)
         imageBundleName -- name of the image bundle (type: string)
         imageBundleKey -- unique key assigned to image bundle (type: string)

      Returns: None

      Raises:
         CvpError -- If parameter data structures are incorrect
      '''

      data = [ { "id" : 1,
         "info" : "Image Bundle Assign:" + imageBundleName + " - To be"
         "assigned to devices under Container" + containerName,
         "infoPreview" : "<b>Image Bundle Assign:</b>" + imageBundleName +
         "- To be assigned to devices under Container" + containerName,
         "action" : "associate",
         "nodeType" : "imagebundle",
         "nodeId" : imageBundleKey,
         "toId" : containerKey,
         "toIdType" : "container",
         "fromId" : "",
         "nodeName" : imageBundleName,
         "fromName" : "",
         "childTasks" : [],
         "parentTask" : "" } ]
      self._saveTopology( data )

# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
'''
@Copyright: 2015 Arista Networks, Inc.
Arista Networks, Inc. Confidential and Proprietary.

Cvp.py is a library which can be used to perform various
actions over the cvp instance. There are numerous methods each
corresponding to each action. Methods are listed below in the Cvp class.
'''
import os
import Queue
import cvpServices
import errorCodes

def encoder( obj ):
   '''This method states the encoding specifications for the data which
   is to be dumped in a file'''
   if hasattr( obj, 'jsonable' ):
      return obj.jsonable()
   else:
      raise TypeError

class Image( object ):
   '''Image class, stores all required information about
   an image.

   state variables:
      name -- name fo the image
      Key -- unique key assigned to image
      imageId -- Cvp internally generated field. Endpoint for
      downloading the image from the Cvp
   '''
   def __init__( self, name, key, imageId ):
      self.name = name
      self.key = key
      self.imageId = imageId

   def __eq__( self, that ):
      return ( self.name == that.name and
            self.key == that.key and
            self.imageId == that.imageId )

   def jsonable( self ):
      ''' Returns dictionary object which implements class namespace'''
      return self.__dict__

class Container( object ):
   '''Container class, stores all required information about
   a container

   State variables:
      name -- name of the container
      key -- unique key assigned to container by Cvp application
      parentId -- unique key assigned to the parent
      configlets -- list of configlet name assigned to container
      imageBundle -- name of the image bundle assigned to container
      parentName -- Name of the parent container
   '''

   def __init__( self, name, key, parentId, configlets, imageBundle,
         parentName ):
      self.name = name
      self.key = key
      self.parentId = parentId
      self.configlets = configlets
      self.imageBundle = imageBundle
      self.parentName = parentName

   def __eq__( self, that ):
      return ( self.name == that.name and
            self.key == that.key and
            self.parentId == that.parentId and
            self.configlets == that.configlets and
            self.imageBundle == that.imageBundle and
            self.parentName == that.parentName )

   def jsonable( self ):
      ''' Returns dictionary object which implements class namespace'''
      return self.__dict__

class Task( object ):
   ''' Task class, Stores information about a Task

   State variables:
      taskId -- work order Id assigned to the task
      description -- information explaining what task is about
   '''

   def __init__( self, taskId, description ):
      self.taskId = taskId,
      self.description = description

   def __eq__( self, that ):
      return ( self.taskId == that.taskId and
            self.description == that.description )

   def jsonable( self ):
      ''' Returns dictionary object which implements class namespace'''
      return self.__dict__

class Device( object ):
   ''' Device class helps store all the information about a particular device

   state variables:
      ipAddress -- ip address of the device
      fqdn -- fully qualified domain name for the device
      key -- unique key assigned to the device
      containerName -- name of the parent container
      containerId -- uniqu Id assigned to the parent container
      imageBundle -- name of the imageBundle assigned to device
      configlets -- list of names of configlets assigned to the device
   '''
   def __init__( self, ipAddress, fqdn, key, containerName, containerId,
         imageBundle, configlets ):
      self.ipAddress = ipAddress
      self.fqdn = fqdn
      self.key = key
      self.containerName = containerName
      self.containerId = containerId
      self.imageBundle = imageBundle
      self.configlets = configlets

   def __eq__( self, that ):
      return ( self.ipAddress == that.ipAddress and
            self.fqdn == that.fqdn and self.key == that.key and
            self.containerName == that.containerName and
            self.containerId == that.containerId and
            self.imageBundle == that.imageBundle and
            self.configlets == that.configlets )

   def jsonable( self ):
      ''' Returns dictionary object which implements class namespace'''
      return self.__dict__

class Configlet( object ):
   '''Configlet class stores all the information necessary about the
   configlet

   state variables:
      name -- name of the configlet
      config -- configuration information inside configlet
      key -- unique key assigned to the configlet
      containerList -- List of containers to which this configlet is applied
      deviceList -- List of devices to which this configlet is applied
   '''
   def __init__( self, name, config, key, containerList, deviceList ):
      self.name = name
      self.config = config
      self.key = key
      self.containerList = containerList
      self.deviceList = deviceList

   def __eq__( self, that ):
      return ( self.name == that.name and
             self.config == that.config and
             self.containerList == that.containerList and
             self.deviceList == that.deviceList )

   def jsonable( self ):
      ''' Returns dictionary object which implements class namespace'''
      return self.__dict__

class ImageBundle( object ):
   '''ImageBundle class objects stores all necessary information about the
   bundle

   state variables:
      name -- name of the image bundle
      key -- unique key assinged to the image bundle
      imageKeys -- keys corresponding to images present in this image bundle
      deviceList -- List of devices to which image bundle is mapped to
      containerList -- list of containers to which image bundle is mapped to
      certified -- indicates whether image bundle is certified or not
   '''
   def __init__( self, name, key, imageKeys, certified, containerList,
         deviceList ):
      self.name = name
      self.key = key
      self.imageKeys = imageKeys
      self.deviceList = deviceList
      self.containerList = containerList
      self.certified = certified

   def __eq__( self, that ):
      return ( self.name == that.name and
             self.key == that.key and self.imageKeys == that.imageKeys and
             self.containerList == that.containerList and
             self.deviceList == that.deviceList and
             self.certified == that.certified )

   def jsonable( self ):
      ''' Returns dictionary object which implements class namespace'''
      return self.__dict__

class Cvp( object ):
   '''Class Cvp contains all the methods essentials for downloading the
   Cvp state, restoring the Cvp State, deletion of Cvp State, modification of
   cvp state

   Public methods:
      authenticate( username, password )
      getDevices()
      getDevice( deviceIpAddress )
      addDevice( device, loginCredentials )
      addDevices( deviceList )
      deviceComplainceCheck( deviceIpAddress )
      deleteDevice( device )
      getConfiglets()
      getConfiglet( configName )
      addConfiglet( configlet )
      updateConfiglet( configlet )
      deleteConfiglet( configlet )
      mapConfigToDevice( device , configList )
      addContainer( container )
      getContainers()
      getContainer( containerName )
      getRootContainerInfo()
      renameContainer( oldContainerName, newContainerName )
      addContainers( containerInfoList )
      deleteContainer( container )
      getImages( storageDirPath )
      getImage(  imageName , storageDirPath )
      addImage( imageName )
      getImageBundles()
      getImageBundle( imageBundleName )
      deleteImageBundle( imageBundle )
      addImageBundle( imageBundle, imageNameList )
      updateImageBundle( imageBundle, imageNameList )
      mapImageBundleToDevice( device, imageBundleName)
      mapImageBundleToContainer( container, imageBundleName )
      mapConfigToContainer( container , configNameList )
      removeConfigFromContainer( container, configList )
      executeAllPendingTask()
      executeTask( taskId )
      getPendingTasksInfo()
      monitorTaskStatus( taskIdList )

   State variables:
      cvpService -- CvpService class instance

      '''

   def __init__( self, host, ssl=False, port=80 ):
      '''Constructer for Cvp class.'''
      self.cvpService = cvpServices.CvpService( host, ssl, port )

   def authenticate( self, username, password ):
      '''Authenticate the user login credentials

      Arguments:
         username -- username for login ( type : string )
         password -- login pasword (type : String )

      Raises:
         CvpError -- If invalid login creedentials

      Returns None'''
      self.cvpService.authenticate( username, password )

   def _getContainerConfigMap( self, configNameList ):
      '''Finds which configlets are  mapped to which containers

      Arguments:
         configNameList -- List of configlet names (type: List of strings )

      Returns:
         configMap -- Dictionary with keys as container name and
            value is list of configlet applied to that container ( type : Dict )
      '''
      configMap = {}
      for configName in configNameList:
         containers = self.cvpService.configAppliedContainers( configName )
         for container in containers:
            configList = []
            key = container[ 'containerName' ]
            if key in configMap:
               configList = configMap[ container[ 'containerName' ] ]
               configList.append( configName )
               configMap[ container[ 'containerName' ] ] = configList
            else :
               configList.append( configName )
               configMap[ container[ 'containerName' ] ] = configList
      return configMap

   def _getDeviceConfigMap( self, configNameList ):
      '''Finds which configlets are mapped to which devices.

      Arguments:
         configNameList -- List of configlet names (type: List of strings )  )

      Returns:
         configMap -- Dictionary with keys as device Ips and
         value is list of configlets applied to that device ( type : Dict )
      '''
      configMap = {}
      for configName in configNameList:
         devices = self.cvpService.configAppliedDevices( configName )
         for device in devices:
            configList = []
            key = device[ 'ipAddress' ]
            if key in configMap:
               configList = configMap[ device[ 'ipAddress' ] ]
               configList.append( configName )
               configMap[device[ 'ipAddress' ] ] = configList
            else:
               configList.append( configName )
               configMap[ device[ 'ipAddress' ] ] = configList
      return configMap

   def _getContainerImageBundleMap( self, imageBundleNameList ):
      '''Finds which image bundle is mapped to which containers.

      Argument:
         imageBundleNameList -- List of image bundle names ( type : String )

      Returns:
         imageBundleMap -- Dictionary with keys as container names and
         value is image bundle applied to that container ( type : Dict )
      '''
      imageBundleMap = {}
      for imageBundleName in imageBundleNameList:
         containerList = self.cvpService.imageBundleAppliedContainers(
               imageBundleName )
         for container in containerList:
            imageBundleMap[ container [ 'containerName' ] ] = imageBundleName
      return imageBundleMap

   def _getDeviceImageBundleMap( self, imageBundleNameList ):
      '''Finds which image bundle is mapped to which devices.

      Argument:
         imageBundleNameList -- List of image bundle names ( type : String )

      Returns:
         imageBundleMap -- Dictionary with keys as device Ips and
         value is image bundle applied to that device ( type : Dict )
      '''
      imageBundleMap = {}
      for imageBundleName in imageBundleNameList:
         devices = self.cvpService.imageBundleAppliedDevices( imageBundleName )
         for device in devices:
            imageBundleMap[ device [ 'ipAddress' ] ] = imageBundleName
      return imageBundleMap

   def _getImageBundleNameList( self ):
      ''' finds the list of image bundles present in the cvp instance

      Arguments None

      Returns:
         imageBundleNameList -- Name of all image bundles( type : List of strings ) )
      '''
      imageBundleNameList = []
      imageBundles = self.cvpService.getImageBundles()
      for imageBundle in imageBundles:
         imageBundleNameList.append( imageBundle[ 'name' ] )
      return imageBundleNameList

   def _getConfigNameList( self ):
      '''finds the list of configlets present in the cvp instance

      Arguments None

      Returns:
         configNameList -- Name of all configlets( type : List of strings ) )
      '''
      configNameList = []
      configlets = self.cvpService.getConfigletsInfo()
      for config in configlets:
         configNameList.append( config[ 'name' ] )
      return configNameList

   def getDevices( self ):
      '''Collect information of all the devices. Information of device consist
      of the device specifications like ip address, mac address, configlets and
      image bundle applied to device.

      Arguments None

      Returns:
         deviceInfoList -- List of device ( type : List of Device ( class ) )
      '''
      imageBundleNameList = self._getImageBundleNameList()
      imageMap = self._getDeviceImageBundleMap( imageBundleNameList )
      configNameList = self._getConfigNameList()
      configMap = self._getDeviceConfigMap( configNameList )
      devices, containers = self.cvpService.getInventory()
      deviceContainer = {}
      deviceInfoList = []
      for deviceMacAddress, parentName in containers.iteritems():
         deviceContainer[ deviceMacAddress ] = parentName
      for dut in devices:
         if not deviceContainer[ dut[ 'key' ] ]:
            raise cvpServices.CvpError( errorCodes.INVALID_CONTAINER_NAME )
         parentContainerName = deviceContainer[ dut[ 'key' ] ]
         parentContainerId = 'undefined_container' if ( parentContainerName
               == 'Undefined' ) else self._getContainerInfo(
                     parentContainerName )[ 'key' ]
         appliedConfigs = configMap[ dut[ 'ipAddress' ] ] if ( dut[ 'ipAddress' ]
               in configMap ) else ''
         appliedImageBundle = imageMap[ dut[ 'ipAddress' ] ] if ( dut[ 'ipAddress' ]
               in imageMap ) else ''
         deviceInfoList.append( Device( dut[ 'ipAddress' ], dut[ 'fqdn' ],
            dut[ 'key' ], parentContainerName, parentContainerId,
            appliedImageBundle, appliedConfigs ) )
      return deviceInfoList

   def _getContainerInfo( self, containerName ):
      '''Returns container information for given container name

      Argument:
         containerName -- name of the contianer ( type : String)

      Raises :
         CvpError -- Name of the container ( containerName ) is invalid

      Returns:
         container -- all information of particular container
            ( type: Container ( class ) )
      '''
      containersInfo = self.cvpService.searchContainer( containerName )
      if not containersInfo:
         raise cvpServices.CvpError( errorCodes.INVALID_CONTAINER_NAME )
      for container in containersInfo:
         if container[ 'name' ] == containerName:
            return container

   def getDevice( self , deviceIpAddress ):
      '''Retrieve information about device.Information of device consist
      of the device specifications like ip address, mac address, configlets and
      image bundle applied to device.

      Argument:
         deviceIpAddress -- Ip address of the device ( type : String )

      Returns:
         deviceInfo -- Information about the device ( type : Device ( class ) )
      '''
      imageBundleNameList = self._getImageBundleNameList()
      imageMap = self._getDeviceImageBundleMap( imageBundleNameList )
      configNameList = self._getConfigNameList()
      configMap = self._getDeviceConfigMap( configNameList )
      devices, containers = self.cvpService.getInventory()
      for dut in devices:
         if dut[ 'ipAddress' ] != deviceIpAddress:
            continue
         for deviceMacAddress, parentName in containers.iteritems():
            if deviceMacAddress == dut[ 'key' ]:
               parentContainerName = parentName
               break
         if not parentContainerName:
            raise cvpServices.CvpError( errorCodes.INVALID_CONTAINER_NAME )
         parentContainerId = 'undefined_container' if ( parentContainerName
               == 'Undefined' ) else self._getContainerInfo(
                     parentContainerName )[ 'key' ]
         appliedConfigs = configMap[ dut[ 'ipAddress' ] ] if ( dut[ 'ipAddress' ]
               in configMap ) else ''
         appliedImageBundle = imageMap[ dut[ 'ipAddress' ] ] if ( dut[ 'ipAddress' ]
               in imageMap ) else ''
         deviceInfo = Device( dut[ 'ipAddress' ], dut[ 'fqdn' ],
               dut[ 'key' ], parentContainerName, parentContainerId,
               appliedImageBundle, appliedConfigs )
         break
      return deviceInfo

   def getConfiglets( self ):
      '''Retrieve the full set of Configlets

      Argument None

      Returns:
         configletList -- information of all configlets
            ( type : List of Configlet ( class ) )
      '''
      configletList = []
      configlets = self.cvpService.getConfigletsInfo()
      for config in configlets:
         containerList, deviceList = self._getConfigMap( config[ 'name' ] )
         configletList.append( Configlet( config[ 'name' ], config[ 'config' ],
            config[ 'key' ], containerList, deviceList ) )
      return configletList

   def _getConfigMap( self, configName ):
      ''' Finds Devices and Containers to which a particular
      configlet is mapped to.

      Argument:
         configName -- name of the configlet ( type : String )

      Returns:
         containerList -- list of container names
         deviceList -- List of device ip Addresses
      '''
      containerList = []
      deviceList = []
      containers = self.cvpService.configAppliedContainers( configName )
      for container in containers:
         containerList.append( container[ 'containerName' ] )
      devices = self.cvpService.configAppliedDevices( configName )
      for device in devices:
         deviceList.append( device[ 'ipAddress' ] )
      return containerList, deviceList

   def _getImageBundleMap( self, imageBundleName ):
      ''' Finds Devices and Containers to which a particular
      imageBundle is mapped to

      Argument:
         imageBundleName -- name of the image bundle ( type : String )

      Returns:
         containerList -- List of container names
         deviceList -- List of device ip addresses
      '''
      containerList = []
      deviceList = []
      containers = self.cvpService.imageBundleAppliedContainers( imageBundleName )
      for container in containers:
         containerList.append( container[ 'containerName' ] )
      devices = self.cvpService.imageBundleAppliedDevices( imageBundleName )
      for device in devices:
         deviceList.append( device[ 'ipAddress' ] )
      return containerList, deviceList

   def getContainers( self ):
      '''Retrieve the hierarchy of the containers and store information on all
      of these containers. Information of container consist of specifications
      like container Key, parent container key, container name, configlets and
      image bundle applied to container.

      Argument None

      Returns:
         containerInfoList -- list of container informations
            ( type : List of Container ( class ) )
      '''
      imageBundleNameList = self._getImageBundleNameList()
      imageMap = self._getContainerImageBundleMap( imageBundleNameList )
      configNameList = self._getConfigNameList()
      configMap = self._getContainerConfigMap( configNameList )
      containers, _ = self.cvpService.retrieveInventory()
      rawContainerInfoList = []
      rawContainerInfoList.append( containers )
      containerInfoList = []
      containerInfoList = self._recursiveParse( containerInfoList,
            rawContainerInfoList, configMap, imageMap, '' )
      return containerInfoList

   def _recursiveParse(self, containerInfoList, childContainerList,
         configMap, imageMap, parentName):
      ''' internal function for recursive depth first search to obtain container
      information from the container hierarchy. It handles different cases
      like the configlet applied or not, image bundle applied or not to containers'''

      for container in childContainerList:
         if container[ 'childContainerList' ]:
            containerInfoList = self._recursiveParse( containerInfoList,
                  container[ 'childContainerList' ], configMap, imageMap,
                  container[ 'name' ] )
         parentContainerName = '' if container[ 'key' ] == 'root' else parentName
         appliedConfigs = configMap[ container[ 'name' ] ] if ( container[ 'name' ]
               in configMap ) else ''
         appliedImageBundle = imageMap[ container[ 'name' ] ] if (
               container[ 'name' ] in imageMap ) else ''
         containerInfoList.append( Container( container[ 'name' ],
            container[ 'key' ], container[ 'parentContainerId' ], appliedConfigs,
            appliedImageBundle, parentContainerName ) )
      return containerInfoList

   def getContainer( self, containerName ):
      '''Retrieve a container Information.Information of container consist of
      specifications like container Key, parent container key, container name,
      configlets and image bundle applied to container

      Arguments
         ContainerName -- name of the container ( type : String )

      Raises:
         CvpError -- If container name is invalid

      Returns:
         containerInfo -- Information about the container( type : Container(
         class ) )
      '''
      container = self._getContainerInfo( containerName )
      imageBundleNameList = self._getImageBundleNameList()
      imageMap = self._getContainerImageBundleMap( imageBundleNameList )
      configNameList = self._getConfigNameList()
      configMap = self._getContainerConfigMap( configNameList )
      parentName = '' if container[ 'key' ] == 'root' else self._getparentInfo(
            container[ 'parentId' ] )
      appliedConfigs = configMap[ container[ 'name' ] ] if ( container[ 'name' ] in
            configMap ) else ''
      appliedImageBundle = imageMap[ container[ 'name' ] ] if (  container[ 'name' ]
            in imageMap ) else ''
      containerInfo = Container( container[ 'name' ], container[ 'key' ],
            container[ 'parentId' ], appliedConfigs,
            appliedImageBundle, parentName )
      return containerInfo

   def getImages( self , storageDirPath='' ):
      ''' Images are downloaded and saved to the file path.

      Argument:
         storageDirPath -- path to directory for storing image files ( optional )
            ( type : String )

      Returns:
         imageList -- List of inforamtion of images downloaded
            ( type : List of Image ( class ) )'''

      imageList = []
      images = self.cvpService.getImagesInfo()
      for image in images:
         imageList.append( Image( image[ 'name' ], image[ 'key' ],
            image[ 'imageId' ] ) )
         self.cvpService.downloadImage( image[ 'name' ], image[ 'imageId' ],
               storageDirPath )
      return imageList

   def getImage( self, imageName , storageDirPath='' ):
      ''' Image is downloaded and saved in the workspace

      Argument :
         imageName -- name of image to be downloaded ( type : String )
         storageDirPath -- path to directory for storing image files ( optional )
         ( type : String )

      Raises:
         CvpError -- If image name is incorrect

      Returns:
         imageInfo -- information of image downloaded. ( type : Image ( class )
      '''
      images = self.cvpService.getImagesInfo()
      imagePresentFlag = False
      for image in images:
         if image[ 'name' ] == imageName:
            imagePresentFlag = True
            imageInfo = Image( image[ 'name' ], image[ 'key' ],
                  image[ 'imageId' ] )
            self.cvpService.downloadImage( image[ 'name' ], image[ 'imageId' ],
                  storageDirPath )
            break
      if imagePresentFlag == False:
         raise cvpServices.CvpError( errorCodes.INVALID_IMAGE_NAME )
      return imageInfo

   def getConfiglet( self, configName ):
      '''Retrieve a specific configlet.

      Argument:
         configName -- name of the configlet ( type : String )

      Raises:
         CvpError : If configlet name is invalid

      Returns:
         Configlet -- information of the configlet ( type : Configlet ( class ) )
      '''
      config = self.cvpService.getConfigletByName( configName )
      return Configlet( config[ 'name' ], config[ 'config' ], config[ 'key' ],
            '', '' )

   def _getparentInfo( self , parentId ):
      ''' retrieve information of parent for newly added container using the
      recursive Depth First Search returns name of the parent container'''
      if parentId == None:
         return ''
      containers, _ = self.cvpService.retrieveInventory()
      rawContainersInfo = []
      rawContainersInfo.append( containers )
      parentName = self._recursiveParentInfo( rawContainersInfo, parentId )
      return parentName

   def _recursiveParentInfo( self, childContainerList, parentId ):
      ''' internal function for getting parent container info in the hierarchy'''
      for container in childContainerList:
         if container[ 'key' ] == parentId:
            return container[ 'name' ]
         elif len( container[ 'childContainerList' ] ) > 0 :
            parentName = self._recursiveParentInfo(
                  container[ 'childContainerList' ], parentId )
            return parentName

   def addContainers( self, containerInfoList ):
      '''Add containers to the inventory by maintaining the hierarchy of the
      containers

      Argument:
         containerInfoList -- List of container inforamtion
            ( type : List of Container ( class ) )

      Raise :
         Assertion Error -- if container is not Container type
         CvpError -- If container already exists
         CvpError -- If parent container name is invalid

      Returns None
      '''
      currRootContainerInfo = self.getRootContainerInfo()
      containerCount = len( containerInfoList )
      parentQueue = Queue.Queue()
      parentName = currRootContainerInfo.name
      while containerCount > 1 :
         for container in containerInfoList:
            assert isinstance( container, Container )
            if container.parentName == parentName:
               self.addContainer( container )
               parentQueue.put( container.name )
               containerCount = containerCount - 1
         parentName = parentQueue.get()

   def addConfiglet( self, configlet ):
      '''Add a configlet to cvp inventory

      Argument:
         configlet -- information of the new configlet
            ( type : Configlet ( class ) )

      Raises:
         CvpError -- If configlet name is invalid
         Assertion Error -- If configlet is not of type Configlet

      Return None
      '''
      assert isinstance( configlet, Configlet )
      self.cvpService.addConfiglet( configlet.name, configlet.config )

   def updateConfiglet( self, configlet ):
      ''' updating an existing configlet in Cvp instance

      Argument:
          configlet -- updated information of the configlet
            ( type : Confgilet ( class ) )

      Raises:
         CvpError -- If configlet name is invalid
         Assertion Error -- If configlet is not of type Configlet
      Returns None
      '''
      assert isinstance( configlet, Configlet )
      currConfig = self.cvpService.getConfigletByName( configlet.name )
      self.cvpService.updateConfiglet( configlet.name, configlet.config,
            currConfig[ 'key' ] )

   def deleteConfiglet( self, configlet ):
      '''Remove a configlet from the Cvp instance

      Argument:
         configlet -- information of the configlet to be removed
            ( type : Confgilet ( class ) )

      Raises:
         CvpError -- If configlet name is invalid
         Assertion Error -- If configlet is not of type Configlet

      Returns None
      '''
      assert isinstance( configlet, Configlet )
      self.cvpService.deleteConfiglet( configlet.name, configlet.key )

   def updateImageBundle( self, imageBundle, imageNameList ):
      '''update an image bundle in Cvp instance

      Argument:
         imageBundle -- updated image bundle information.
            ( type : ImageBundle ( class ) )
         imageNameList -- names of the images

      Raises:
         Assertion Error -- if imagebundle is not ImageBundle type
         CvpError -- If image bundle name is invalid

      Returns None
      '''
      currImageBundle = self.cvpService.getImageBundleByName( imageBundle.name )
      imageBundleKey = currImageBundle[ 'id' ]
      imageInfoList = []
      for imageName in imageNameList:
         imageData = self.addImage( str( imageName ) )
         imageInfoList.append( imageData )
      self.cvpService.updateImageBundle( imageBundle.name, imageBundle.certified,
            imageInfoList, imageBundleKey )

   def addImageBundle( self, imageBundle, imageNameList ):
      ''' Add an image bundle with an image.

      Arguments:
         imageBundle -- image bundle inforamtion object ( type: ImageBundle
         (class ) ) imageNameList -- name of the images in image bundle ( type
         : List od string )

      Raises:
         CvpError -- If image bundle with same name already exists
         Assertion Error -- If imageBundle is not of type ImageBundle

      Returns None
      '''
      assert isinstance( imageBundle, ImageBundle )
      imageInfoList = []
      for imageName in imageNameList:
         imageData = self.addImage( str( imageName ) )
         imageInfoList.append( imageData )
      self.cvpService.saveImageBundle( imageBundle.name, imageBundle.certified,
            imageInfoList )

   def addImage( self, imageName ):
      '''Check if image is already present in CVP instance or not.
      If not then add the image to the CVP in instance.

      Arguments:
         imageName -- name of the image

      Returns:
         imageData -- information of the added image
      '''
      imageAddFlag = False
      images = self.cvpService.getImagesInfo()
      for image in images:
         if image[ 'name' ] == imageName:
            imageAddFlag = True
            break
      if imageAddFlag == False:
         imageInfo = self.cvpService.addImage( imageName )
         imageData = { 'name' : os.path.basename( imageName ),
               'imageSize' : imageInfo[ 'imageSize' ],
               'imageId' : imageInfo[ 'imageId' ],
               'md5' : imageInfo[ 'md5' ],
               'version' : imageInfo[ 'version' ],
               'key' : None }
         return imageData
      else:
         for image in images:
            if imageName == image['name']:
               imageData = { 'name' : os.path.basename( imageName ),
                     'imageSize' : image[ 'imageSize' ],
                     'imageId' : image[ 'imageId' ],
                     'md5' : image[ 'md5' ],
                     'version' : image[ 'version' ],
                     'key' : image[ 'key' ] }
         return imageData

   def mapImageBundleToDevice( self, device, imageBundleName):
      '''Map image Bundle to device

      Arguments:
         imageBundleName -- name of the image bundle ( type : String )
         device -- name of the device ( type : Device ( class ) )

      Raises:
         Assertion Error -- If device is not Device type
         CvpError -- If image bundle name is invalid

      Returns None
      '''
      assert isinstance( device, Device )
      if not imageBundleName:
         return
      imageBundleKey = ''
      imageBundles = self.cvpService.getImageBundles()
      for imageBundle in imageBundles:
         if imageBundle[ 'name' ] == imageBundleName:
            imageBundleKey = imageBundle[ 'key' ]
            break
      if imageBundleKey == '':
         raise cvpServices.CvpError( errorCodes.INVALID_IMAGE_BUNDLE_NAME )
      self.cvpService.applyImageBundleToDevice( device.key, device.fqdn,
            imageBundleName, imageBundleKey )

   def mapImageBundleToContainer( self, container, imageBundleName ):
      '''Map imageBundle to container

      Arguments:
         container -- name of the container ( type : Container ( class ) )
         imageBundleName -- name of the image bundle ( type : String )

      Raises:
         Assertion Error -- If container is not Container type
         CvpError -- If container name ( name ) is invalid
         CvpError -- If image bundle name is invalid

      Returns None
      '''
      assert isinstance( container, Container )
      if not imageBundleName:
         return 'No image bundle name provided'
      imageBundleKey = ''
      containerInfo = self._getContainerInfo( container.name )
      containerKey = containerInfo[ 'key' ]
      imageBundles = self.cvpService.getImageBundles()
      for imageBundle in imageBundles:
         if imageBundle[ 'name' ] == imageBundleName:
            imageBundleKey = imageBundle[ 'key' ]
            break
      if imageBundleKey == '':
         raise cvpServices.CvpError( errorCodes.INVALID_IMAGE_BUNDLE_NAME )
      self.cvpService.applyImageBundleToContainer( container.name, containerKey,
            imageBundleName, imageBundleKey )

   def _getConfigKeys( self, configNameList ):
      '''Returns keys for corresponding configlet names in the
      configNameList

      Arguments:
         configNameList -- List of configlet names to be applied
               ( type : List of String )

      Raises:
         CvpError -- If the configlet names are invalid

      Returns:
         configKeyList -- List of the configlet keys ( type : List of Strings ) )
      '''
      configKeyList = []
      configNum = len( configNameList )
      configlets = self.cvpService.getConfigletsInfo()
      for config in configlets:
         if config[ 'name' ] in configNameList:
            configNum -= 1
            configKeyList.append( config[ 'key' ] )
      if configNum > 0:
         raise cvpServices.CvpError( errorCodes.INVALID_CONFIGLET_NAME )
      return configKeyList

   def mapConfigToContainer( self, container , configNameList ):
      '''Map the configlets to container

      Arguments:
         container -- container to be added ( type : Container( class ) )
         configNameList -- List of configlet name to be applied
               ( type : List of string )
      Raises:
         Assertion Error -- If container is not Container type
         CvpError -- If the configlet names are invalid
         CvpError -- If container name ( name ) is invalid

      Returns None
      '''
      assert isinstance( container, Container )
      if not configNameList:
         return 'No configlets to map'
      configKeyList = self._getConfigKeys( configNameList )
      containerInfo = self._getContainerInfo( container.name )
      containerKey = containerInfo[ 'key' ]
      self.cvpService.applyConfigToContainer( container.name, containerKey,
            configNameList, configKeyList )

   def removeConfigFromContainer( self, container, configList ):
      '''remove configlet mapped to containers

      Arguments:
         container -- container to be added ( type : Container( class ) )
         configList -- List of configlet to be applied
               ( type : List of Configlet( class ) )
      Raises:
         Assertion Error -- If container is not Container type
         CvpError -- If the configlet names are invalid
         CvpError -- If container name ( name ) is invalid

      Returns None
      '''
      assert isinstance( container, Container )
      if not configList:
         return 'No configlets to map'
      configKeyList = self._getConfigKeys( configList )
      containerInfo = self._getContainerInfo( container.name )
      containerKey = containerInfo[ 'key' ]
      self.cvpService.removeConfigFromContainer( container.name, containerKey,
            configList, configKeyList )

   def addContainer( self, container ):
      '''Add container to the inventory

      Arguments:
         container -- container to be added ( type : Container( class ) )

      Raises:
         Assertion Error -- If container is not Container type
         CvpError -- If container parent name ( parentName ) is invalid
         CvpError -- If container name ( name ) is invalid
         CvpError -- If container already exists.

      Returns None
      '''
      assert isinstance( container, Container )
      parentContainerName = container.parentName
      parentContainerInfo = self._getContainerInfo( parentContainerName )
      parentContainerId = parentContainerInfo[ 'key' ]
      self.cvpService.addContainer( container.name,
            container.parentName, parentContainerId )

   def addDevice( self, device, loginCredentials = None ):
      '''Add the device in proper container in Cvp Inventory

      Arguments:
         device -- devices to be added to inventory ( type : Device( class ) )
         loginCredentials -- credentials for device login ( optional )
            ( type : Dict ( Key - username, value - password )
      Raises:
         Assertion Error -- If device is not Device type
         CvpError -- If device status is login after connection attempt
         CvpError -- If device stauts is failed after connection attempt
      Returns None
      '''
      assert isinstance( device, Device )
      if loginCredentials:
         status = self._getDeviceStatus( device )
         if status:
            if status[ 'status' ] == 'Login':
               self._retryAddDevice( device, loginCredentials )
         else:
            self._addDevice( device, loginCredentials )
            status = self._getDeviceStatus( device )
            if status:
               if status[ 'status' ] == 'Login':
                  self._retryAddDevice( device, loginCredentials )
      else:
         self._addDevice( device, loginCredentials )
      self.cvpService.saveInventory()

   def _addDevice( self, device, loginCredentials ):
      '''Add device internal function. This method checks the status of the
      first attempt of device addition. If status is duplicate it deletes the
      recently added device. If status is login it raises exception of unauthorised
      user. If status is failure then it raises exception of connection failure
      '''

      parentContainerName = device.containerName
      if parentContainerName == 'Undefined':
         parentContainerId = 'undefined_container'
      else:
         parentContainerInfo = self._getContainerInfo( parentContainerName )
         parentContainerId = parentContainerInfo[ 'key' ]
      status = self._getDeviceStatus( device )
      if not status:
         self.cvpService.addToInventory( device.ipAddress, parentContainerName,
               parentContainerId )
         status = self._getDeviceStatus( device )
         while status[ 'status' ] == 'Connecting':
            status = self._getDeviceStatus( device )
      self.cvpService.saveInventory()
      if status[ 'status' ] == 'Duplicate' :
         self.cvpService.deleteDuplicateDevice( status[ 'key' ] )
      elif status[ 'status' ] == 'Connected' :
         self.cvpService.saveInventory()
      elif ( status[ 'status' ] == 'Login' and
            status[ 'statusMessage' ] == 'Unauthorized User' ):
         if not loginCredentials:
            raise cvpServices.CvpError( errorCodes.DEVICE_LOGIN_UNAUTHORISED )
      else:
         raise cvpServices.CvpError( errorCodes.DEVICE_CONNECTION_ATTEMPT_FAILURE )

   def addDevices( self, deviceList ):
      '''Adding devices to the inventory in pipeline manner

      Argument:
         deviceList -- List of devices to be added to inventory
               ( type : List of Device objects )

      Raises:
         Assertion Error -- If device objects are not of type Device
         CvpError -- If parent container name is invalid

      Returns:
         connectedDeviceList -- List of device successfully connected
               ( type : List of Device( class ) )
         unauthorisedDeviceList -- List of devices for whom user doen't have
               authentication ( type : List of Device( class ) )
         connFailureDeviceList --  Failure to connect device list
               ( type : List of Device( class ) )
      '''
      connectedDeviceList = []
      unauthorisedDeviceList = []
      connFailureDeviceList = []
      for device in deviceList:
         assert isinstance( device, Device )
         parentContainerName = device.containerName
         if parentContainerName == 'Undefined':
            parentContainerId = 'undefined_container'
         else:
            parentContainerInfo = self._getContainerInfo( parentContainerName )
            parentContainerId = parentContainerInfo[ 'key' ]
         status = self._getDeviceStatus( device )
         if not status:
            self.cvpService.addToInventory( device.ipAddress, parentContainerName,
                  parentContainerId )

      for device in deviceList:
         status = self._getDeviceStatus( device )
         while status[ 'status' ] == 'Connecting' :
            status = self._getDeviceStatus( device )
         if status[ 'status' ] == 'Connected':
            connectedDeviceList.append( device )
         elif status[ 'status' ] == 'Login':
            unauthorisedDeviceList.append( device )
         elif status[ 'status' ] == 'Duplicate':
            connectedDeviceList.append( device )
            self.cvpService.deleteDuplicateDevice( status[ 'key' ] )
         else:
            connFailureDeviceList.append( device )
      self.cvpService.saveInventory()
      return ( connectedDeviceList, unauthorisedDeviceList, connFailureDeviceList )

   def _getDeviceStatus( self, device ):
      '''Retrieve the device status from the Cvp instance

      Arguments:
         device -- device information object ( type : Device( class ) )

      Raises:
         Assertion Error -- If device is not of type Device

      Returns:
         deviceInfo -- Information about the device.( type : Dict )
      '''
      assert isinstance( device, Device )
      _, connFailureDevices = self.cvpService.retrieveInventory()
      for deviceInfo in connFailureDevices:
         if ( deviceInfo[ 'fqdn' ] == device.fqdn.split('.')[ 0 ] or
               deviceInfo[ 'ipAddress' ] == device.ipAddress ):
            return deviceInfo

   def _retryAddDevice( self, device, loginCredentials ):
      '''Retry addition of new devices to containers in Cvp Inventory. Devices
      for whom first attempt of addtion was failure due to unauthorised users.

      Arguments:
         device -- device information object ( type : Device( class ) )
         loginCredentials -- login credentials for the device ( type : Dict }

      Raises:
         Assertion Error -- If device is not of type Device
         CvpError -- If device status is still login after using the login
         credentials

      Returns None
      '''
      assert isinstance( device, Device )
      _, connFailureDevices = self.cvpService.retrieveInventory()
      for deviceInfo in connFailureDevices:
         if ( deviceInfo[ 'fqdn' ] == device.fqdn.split('.')[ 0 ] or
               deviceInfo[ 'ipAddress' ] == device.ipAddress ):
            deviceKey = deviceInfo[ 'key' ]
            break

      for username in loginCredentials:
         self.cvpService.retryAddToInventory( deviceKey,
               device.ipAddress, username, loginCredentials[ username ] )
         status = self._getDeviceStatus( device )
         while status[ 'status' ] == 'Connecting':
            status = self._getDeviceStatus( device )
         if status[ 'status' ] == 'Connected':
            break
      if status[ 'status' ] == 'Login':
         raise cvpServices.CvpError( errorCodes.DEVICE_INVALID_LOGIN_CREDENTIALS )

   def mapConfigToDevice( self, device , configList ):
      '''applying configs mentioned in configList to the device.

      Arguments:
         device -- device information object ( type : Device( class ) )
         configList -- List of configlets to be applied
         ( type : List of Strings )

      Returns None

      Raises:
         Assertion Error -- If device is not of type Device
         CvpError -- If device information is incorrect
         CvpError -- If configList contains invalid configlet name
      '''
      self.cvpService.saveInventory()
      if not configList :
         return 'No configlet in configlet List'
      configKeyList = self._getConfigKeys( configList )
      assert isinstance( device, Device )
      self.cvpService.applyConfigToDevice( device.ipAddress,
            device.fqdn, device.key, configList, configKeyList )

   def executeAllPendingTask( self ):
      '''Executes all the pending tasks.

      Arguments None

      Returns None
      '''
      tasks = self.cvpService.getTasks()
      for task in tasks:
         if task['workOrderUserDefinedStatus'] == 'Pending':
            self.executeTask( task[ 'workOrderId' ] )

   def executeTask( self, taskId ):
      '''Executes task having id taskId.

      Arguments:
         taskId -- Work order Id of the task ( type : int )

      Returns None

      Raises:
         CvpError -- if task Id is invalid
      '''
      taskNum = int( taskId )
      self.cvpService.executeTask( taskNum )

   def getPendingTasksInfo( self ):
      '''Finds all the pending tasks from the Cvp instance

      Arguments: None

      Returns:
         taskList -- List of Task objects, each object providing
         information about a pending task ( type : List of Task objects )
      '''
      taskList = []
      tasks = self.cvpService.getTasks()
      for task in tasks:
         if task['workOrderUserDefinedStatus'] == 'Pending':
            taskList.append( Task( str( task['workOrderId'] ),
               task['description'] ) )
      return taskList

   def monitorTaskStatus( self, taskIdList ):
      '''Get information about the tasks whose Id is present in taskIdList

      Argument:
         taskId -- Id of the task

      Returns:
         taskStatus -- Current status of the task
      '''
      tasks = self.cvpService.getTasks()
      while len( taskIdList ) > 0 :
         for task in tasks:
            if task[ 'workOrderId' ] in taskIdList:
               if ( task['workOrderUserDefinedStatus'] == 'Completed' or
                     task['workOrderUserDefinedStatus'] == 'Failed' ):
                  taskIdList.remove( str ( task[ 'workOrderId' ] ) )
                  break
         tasks = self.cvpService.getTasks()

   def getImageBundles( self ):
      '''Retrieves information on all the image bundles.Image bundle information
      consist of images information, image bundle key and name, devices and
      containers to which the image bunudle is mapped to.

      Arguments: None

      Returns:
         imageBundleList -- List of ImageBundle object, each object providing
         information about an image bundle ( type: List of ImageBundle objects )
      '''
      imageBundles = self.cvpService.getImageBundles()
      imageBundleList = []
      for bundle in imageBundles:
         containerList, deviceList = self._getImageBundleMap( bundle[ 'name' ] )
         imageBundleList.append( ImageBundle( bundle[ 'name' ], bundle[ 'key' ],
            bundle['imageIds'], bundle[ 'isCertifiedImageBundle' ] ,
            containerList, deviceList ) )
      return imageBundleList

   def getImageBundle( self, imageBundleName ):
      '''Retrieves image bundle from Cvp instance. Image bundle information
      consist of images information, image bundle key and name, devices and
      containers to which the image bunudle is mapped to.

      Arguments:
         imageBundleName -- name of image bundle ( type : String )

      Returns:
         ImageBundle -- ImageBundle object contains all required image bundle
         information ( type : ImageBundle( class ) )
      '''
      bundle = self.cvpService.getImageBundleByName( imageBundleName )
      imageKeyList = []
      for image in bundle[ 'images' ]:
         imageKeyList.append( image[ 'key' ] )
      containerList, deviceList = self._getImageBundleMap( bundle[ 'name' ] )
      return ImageBundle( bundle[ 'name' ], bundle[ 'id' ],
         imageKeyList, bundle[ 'isCertifiedImage' ], containerList,
         deviceList )

   def deleteImageBundle( self, imageBundle ):
      '''Deletes image bundle from cvp instance

      Arguments:
         imageBundle -- image bundle to be deleted ( type : ImageBundle( class ) )

      Raises:
         Assertion Error -- If imagebundle is not ImageBundle type
         CvpError -- If image bundle key is invalid
         CvpError -- If image bundle is applied to any entity

      Returns None
      '''
      assert isinstance( imageBundle, ImageBundle )
      self.cvpService.deleteImageBundle( imageBundle.key, imageBundle.name )

   def deviceComplainceCheck( self, deviceIpAddress ):
      '''Run compliance check on the device

      Argument:
         deviceIpAddress -- Ip address of the device.

      Returns:
         complianceCheck -- Boolean flag indicating successful or un-successful
                            compliance check

      Raises:
         CvpError -- If device mac address ( deviceMacAddress ) is invalid
      '''
      device = self.getDevice( deviceIpAddress )
      configIdList = self._getConfigKeys( device.configlets )
      complianceReport = self.cvpService.deviceComplianceCheck( configIdList,
            device.key )
      if complianceReport[ 'complianceIndication' ] != 'NONE' :
         complianceCheck = False
      else:
         complianceCheck = True
      return complianceCheck

   def renameContainer( self, oldContainerName, newContainerName ):
      ''' Renames the container to desired new name

      Arguments:
         oldContainerName -- Current name of the container
         newContainerName -- New desired name of the container

      Returns: None

      Raises:
         CvpError -- If the oldContainerName is invalid
      '''
      containerKey = self._getContainerInfo( oldContainerName )[ 'key' ]
      self.cvpService.changeContainerName( oldContainerName, newContainerName,
            containerKey )

   def getRootContainerInfo( self ):
      ''' Returns information about the root container
      Arguemtns: None

      Raises: None

      Returns:
         container -- Container object containing information about root container
      '''
      container, _ = self.cvpService.retrieveInventory()
      return self.getContainer( container[ 'name' ] )

   def deleteContainer( self, container ):
      '''delete the container from the Cvp inventory

      Argument:
         container -- container to be deleted. ( type : Container(class) )

      Raises:
         Assertion Error -- If container is not Container type
         CvpError -- If parent container name ( parentName )is invalid
         CvpError -- If container name ( name ) is invalid

      Returns None
      '''
      assert isinstance( container, Container )
      containerKey = ''
      parentKey = ''
      containerInfo = self._getContainerInfo( container.name )
      containerKey = containerInfo[ 'key' ]
      parentInfo = self._getContainerInfo( container.parentName )
      parentKey = parentInfo[ 'key' ]
      self.cvpService.deleteContainer( container.name, containerKey,
            container.parentName, parentKey )

   def deleteDevice( self, device ):
      '''Delete the device from the Cvp inventory.

      Arguments:
         device -- device to be deleted.( type : Device(class) )

      Raises:
         Assertion Error -- If device is not Device type
         CvpError -- If parent container name ( containerName ) is invalid

      Returns: None
      '''
      assert isinstance( device, Device )
      if device.containerName == 'Undefined':
         containerKey = 'undefined_container'
      else:
         containerInfo = self._getContainerInfo( device.containerName )
         containerKey = containerInfo[ 'key' ]
      self.cvpService.deleteDevice( device.key, device.containerName, containerKey )

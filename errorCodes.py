# Copyright (c) 2015 Arista Networks, Inc.  All rights reserved.
# Arista Networks, Inc. Confidential and Proprietary.
'''
@Copyright: 2015 Arista Networks, Inc.
Arista Networks, Inc. Confidential and Proprietary.

Error codes for the Cvp tool
'''

NO_ERROR_CODE = 0
UNKNOWN_ERROR_CODE = 1
UNKNOWN_REQUEST_RESPONSE = 2
INVALID_LOGIN_CREDENTIALS = 100
USER_UNAUTHORISED = 101
CONFIGLET_ALREADY_EXIST = 1001
INVALID_CONFIGLET_NAME = 1002
CONFIG_CVP_RUNTIME_EXCEPTION = 1003
CONFIG_DATABASE_ACCESS_FAILURE = 1004
CONFIG_UPDATE_FAILURE = 1005
IMAGE_BUNDLE_CVP_RUNTIME_EXCEPTION = 2000
IMAGE_BUNDLE_ALREADY_EXIST = 2001
INVALID_IMAGE_BUNDLE_NAME = 2002
CANNOT_DELETE_IMAGE_BUNDLE = 2003
DATABASE_ACCESS_FAILURE = 2004
IMAGE_BUNDLE_DATABASE_CONNECTION_FAILURE = 2005
CONTAINER_ALREADY_EXIST = 3001
INVALID_CONTAINER_NAME = 3002
DEVICE_ALREADY_EXISTS = 4001
DEVICE_LOGIN_UNAUTHORISED = 4002
DEVICE_INVALID_LOGIN_CREDENTIALS = 4003
DEVICE_CONNECTION_ATTEMPT_FAILURE = 4005
INVALID_IMAGE_NAME = 5001
INVALID_TASK_ID = 6001
ENTITY_ALREADY_EXISTS = 7001
JSON_STRING_AS_BEAN_CLASS = 7002

ERROR_MAPPING = { NO_ERROR_CODE : "No error code provided",
      UNKNOWN_ERROR_CODE: "Unknown error code",
      UNKNOWN_REQUEST_RESPONSE : " Request response is not Json" ,
      INVALID_LOGIN_CREDENTIALS : " Incorrect Cvp login credentials",

      CONFIGLET_ALREADY_EXIST: "Configlet already exists ",
      INVALID_CONFIGLET_NAME: "Invalid Configlet name",
      CONFIG_CVP_RUNTIME_EXCEPTION : "Runtime exception in configlet management",
      CONFIG_DATABASE_ACCESS_FAILURE : "Configlet info access from Database failure",
      CONFIG_UPDATE_FAILURE : "Configlet update failure",

      IMAGE_BUNDLE_CVP_RUNTIME_EXCEPTION : " Runtime exception in image bundle "
      "management ",
      IMAGE_BUNDLE_ALREADY_EXIST: "Image bundle already exists",
      INVALID_IMAGE_BUNDLE_NAME: "Invalid Image Bundle name",
      CANNOT_DELETE_IMAGE_BUNDLE: "Cannot delete image bundle,currently applied to"
      " one or more entity ",
      DATABASE_ACCESS_FAILURE : "Information access from Database failure",
      IMAGE_BUNDLE_DATABASE_CONNECTION_FAILURE : "Database connection failure in"
      " image bundle management",

      CONTAINER_ALREADY_EXIST: "Container already exists",
      INVALID_CONTAINER_NAME: "Invalid container name",
      DEVICE_ALREADY_EXISTS: "Device already exists",
      DEVICE_LOGIN_UNAUTHORISED: "User unauthorised to login into the device",
      DEVICE_INVALID_LOGIN_CREDENTIALS: "Incorrect device login credentials",
      DEVICE_CONNECTION_ATTEMPT_FAILURE : "Failure to setup connection with device",

      INVALID_IMAGE_NAME : "Invalid Image Name",
      INVALID_TASK_ID : " Invalid Task Id",
      ENTITY_ALREADY_EXISTS : "Entity already exists in the inventory",
      JSON_STRING_AS_BEAN_CLASS : "Invalid data structure of input" }



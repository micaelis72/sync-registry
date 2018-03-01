#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib2
import json
import subprocess

class Docker:

  def __init__(self,remoteURL,localURL,imageName):
  	self.FNULL = open(os.devnull, 'w')
  	self.remoteURL = remoteURL
  	self.localURL = localURL
  	self.imageName = imageName

  def setCurrentTag(self,tagNumber):
    self.tagNumber = tagNumber

  def fetchImage(self):
    errcode = subprocess.call(["docker","pull",(self.remoteURL + "/" + self.imageName +':' + self.tagNumber)], stdout=self.FNULL, stderr=subprocess.STDOUT)
    return errcode

  def setTagImage(self):
    errcode=subprocess.call(["docker","tag",self.remoteURL + "/" + self.imageName +':' + self.tagNumber, self.localURL + "/" +  self.imageName + ":" + self.tagNumber], stdout=self.FNULL, stderr=subprocess.STDOUT)
    return errcode

  def uploadImage(self):
    errcode = subprocess.call(["docker","push", self.localURL + "/" + self.imageName + ":" + self.tagNumber], stdout=self.FNULL, stderr=subprocess.STDOUT)
    return errcode
  
  def removeRemoteImage(self,imageNameandTagNumber):
  	errcode = subprocess.call(["docker","rmi","-f",(self.remoteURL + "/" + imageNameandTagNumber)], stdout=self.FNULL, stderr=subprocess.STDOUT)
  	return errcode

  def removeLocalImage(self,imageNameandTagNumber):
  	errcode = subprocess.call(["docker","rmi","-f",(self.localURL + "/" + imageNameandTagNumber)], stdout=self.FNULL, stderr=subprocess.STDOUT)
  	return errcode	

  def getTags(self, URL, version):
    try:
      if(version == 1):
        url = 'https://' + URL + '/v1/repositories/' + self.imageName + '/tags'
        return json.load(urllib2.urlopen(url))
      elif(version == 2):
        url =  'https://' + URL + '/v2/' + self.imageName + '/tags/list'
        return json.load(urllib2.urlopen(url))
    except urllib2.HTTPError, e:
      return e.code 

  def imageExists(self, tagNumber):
  	url = self.localURL
  	result = self.getTags(url, 2)
  	if (type(result) is not int):
  		for tagLocal in (self.getTags(url, 2))['tags']:
  			if ((tagNumber == tagLocal) and (tagNumber != 'latest')):
  				return True
  	return False

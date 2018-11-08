#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import requests
import subprocess

class Docker:

  def __init__(self,remoteURL,localURL,imageName):
  	self.FNULL = open(os.devnull, 'w')
  	self.remoteURL = remoteURL
  	self.localURL = localURL
  	self.imageName = imageName
        requests.packages.urllib3.disable_warnings()

  def setTag(self,tagNumber):
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

  def getTags(self, URL):
    try:
      url = 'https://' + URL + '/v2/' + self.imageName + '/tags/list'
      r = requests.get(url, allow_redirects=True)
      return r.json()
    except requests.exceptions.RequestException as e:
      return e

  def imageExists(self, tagNumber):
  	url = self.localURL
  	result = self.getTags(url)
        for tagLocal in (self.getTags(url))['tags']:
  	   if ((tagNumber == tagLocal) and (tagNumber != 'latest')):
  	      return True
  	return False

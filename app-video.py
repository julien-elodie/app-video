#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import os

dir = 'videos/'
if not os.path.exists(dir):
    os.mkdir(dir)

headers = {
    'cache-control': "no-cache",
    'postman-token': "bcb916fd-f10f-93fb-ae50-62ebad93f2b3"
}


class Appvideodownload(object):
    """docstring for Appvideodownload."""

    def __init__(self):
        super(Appvideodownload, self).__init__()
        self.page = 0
        self.itemNumber = 0
        self.innerItemNumber = 0
        self.totalNumber = 0
        self.json = []
        self.videos = {}

    def getBasicInformations(self, url, querystring):
        while True:
            querystring['page'] = str(self.page)
            res = requests.request(
                "GET", url, headers=headers, params=querystring)
            Json = json.loads(res.text)
            if Json['content']:
                self.itemNumber = 0
                while self.itemNumber < len(Json['content']):
                    self.json = Json['content'][self.itemNumber]
                    Id = Json['content'][self.itemNumber]['id']
                    Href = Json['content'][self.itemNumber]['videoHref']
                    self.itemNumber += 1
                    self.totalNumber += 1
                    self.videos[Id] = Href
                    print self.totalNumber
                self.page += 1
            else:
                break

    def getAdvancedInformations(self, url):
        while True:
            querystring = {"page": str(self.page), "size": "5"}
            res = requests.request(
                "GET", url, headers=headers, params=querystring)
            Json = json.loads(res.text)
            if Json['content']:
                self.itemNumber = 0
                while self.itemNumber < len(Json['content']):
                    basicJson = Json['content'][self.itemNumber]
                    self.innerItemNumber = 0
                    while self.innerItemNumber < len(basicJson['tvlist']):
                        self.json = basicJson['tvlist'][self.innerItemNumber]
                        Id = basicJson['tvlist'][self.innerItemNumber]['id']
                        url_inner = 'http://api.lvshiv.com/lvshiv/travelVideos/' + \
                            str(Id)
                        res = requests.get(url_inner)
                        Href = 'http://lvshiv.oss-cn-hangzhou.aliyuncs.com/' + \
                            json.loads(res.text)['videoId']
                        self.innerItemNumber += 1
                        self.totalNumber += 1
                        self.videos[Id] = Href
                    self.itemNumber += 1
                    # print self.totalNumber
                self.page += 1
            else:
                break

    def videoDownload(self):
        for video in self.videos.keys():
            filename = str(video) + '.mp4'
            url = self.videos[video]
            print filename + u'开始下载'
            res = requests.get(url)
            with open(dir + filename, 'wb') as code:
                code.write(res.content)
            print filename + u'下载完成'

    def simpleDownload(self):
        url = "http://api.lvshiv.com/lvshiv/travelVideos/hotVideos"
        querystring = {"page": '', "size": "20"}
        self.getBasicInformations(url, querystring)
        self.page = 0
        url = "http://api.lvshiv.com/lvshiv/travelJxVideos"
        querystring = {"isShow": "false", "page": '',
                       "req_type": "formal", "size": "10"}
        url = "http://api.lvshiv.com/lvshiv/subjectVideos/index"
        self.getBasicInformations(url, querystring)
        self.page = 0
        self.getAdvancedInformations(url)
        self.videoDownload()


app = Appvideodownload()
app.simpleDownload()

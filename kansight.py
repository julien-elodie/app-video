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
    'postman-token': "61fed78c-93e1-81da-a37d-194965d6adb7"
}


class Kansight(object):

    """docstring for Kansight."""

    def __init__(self):
        super(Kansight, self).__init__()
        self.ColumnID = []
        self.ColumnName = []
        self.VideoID = []
        self.VideoName = []
        self.videoHref = []

    def getIndexColumn(self):
        url = 'http://www.kansight.com/index.php/apis/android/ver1/v1_a_21/Index/indexColumn'
        res = requests.get(url, headers=headers)
        Json = json.loads(res.text)
        for item in Json['data']['result']:
            self.ColumnID.append(item['id'])
            self.ColumnName.append(item['cname'].replace(' ', ''))

    def getColumn(self):
        url = 'http://www.kansight.com/index.php/apis/android/ver1/v1_a_21/Column/getColumn'
        for id in self.ColumnID:
            for page in range(1, 100):
                postData = {
                    'page': page,
                    'id': id
                }
                res = requests.post(url, headers=headers, data=postData)
                Json = json.loads(res.text)
                if Json['data']['reason'] == 1001:
                    for item in Json['data']['result']['data']:
                        self.VideoID.append(item['id'])
                        self.VideoName.append(item['title'])
                else:
                    break

    def getVideo(self):
        url = 'http://www.kansight.com/index.php/apis/android/ver1/v1_a_21/Videos/getOfficialVideo'
        for vid in self.VideoID:
            postData = {
                'vid': vid
            }
            res = requests.post(url, headers=headers, data=postData)
            Json = json.loads(res.text)
            self.videoHref.append(Json['data']['result']['data']['video_url'])
            print Json['data']['result']['data']['video_url']

    def downloadVideo(self, dir):
        for i in range(len(self.VideoName)):
            if not self.videoHref[i] == None:
                filename = self.VideoName[i1] + '.mp4'
                url = self.videoHref[i]
                print filename + u'开始下载'
                res = requests.get(url)
                with open(dir + filename, 'wb') as code:
                    code.write(res.content)
                print filename + u'下载完成'

    def simpleDownload(self):
        self.getIndexColumn()
        self.getColumn()
        self.getVideo()
        # self.downloadVideo(dir)

kansight = Kansight()
kansight.simpleDownload()

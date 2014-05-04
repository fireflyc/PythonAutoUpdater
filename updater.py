#coding=utf-8
__author__ = 'fireflyc'

import urllib2
import json
import os


class Updater:
    def __init__(self, check_updater_url, cur_version="1.0.0"):
        self.remote_file_list = []
        self.check_updater_url = check_updater_url
        self.cur_version = cur_version

    def check(self):
        update_json = urllib2.urlopen(self.check_updater_url, "cur_version=%s" % self.cur_version).read()
        update_result = json.loads(update_json)
        #verify success is True
        if (not "success" in update_result) or (not update_result["success"]):
            return False

        #verify "update file list" is exist
        if not "data" in update_result:
            return False

        for remote_file in update_result["data"]:
            self.remote_file_list.append(RemoteFile(remote_file))
        return self.remote_file_list

    def update(self, download_path, next_file_progress, notify_progress, chunk_size=1024 * 1024):
        download_files = []
        for remote_file in self.remote_file_list:
            next_file_progress(remote_file)
            remote_file.download(download_path, notify_progress, chunk_size)
            download_files.append(os.path.join(download_path, remote_file.name()))
        return download_files


class RemoteFile:
    def __init__(self, url):
        self.url = url
        self.download_file = self.url.split("/")[-1]

    def path(self):
        return self.url

    def name(self):
        return self.download_file

    def __str__(self):
        return self.path()

    def __unicode__(self):
        return self.path()

    def download(self, download_path, notify_progress, chunk_size):
        http_response = urllib2.urlopen(self.url)
        total_size = http_response.info().getheader("Content-Length").strip()
        if not total_size:
            total_size = 0
        total_size = int(total_size)
        read_size = 0

        download_file = open(os.path.join(download_path, self.download_file), "wb")
        try:
            chunk = True
            while chunk:
                chunk = http_response.read(chunk_size)
                read_size += len(chunk)
                download_file.write(chunk)
                if total_size <= read_size:
                    break
                if notify_progress:
                    notify_progress(read_size, total_size)
        finally:
            download_file.close()



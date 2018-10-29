import vk_api
import datetime
import os
import time
import json
import urllib.request


def get_vk_api():
    file_descriptor = open("json.auth", "r")
    auth = json.load(file_descriptor)
    vk_session = vk_api.VkApi(auth["login"], auth["password"]);
    vk_session.auth(token_only=True)
    vk = vk_session.get_api()
    return vk


def get_targets():
    file_descriptor = open("targets.json", "r")
    targets = json.load(file_descriptor)
    return targets["id"]

def dowload_all_photos(vk,target):
    offset=0;
    while True:
        response = vk.photos.getAll(owner_id=target, offset=offset, count=200, skip_hidden=0)
        for photo in response["items"]:
            url = photo["sizes"][len(photo["sizes"])-1]["url"]
            print("dowloading: " + str(url))
            urllib.request.urlretrieve(url, str(photo["id"])+".jpg")
        if response["count"]!=200 :
            break;
        offset += 200

def dowload_all_user_photos(vk,target):
    offset=0;
    while True:
        response = vk.photos.getUserPhotos(user_id=target, offset=offset, count=200, skip_hidden=0)
        for photo in response["items"]:
            url = photo["sizes"][len(photo["sizes"])-1]["url"]
            print("dowloading: " + str(url))
            urllib.request.urlretrieve(url, str(photo["id"])+".jpg")
        if response["count"]!=200 :
            break;
        offset += 200


vk=get_vk_api()
targets=get_targets()
for target in targets:
    try:
        os.mkdir(str(target))
    except FileExistsError:
        print ("already exist")
    os.chdir(str(target))
    dowload_all_photos(vk, target)
    dowload_all_user_photos(vk, target)
    os.chdir("..")


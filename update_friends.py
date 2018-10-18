import vk_api
import datetime
import os
import time
import json

timeFormatBase = '%Y-%m-%d-%H-%M-%S'
timeFormatFriends = timeFormatBase + '.txt'
timeFormatFriendsFull = timeFormatBase + '_Full.txt'
timeFormatFollowers = timeFormatBase + '_followers.txt'

targetUserId = 0

def get_vk_api():
	fd = open("json.auth", "r")
	auth = json.load(fd)
	vk_session = vk_api.VkApi(auth["login"], auth["password"]);
	vk_session.auth(token_only=True)
	vk = vk_session.get_api()
	return vk


def get_targets():
	fd = open("targets.json", "r")
	targets = json.load(fd)
	return targets["id"]

vk = get_vk_api()
targetUserId = get_targets()[0];


friends_ids = vk.friends.get(user_id=targetUserId)


def update_data(vk,tragetUserId):
	friends_ids = vk.friends.get(user_id=targetUserId)
	ts = time.time();
	st = datetime.datetime.fromtimestamp(ts).strftime(timeFormatFriends)
	file = open(st, 'w+')
	file.write(json.dumps(friends_ids))

	friends = vk.friends.get(user_id=targetUserId, fields='name')
	ts = time.time();
	st = datetime.datetime.fromtimestamp(ts).strftime(timeFormatFriendsFull)
	file = open(st, 'w+')
	file.write(json.dumps(friends))

	followers = vk.users.getFollowers(user_id=targetUserId, fields='name')
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime(timeFormatFollowers)
	file = open(st, 'w+')
	file.write(json.dumps(followers))
	return friends_ids

def print_diff ( set1, set2):
        print ("deleted")
        print(set1 - set2)
        print ("added")
        print (set2 - set1)


dir = os.listdir("./")
times = []
filenames= []
for filename in dir:
    flag = False
    try:
        filenameParsed = datetime.datetime.strptime(str(filename), timeFormatFriends)
    except:
        flag = True
    if not flag:
        times.append(filenameParsed)
        filenames.append(filename)

times.sort()
for i in range(len(times)):

    filename = times[i].strftime(timeFormatFriends)
    fd=open(filename,"r")

    data = json.load(fd)
    fd.close()

    if (i+1 == len(times)):
    	print_diff( set(data["items"]) , set(friends_ids["items"]))
    else:
        filename2 = times[i+1].strftime(timeFormatFriends)
        fd = open (filename2,"r")
        data2 = json.load(fd)
        fd.close()
        print (filename2)
        print_diff ( set(data["items"]), set(data2["items"]))
    print ("")


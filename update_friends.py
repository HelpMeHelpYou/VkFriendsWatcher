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


vk = get_vk_api()
targetUserId = get_targets()[0];

friends_ids = vk.friends.get(user_id=targetUserId)


def update_data(vk_instance, traget_user_id):
    friends_ids = vk_instance.friends.get(user_id=targetUserId)
    current_time = time.time()
    file_name = datetime.datetime.fromtimestamp(current_time).strftime(timeFormatFriends)
    file_descriptor = open(file_name, 'w+')
    file_descriptor.write(json.dumps(friends_ids))
    file_descriptor.close()

    friends = vk_instance.friends.get(user_id=targetUserId, fields='name')
    file_name = datetime.datetime.fromtimestamp(current_time).strftime(timeFormatFriendsFull)
    file_descriptor = open(file_name, 'w+')
    file_descriptor.write(json.dumps(friends))
    file_descriptor.close()

    followers = vk_instance.users.getFollowers(user_id=targetUserId, fields='name')
    st = datetime.datetime.fromtimestamp(current_time).strftime(timeFormatFollowers)
    file_descriptor = open(st, 'w+')
    file_descriptor.write(json.dumps(followers))
    file_descriptor.close()
    return friends_ids


def print_diff(string, string2, set1, set2):
    if set1 != set2:
        print string
        print string2
        print ("deleted")
        print(set1 - set2)
        print ("added")
        print (set2 - set1)
        print("")


current_dir = os.listdir("./")
times = []
filenames= []
for filename in current_dir:
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
    fd = open(filename, "r")

    data = json.load(fd)
    fd.close()

    if i+1 == len(times):
        print_diff(filename, "now", set(data["items"]), set(friends_ids["items"]))
    else:
        filename2 = times[i+1].strftime(timeFormatFriends)
        fd = open(filename2, "r")
        data2 = json.load(fd)
        fd.close()
        print_diff(filename, filename2, set(data["items"]), set(data2["items"]))


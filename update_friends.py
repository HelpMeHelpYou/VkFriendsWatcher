import vk_api
import datetime
import os
import time
import json



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

def update_friend_data(vk_instance, traget_user_id,format,fields = []):
    friends_ids = vk_instance.friends.get(user_id=targetUserId, fields=fields)
    current_time = time.time()
    file_name = datetime.datetime.fromtimestamp(current_time).strftime(format)
    file_descriptor = open(file_name, 'w+')
    file_descriptor.write(json.dumps(friends_ids))
    file_descriptor.close()

def update_follower_data(vk_instance, traget_user_id, format, fields=[]):
    friends_ids = vk_instance.users.getFollowers(user_id=targetUserId, fields=fields)
    current_time = time.time()
    file_name = datetime.datetime.fromtimestamp(current_time).strftime(format)
    file_descriptor = open(file_name, 'w+')
    file_descriptor.write(json.dumps(friends_ids))
    file_descriptor.close()




def print_diff(vk, string, string2, set1, set2):
    if set1 != set2:
        print (string)
        print (string2)
        print ("deleted")
        diff1 = set1 - set2
        print(diff1)
        print(list(diff1))
        if diff1:
            names=[]
            for id in list(diff1):
                name = (vk.users.get(user_ids=id))
                names.append(name)
                print(name)

        print ("added")
        diff2  = set2 - set1
        print (diff2)
        if diff2:
            names=[]
            for id in list(diff2):
                name = (vk.users.get(user_ids=id))
                names.append(name)
                print(name)
        print("")

def get_files_specified_format(format):
    current_dir = os.listdir("./")
    times = []
    for filename in current_dir:
        flag = False
        try:
            filenameParsed = datetime.datetime.strptime(str(filename), format)
        except:
            flag = True
        if not flag:
            times.append(filenameParsed)
    times.sort()
    return times

def print_history(times,format):
    for i in range(len(times)):
        filename = times[i].strftime(format)
        fd = open(filename, "r")

        data = json.load(fd)
        fd.close()

        if i+1 == len(times):
            continue
            print_diff(vk, filename, "now", set(data["items"]), set(friends_ids["items"]))
        else:
            filename2 = times[i+1].strftime(format)
            fd = open(filename2, "r")
            data2 = json.load(fd)
            fd.close()
            print_diff(vk, filename, filename2, set(data["items"]), set(data2["items"]))

timeFormatBase = '%Y-%m-%d-%H-%M-%S'
timeFormatFriends = timeFormatBase + '.txt'
timeFormatFriendsFull = timeFormatBase + '_Full.txt'
timeFormatFollowers = timeFormatBase + '_followers.txt'

targetUserId = 0

vk = get_vk_api()
targetUserId = get_targets()[0];

times = get_files_specified_format(timeFormatFriends)

print_history(times,timeFormatFriends)

friends_ids = vk.friends.get(user_id=targetUserId)
update_friend_data(vk, targetUserId, timeFormatFriends)
update_friend_data(vk, targetUserId, timeFormatFriendsFull, fields=["name"])
update_follower_data(vk, targetUserId, timeFormatFollowers, fields=[])



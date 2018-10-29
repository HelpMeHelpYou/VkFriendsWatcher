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


def get_filename_from_time(datetime,format):
    return datetime.strftime(format)


def ids_from_friends_response (response):
    result = []
    try:
        result = [d['id'] for d in response["items"]]
    except:
        result = response["items"]
    return result

def update_f_data(vk_instance,method, traget_user_id,format,current_time,fields = [],last_time=[], previous_time=[]):
    response = method(user_id=traget_user_id, fields=fields)
    to_delete = False
    last_time_file_name =[]
    if last_time and previous_time:
        try:
            last_time_file_name = get_filename_from_time(last_time, format)
            previous_time_file_name = get_filename_from_time(previous_time, format)
            fdlast = open(last_time_file_name, "r")
            data_last = json.load(fdlast)
            fdprevious = open(previous_time_file_name, "r")
            data_previous = json.load(fdprevious)
            id_last = ids_from_friends_response(data_last)
            id_priv = ids_from_friends_response(data_previous)
            id_curr = ids_from_friends_response(response=response)
            if (id_priv == id_curr) and (id_last == id_curr):
                to_delete = True
            fdlast.close()
            fdprevious.close()
        except:
            pass
    file_name = datetime.datetime.fromtimestamp(current_time).strftime(format)
    file_descriptor = open(file_name, 'w+')
    file_descriptor.write(json.dumps(response))
    file_descriptor.close()
    if to_delete:
        os.remove(last_time_file_name)


def update_friend_data(vk_instance, traget_user_id,format,current_time,fields = [],last_time=[],previous_time=[]):
    return update_f_data(vk_instance,vk_instance.friends.get,traget_user_id, format,  current_time, fields = fields,last_time=last_time,previous_time=previous_time)


def update_follower_data(vk_instance, traget_user_id, format,current_time,fields=[],last_time=[],previous_time=[]):
    return update_f_data(vk_instance,vk_instance.users.getFollowers, traget_user_id,format, current_time,fields = fields,last_time=last_time,previous_time=previous_time)


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

#print_history(times,timeFormatFriends)

current_time = time.time()
times = get_files_specified_format(timeFormatFriends)
update_friend_data(vk, targetUserId, timeFormatFriends,current_time, last_time=times[-1], previous_time=times[-2])
times = get_files_specified_format(timeFormatFriendsFull)
update_friend_data(vk, targetUserId, timeFormatFriendsFull,current_time, fields=["name"],last_time=times[-1], previous_time=times[-2])
times = get_files_specified_format(timeFormatFollowers)
update_follower_data(vk, targetUserId, timeFormatFollowers,current_time, fields=[],last_time=times[-1], previous_time=times[-2])



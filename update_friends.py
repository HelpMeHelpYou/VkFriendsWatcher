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

fd = open("json.auth", "r")
auth = json.load(fd)

vk_session = vk_api.VkApi(auth["login"], auth["password"]);
vk_session.auth(token_only=True)
vk = vk_session.get_api()

fd = open("targets.json", "r")
targets = json.load(fd)

targetUserId = targets["id"][0];

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

dir = os.listdir("./")
times = []

for filename in dir:
    flag = False
    try:
		filenameParsed = datetime.datetime.strptime(str(filename), timeFormatFriends)
    except:
        flag = True
    if not flag:
        times.append(filenameParsed)

try:
    youngest_entry = max(times)
    youngest_file = youngest_entry.strftime(timeFormatFriends)
    fd=open(youngest_file,"r")

    data = json.load(fd)

    print(set(data["items"]).union(set(friends_ids["items"])))

finally:
    exit(0)
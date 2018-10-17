import vk_api
import datetime
import os
import time
import json

timeFormatBase = '%Y-%m-%d-%H-%M-%S'
timeFormatFriends =  timeFormatBase + '.txt'
timeFormatFriendsFull = timeFormatBase + '_Full.txt'
timeFormatFollowers = timeFormatBase + '_followers.txt'

targetUserId = 0
vk_session = vk_api.VkApi('***', '****')
vk_session.auth(token_only=True)
vk = vk_session.get_api()

friends = vk.friends.get(user_id=targetUserId,order='name')
ts = time.time();
st = datetime.datetime.fromtimestamp(ts).strftime(timeFormatFriends)
file = open(st, 'w+')
file.write(json.dumps(friends)) 

friends = vk.friends.get(user_id=targetUserId,fields='name')
ts = time.time();
st = datetime.datetime.fromtimestamp(ts).strftime(timeFormatFriends)
file = open(st, 'w+')
file.write(json.dumps(friends))

followers = vk.users.get(user_id=targetUserId,fields='name') 
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime(timeFormatFollowers)
file = open(st, 'w+')
file.write(json.dumps(followers))

dir = os.listdir()
times = []

for filename in dir:
	try:
		times.append(datetime.datetime.strptime(str(file.name), timeFormatFriends))
	except:
		continue
youngest_entry = max(times)
youngest_file = youngest_entry.strftime(timeFormatFriends)
fd=open(youngest_file,"r")

#data = json.load(fd)
#print(set(data.item) & set(friends_ids.item))


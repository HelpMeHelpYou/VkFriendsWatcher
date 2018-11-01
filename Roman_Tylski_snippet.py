
import vk_api
import datetime
import os
import time
import json


print (os.getcwd())

def get_vk_api():
    file_descriptor = open("json.auth", "r")
    auth = json.load(file_descriptor)
    vk_session = vk_api.VkApi(auth["login"], auth["password"]);
    vk_session.auth(token_only=True)
    vk = vk_session.get_api()
    return vk
vk = get_vk_api()

response = vk.database.getUniversities(q="НИ РХТУ")
UniversityID = response["items"][0]["id"]
offset = 0
result=[]
while True:
    response = vk.users.search(university=UniversityID, offset=offset)
    c = len(response["items"])
    if (c == 0):
        break
    else:
        offset += c
        print(offset/response["count"] * 100)
    for friend in response["items"]:
        try:
            response = vk.friends.get(user_id=friend["id"])
            if (87449484 in response["items"]):
            #if (2836 in response["items"]):
                result.append(friend["id"]);
        except:
            pass

print(result)
file_descriptor = open("Roman_friends_in_university.txt", 'w+')
file_descriptor.write(json.dumps(result))
file_descriptor.close()

response = vk.database.getUniversities(q="ТПУ")
UniversityID = response["items"][0]["id"]
offset = 0
result=[]
while True:
    response = vk.users.search(university=UniversityID, offset=offset)
    c = len(response["items"])
    if (c == 0):
        break
    else:
        offset += c
        print(offset/response["count"] * 100)
    for friend in response["items"]:
        try:
            response = vk.friends.get(user_id=friend["id"])
            if (87449484 in response["items"]):
            #if (2836 in response["items"]):
                result.append(friend["id"]);
        except:
            pass


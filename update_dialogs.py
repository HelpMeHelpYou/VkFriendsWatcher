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

def save_conversation(vk,conversation):
    if ( True ): #conversation["peer"]["type"] == "user"):
        offset = 0;
        messages = []
        while True:
            response = vk.messages.getHistory(peer_id=conversation["peer"]["id"], count=200, offset=offset)
            messages = messages + response["items"];
            if len(response["items"]) != 200:
                break
            else:
                offset += 200

        file_descriptor = open(str(conversation["peer"]["id"]), 'w+')
        print(messages,file = file_descriptor)#.write(json.dumps(messages))
        file_descriptor.close()


def dowload_all_conversations(vk,target):
    offset=0;
    while True:
        response = vk.messages.getConversations(offset=offset, count=200)
        for conversation in response["items"]:
            save_conversation(vk,conversation["conversation"])
        if len(response["items"])!=200 :
            break;
        offset += 200

vk = get_vk_api()

try:
    os.mkdir("dialogs")
except FileExistsError:
    print ("already exist")
os.chdir("dialogs")


dowload_all_conversations(vk, 0)
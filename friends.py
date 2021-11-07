import vk

with open("access_token.auth", "r") as f:
    token = f.readline().strip()

version = "5.81"
vk_session = vk.Session(access_token=token)
vk_api = vk.API(vk_session)
user_id = int(input())

print(vk_api.friends.get(v=version, user_id=498061652))
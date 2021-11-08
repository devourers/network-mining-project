import vk

def connect():
    try:
        with open("access_token.auth", "r") as f:
            token = f.readline().strip()
    except:
        print("No file 'access_token.auth', cannot login")
    vk_session = vk.Session(access_token=token)
    vk_api = vk.API(vk_session)
    return vk_api
# NetX project, 9-th semester

## Installation and preparation

1. Install `requirements.txt` via ```pip install -r requirements.txt```

2. Form file `acess_token.auth` which consists of a single line — VK Api token for some app with access to API method `friends.get`, i.e.:
```
e78876c6eeeeeee76c6b2e7f18c8fee788e78876c6860fd9234ae0cd14c8d9dbb6
```
On how to get VK API token please consult [this link](https://vk.readthedocs.io/en/latest/vk-api/#making-api-request)

3. Form file `user.ids`, which consists of two lines: main account user ID and personal account user ID, i.e.:
```
1111111111
2222222222
```

You can check user ID either with settings of your profile or via "Friends" page.

4. *If you have hidden friends*: form 2 files -- `user1.friends` and `user2.friends`. Each of those files consists of n lines of VK IDs of your hidden friends. `user1.friends` refers to user ID in first line of file `user.ids`, and `user2.friends` to second line of the same file.

## Usage

This repository consists of two primary methods:

1. **Construct an ego network for your main and personal VK account**, with some degree of analysation (main stats like node count, edge count, clustering, etc.), lambda clustering and clique community detection.

2. **Netstalking demo**. This is a demo which counts netstalking coefficient (NC) for two of your profiles. For this to work, please make sure to unprivate both of your pages (at least for the time of performing demo). Optionally, you can play with number of visible friends to see how it affects the NC.

### Privacy
At no point of programm running does it save your user IDs, ID of your friends or any data conecerning them. For your personal research you can modify it to save or output some user IDs to provide more context, but this is up to you.
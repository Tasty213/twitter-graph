from enum import Enum
from operator import truediv
import requests
import json

SEED_USER_ID = 1179455215
SEED_USER_NAME = "EdwardJDavey"
SEED_USER_DISPLAY_NAME = "Ed Davey MP 🔶 🇬🇧 🇪🇺"
SEED_USER_BIO = "Leader of @ LibDems, husband, father, carer, and MP for Kingston & Surbiton. Campaigning for a greener, fairer and more caring country."
BATCH_SIZE = 1000
FOLLOWERS = "Lu1NrNw85tgj2FTdTATuzg/Followers"
FOLLOWING = "rmZGQ1NwDXKVmRB1XBfm2w/Following"

USER_GROUP_MAPPING = {
    "Liberal Democrat": "🔶",
    "FBPE": "#FBPE"
}


def get_users_batch(user_id: int, batch_size: int, endpoint: str, cursor: str = ""):

    url = f"https://twitter.com/i/api/graphql/{str(endpoint)}"

    parameters = {"userId": str(user_id),
                  "count": batch_size,
                  "includePromotedContent": False,
                  "withSuperFollowsUserFields": True,
                  "withDownvotePerspective": False,
                  "withReactionsMetadata": False,
                  "withReactionsPerspective": False,
                  "withSuperFollowsTweetFields": True,
                  "__fs_dont_mention_me_view_api_enabled": False,
                  "__fs_interactive_text_enabled": False,
                  "__fs_responsive_web_uc_gql_enabled": False}

    if cursor != "":
        parameters["cursor"] = cursor

    querystring = {"variables": json.dumps(parameters)}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Accept": "*/*",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "utf-8",
        "content-type": "application/json",
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-client-language": "en",
        "x-twitter-active-user": "yes",
        "x-csrf-token": "c6b3fb66a0b5aa019667c552d4d4257383241a6414e1a295be6ebb072e0f2548734c2bdd707b5ab1802da6c17e6d99e0f20a81b21820341c2f54ef1103887ce00482257a203c7d4aec6551fcb8e7783b",
        "DNT": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
        "Referer": "https://twitter.com/EdwardJDavey/followers",
        "Connection": "keep-alive",
        "Cookie": "kdt=P4usfIONScz7pbcsLMQebQr8NnLeumm12AUONw12; auth_token=016482153255ff135e5442866206ff67dd3ba014; eu_cn=1; dnt=1; g_state={i_l:0}; auth_multi=151193935:be479380a647f5e4688692f8426a884da978056e|2160143997:c755f6ecc25e83d567d9707f259c14e35f4cfc60; night_mode=2; twid=u%3D1363106815073017860; ads_prefs=HBESAAA=; guest_id=v1%3A164219455617719660; ct0=c6b3fb66a0b5aa019667c552d4d4257383241a6414e1a295be6ebb072e0f2548734c2bdd707b5ab1802da6c17e6d99e0f20a81b21820341c2f54ef1103887ce00482257a203c7d4aec6551fcb8e7783b; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A164219455617719660; guest_id_marketing=v1%3A164219455617719660; personalization_id=v1_HbiOgNGytorQmGNo6ZJBrQ==",
        "TE": "trailers"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring).json()
    followers = response['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][:-2]
    cursor = response['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][-2]["content"]["value"]
    return followers, cursor


def extract_users(users: list[dict]):
    extracted_users = []
    for user in users:
        extracted_users.append(extract_user(user))
    return assign_users_to_groups(USER_GROUP_MAPPING, extracted_users)


def extract_user(follower: dict):
    return {"userId": follower['content']['itemContent']['user_results']['result']['rest_id'],
            "userName": follower['content']['itemContent']['user_results']['result']['legacy']['screen_name'],
            "displayName": follower['content']['itemContent']['user_results']['result']['legacy']['name'],
            "bio": follower['content']['itemContent']['user_results']['result']['legacy']['description']}


def get_seed_user():
    return {
        "userId": SEED_USER_ID,
        "userName": SEED_USER_NAME,
        "displayName": SEED_USER_DISPLAY_NAME,
        "bio": SEED_USER_BIO
    }


def process_user(user: dict):
    print(user)
    if user_node_exists(user):
        return
    create_user_node(user)
    followers, following = get_user_followers_and_following(user)
    for follower in followers:
        process_user(follower)
        create_relationship(follower["userId"], user["userId"], "FOLLOWS")
    for followee in following:
        process_user(followee)


def create_relationship(source: str, target: str, label: str):
    pass


def create_user_node(user: dict):
    pass


def user_node_exists(user: dict):
    pass


def get_user_followers_and_following(user: dict):
    followers = get_users(user, FOLLOWERS)
    following = get_users(user, FOLLOWING)
    return followers, following


def get_users(user: dict, endpoint: str):
    users = []
    cursor = ""
    while True:
        new_users, cursor = get_users_batch(
            user["userId"], BATCH_SIZE, endpoint, cursor)
        users.extend(new_users)
        if cursor.startswith("0|"):
            break
    users = extract_users(users)
    return users


def assign_users_to_groups(mappings: dict, users: list[dict], include_users_with_no_group: bool = False):
    output_users = []
    for user in users:
        user["groups"] = extract_user_groups(mappings, user)
        if user["groups"] != [] or include_users_with_no_group:
            output_users.append(user)
    return output_users


def extract_user_groups(mappings: dict, user: dict):
    groups = []
    for group in mappings.keys():
        if search_dict_for_value(mappings[group], user):
            groups.append(group)
    return groups


def search_dict_for_value(search_string: str, dictionary: dict):
    for value in dictionary.values():
        if search_string in value:
            return True
    return False


if __name__ == "__main__":
    seed_user = get_seed_user()
    process_user(seed_user)

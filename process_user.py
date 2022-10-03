import json
from typing import Dict, List

import requests
from kafka import KafkaProducer

from User import User
from twitter_api.twitter_api import TwitterApi
from twitter_api.twitter_api import TwitterRequest

BATCH_SIZE = 1000
FOLLOWERS = "Lu1NrNw85tgj2FTdTATuzg/Followers"
FOLLOWING = "rmZGQ1NwDXKVmRB1XBfm2w/Following"

USER_GROUP_MAPPING = {
    "Liberal Democrat": "🔶",
    "FBPE": "#FBPE"
}


class UserProcessor:
    def __init__(self):
        self.producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.api = TwitterApi()

    def __del__(self):
        self.producer.flush()

    def process_user(self, user: User):
        print(user)
        followers, following = self.get_user_followers_and_following(user)
        for follower in followers:
            self.producer.send("twitter-users", follower)
        for followee in following:
            self.producer.send("twitter-users", followee)

    def get_user_followers_and_following(self, user: User):
        followers = self.get_users(user, FOLLOWERS)
        following = self.get_users(user, FOLLOWING)
        return followers, following

    def get_users(self, user: User, endpoint: str):
        users = []
        cursor = ""
        while True:
            request = TwitterRequest(user, BATCH_SIZE, endpoint, {"userId": user.user_id,
                                                                  "count": BATCH_SIZE,
                                                                  "includePromotedContent": False,
                                                                  "withSuperFollowsUserFields": True,
                                                                  "withDownvotePerspective": False,
                                                                  "withReactionsMetadata": False,
                                                                  "withReactionsPerspective": False,
                                                                  "withSuperFollowsTweetFields": True,
                                                                  "__fs_dont_mention_me_view_api_enabled": False,
                                                                  "__fs_interactive_text_enabled": False,
                                                                  "__fs_responsive_web_uc_gql_enabled": False}, cursor)
            new_users, cursor = self.api.get_users_batch(request)
            users.extend(new_users)
            if cursor.startswith("0|"):
                break
        users = self.extract_users(users)
        return users

    @staticmethod
    def get_users_batch(user_id: int, batch_size: int, endpoint: str, cursor: str = ""):
        print(f"getting user batch {cursor}")
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
            "x-csrf-token": "02ae337c183a7567cd81c3f012f6e873965da4aafadbf1a5591e649c932a4f7aa8b1ed2cfa7c3559d8eabea7a45a5ff5e0a072801669ebff488fd790cbdb4dd88f337fde17c2d840d961de63279a5ac5",
            "DNT": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "Referer": "https://twitter.com/EdwardJDavey/followers",
            "Connection": "keep-alive",
            "Cookie": "guest_id=v1%3A165558872389902029; d_prefs=MToxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; guest_id_ads=v1%3A165558872389902029; guest_id_marketing=v1%3A165558872389902029; personalization_id=\"v1_Rn6XadoEGX0nUsv7ugMpkg==\"; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; ct0=02ae337c183a7567cd81c3f012f6e873965da4aafadbf1a5591e649c932a4f7aa8b1ed2cfa7c3559d8eabea7a45a5ff5e0a072801669ebff488fd790cbdb4dd88f337fde17c2d840d961de63279a5ac5; gt=1573620365968003072; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCNf9Cm%252BDAToMY3NyZl9p%250AZCIlMWRmOTVmODhiZjJlODdlZmI0NWMwNDBkN2ViMmMyNzk6B2lkIiU3MzBi%250AODMzZjdlNGIyNTJlYTVjNTg2OGUzNmQzY2ZkYg%253D%253D--2edf72a74d2a42d81325f5767e641cba0288ddb8; g_state={\"i_l\":0}; kdt=juhPKWODtI1JGnkoMgFzodpGAxFciA9E4iOKaBY1; twid=u%3D1363106815073017860; auth_token=bd42260a2e532b43943c95a1a20c41bedc283621; att=1-JPLwunpDcgoZMyLkhRFSVGQd8g2y4V3YWhj3HoCR",
            "TE": "trailers"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring).json()
        followers = response['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][:-2]
        cursor = \
            response['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][-2]["content"][
                "value"]
        return followers, cursor

    def extract_users(self, users: List[Dict]):
        extracted_users = []
        for user in users:
            extracted_users.append(self.extract_user(user))
        return self.assign_users_to_groups(USER_GROUP_MAPPING, extracted_users)

    @staticmethod
    def extract_user(follower: Dict):
        return {"userId": follower['content']['itemContent']['user_results']['result']['rest_id'],
                "userName": follower['content']['itemContent']['user_results']['result']['legacy']['screen_name'],
                "displayName": follower['content']['itemContent']['user_results']['result']['legacy']['name'],
                "bio": follower['content']['itemContent']['user_results']['result']['legacy']['description']}

    def create_user_node(self, user: Dict):
        pass

    def user_node_exists(self, user: Dict):
        pass

    def assign_users_to_groups(self, mappings: Dict, users: List[Dict], include_users_with_no_group: bool = False):
        output_users = []
        for user in users:
            user["groups"] = self.extract_user_groups(mappings, user)
            if user["groups"] != [] or include_users_with_no_group:
                output_users.append(user)
        return output_users

    def extract_user_groups(self, mappings: Dict, user: Dict):
        groups = []
        for group in mappings.keys():
            if self.search_dict_for_value(mappings[group], user):
                groups.append(group)
        return groups

    @staticmethod
    def search_dict_for_value(search_string: str, dictionary: Dict):
        for value in dictionary.values():
            if search_string in value:
                return True
        return False

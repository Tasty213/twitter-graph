import json

import requests
from twitter_api.requests.generic import TwitterRequest


class TwitterApi:
    def __init__(self):
        self.session = requests.session()
        self.session.headers = {
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

    def get_users_batch(self, settings: TwitterRequest):
        print(f"getting user batch {settings.cursor}")
        url = f"https://twitter.com/i/api/graphql/{str(settings.endpoint)}"
        parameters = {"userId": str(settings.user.user_id),
                      "count": settings.batch_size,
                      "includePromotedContent": False,
                      "withSuperFollowsUserFields": True,
                      "withDownvotePerspective": False,
                      "withReactionsMetadata": False,
                      "withReactionsPerspective": False,
                      "withSuperFollowsTweetFields": True,
                      "__fs_dont_mention_me_view_api_enabled": False,
                      "__fs_interactive_text_enabled": False,
                      "__fs_responsive_web_uc_gql_enabled": False}
        parameters = settings.parameters
        if settings.cursor != "":
            parameters["cursor"] = settings.cursor

        querystring = {"variables": json.dumps(parameters)}

        response = self.session.get(url, params=querystring).json()
        followers = response['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][:-2]
        print(followers)
        cursor = \
            response['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][-2]["content"][
                "value"]
        return followers, cursor

    def generic_api_request(self, settings: TwitterRequest):
        print(f"performing generic api request")
        url = f"https://twitter.com/i/api/graphql/{str(settings.endpoint)}"
        parameters = {"userId": str(settings.user.user_id),
                      "count": settings.batch_size,
                      "includePromotedContent": False,
                      "withSuperFollowsUserFields": True,
                      "withDownvotePerspective": False,
                      "withReactionsMetadata": False,
                      "withReactionsPerspective": False,
                      "withSuperFollowsTweetFields": True,
                      "__fs_dont_mention_me_view_api_enabled": False,
                      "__fs_interactive_text_enabled": False,
                      "__fs_responsive_web_uc_gql_enabled": False}

        if settings.cursor != "":
            parameters["cursor"] = settings.cursor

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
        response = self.session.get(url, headers=headers, params=querystring).json()
        followers = response['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][:-2]
        print(followers)
        cursor = \
            response['data']['user']['result']['timeline']['timeline']['instructions'][-1]['entries'][-2]["content"][
                "value"]
        return followers, cursor

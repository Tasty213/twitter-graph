from User import User
from twitter_api.requests.generic import TwitterRequest


class UserRequest(TwitterRequest):
    def __init__(self, batch_size: int, cursor: str, user: User, endpoint: str):
        parameters = {"userId": user,
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
        super(UserRequest, self).__init__(endpoint, parameters)

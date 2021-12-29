# Twitter API Initializer: Configures Twitter API for use with Twitter Account credentials, as passed into the module
# via the JSON-formatted object 'twitter_credentials', which must include key:values for these keys:
#    'consumer_key'
#    'consumer_secret'
#    'access_token'
#    'access_token_secret'
# 0.0) Prerequisites
#      0.1) Python Dependencies:
#           0.1.1) Python package 'tweepy' shall be installed into the active Python environment.
#      0.2) Configuration Dependencies:
#           0.2.a) Twitter: The target Twitter account shall be properly configured for Twitter API access.
#           0.2.b) The calling module shall have already loaded the secret Twitter account keys into the JSON-formatted
#                   'twitter_credentials' object, and shall have passed that object into this module. This
#                   'twitter_credentials' object shall cointain valid key:value pairs for these keys:
#                       'consumer_key', 'consumer_secret', 'access_token', 'access_token_secret'
# 1.0) Run-time notes:
#   1.1) Usage:
#       1.1.1) standalone?: No.
#       1.1.2) call from another module?: Yes, by doing the following from the calling module:
#            >>> import init_twitter_api
#            >>> with open('<path>/<file>') as file:
#                   twitter_credentials = json.load(file)     # where '<path>/<file>' is the location/file of the JSON
#                                                             # file containing the target Twitter account's secret keys
#                                                             # (e.g., '../twitter_credentials_thirstybot.json')
#            >>> api = init_twitter_api.init_twitter_api(twitter_credentials) # passes the 'twittere_credentials' on
#                                                             # to this module, which are returned to the 'api' object.
#                                                             # That 'api' object should subsequntly be passed along by
#                                                             # the calling function to any function/module that needs
#                                                             # the Twitter/tweepy API (e.g., 'lets_tweet_message').
# 2.0) Changelog:
#       Version 1.0: Original version.


def init_twitter_api(twitter_credentials):  # 'credentials' is a string-formatted location/json file
    import tweepy  # import tweepy Twitter API
    auth = tweepy.OAuthHandler(twitter_credentials['consumer_key'],
                               twitter_credentials['consumer_secret'])
    auth.set_access_token(twitter_credentials['access_token'],
                          twitter_credentials['access_token_secret'])
    return tweepy.API(auth)

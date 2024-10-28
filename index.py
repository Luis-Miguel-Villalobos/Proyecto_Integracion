import tweepy
import account as a

print("Extractor de tweets")
cliente= tweepy.Client(a.Bearer_Token, a.API_Key, a.API_Key_Secret, a.Access_Token, a.Access_Token_Secret)

auth= tweepy.OAuth1UserHandler(a.API_Key, a.API_Key_Secret, a.Access_Token, a.Access_Token_Secret)
api = tweepy.API(auth)

cliente.create_tweet(text="Hello Twitter!")


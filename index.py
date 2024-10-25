import tweepy
import account

client= tweepy.OAuthHandler(account.API_Key, account.API_Key_Secret)
client.set_access_token(account.Access_Token, account.Access_Token_Secret)
api = tweepy.API(client)

tweet= "hola este es mi primer tweet con Tweepy"
response= api.update_status(status=tweet)

print("Tweet posteado bien",response)
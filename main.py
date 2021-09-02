from instagramBot import InstaFollower

# Extra account to use
username = YOUR_USERNAME
password = YOUR_PASSWORD

bot = InstaFollower(username)

bot.login(password)
bot.unfollow()
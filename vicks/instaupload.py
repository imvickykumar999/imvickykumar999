from instabot import Bot
# import getpass
bot = Bot()

def upload(user, passwd, path, cap):
    bot.login(username = user, password = passwd)
    up = bot.upload_photo(path, caption = cap)
    return up

# user = input('Enter Username : ')
# passwd = getpass.getpass('Enter Password : ')
#
# path = input('Photo name.jpg : ')
# cap = input('Enter Caption : ')

# upload(user, passwd, path, cap)

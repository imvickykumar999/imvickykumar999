
def instaup(file):
    from PIL import Image
    import urllib.request

    def make_square(im, min_size=256, fill_color=(255,255,255,0)):
        x, y = im.size
        size = max(min_size, x, y)
        new_im = Image.new('RGB', (size, size), fill_color)
        new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
        return new_im

    # urllib.request.urlretrieve(file, "00000001.jpg")
    # file = "00000001.jpg"

    test_image = Image.open(file)
    new_image = make_square(test_image)
    new_image.save(file)

    from instabot import Bot
    bot = Bot()

    def upload(user, passwd, path, cap):
        bot.login(username = user, password = passwd)
        up = bot.upload_photo(path, caption = cap)
        return up

    user = '_____.___alone___._____'
    passwd = 'Hellovix999@'

    path = file
    cap = '🔥This image is uploaded using python code✨'

    upload(user, passwd, path, cap)


# https://adafruit-io-python-client.readthedocs.io/en/latest/data.html

from Adafruit_IO import Client, Data

aio = Client('imvickykumar999',
             'aio_VwQb718pVsvDw9zrSKBJLMUDQHnQ')

feed = 'ledswitch'

def rec():
    data = aio.receive(feed)
    return data.value
    # print(data.value)

def send(o='ON'):
    test = aio.feeds(feed)
    aio.send_data(test.key, o.upper())

# def batch_send():
#     data_list = [Data(value='ON'), Data(value='OFF')]
#     aio.create_data(feed, data_list)


from json import dumps
from httplib2 import Http

def main(url):
    bot_message = {
        'text' : text,
          "cards": [
            {
              "sections": [
                {
                  "widgets": [
                    {
                      "textParagraph": {
                        "text": "<b>Roses</b> are <font color=\"#ff0000\">red</font>,<br><i>Violets</i> are <font color=\"#0000ff\">blue</font>"
                      }
                    }
                  ]
                }
              ]
            },
            {
          "sections": [
            {
              "widgets": [
                {
                  "image": {
                    "imageUrl": "https://developers.google.com/chat/images/cards-image.png",
                    "onClick": {
                      "openLink": {
                        "url": "https://developers.google.com/chat/api/guides/message-formats/cards#image_widget/"
                      }
                    }
                  }
                }
              ]
            }
          ]
        }
      ]
    }

    message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )

    return response

if __name__ == '__main__':
    text = input('Write message : ')

    if text == '':
        text = '''
    Hey Vicks,
    Hello from a Python script!
    '''
    url = 'https://chat.googleapis.com/v1/spaces/AAAA-pCtR2s/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=ZtcRtCCJrX12a_D2s4zG_J7oXBNFFnBW8LRCUh3IBCM'
    response = main(url)
    print(response)
  
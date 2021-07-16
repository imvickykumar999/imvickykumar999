
# pip install imvickykumar999
# C:\Users\Vicky\anaconda3\Lib\site-packages\vicksbase
# https://stackoverflow.com/questions/1802971/nameerror-name-self-is-not-defined

# import json
# from datetime import datetime
# import socket

# print("Your Computer Name is:" + hostname)
# print("Your Computer IP Address is:" + IPAddr)

class vicks:
    def __init__(self,
                password,
                name = 'Anonymous',
                link = 'https://chatting-c937e-default-rtdb.firebaseio.com/',
                ):

        try:
            self.link = link
            self.name = name
            self.password = password

            from vicksbase import firebase as f
            self.firebase_obj = f.FirebaseApplication(self.link, None)
            # print(self.pull(child = '/'))

        except Exception as e:
            print(e)
            print('try: pip install imvickykumar999')

    def show(self):
        return self.link, self.name

    def pull(self,
             child = 'Group/Chat'):

        if self.password == '@Hey_Vicks':
            # dt = datetime.now()
            # d = str(dt).split()[0]
            #
            # if child == None:
            #     child = f'Group/Chat/{d}'

            result = self.firebase_obj.get(f'{child}', None)
            return result

        else:
            error = '\n...Wrong Credentials !!!\n'
            print(error)
            return error

    def push(self, data = None,
                   child = 'Group/Chat'):

        if self.password == '@Hey_Vicks':
            # dt = datetime.now()
            # d = str(dt).split()[0]
            # t = str(dt).split()[1].split('.')[0]

            # if child == None:
            #     child = f"Group/Chat"
                # child = f"Group/Chat/{d}/{t}@{self.name}"

            if data == None:
                data = f"...hi, I am {self.name}"

            self.firebase_obj.post(child, self.name + ' => ' + data)
            # self.firebase_obj.put('/', child, data)
            # return self.pull(child = '/')

        else:
            error = '\n...Wrong Credentials !!!\n'
            print(error)
            return error

    def remove(self, child = 'A/B/C/led2'): # danger to run... loss of data.

        if self.password == '@Hey_Vicks':
            data = self.firebase_obj.delete('/', child)
            # return self.pull(child = '/')

        else:
            error = '\n...Wrong Credentials !!!\n'
            print(error)
            return error

    # def save(self,
    #          child = None):
    #
    #     if self.password == '@Hey_Vicks':
    #         dt = datetime.now()
    #         d = str(dt).split()[0]
    #
    #         if child == None:
    #             child = f'Group/Chat/{d}'
    #
    #         with open('data.json', 'w', encoding ='utf8') as json_file:
    #             json.dump(self.pull(child), json_file, ensure_ascii = False)
    #
    #     else:
    #         error = '\n...Wrong Credentials !!!\n'
    #         print(error)
    #         return error

# link = 'https://chatting-c937e-default-rtdb.firebaseio.com/'
# obj = vicks(link)

# f = obj.show()
# f = obj.pull()
# f = obj.push(1)
# f = obj.remove()

# print(f)
# input('Press Enter to Exit...')

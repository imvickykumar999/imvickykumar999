
def encrypt(key = 'monarchy', text = "instruments"):

    # key = 'monarchy'
    # key = input('\nEnter key : ')
    key = list(key.upper().replace(' ', ''))
    key = sorted(set(key), key=key.index)
    # key

    import string
    alpha = [letter for letter in string.ascii_uppercase]
    # print(alpha)

    # text = "instruments"
    # text = input('\nEnter text : ')
    plain_text = text.replace(' ', '')
    plain_text = list(plain_text.upper())

    if len(plain_text)%2:
        plain_text+='Z'

    plain_text = [sub for sub in plain_text if sub.isalpha()]
    # plain_text

    box = set(alpha) - set(key)

    # If the plaintext contains J, then it is replaced by I.
    if 'J' in plain_text:
        box = list(box - set('I'))
    else:
        box = list(box - set('J'))

    box.sort()
    box = key + box
    # print(box)

    matrix = [[0 for i in range(5)] for j in range(5)]

    x=0
    for i in range(5):
        for j in range(5):
            matrix[i][j] = box[x]
            x+=1

    # matrix

    import numpy as np

    matrix = np.array(matrix)
    plain_text = np.array(plain_text)
    box = np.array(box)
    key = np.array(key)

    print(matrix)

    text2d = [[0 for i in range(2)] for j in range(len(plain_text)//2)]
    text2d

    x=0
    for i in range(len(plain_text)//2):
        for j in range(2):
            text2d[i][j] = plain_text[x]
            x+=1

    # text2d

    json = []
    for i in range(len(text2d)):
        for j in range(2):
            pos = np.where(matrix == text2d[i][j])
            json.append([text2d[i][j], [int(pos[0]), int(pos[1])]])
    # json

    print()
    emp = []
    for i in range(0, len(json), 2):
        a = json[i][1][0]
        b = json[i+1][1][0]
        c = json[i][1][1]
        d = json[i+1][1][1]

    #     print(a,c)
    #     print(b,d)

        if a==b:
            print(matrix[a][c], '->', matrix[a][(c+1)%5])
            emp.append(matrix[a][(c+1)%5])
            print(matrix[b][d], '->', matrix[b][(d+1)%5])
            emp.append(matrix[b][(d+1)%5])
        elif c==d:
            print(matrix[a][c], '->', matrix[(a+1)%5][c])
            emp.append(matrix[(a+1)%5][c])
            print(matrix[b][d], '->', matrix[(b+1)%5][d])
            emp.append(matrix[(b+1)%5][d])
        else:
            print(matrix[a][c], '->', matrix[a][d])
            emp.append(matrix[a][d])
            print(matrix[b][d], '->', matrix[b][c])
            emp.append(matrix[b][c])
    # emp

    output = ''.join(emp)
    print()
    # print(text.upper(), '=', output)

    out2d = [[0 for i in range(2)] for j in range(len(plain_text)//2)]
    # out2d

    x=0
    for i in range(len(emp)//2):
        for j in range(2):
            out2d[i][j] = emp[x]
            x+=1
    # out2d

    tpair = ''
    for i in text2d:
        for j in range(0,2,2):
            tpair += f'{i[j]}{i[j+1]}  '

    # tpair

    epair = ''
    for i in out2d:
        for j in range(0,2,2):
            epair += f'{i[j]}{i[j+1]}  '

    # epair

    print(tpair)
    print()

    print(epair)
    print()

    return tpair, epair


key = 'monarchy'
text = "instruments"
encrypt(key, text)

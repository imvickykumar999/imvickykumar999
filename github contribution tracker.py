import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt 

user = input('Enter Username : ')
if user == '':
    user = 'imvickykumar999'
    
print()
followers = requests.get('https://api.github.com/users/'+ user +'/followers').json()

follower = []
for i, j in enumerate(followers):
    value = list(j.values())[0]
    
    follower.append(value)
    print(i+1, value)
follower.append(user)

index = True
while index:
    index = input('\nEnter index : ')
    if index == '':
        index = 0
    select = follower[int(index)-1]
    
# select = user

    print(f" => [ {select} ]  {'='*90}>\n")
    url = 'https://github.com/' + select

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html5lib')

    s = ('color-text-primary ws-normal text-left',
         'ml-0 py-1 d-flex', 
         'float-left ws-normal text-left color-text-primary', 
         'd-flex py-1', )

    try:
        lst = soup.findAll('span', attrs= {'class' : s[0]})
        created = lst[0].text.strip().replace('\n', '').split(' ')
        for i in created:
            if i != '':
                print(i, end=' ')
        print('\n', '-'*90, '\n')

        lst = soup.findAll(class_= s[1])
        for i in range(len(lst)):
            repo = lst[i].findAll('a')[1]['href']
            commit = lst[i].findAll('a')[1].text.strip()

            print(f"=> \t https://github.com{repo} \t {commit}")
            print()
    except Exception as e:
        pass

    try:
        lst = soup.findAll('span', attrs= {'class' : s[2]})
        created = lst[0].text.strip().replace('\n', '').split(' ')
        for i in created:
            if i != '':
                print(i, end=' ')
        print('\n', '-'*90, '\n')

        lst = soup.findAll(class_= s[3])
        for i in range(len(lst)):
            lang = lst[i].findAll('span')[-1].text.replace('\n', '')
            link = lst[i].a['href']
            date = lst[i].time.text.strip()

            print(f"=> \t https://github.com{link} \t\t\t {lang} \t {date}")
            print()
    except Exception as e:
        pass


    lst = soup.find (class_= 'border py-2 graph-before-activity-overview')
    glist = lst.g.findAll('rect')
    x, y = [], []

    for i in range (len (glist)):
        dc = int (glist [i]['data-count'])
        y.append(dc)
        dd = int (glist [i]['data-date'].split('-')[2])
        x.append(dd)

    print('\nPrinting Contribution Graph\n')
    nd = True
    while nd:
        nd = input('Last n days (e.g, 10) : ')
        d = input('For no. of Days (e.g, 7 < nd) : ')

        if nd == '' or d == '':
            nd = 10
            d = 3
        else:
            nd = int(nd)
            d = int(d)

        if nd:
            if d==nd:
                ux = x[-nd:] + [x[-1]]
                uy = y[-nd:] + [y[-1]]
            else:
                ux = x[-nd : d-nd]
                uy = y[-nd : d-nd]

            plt.xlabel ('\n' + ' / '.join (glist[-nd]['data-date'].split('-')[:-1]) + ' / Date -->', 
                       fontweight = "bold") 
            plt.ylabel ('No. of Contribution -->\n', fontweight = "bold")
            plt.title (f"GitHub Public Contribution\nTracker of {select}\n",
                       fontweight = "bold")
            plt.grid (True, color = "grey", linewidth = "1", linestyle = "-.")

            plt.xlim([ux[0]-1, ux[-1]+1])
            plt.ylim(0, max(uy)+5)

            plt.bar (ux, uy) 
            plt.show ()
            print(f''' >>> max. Contribution b/w,\n
            {glist[-nd]['data-date']}
            and, {glist[d-nd-1]['data-date']}
            \n...is {max(uy)}
            ''')
        else:
            break

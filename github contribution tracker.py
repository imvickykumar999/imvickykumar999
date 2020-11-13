import requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt 

user = input ('Enter GitHub Username : ')
if user == '':
    user = 'imvickykumar999'
    
url = 'https://github.com/' + user
page = requests.get (url)
soup = BeautifulSoup (page.content, 'html5lib')

lst = soup.find (class_= 'border py-2 graph-before-activity-overview')
glist = lst.g.findAll('rect')
x, y = [], []

for i in range (len (glist)):
    dc = int (glist [i]['data-count'])
    y.append(dc)
    dd = int (glist [i]['data-date'].split('-')[2])
    x.append(dd)

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
        plt.title (f"GitHub Public Contribution\nTracker of {user}\n",
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
        

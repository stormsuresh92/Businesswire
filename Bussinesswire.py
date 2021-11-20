from requests_html import HTMLSession
import pandas as pd
from alive_progress import alive_bar
from time import sleep


data = []
def page(x):
    s = HTMLSession()
    url = f'https://www.businesswire.com/portal/site/home/template.PAGE/news/?javax.portlet.tpst=ccf123a93466ea4c882a06a9149550fd&javax.portlet.prp_ccf123a93466ea4c882a06a9149550fd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_ccf123a93466ea4c882a06a9149550fd_ndmHsc=v2*A1630666800000*B1633238694953*DgroupByDate*G{x}*N1000003&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken'
    r = s.get(url)
    content = r.html.find('ul.bwNewsList li')
    with alive_bar(len(content), title=f'Getting page {x}', bar='classic2', spinner='classic') as bar:
        for item in content:
            title = item.find('a.bwTitleLink span', first=True).text
            links = 'https://www.businesswire.com' + item.find('a.bwTitleLink', first=True).attrs['href']
            date = item.find('div.bwTimestamp', first=True).text.split('-')[-2]
            time = item.find('div.bwTimestamp', first=True).text.split('-')[-1]
            dic = {
                'Title':title,
                'Urls':links,
                'Updated_Date':date,
                'Updated_Time':time
            }
            data.append(dic)
            sleep(0.1)
            bar()
        
endpage = int(input('Enter end page:'))
for x in range(1, endpage):
    page(x)

df = pd.DataFrame(data)
df.to_csv('Downloded file.csv', index=False)
print('\n')
print('Download completed')
input()

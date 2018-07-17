import requests
from urllib.parse import urlencode
from multiprocessing.pool import Pool
import csv
import pymysql
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.99 Safari/537.36'
}

def get_page(url):
    try:
        page = requests.get(url, headers=headers)
        if page.status_code == 200:
            return page.json()
    except requests.ConnectionError:
        return None

def get_info(json):
    if json.get('data'):
        item = json.get('data')
        if item.get('articleList'):
            for info in item.get('articleList'):
                title = info.get('title')
                view_count = info.get('view_count')
                comment_count = info.get('comment_count')
                item = {
                    'title': title,
                    'view_count': view_count,
                    'comment_count': comment_count
                }
                print(item)
                db = pymysql.connect(host='localhost', user='root', passwd='******', port=3306,
                                     db='spiders')
                cursor = db.cursor()
                sql_1 = 'CREATE TABLE IF NOT EXISTS acfun (' \
                        'title VARCHAR(255) NOT NULL, ' \
                        'view_count INT NOT NULL, ' \
                        'comment_count INT NOT NULL, ' \
                        'PRIMARY KEY (title))'
                cursor.execute(sql_1)

                table = 'acfun'
                keys = ', '.join(item.keys())
                values = ', '.join(['%s'] * len(item))
                sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
                try:
                    if cursor.execute(sql, tuple(item.values())):
                        print('Successful')
                        db.commit()
                except:
                    print('Failed')
                    db.rollback()
                db.close()

'''
def save_data(item):
    db = pymysql.connect(host='localhost', user='root', passwd='lww890226', port=3306,
                         db='spiders')
    cursor = db.cursor()
    sql = 'INSERT INTO acfun (title,view_count,comment_count) VALUES (%s,%s,%s)'
    try:
        cursor.execute(sql, (item['title'], item['view_count'], item['comment_count']))
        print('Successful')
        db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()
    '''

'''
    table = 'acfun_articleList'
    keys = ', '.join(item.keys())
    values = ', '.join(['%s'] * len(item))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(item.values())):
            print('Successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()
'''

'''
                filename = 'acfun.csv'
                with open(filename, 'a') as csvfile:
                    fieldnames = ['title', 'view_count', 'comment_count']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'title': title, 'view_count': view_count, 'comment_count': comment_count})

                    # f.write('标题：' + item['title'] + ',' + '点击量：' + str(item['view_count']) + ',' + str(item['comment_count'] + '\n'))
'''

if __name__ == '__main__':

    h = 'http://webapi.aixifan.com/query/article/list?' \
        'pageNo={}&size=10&realmIds=5%2C22%2C1%2C2%2C4' \
        '&originalOnly=false&orderType=2&periodType=-1&filterTitleImage=true'
    urls = [h.format(str(i)) for i in range(1, 11)]
    for url in urls:
        json = get_page(url)
        get_info(json)


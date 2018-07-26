import requests
from urllib.parse import urlencode
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.99 Safari/537.36'
}

def get_channelurl(pageNo, realmIds):
    params = {
        'pageNo': pageNo,
        'size': '10',
        'realmIds': realmIds,
        'originalOnly': 'false',
        'orderType': '2',
        'periodType': '-1',
        'filterTitleImage': 'true'
    }
    url = 'http://webapi.aixifan.com/query/article/list?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_info(json):
    if json.get('data'):
        item = json.get('data')
        if item.get('articleList'):
            totalPage = item.get('totalPage')
            for info in item.get('articleList'):
                title = info.get('title')
                view_count = info.get('view_count')
                comment_count = info.get('comment_count')
                item = {
                    'totalPage': totalPage,
                    'title': title,
                    'view_count': view_count,
                    'comment_count': comment_count
                }
                return item

def save_data(item):
    print(item)

def main():
    for realmIds in range(1, 24):
        pageNo = 1
        json_start = get_channelurl(pageNo, realmIds)
        item = get_info(json_start)
        try:
            sum = item.get('totalPage')
            for pageNo in range(1, int(sum)):
                json = get_channelurl(pageNo, realmIds)
                info = get_info(json)
                save_data(info)
        except AttributeError :
            pass


if __name__ == '__main__':
    main()

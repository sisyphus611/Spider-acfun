import requests
from urllib.parse import urlencode
import time
import os
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.99 Safari/537.36'
}

def get_channelurl(pageNo, realmIds):
    # 分析构造各分区信息接口url，通过分析realmIds为关键字段，由1-23数字代表各个分区，但是其中3，19，20为空
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
    # 解析获取的json数据，提取总页数，分区名，类型名，文章名，文章id，发布者，点击量，评论数，香蕉数等信息
    if json.get('data'):
        item = json.get('data')
        if item.get('articleList'):
            totalPage = item.get('totalPage')
            for info in item.get('articleList'):
                channel_name = info.get('channel_name')
                realm_name = info.get('realm_name')
                title = info.get('title')
                id = info.get('id')
                username = info.get('username')
                view_count = info.get('view_count')
                comment_count = info.get('comment_count')
                banana_count = info.get('banana_count')
                yield {
                    'totalPage': totalPage,
                    'channel_name': channel_name,
                    'realm_name': realm_name,
                    'title': title,
                    'id': id,
                    'username': username,
                    'view_count': view_count,
                    'comment_count': comment_count,
                    'banana_count': banana_count
                }


def save_data(item):
    # 数据保存到csv文件

    if not os.path.exists(item.get('channel_name')):
        os.mkdir(item.get('channel_name'))
    try:
        file_csv_path = '{0}/{1}.{2}'.format(item.get('channel_name'), item.get('realm_name'), '.csv')
        if not os.path.exists(file_csv_path):
            with open(file_csv_path, 'a', encoding='utf-8') as csvfile:
                fieldnames = ['totalPage', 'channel_name', 'realm_name', 'title', 'id', 'username',
                              'view_count', 'comment_count', 'banana_count']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(item)
        else:
            print('下载完毕', file_csv_path)
    except:
        pass


def main():
    # 利用每个分区第一页获取该分区总页数并构造分页函数，遍历整个文章区
    for realmIds in range(1, 24):
        pageNo_start = 1
        json_start = get_channelurl(pageNo_start, realmIds)
        item = get_info(json_start)
        try:
            sum = item.get('totalPage')
            for pageNo in range(1, int(sum)):
                json = get_channelurl(pageNo, realmIds)
                for info in get_info(json):
                    print(info)
                    save_data(info)
        except AttributeError:
            pass


if __name__ == '__main__':
    main()

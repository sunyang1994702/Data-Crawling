import requests
import json
import time
from datetime import timedelta, datetime
from bs4 import BeautifulSoup
import csv


def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36' }
    
    cookies = {
        'Cookie': ''    }
    ## It need cookies to request the website. Otherwise it will return None.
    html = requests.get(url, headers=headers, cookies=cookies)
    if html.status_code ==200:
        return html.content
    else:
        return ""


def parse_data(html):
    ## Use jaon to load html content!
    json_data = json.loads(html)['cmts']
    comments = []
    try:
        for item in json_data:
            comment = [
                item['nickName'],
                item['cityName'] if 'cityName' in item else '',
                item['content'].strip().replace('\n', ''),
                item['score'],
                item['startTime'],
                item['tagList']['fixed'][0]['name'] if 'tagList' in item else ''
            ]
            comments.append(comment)
        return comments
    except Exception as e:
        print("Problem in Parsing html data!: {}".format(e))


def save_data(comments):
    with open("nihaolihuanying_review.csv", 'a+', newline='', encoding='utf-8-sig') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(comments)


def main():
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Time: {}".format(start_time))
    end_time = '2021-02-12 00:00:00'

    while start_time > end_time:
        ## At almost 15 reviews for one time request. So changing startTime to get more reviews. 
        url = 'http://m.maoyan.com/mmdb/comments/movie/{}.json?_v_=yes&offset=15&startTime='.format(movie_id) + start_time.replace(' ', '%20')
        html = ""
        try:
            html = get_data(url)
        except Exception:
            print("Request url Failed!!!")
            time.sleep(1)
            html = get_data(url)
        else:
            time.sleep(10)

        comments = parse_data(html)
        start_time = comments[-1][-2]
        print("Time: {}".format(start_time))
        save_data(comments)
        print("Data Save Successfully!!")
        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=-10)
        start_time = datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')

        

if __name__ == '__main__':
    ## <你好，李焕英>
    movie_id = '1299372'
    main()



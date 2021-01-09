import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('UI_joonggo.html')

@app.route('/search', methods=['GET'])
def search_word():
    search_receive = request.form['search_give']
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://www.daangn.com/search/'
    plus_url = search_receive
    full_url = url + plus_url

    data = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    products = soup.select('#flea-market-wrap > article')

    for product in products:
        a_tag = product.select_one('div.article-info > div > span.article-title')
        if a_tag is not None:
            img = product.select_one('div.card-photo > img')['src']
            name = product.select_one('article > a > div.article-info > div > span.article-title').text
            price = product.select_one('article > a > div.article-info > p.article-price').text  # td 태그 사이의 텍스트를 가져오기

            card = {'product_url': full_url, 'product_img': img, 'product_name': name, 'product_price': price}

    return jsonify({'result': 'success', 'searching_info': card})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

# # URL을 읽어서 HTML를 받아오고,
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#
#
# url = 'https://www.daangn.com/search/'
# plus_url = input('Wanna search?')
# full_url = url + plus_url
#
# # https://www.daangn.com/search/%EA%B0%A4%EB%9F%AD%EC%8B%9C%ED%83%AD
#
# data = requests.get(full_url, headers=headers)
# # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup = BeautifulSoup(data.text, 'html.parser')
# # select를 이용해서, tr들을 불러오기
# products = soup.select('#flea-market-wrap > article')
# #flea-market-wrap > article:nth-child(4) > a > div.card-photo > img
# #flea-market-wrap > article:nth-child(4) > a > div.article-info > div > span.article-title
# #flea-market-wrap > article:nth-child(3) > a > div.article-info > div
# #flea-market-wrap > article:nth-child(4) > a > div.article-info > p.article-price
#
# # movies (tr들) 의 반복문을 돌리기
# for product in products:
#     # movie 안에 a 가 있으면,
#     a_tag = product.select_one('div.article-info > div > span.article-title')
#     if a_tag is not None:
#         product_img = product.select_one('div.card-photo > img')['src']
#         name = product.select_one('article > a > div.article-info > div > span.article-title').text
#         price = product.select_one('article > a > div.article-info > p.article-price').text  # td 태그 사이의 텍스트를 가져오기
#         print(product_img, name, price)



import requests
import json
from pymongo import MongoClient
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

client = MongoClient('mongodb://sparta:sparta123!@usedmarket.shop', 27017)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('UI_joonggo.html')

@app.route('/search', methods=['GET'])
def search_word():
    search_receive = request.args.get('search_give')
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = 'https://www.daangn.com/search/'
    plus_url = search_receive
    more_url = '/more/flea_market?page='
    full_url = url + plus_url + more_url

    for page_number in range(1, 5):
        full_url = url + plus_url + more_url + str(page_number)
    first_url = url + plus_url

    data = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    products = soup.select('#flea-market-wrap > article')
    data2 = requests.get(first_url,headers=headers)
    soup2 = BeautifulSoup(data2.text, 'html.parser')

    # >> # flea-market-wrap > article
    # flea-market-wrap > article:nth-child(2) > a > div.article-info > p.article-region-name

    products = soup.select('article')
    first_products = soup2.select('#flea-market-wrap > article')

    cards = []
    for first_product in first_products:
        a_tag = first_product.select_one('div.article-info > div > span.article-title')
        if a_tag is not None:
            img1 = first_product.select_one('div.card-photo > img')['src']
            name1 = first_product.select_one('article > a > div.article-info > div > span.article-title').text
            price1 = first_product.select_one('article > a > div.article-info > p.article-price').text  # td 태그 사이의 텍스트를 가져오기
            location1 = first_product.select_one('article > a > div.article-info > p.article-region-name').text

            card1 = {'product_url': first_url, 'product_img': img1, 'product_name': name1, 'product_price': price1, 'product_location': location1}
            cards.append(card1)

    for product in products:
        a_tag = product.select_one('div.article-info > div > span.article-title')
        if a_tag is not None:
            img = product.select_one('div.card-photo > img')['src']
            name = product.select_one('article > a > div.article-info > div > span.article-title').text
            price = product.select_one('article > a > div.article-info > p.article-price').text  # td 태그 사이의 텍스트를 가져오기
            location = product.select_one('article > a > div.article-info > p.article-region-name').text
            card = {'product_url': full_url, 'product_img': img, 'product_name': name, 'product_price': price, 'product_location': location}
            cards.append(card)

    data_jg = requests.post("https://search-api.joongna.com/v25/search/product", json={
        "filter": {"categoryDepth": 0, "categorySeq": 0,
                   "dateFilterParameter": {"sortEndDate": None, "sortStartDate": None}, "flawedYn": 0,
                   "fullPackageYn": 0, "limitedEditionYn": 0, "maxPrice": 2000000000, "minPrice": 0,
                   "productCondition": -1, "tradeType": 0}, "osType": 2, "searchQuantity": 40,
        "searchStartTime": "2021-01-20 15:53:44", "searchWord": search_receive, "sort": "RECOMMEND_SORT", "startIndex": 0,
        "productFilter": "APP"})

    soup_jg = BeautifulSoup(data_jg.text, 'html.parser')
    a = soup_jg.text
    product_data = json.loads(a)

    for i in range(0, 40):
        product_imgae_jg = product_data["data"]["items"][i]["detailImgUrl"]
        product_title_jg = product_data["data"]["items"][i]["title"]
        product_price_jg = product_data["data"]["items"][i]["price"]
        product_location_jg = product_data["data"]["items"][i]["mainLocationName"]
        # product_url_num_jg = product_data["data"]["items"][i]["seq"]
        # product_url_jg = 'https://m.joongna.com/product-detail/' + product_url_num_jg.var()

        card_jg = {'product_img': product_imgae_jg, 'product_name': product_title_jg,
                   'product_price': product_price_jg, 'product_location': product_location_jg}
        cards.append(card_jg)

    url_hello = 'https://www.hellomarket.com/api/search/items?q='
    full_url_hello = url_hello + search_receive
    data_hello = requests.get(full_url_hello, headers=headers)
    soup_hello = BeautifulSoup(data_hello.text, 'html.parser')
    b = soup_hello.text
    product_data_hello = json.loads(b)

    for i in range(2, 30):
        # product_url_hello = product_data_hello["list"][i]["item"]["media"]["imageUrl"]
        product_image_hello = product_data_hello["list"][i]["item"]["media"]["imageUrl"]
        product_title_hello = product_data_hello["list"][i]["item"]["title"]
        product_price_hello = product_data_hello["list"][i]["item"]["property"]["price"]["text"]

        card_jg = {'product_img': product_image_hello, 'product_name': product_title_hello,
                   'product_price': product_price_hello}
        cards.append(card_jg)


    return jsonify({'result': 'success', 'searching_info': cards})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


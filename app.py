import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

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
    for page_number in range(1, 5):
        full_url = url + plus_url + more_url + str(page_number)
    first_url = url + plus_url
    product_detail = 'https://www.daangn.com'

    data = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    data2 = requests.get(first_url, headers=headers)
    soup2 = BeautifulSoup(data2.text, 'html.parser')

    # # flea-market-wrap > article
    # #image-slider > div > div
    # flea-market-wrap > article:nth-child(3) > a.href

    products = soup.select('article')
    first_products = soup2.select('#flea-market-wrap > article')

    cards = []
    for first_product in first_products:
        a_tag = first_product.select_one('div.article-info > div > span.article-title')
        if a_tag is not None:
            img1 = first_product.select_one('div.card-photo > img')['src']
            name1 = first_product.select_one('article > a > div.article-info > div > span.article-title').text
            price1 = first_product.select_one('article > a > div.article-info > p.article-price').text
            url1 = first_product.select_one('article > a.href').string
            product_domain1 = product_detail + url1

            card1 = {'product_url': product_domain1, 'product_img': img1, 'product_name': name1, 'product_price': price1}
            cards.append(card1)

    for product in products:
        a_tag = product.select_one('div.article-info > div > span.article-title')
        if a_tag is not None:
            img = product.select_one('div.card-photo > img')['src']
            name = product.select_one('article > a > div.article-info > div > span.article-title').text
            price = product.select_one('article > a > div.article-info > p.article-price').text
            url2 = product.select_one('article > a.href').string
            product_domain2 = product_detail + url2


            card = {'product_url': product_domain2, 'product_img': img, 'product_name': name, 'product_price': price}
            cards.append(card)

    return jsonify({'result': 'success', 'searching_info': cards})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


from django.shortcuts import render, redirect  # redirectを追加
from django.views.generic import View
from .forms import SearchForm
import json
import requests
from django.http.response import HttpResponse


SEARCH_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId=1004224127963110171'  
# 楽天(https://webservice.rakuten.co.jp/api/booksbooksearch/)のurlをコピーして貼り付け
# urlの最後に'format=json'を記入しフォーマットをjson形式にする
# urlの最後に'&'を点けることで商品をフィルタリングをすることができる
# '&'の後にアプリケーションidを記入

def get_api_data(params):
    api = requests.get(SEARCH_URL, params=params).text
    result = json.loads(api)
    items = result['Items']
    return items


class CallbackView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        return render(request, 'app/index.html', {  # 指定したテンプレートにデータを渡す
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        if form.is_valid():
            keyword = form.cleaned_data['title']
            params = {
                'title' : keyword,
                'hits' : 28,
            }
            items = get_api_data(params)
            book_data = []
            for i in items:
                item = i['Item']
                title = item['title']
                image = item['largeImageUrl']
                isbn = item['isbn']
                query = {
                    'title' : title,
                    'image' : image,
                    'isbn' : isbn,
                }
                book_data.append(query)

            return render(request, 'app/book.html', {  # 指定したテンプレートにbook_data,keywordを渡す
                'book_data': book_data,
                'keyword': keyword,
            })

        return render(request, 'app/index.html', {  # 指定したテンプレートにデータを渡す
            'form': form,
        })


class DetailView(View):
    def get(self, request, *args, **kwargs):
        isbn = self.kwargs['isbn']  # 引数からisbnを取り出す
        params = {
            'isbn': isbn
        }

        items = get_api_data(params)  # api_data関数の引数にisbnを渡すことで特定の書籍情報を取得することができる
        items = items[0]
        item = items['Item']  # アイテムデータを取得
        # 取得するデータの名前はapiのマニュアルに記載されているので参考にする
        title = item['title']  
        image = item['largeImageUrl']
        author = item['author']
        itemPrice = item['itemPrice']
        salesDate = item['salesDate']
        publisherName = item['publisherName']
        size = item['size']
        isbn  = item['isbn']
        itemCaption = item['itemCaption']
        itemUrl = item['itemUrl']
        reviewAverage = item['reviewAverage']
        reviewCount = item['reviewCount']

        # 取得したデータをbook_dataに辞書形式で格納する
        book_data = {
            'title': title, 
            'image': image,
            'author': author,
            'itemPrice': itemPrice,
            'salesDate': salesDate,
            'publisherName': publisherName,
            'size': size,
            'isbn': isbn,
            'itemCaption': itemCaption,
            'itemUrl': itemUrl,
            'reviewAverage': reviewAverage,
            'reviewCount': reviewCount,
            'average': float(reviewAverage) * 20
        }

        return render(request, 'app/detail.html' , {
            'book_data': book_data
        })






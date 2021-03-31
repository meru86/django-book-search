from django.urls import path
from .views import CallbackView
from .views import DetailView
from app import views  # appファイルのviews.pyを読み込む

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
	path('callback/', CallbackView.as_view(), name='callback'),
	path('detail/<str:isbn>', DetailView.as_view(), name='detail'),  # isbnをurlに表示してどの書籍の詳細画面か判別する
]
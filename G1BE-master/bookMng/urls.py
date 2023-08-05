from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('search', views.search, name='search'),
    path('searchresults/', views.searchresults, name='searchresults'),
    path('messagebox', views.messagebox, name='messagebox'),
    path('book_add/<int:book_id>', views.book_add, name='book_add'),
    path('purchase', views.purchase, name='purchase'),
]


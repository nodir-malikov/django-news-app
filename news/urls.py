from django.urls import include, path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('', cache_page(15)(views.HomeNews.as_view()), name='index'),
    path('', views.HomeNews.as_view(), name='index'),
    # path('cat/<int:category_id>', views.get_category, name='category'),
    path('cat/<int:category_id>', views.NewsByCategory.as_view(), name='category'),
    # path('news/<int:news_id>', views.view_news, name='view_news'),
    path('news/<int:news_id>', views.ViewNews.as_view(), name='view_news'),
    # path('news/add-news/', views.add_news, name='add_news'),
    path('news/add-news/', views.CreateNews.as_view(), name='add_news'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('mail/', views.send_email, name='mail'),
    path('contact/', views.contact, name='contact'),
]

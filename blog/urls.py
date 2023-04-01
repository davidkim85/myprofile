from django.urls import path, include
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post, name='post'),
    path('search/', views.search, name='search'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    path('<int:post_id>/<int:user_id>/comment/',views.post_comment, name='post_comment'),

]
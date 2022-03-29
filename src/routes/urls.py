from django.urls import path, re_path
from .views import *

app_name = 'routes'
urlpatterns = [
    path('my-profile/', MyProfileView.as_view(), name='profile'),
    path('my-profile/tutorial/', AddRouteTutorialView.as_view(), name='tutorial'),
    path('my-profile/add-route/', AddRouteView.as_view(), name='add-route'),
    path('my-profile/my-comments/', MyCommentsView.as_view(), name='my-comments'),
    re_path(r'^my-profile/my-routes/edit-route/(?P<route>\d+)/next=(?P<next_url>.+)$', 
        EditRouteFullView.as_view(), name='edit-route-full'),
    re_path(r'^my-profile/my-routes/edit_route/(?P<route>\d+)/next=(?P<next_url>.+)$', 
        EditRouteView.as_view(), name='edit-route'),
    re_path(r'^my-profile/my-routes/delete-route/(?P<route>\d+)/next=(?P<next_url>.+)$', 
        DeleteRouteView.as_view(), name='delete-route'),
    re_path(r'^my-profile/my-routes/delete-route/(?P<route>\d+)/confirmed=(?P<confirmed>[^/]+)/next=(?P<next_url>.+)$', 
        DeleteRouteView.as_view(), name='delete-route'),
    re_path(r'^my-profile/my-routes/add-favorite-route/(?P<route>\d+)/next=(?P<next_url>.+)$', 
        AddFavoriteRouteView.as_view(), name='add-favorite-route'),
    re_path(r'^my-profile/my-routes/delete-favorite-route/(?P<route>\d+)/next=(?P<next_url>.+)$', 
        DeleteFavoriteRouteView.as_view(), name='delete-favorite-route'),
    re_path(r'^my-profile/my-routes/add-route-rate/(?P<route>\d+)/next=(?P<next_url>.+)$', 
        AddRouteRateView.as_view(), name='add-route-rate'),
    re_path(r'^my-profile/my-routes/add-route-comment/(?P<route>\d+)/next=(?P<next_url>.+)$', 
        AddRouteCommentView.as_view(), name='add-route-comment'),
    re_path(r'^my-profile/my-routes/add-comment-rate/(?P<comment>\d+)/(?P<rate>-?1)/next=(?P<next_url>.+)$', 
        AddCommentRateView.as_view(), name='add-comment-rate'),
    re_path(r'^my-profile/my-routes/(?:page/(?P<page_number>\d+)/)?$', 
        MyRoutesView.as_view(), name='my-routes'),
    re_path(r'^my-profile/my-routes/route-detail/(?P<route>\d+)/$', 
        MyRouteDetailView.as_view(), name='my-route-detail'),
    re_path(r'^my-profile/my-routes/route-weather/(?P<route>\d+)/$', 
        MyRouteWeatherView.as_view(), name='my-route-weather'),
    re_path(r'^my-profile/favorite-routes/(?:page/(?P<page_number>\d+)/)?$', 
        FavoriteRoutesView.as_view(), name='favorite-routes'),
    re_path(r'^my-profile/favorite-routes/route-detail/(?P<route>\d+)/$', 
        FavoriteRouteDetailView.as_view(), name='favorite-route-detail'),
    re_path(r'^my-profile/favorite-routes/route-weather/(?P<route>\d+)/$', 
        FavoriteRouteWeatherView.as_view(), name='favorite-route-weather'),
    re_path(r'^published-routes/(?:page/(?P<page_number>\d+)/)?$', 
        RoutesView.as_view(), name='routes'),
    re_path(r'^published-route-detail/(?P<route>\d+)/$', 
        RouteDetailView.as_view(), name='route-detail'),
    re_path(r'^published-route-weather/(?P<route>\d+)/$', 
        RouteWeatherView.as_view(), name='route-weather'),
    re_path(r'^search/(?:page/(?P<page_number>\d+)/)?$', 
        SearchRoutesView.as_view(), name='find'),
]
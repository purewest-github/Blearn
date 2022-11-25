from django.urls import path, include


from .views import signupfunc, loginfunc, logoutfunc, ContentCreate, ContentList, ContentDetail,  ContentDelete, ContentList2, ContentList3, ContentList4

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('detail/<int:pk>', ContentDetail.as_view(), name='detail'),
    path('list1/', ContentList.as_view(), name='list1'),
    path('list2/', ContentList2.as_view(), name='list2'),
    path('list3/', ContentList3.as_view(), name='list3'),
    path('list4/', ContentList4.as_view(), name='list4'),
    path('create/', ContentCreate.as_view(), name='create'),
    path('delete/<int:pk>', ContentDelete.as_view(), name='delete'),
]
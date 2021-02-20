from django.urls import path, include
from rest_framework.routers import DefaultRouter
from first import views
from django.conf.urls import include
from rest_framework.documentation import include_docs_urls # microblog_v3

router = DefaultRouter()
router.register(r'articles', views.ArticleAPIViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'createusers', views.CreateUserViewSet, 'create-user')
router.register(r'userprofile', views.UserProfileViewSet, 'user-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='firts')),
]

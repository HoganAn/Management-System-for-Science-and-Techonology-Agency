from django.urls import path
from rest_framework_nested import routers
from .views import CaseModelViewSet, ServiceModelViewSet, UserKeywordsAPIView, ServiceTypeStatsAPIView, CaseDocViewSet, \
    ServDocViewSet, StatsAPIView

router = routers.SimpleRouter()
router.register('case', CaseModelViewSet, basename='case')
router.register('case-doc', CaseDocViewSet, basename='case-doc')
router.register('serv-doc', ServDocViewSet, basename='serv-doc')

cases_router = routers.NestedSimpleRouter(router, 'case', lookup='case')
cases_router.register('service', ServiceModelViewSet, basename='service')

urlpatterns = [
    path('user-keywords/', UserKeywordsAPIView.as_view()),
    path('service-type-statistics/', ServiceTypeStatsAPIView.as_view()),
    path('stats/', StatsAPIView.as_view())
]
urlpatterns += router.urls
urlpatterns += cases_router.urls

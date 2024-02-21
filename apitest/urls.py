from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from apitest.views import (
    AdminHomeAPI,
    AdminHomeAPI2,
    AdminLoginAPI,
    AdministratorAPI,
    AppconfigAPI,
    Base64CodeView,
    BusinessDetailsAPI,
    BusinessesAPI,
    ClientDetailsAPI,
    DevelopersAPI,
    EstimatedetailAPI,
    GetClientByB,
    GetEstimatesByUB,
    GetEstimatesByClient,
    GetSubUserList,
    GetUserDetails,
    PlydetailsAPI,
    SubscriptionDetailsAPI,
    SubscriptionEndingSoon,
    SubscriptionforBusiness,
    TransactionAPI,
    UserdetailAPI,
)

router = routers.DefaultRouter()
router.register(r"Administrators", AdministratorAPI)
router.register(r"AppConfig", AppconfigAPI)
router.register(r"BusinessDetails", BusinessDetailsAPI)
router.register(r"Businesses", BusinessesAPI)
router.register(r"ClientsDetails", ClientDetailsAPI)
router.register(r"Developers", DevelopersAPI)
router.register(r"EstimateDetails", EstimatedetailAPI)
router.register(r"PlyDetails", PlydetailsAPI)
router.register(r"SubscriptionsDetails", SubscriptionDetailsAPI)
router.register(r"UserDetails", UserdetailAPI)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/AdminHome/", AdminHomeAPI.as_view()),
    path("api/AdminHome2/", AdminHomeAPI2.as_view()),
    path("api/AdminLogin/", AdminLoginAPI.as_view()), 
    path('api/BusinessSearch/search/', BusinessDetailsAPI.as_view({'get': 'search'})), 
    path("api/GetClientByB/<int:businessid>/", GetClientByB.as_view()),
    path("api/GetEstimatesByUB/<int:businessid>/<int:userid>/",GetEstimatesByUB.as_view()),
    path("api/GetEstimatesByClient/<int:clientid>/",GetEstimatesByClient.as_view()),
    path("api/GetSubUserList/<int:businessid>/", GetSubUserList.as_view()),
    path("api/GetUserDetails/<int:mobileno>/<str:androidid>/", GetUserDetails.as_view()),
    path("api/SubcriptionEndingSoon/", SubscriptionEndingSoon.as_view()),
    path("api/SubscriptionforBusiness/<int:businessid>", SubscriptionforBusiness.as_view()),
    path("api/TransactionDetails/",
        TransactionAPI.as_view({"get": "list", "post": "create"}),
    ),
    path("api/TransactionDetails/<int:businessid>/<int:pk>/",
        TransactionAPI.as_view(
            {
                "get": "retrieve",
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }),
    ),
    path('api/UserSearch/search/', UserdetailAPI.as_view({'get': 'search'})), 
    path("api/UploadCode/", Base64CodeView.as_view()),
    path("api/UploadCode/", Base64CodeView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

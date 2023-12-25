from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from apitest.views import (
    AdministratorAPI,
    AppconfigAPI,
    Base64CodeView,
    BusinessDetailsAPI,
    BusinessesAPI,
    ClientDetailsAPI,
    DevelopersAPI,
    SpecificBusinessAPI,
    SubscriptionDetailsAPI,
    EstimatedetailAPI,
    PlydetailsAPI,
    TransactionAPI,
    UserDetailsView,
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
router.register(r"TransactionDetails", TransactionAPI)
router.register(r"UserDetails", UserdetailAPI)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/UploadCode/", Base64CodeView.as_view()),
    path("api/EstimatesByBusinessID/<int:businessid>/", SpecificBusinessAPI.as_view()),
    path('api/UsersByRole/<int:user_id>/', UserDetailsView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from apitest.views import AdministratorAPI, AppconfigAPI, BusinessDetailsAPI, BusinessesAPI, ClientDetailsAPI, DevelopersAPI, SubscriptionDetailsAPI, EstimatedetailAPI, PlydetailsAPI, TransactionAPI, UserdetailAPI
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'Administrators', AdministratorAPI)
router.register(r'AppConfig', AppconfigAPI)
router.register(r'Business Details', BusinessDetailsAPI)
router.register(r'Businesses', BusinessesAPI)
router.register(r'Clients Details', ClientDetailsAPI)
router.register(r'Developers', DevelopersAPI)
router.register(r'Estimate Details', EstimatedetailAPI)
router.register(r'Ply Details', PlydetailsAPI)
router.register(r'Subscriptions Details', SubscriptionDetailsAPI)
router.register(r'Transaction Details', TransactionAPI)
router.register(r'User Details', UserdetailAPI)

urlpatterns = [
    path('api/', include(router.urls))
    # path('All Clients/', Clients.as_view({'get': 'list'})),
    # path('Client Details/<int:pk>/', Clients.as_view({'get': 'retrieve'})),
    # path('Add Client/', Clients.as_view({'post': 'create'})),
    # path('Update Client/<int:pk>/', Clients.as_view({'put': 'update'})),
    # path('Partial_Update Client/<int:pk>/', Clients.as_view({'patch': 'partial_update'})),
    # path('Delete Client/<int:pk>/', Clients.as_view({'delete': 'destroy'})),
    # path('All Subscriptions/', Subscription.as_view({'get': 'list'})),
    # path('Subscription Details/<int:pk>/', Subscription.as_view({'get': 'retrieve'}))
]

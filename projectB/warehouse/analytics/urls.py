# analytics/urls.py
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('reports', views.InventoryReportViewSet)
router.register('alerts', views.StockAlertViewSet)

urlpatterns = router.urls

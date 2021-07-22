from django.contrib import admin
from django.urls import include, path
from stockmgmgt import views
from django.contrib import admin

admin.site.site_header = "Wabcom"
admin.site.index_template = "admin/custom_index.html"
admin.site.enable_nav_sidebar = False
admin.autodiscover()

urlpatterns = [
    path('', views.home, name='home'),
    path('list_items/', views.list_items, name='list_items'),
    path('add_items/', views.add_items, name='add_items'),
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('stock_detail/<str:pk>/', views.stock_detail, name="stock_detail"),
    path('issue_items/<str:pk>/', views.issue_items, name="issue_items"),
    path('receive_items/<str:pk>/', views.receive_items, name="receive_items"),
    path('list_history/', views.list_history, name='list_history'),
    path('report/', views.report, name='report'),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
] 
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transfer/', views.transfer_view, name='transfer'),
    path('history/', views.history_view, name='history'),
    path('receipt/<int:tx_id>/', views.receipt_view, name='receipt'),
    path('loan/', views.loan_application_view, name='loan_application'),
    path('atm-request/', views.atm_request_view, name='atm_request'),
    path('', views.dashboard_view, name='home'),
]

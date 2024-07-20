from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="home"),
     path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('account/create', create_account, name='create_account'),
    path('dashboard/<str:username>', dashboard, name='dashboard'),
    path('invoice/<str:id>', payment_invoice, name='invoice'),
    path('account/transections', transection, name='transections'),
    
    path('validate_account/', validate_and_fetch_account, name='validate_and_fetch_account'),
    # path('deposit/', deposit_amount, name='deposit'),
    path('withdraw/', withdraw_amount, name='withdraw'),
]

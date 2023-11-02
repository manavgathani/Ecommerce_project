from django.urls import path
from . import views
urlpatterns = [
   path('',views.index,name='index'),
   path('signup/',views.signup,name='signup'),
   path('login/',views.login,name='login'),
   path('logout/',views.logout,name='logout'),
   path('change-password/',views.change_password,name='change-password'),
   path('profile/',views.profile,name='profile'),
   path('forgot-password/',views.forgot_password,name='forgot-password'),
   path('verify-otp/',views.verify_otp,name='verify-otp'),
   path('new-password/',views.new_password,name='new-password'),
   path('seller_index/',views.seller_index,name='seller_index'),
   path('seller_add_product/',views.seller_add_product,name='seller_add_product'),
   path('seller_view_product/',views.seller_view_product,name='seller_view_product'),
   path('seller_product_details/<int:pk>/',views.seller_product_details,name='seller_product_details'),
   path('seller_edit_product/<int:pk>/',views.seller_edit_product,name='seller_edit_product'),
    path('seller_delete_product/<int:pk>/',views.seller_delete_product,name='seller_delete_product'),
]
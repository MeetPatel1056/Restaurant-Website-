from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index, name ='home'),
    path('menu',views.Menu,name="Menu"),
    path('event',views.event,name='event'),
    path('sign_up',views.Sign_Up,name='Sign_Up'),
    path('login',views.Login,name='Login'),
    path('CheckLogin', views.CheckLogin, name="CheckLogin"),
    path('logout', views.Logout, name='logout'),
    path('edit_profile/', views.editprofile, name='edit_profile'),
    path('updateprofile',views.updateprofile,name="update"),
    path('forgot',views.forgot,name="Forgot"),
    path('forgot_password', views.forgotpassword, name='forgot_password'),
    path('insert', views.insertdata, name="insert"),
    path('contact',views.Contact,name ='contact'),
    path('insert_contact', views.insert_contact, name ='contact'),
    path('booking', views.Booking, name='booking'),
    path('insert_booking', views.insert_booking, name='insert_booking'),
    path('<int:product_id>', views.product_details, name='product_details'),  # Product details route
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<int:order_id>', views.order_success_view, name='order_success'),
    path('order-history/', views.order_history_view, name='order_history'),
    path('booking-history/', views.booking_history, name='booking_history'),
]

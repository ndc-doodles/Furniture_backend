from django.urls import path, re_path
from . views import*
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    # path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


    path('dashboard', views.dashboard, name="dashboard"),
    path('listing', views.admin_productlisting, name="listing"),
    path('admin_contact', views.admin_contact, name="admin_contact"),
    path('admin_enquiry', views.admin_enquiry, name="admin_enquiry"),
    path('category', views.category, name="category"),
    

    path('contact', views.contact, name="contact"),
    path('about',views.about, name="about"),
    path('product',views.product, name="product"), 
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('base',views.base, name="base"),
    re_path(r'^.*$', views.index, name="redirect_to_index"),

]
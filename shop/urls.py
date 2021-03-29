from django.urls import path

from . import views

urlpatterns = [
    path('', views.AboutView.as_view(), name='aboutme'),
    path('aboutme/', views.AboutView.as_view(), name='aboutme'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout_page'),
    path(r'activation/<id>/<token>', views.ActivationView.as_view(), name='activation'),
    path('goods/', views.GoodsListView.as_view(), name='all_goods'),
    path('add_good', views.AddProductView.as_view(), name='add_good'),
    path('add_to_cart/<id>', views.AddToCart.as_view(), name='add_to_cart'),
    path('delete_from_cart/<id>', views.DeleteFromCart.as_view(), name='delete_from_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('category/<id>', views.CategoryProductList.as_view(), name='category_list')
]

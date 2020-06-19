from django.urls import path

from .views.RestaurantViews import RestaurantListView
from .views.OrderViews import OrderListView
from .views.ProductViews import ProductListView, AddProductView, UpdateProductView, DeleteProductView
from .views.AuthViews import LoginView, LogoutView

app_name = "restaurateur"

urlpatterns = [

    path('products/', ProductListView.as_view(), name="ProductsView"),
    path('products/add/', AddProductView.as_view(), name="AddProductView"),
    path('products/<int:pk>/edit/', UpdateProductView.as_view(), name="UpdateProductView"),
    path('products/<int:pk>/delete/', DeleteProductView.as_view(), name="DeleteProductView"),

    path('restaurants/', RestaurantListView.as_view(), name="RestaurantView"),

    path('orders/', OrderListView.as_view(), name="OrderListView"),

    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
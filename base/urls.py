from django.urls import path 
from . import views 

urlpatterns = [
    # path("", views.index, name="index"),
    
    path("create_product_category/", views.create_product_category, name="create_product_category"),
    path("get_all_product_categories/", views.get_all_product_categories, name="get_all_product_categories"),
    path("add_new_product/", views.add_new_product, name="add_new_product"),
    path("get_all_products/", views.get_all_products, name="get_all_products"),
    path("get_all_products_inside_category/<str:category_name>/", views.get_all_products_inside_category, name="get_all_products_inside_category"),
    path("create_product_review/", views.create_product_review, name="create_product_review"),
    path("get_products_review/<uuid:product_id>/", views.get_products_review, name="get_products_review"),
]

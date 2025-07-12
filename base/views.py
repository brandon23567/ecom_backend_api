from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import *
from rest_framework import status

# @api_view(["GET"])
# def index(request):
#     return Response({ "message": "This is index page" })


# @api_view(["GET"])
# def new_test_path(request):
#     return Response({ "message": "This is a test path to see my github webhook" })


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_product_category(request):
    category_name = request.data.get("category_name")
    category_description = request.data.get("category_description")
    category_header_image = request.FILES.get("category_header_image")
    
    if not category_name or not category_description or not category_header_image:
        return Response({ "message": "All inputs are required please" }, status=status.HTTP_400_BAD_REQUEST)
    
    new_category_instance = ProductCategory.objects.create(
        category_name=category_name,
        category_description=category_description,
        category_header_image=category_header_image
    )
    
    new_category_instance.save()
    
    return Response({ "message": "New category was addedd" }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_product_categories(request):
    categories_array = []
    
    all_categories_from_db = ProductCategory.objects.all()
    
    for category in all_categories_from_db:
        single_category_data = {
            "category_name": category.category_name,
            "category_description": category.category_description,
            "category_header_image": category.category_header_image.url
        }
        
        categories_array.append(single_category_data)
        
    return Response({ "categories": categories_array }, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_new_product(request):
    current_user = request.user
    
    product_title = request.data.get("product_title")
    product_category_name = request.data.get("product_category")
    product_description = request.data.get("product_description")
    product_price = request.data.get("product_price")
    product_header_image = request.FILES.get("product_header_image")
    product_quantity = request.data.get("product_quantity")
    
    try:
        product_category_model_instance = ProductCategory.objects.get(category_name=product_category_name)
        
        new_product_instance = Product.objects.create(
            user=current_user,
            product_title=product_title, 
            product_category=product_category_model_instance, 
            product_description=product_description, 
            product_price=product_price, 
            product_header_image=product_header_image, 
            product_quantity=product_quantity 
        )
        
        new_product_instance.save()
        
        return Response({ "message": "New product was addedd to db" }, status=status.HTTP_201_CREATED)
    
    except ProductCategory.DoesNotExist:
        return Response({ "message": "Requested category does not exist, please create a new category" }, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_products(request):
    current_user = request.user 
    
    all_products_array = []
    
    products_from_db = Product.objects.all()
    
    for single_product in products_from_db:
        single_product_data = {
            "product_title": single_product.product_title,
            "product_category": single_product.product_category,
            "product_description": single_product.product_description,
            "product_price": single_product.product_price,
            "product_header_image": single_product.product_header_image.url,
            "product_quantity": single_product.product_quantity,
        }
        
        all_products_array.append(single_product_data)
        
    return Response({ "all_products": all_products_array }, status=status.HTTP_200_OK)



@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_products_inside_category(request, category_name):
    current_user = request.user 
    
    try:
        category_model_instance = ProductCategory.objects.get(category_name=category_name)
        
        products_array = []
        
        all_products_for_category = Product.objects.filter(product_category=category_model_instance)
        
        for single_product in all_products_for_category:
            single_product_details = {
                "product_title": single_product.product_title,
                "product_description": single_product.product_description,
                "product_price": single_product.product_price,
                "product_header_image": single_product.product_header_image.url,
                "product_quantity": single_product.product_quantity,
                "product_category": single_product.product_category,
            }
            
            products_array.append(single_product_details)
            
        return Response({ "products_inside_category": products_array }, status=status.HTTP_200_OK)
            
    except ProductCategory.DoesNotExist:
        return Response({ "message": "Model instance not found" }, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_product_review(request):
    current_user = request.user 
    review_rating = request.data.get("review_rating")
    review_body = request.data.get("review_body")
    
    product_id = request.data.get("product_id")
    
    if not product_id:
        return Response({ "message": "Unique id needed to leave a review for the specific product" }, status=status.HTTP_400_BAD_REQUEST)
    
    
    try:
        associated_product_instance = Product.objects.get(product_unique_id=product_id)
        
        new_review_instance = ProductReview.objects.create(
            user=current_user,
            review_rating=review_rating,
            review_body=review_body,
            associated_product=associated_product_instance
        )
        
        new_review_instance.save()
        
        return Response({ "message": "Product review has been published" }, status=status.HTTP_201_CREATED)
    
    except Product.DoesNotExist:
        return Response({ "message": "Requested product not found so we cannot add a review" }, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_products_review(request, product_id):
    current_user = request.user 
    
    if not product_id:
        return Response({ "message": "Product id is required to get the reviews of the products" }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        associated_product_model_instance = Product.objects.get(product_unique_id=product_id)
        
        product_reviews_array = []
        
        all_product_reviews_from_db = ProductReview.objects.filter(associated_product=associated_product_model_instance)
        
        for single_review in all_product_reviews_from_db:
            single_review_data = {
                "review_rating": single_review.review_rating,
                "review_body": single_review.review_body
            }
            
            product_reviews_array.append(single_review_data)
            
        return Response({ "product_reviews": product_reviews_array }, status=status.HTTP_200_OK)
        
    except Product.DoesNotExist:
        return Response({ "message": "No such product was found in our system" }, status=status.HTTP_400_BAD_REQUEST)
    
    
    
from django.db import models
from authentication.models import User 
import uuid
from django.core.validators import MinValueValidator


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    category_description = models.TextField()
    category_header_image = models.ImageField(upload_to="categories_header_images/", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return self.category_name
    
    
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    product_title = models.CharField(max_length=200)
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_header_image = models.ImageField(upload_to="products_header_images/")
    date_uploaded = models.DateTimeField(auto_now_add=True)
    product_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    def __str__(self):
        return self.product_title
    

class ProductImage(models.Model):
    image = models.ImageField(upload_to="products_extra_images/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.product_title
    
    
REVIEW_RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review_rating = models.PositiveSmallIntegerField(choices=REVIEW_RATING_CHOICES)
    review_body = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    associated_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.review_body
from django.contrib import admin
from .models import *

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductReview)

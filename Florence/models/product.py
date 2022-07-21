from django.db import models
from .category import Category
class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    quantity=models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    image = models.ImageField(upload_to='productsimg/')

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()
            
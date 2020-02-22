from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api.models import TimeStamp, BaseNameModel, BaseUniqueNameModel, Seller, Buyer
from api.constants import CONST_PRODUCT_ANSWER_LENGTH, CONST_PRODUCT_QUESTION_LENGTH, CONST_PRODUCT_ID_LENGTH


class Product(BaseNameModel):
    """
    model contains product data
    """
    categories = models.ManyToManyField("Category")
    product_id = models.CharField(max_length=CONST_PRODUCT_ID_LENGTH)
    base_price = models.PositiveIntegerField()
    seller_price = models.PositiveIntegerField(null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    discount = models.PositiveIntegerField(default=0)


class Category(BaseUniqueNameModel):
    """
    Category model
    """
    pass


class ProductImages(TimeStamp):
    """
    model containing images for product
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images")


class ProductQuestions(TimeStamp):
    """
    model contains question asked about products
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    question = models.TextField(max_length=CONST_PRODUCT_QUESTION_LENGTH)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)

class ProductAnswers(TimeStamp):
    """
    model contains answers posted by seller for asked questions on product
    """
    answer = models.TextField(max_length=CONST_PRODUCT_ANSWER_LENGTH)
    question = models.OneToOneField(ProductQuestions, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)

class Reviews(BaseNameModel):
    """
    model contain reviews for product
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="reviews_images", null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)


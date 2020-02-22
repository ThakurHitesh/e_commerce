from rest_framework import serializers
from api.models import Category, Product, ProductQuestions, ProductAnswers, Reviews, ProductImages

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'

class ProductQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductQuestions
        fields = '__all__'

class ProductAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAnswers
        fields = '__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'
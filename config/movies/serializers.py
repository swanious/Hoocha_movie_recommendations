from rest_framework import serializers
from .models import Oneline, Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['title', 'content',]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content',]
        

class OnelineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Oneline
        fields = ['content', 'vote_rating']
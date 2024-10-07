from .models import *

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        # Adding the below line made it work for me.
        instance.is_active = True
        if password is not None:
            # Set password does the hash, so you don't need to call make_password
            instance.set_password(password)
        instance.save()
        return instance


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['title', 'year', 'genre', 'duration', 'rating']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['film', 'author', 'text', 'rating']

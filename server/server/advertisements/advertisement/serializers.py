from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from .models import Advertisement, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class AdvertisementSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        """
        Create and return a new advertisement instance, given the validated data
        """
        advert = Advertisement(title=validated_data['title'],
        text=validated_data['text'], owner=validated_data["owner"])
        advert.save()
        for tag in validated_data['tags']:
            try:
                advert_tag = Tag.objects.get(name=tag['name'])
            except Tag.DoesNotExist:
                # if tag does not exist in database, create it.
                advert_tag = Tag(name=tag['name'])
                advert_tag.save()
            advert.tags.add(advert_tag)
        advert.save()
        return advert

    def update(self, instance, validated_data):
        """
        Update and return a new advertisement instance, given the validated data
        """
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.tags.clear() # clear tags list and create new
        for tag in validated_data['tags']:
            try:
                advert_tag = Tag.objects.get(name=tag['name'])
            except Tag.DoesNotExist:
                advert_tag = Tag(name=tag['name'])
                advert_tag.save()
            instance.tags.add(advert_tag)
        instance.save()
        return instance

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'text', "creation_date", 'tags', 'owner']
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    advertisements = serializers.PrimaryKeyRelatedField(many=True,
    queryset=Advertisement.objects.all())
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data
        """
        user = User.objects.create_user(username=validated_data['username'],
        password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'advertisements', 'password']

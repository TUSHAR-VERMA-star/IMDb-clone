from rest_framework import serializers
from watchlist_app.models import Review, Watchlist, StreamPlatform


class StreamPlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = StreamPlatform
        fields = "__all__"


class WatchlistSerializer(serializers.ModelSerializer):

    platform_name = serializers.StringRelatedField(source='platform.name',read_only = True)

    class Meta:
        model = Watchlist
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)

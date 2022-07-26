from django.shortcuts import render
from django.http import HttpResponse
from yaml import serialize
from watchlist_app.models import Watchlist, StreamPlatform, Review
from rest_framework import filters, generics, status, viewsets
from watchlist_app.api import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from watchlist_app.api.permissions import IsReviewUserOrReadOnly


class WatchlistGV(APIView):
    def get(self, request):
        movies = Watchlist.objects.all()
        serializer = serializers.WatchlistSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetails(APIView):
    def get(self, request, pk):
        data = Watchlist.objects.get(pk=pk)
        serializer = serializers.WatchlistSerializer(data)
        return Response(serializer.data)

    def put(self, request, pk):
        originalData = Watchlist.objects.get(pk=pk)
        serializer = serializers.WatchlistSerializer(
            originalData, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = Watchlist.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StreamingPlatformGV(generics.ListCreateAPIView):
    serializer_class = serializers.StreamPlatformSerializer

    def get_queryset(self):
        return StreamPlatform.objects.all()


class StreamingPlatformDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.StreamPlatformSerializer
    queryset = StreamPlatform.objects.all()


class ReviewList(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    queryset = Review.objects.all()


class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        review_user = self.request.user
        watchlist = Watchlist.objects.get(pk=pk)
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")
        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (
                watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)

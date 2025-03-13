from rest_framework import generics
from .mixins import (
    DisablePaginationMixin
)


class CustomListCreateAPIView(DisablePaginationMixin,
                              generics.ListCreateAPIView):
    pass


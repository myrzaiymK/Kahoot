from rest_framework import filters
from .models import Player


class PlayerSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['name']
        return super().get_search_fields(view, request)

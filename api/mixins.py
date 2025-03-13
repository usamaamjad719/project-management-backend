class DisablePaginationMixin:
    """
    A mixin to disable pagination dynamically based on a query parameter.
    """
    def paginate_queryset(self, queryset):
        disable_pagination = self.request.query_params.get('disablePagination', '').lower() == 'true'
        if disable_pagination:
            return None
        return super().paginate_queryset(queryset)

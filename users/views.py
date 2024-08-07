from rest_framework.viewsets import ModelViewSet
from django.http import Http404
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'telegram_id'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Make sure to capture the custom field from the URL.
        telegram_id = self.kwargs.get(self.lookup_field)
        obj = queryset.filter(telegram_id=telegram_id).first()

        # Optionally, handle the case where no object is found
        if obj is None:
            raise Http404("No User found matching the given telegram_id.")

        # This will check for permissions as well if any are set up
        self.check_object_permissions(self.request, obj)

        return obj
1


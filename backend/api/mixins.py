from rest_framework import mixins, viewsets


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Сборный вьюсет для обработки экземпляров моделей Follow, Favorite, Purchase"""

    pass

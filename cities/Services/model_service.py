class ModelService:

    def create_object(self, serializer):
        serializer.save()
        return serializer
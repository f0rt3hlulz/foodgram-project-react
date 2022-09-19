from rest_framework import status
from rest_framework.response import Response


def add_or_del_obj(pk, request, param, serializer_c):
    obj_bool = param.filter(pk=pk).exists()
    if request.method == 'DELETE' and obj_bool:
        param.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'POST' and not obj_bool:
        param.add(pk)
        serializer = serializer_c(
            param.get(pk=pk),
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)

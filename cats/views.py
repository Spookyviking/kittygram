from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Cat
from .serializers import CatSerializer

# View-функция cat_list() будет обрабатывать только запросы GET и POST, 
# запросы других типов будут отклонены,
# так что в теле функции их можно не обрабатывать
@api_view(['GET', 'POST'])
def cat_list(request):
    # Обработчик для POST-запросов.
    if request.method == 'POST':
        serializer = CatSerializer(data=request.data)
# GET-запросы разрешены в декораторе, но для них нет обработчика, 
# поэтому в ответ на GET-запрос вернётся ошибка 
# 500 Internal Server Error.
# Допишем этот обработчик позже.

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    cats = Cat.objects.all()
    serializer = CatSerializer(cats, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])  # Применили декоратор и указали разрешённые методы
def hello(request):
    # По задумке, в ответ на POST-запрос нужно вернуть JSON с теми данными, 
    # которые получены в запросе.
    # Для этого в объект Response() передаём словарь request.data. 
    if request.method == 'POST':
        return Response({'message': 'Получены данные', 'data': request.data})

    # В ответ на GET-запрос нужно вернуть JSON
    # Он тоже будет создан из словаря, переданного в Response()
    return Response({'message': 'Это был GET-запрос!'})

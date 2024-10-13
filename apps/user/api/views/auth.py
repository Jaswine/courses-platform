from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from apps.user.api.serializers.user_serializers import UserSerializer, UserBaseSerializer
from apps.user.api.utils.token_util import generate_tokens
from apps.user.utils.auth_util import authenticate


@api_view(['POST'])
def sign_in(request):
    """
        Вход пользователя в аккаунт
    """
    # Проверка валидности email и пароля
    serializer = UserBaseSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors,
                    status=HTTP_400_BAD_REQUEST)

    # Аутентификация пользователя по электронной почте и паролю
    user = authenticate(serializer.validated_data.get('email'),
                        serializer.validated_data.get('password'))
    if not user:
        return Response({'error': 'Invalid email or password'},
                    status=HTTP_403_FORBIDDEN)

    # Генерация токенов
    access, refresh = generate_tokens(user)
    return Response({'access': access, 'refresh': refresh},
                    status=HTTP_200_OK)


@api_view(['POST'])
def sign_up(request):
    """
        Регистрация пользователя
    """
    # Создание нового пользователя
    user = UserSerializer(data=request.data)
    if user.is_valid():
        user = user.save()
        # Генерация токенов
        access, refresh = generate_tokens(user)
        return Response({'access': access, 'refresh': refresh},
                        status=HTTP_200_OK)
    return Response(user.errors,
                    status=HTTP_400_BAD_REQUEST)
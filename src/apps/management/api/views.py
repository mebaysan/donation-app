from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework import views, status
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    CreateAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.management.api.serializers import (
    UserSerializer,
    UserRegisterSerializer,
    PasswordChangeSerializer,
    ObtainTokenSerializer,
    ForgotPasswordSerializer,
    CountrySerializer,
    CountryDetailSerializer,
)
from apps.management.models import Country
from apps.management.authentication import JWTAuthentication
from helpers.communication.email import send_password_reset_email
import random
import string

User = get_user_model()


class HealthCheckView(views.APIView):
    """
    A simple healthcheck endpoint that returns a 200 OK status if the API is up and running.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return Response({"status": "ok"})


class GeneratePasswordView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """Generates a random password."""
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = "".join(random.choices(alphabet, k=18))
        return Response({"password": password})


class ObtainTokenView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_phone_number = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = User.objects.filter(username=username_or_phone_number).first()
        if user is None:
            user = User.objects.filter(phone_number=username_or_phone_number).first()

        if user is None or not user.check_password(password):
            return Response(
                {"details": "Lütfen geçerli giriş bilgileri girin."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)

        return Response({"token": jwt_token}, status=status.HTTP_200_OK)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data.pop("confirm_new_password")
            try:
                user = User.objects.create_user(**validated_data)
                return Response(
                    {"details": "Kullanıcı başarıyla oluşturuldu."},
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                return Response(
                    {
                        "details": "Kayıt etmek istediğiniz bilgiler başka bir kullanıcı tarafından alınmış."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except ValidationError:
                return Response(
                    {
                        "details": "Kayıt etmek istediğiniz bilgiler başka bir kullanıcı tarafından alınmış."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception:
                return Response(
                    {"details": "Kullanıcı oluşturulurken hata."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.serializer_class(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except IntegrityError:
            return Response(
                {
                    "details": "Kayıt etmek istediğiniz bilgiler başka bir kullanıcı tarafından alınmış."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError:
            return Response(
                {
                    "details": "Kayıt etmek istediğiniz bilgiler başka bir kullanıcı tarafından alınmış."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"details": "Kullanıcı güncellenirken bir hata meydana geldi."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordChangeView(UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Yanlış parola."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                status=status.HTTP_200_OK,
                data={
                    "details": "Parola başarıyla değiştirildi.",
                },
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_phone_number = serializer.validated_data.get("username")

        user = User.objects.filter(username=username_or_phone_number).first()
        if user is None:
            user = User.objects.filter(phone_number=username_or_phone_number).first()

        if user is None:
            return Response(
                {"details": "Böyle bir kullanıcı bulunamadı."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        send_password_reset_email(user)

        return Response(
            {"details": "Parola sıfırlama maili gönderildi."}, status=status.HTTP_200_OK
        )


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]


class CountryDetailsAPIView(RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

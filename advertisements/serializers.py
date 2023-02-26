from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля "создатель" по-умолчанию. Текущий пользователь является создателем объявления,
        # изменить или переопределить его через API нельзя. Обратите внимание на `context` – он выставляется
        # автоматически через методы ViewSet. Само поле при этом объявляется как `read_only=True`.
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        request_method = self.context['request'].method
        creator = self.context['request'].user
        open_adv_count = Advertisement.objects.filter(creator=creator).filter(status='OPEN').count()

        if request_method == 'POST' and open_adv_count >= 10:
            raise ValidationError('У вас не может быть более 10 открытых запросов.')

        elif request_method in ['PATCH', 'PUT']:
            new_status = data.get('status')
            if new_status == 'OPEN':
                current_status = self.instance.status
                if current_status == 'CLOSED' and open_adv_count >= 10:
                    raise ValidationError('Объявление не открыть - у вас не может быть более 10 открытых объявлений.')
        return data


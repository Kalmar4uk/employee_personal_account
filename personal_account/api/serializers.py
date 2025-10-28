from django.db.models import Q
from django.utils import timezone
from downtimes.models import Downtime
from rest_framework import serializers
from rest_framework_simplejwt.token_blacklist.models import (BlacklistedToken,
                                                             OutstandingToken)
from users.models import GroupJob, User
from utils.functions import check_less_current_time, get_workshift_for_downtime


class TokenCreateSerializer(serializers.Serializer):
    email = serializers.CharField(
        required=True)
    password = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ("password", "email")

    def validate(self, data):
        user = User.objects.filter(email=data.get("email")).first()
        if not user or not user.check_password(data.get("password")):
            raise serializers.ValidationError(
                "Введены некорректные данные!"
            )
        return data


class TokenCreateSerializerV2(serializers.Serializer):
    username = serializers.CharField(
        required=True)
    password = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ("password", "email")

    def validate(self, data):
        email_or_username = data.get("username")
        user = User.objects.filter(
            Q(email=email_or_username) | Q(username=email_or_username)
        ).first()
        if not user or not user.check_password(data.get("password")):
            raise serializers.ValidationError(
                "Введены некорректные данные!"
            )
        return data


class UpdateTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    class Meta:
        fields = ("refresh_token",)

    def validate_refresh_token(self, data):
        if not (token := OutstandingToken.objects.get(token=data)):
            raise serializers.ValidationError(
                "Неизвестный refresh токен"
            )
        if self.context.get("request").user != token.user:
            raise serializers.ValidationError(
                "refresh токен не принадлежит пользователю"
            )
        if (
            token.expires_at <= timezone.now()
            or BlacklistedToken.objects.filter(token__token=data).exists()
        ):
            raise serializers.ValidationError(
                "Срок действия refresh токена уже истек"
            )
        return data


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField()

    class Meta:
        fields = ("access_token", "refresh_token", "token_type")


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "job_title",
            "group_job",
            "is_main"
        )


class UsersSerializerForGroupsJob(UsersSerializer):
    work_today = serializers.SerializerMethodField()

    class Meta(UsersSerializer.Meta):
        model = User
        fields = UsersSerializer.Meta.fields + ("work_today",)

    def get_work_today(self, obj):
        shift = obj.workshifts.filter(date_start=timezone.now().date()).first()
        holiday = obj.holidays.filter(date=timezone.now().date()).first()
        if not shift and holiday:
            return "Отпуск"
        if not shift and not holiday:
            return "Выходной"
        return f"{shift.time_start} - {shift.time_end}"


class UserSerializerForDowntime(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")


class GroupJobSerializer(serializers.ModelSerializer):
    employees = UsersSerializerForGroupsJob(many=True, source="users")

    class Meta:
        model = GroupJob
        fields = ("id", "title", "employees")


class ListGroupsJobSerializer(serializers.ModelSerializer):
    count_employees = serializers.SerializerMethodField()
    is_main = serializers.SerializerMethodField()

    class Meta:
        model = GroupJob
        fields = ("id", "title", "count_employees", "is_main")

    def get_count_employees(self, value):
        return value.users.count()

    def get_is_main(self, value):
        main = value.users.filter(is_main=True).first()
        return UsersSerializerForGroupsJob(main).data


class CreateAndUpdateSerializer(serializers.ModelSerializer):
    start_downtime = serializers.DateTimeField()
    end_downtime = serializers.DateTimeField()

    class Meta:
        model = Downtime
        fields = (
            "id",
            "service",
            "start_downtime",
            "end_downtime",
            "link_task",
            "description"
        )

    def validate(self, data):
        if data.get("end_downtime") < data.get("start_downtime"):
            raise serializers.ValidationError(
                "Дата и время старта не может быть меньше даты и времени конца"
            )
        return data

    def validate_start_downtime(self, data):
        if check_less_current_time(data=data):
            raise serializers.ValidationError(
                "Дата старта не может быть меньше текущего времени"
            )
        return data

    def validate_end_downtime(self, data):
        if check_less_current_time(data=data):
            raise serializers.ValidationError(
                "Дата конца не может быть меньше текущего времени"
            )
        return data

    def create(self, validated_data):
        downtime = Downtime.objects.create(**validated_data)
        start_downtime = validated_data.get("start_downtime")
        shifts = get_workshift_for_downtime(start_downtime=start_downtime)
        downtime.gsma_employee = shifts.employee
        downtime.save()
        return downtime

    def to_representation(self, instance):
        return DowntimeSerializer(instance, context={
            'request': self.context.get('request')
        }).data


class DowntimeSerializer(serializers.ModelSerializer):
    gsma_employee = UserSerializerForDowntime()

    class Meta:
        model = Downtime
        fields = (
            "id",
            "service",
            "start_downtime",
            "end_downtime",
            "link_task",
            "description",
            "gsma_employee"
        )


class CalendarSerializer(serializers.Serializer):
    date = serializers.DateField()
    type = serializers.CharField()
    time = serializers.CharField()


class UserCalendarSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    calendar = CalendarSerializer(many=True)

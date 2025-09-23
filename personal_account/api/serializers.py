from django.utils import timezone
from rest_framework import serializers

from users.models import GroupJob, User
from lk.models import Holiday, WorkShifts


class TokenSerializer(serializers.Serializer):
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


class CalendarSerializer(serializers.Serializer):
    date = serializers.DateField()
    type = serializers.CharField()
    time = serializers.CharField()


class WorkShiftsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkShifts
        fields = ("date_start", "date_end", "time_start", "time_end")

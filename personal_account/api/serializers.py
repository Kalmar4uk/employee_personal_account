from rest_framework import serializers

from lk.models import Holiday, WorkShifts
from users.models import GroupJob, User


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


class GroupJobSerializer(serializers.ModelSerializer):
    employees = UsersSerializer(many=True, source="users")

    class Meta:
        model = GroupJob
        fields = ("id", "title", "employees")


class ListGroupsJobSerializer(serializers.ModelSerializer):
    count_employees = serializers.SerializerMethodField()

    class Meta:
        model = GroupJob
        fields = ("id", "title", "count_employees")

    def get_count_employees(self, value):
        return value.users.count()


class WorkShiftsSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkShifts
        exclude = ["id", "employee", "type"]


class HolidaysSerializer(serializers.ModelSerializer):

    class Meta:
        model = Holiday
        exclude = ["employee", "status"]

from rest_framework import serializers
from apitest.models import (
    Administrators,
    Appconfig,
    Clientdetails,
    Subscriptiondetails,
    Businessdetails,
    Businesses,
    Developers,
    Estimatedetails,
    Plydetails,
    Transactiondetails,
    Userdetails,
)


class AdministratorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrators
        fields = "__all__"


class AppconfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appconfig
        fields = "__all__"


class BusinessdetailSerializer(serializers.ModelSerializer):
    estimate_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Businessdetails
        fields = "__all__"


class BusinessesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Businesses
        fields = "__all__"


class ClientdetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientdetails
        fields = "__all__"


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developers
        fields = "__all__"


class EstimatedetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimatedetails
        fields = "__all__"


class PlydetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plydetails
        fields = "__all__"


class SubscriptiondetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptiondetails
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactiondetails
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userdetails
        fields = "__all__"


class Base64CodeSerializer(serializers.Serializer):
    base64_code = serializers.CharField()

class AdminLoginSerializer(serializers.Serializer):
    adminname = serializers.CharField(required=True)
    adminpassword = serializers.CharField(required=True)
import os
import base64
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import (
    Administrators,
    Appconfig,
    Businessdetails,
    Businesses,
    Developers,
    Clientdetails,
    Subscriptiondetails,
    Estimatedetails,
    Plydetails,
    Transactiondetails,
    Userdetails,
)
from .serializers import (
    AdministratorsSerializer,
    AppconfigSerializer,
    Base64CodeSerializer,
    BusinessdetailSerializer,
    BusinessesSerializer,
    DeveloperSerializer,
    ClientdetailSerializer,
    SubscriptiondetailSerializer,
    EstimatedetailSerializer,
    PlydetailSerializer,
    TransactionSerializer,
    UserSerializer,
)


# API for Image Code
class Base64CodeView(APIView):
    serializer_class = Base64CodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            base64_code = serializer.validated_data["base64_code"]

            # Specify the file path for the "Image_Code.txt" file
            file_name = "Image_Code.txt"
            save_path = os.path.join(settings.MEDIA_ROOT, file_name)
            code_file_path = os.path.join(settings.MEDIA_ROOT, save_path)

            # Write the base64 code to the file, replacing existing content
            with open(code_file_path, "w") as code_file:
                code_file.write(base64_code)

            response_data = {
                "message": "Base64 code stored successfully",
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API for Administrator
class AdministratorAPI(ModelViewSet):
    queryset = Administrators.objects.all()
    serializer_class = AdministratorsSerializer

    def list(self, request, *args, **kwargs):
        try:
            admin = Administrators.objects.all()
            serializer = self.get_serializer(admin, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Admin Details",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = (
                "An error occurred while fetching administrators: {}".format(str(e))
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Administrator details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch administrator details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            adminpassword = request.data.get("adminpassword")
            hashpassword = make_password(adminpassword)
            request.data["adminpassword"] = hashpassword
            # print(check_password('Actual Password', 'encrypted password'))
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Administrator added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add administrator: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Administrator updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update administrator: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Administrator partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update administrator: {}".format(
                str(e)
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Administrator deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete administrator: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Appconfig
class AppconfigAPI(ModelViewSet):
    queryset = Appconfig.objects.all()
    serializer_class = AppconfigSerializer

    def list(self, request, *args, **kwargs):
        try:
            appconf = Appconfig.objects.all()
            serializer = self.get_serializer(appconf, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Appconfig",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "An error occurred while fetching appconfig: {}".format(
                str(e)
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Appconfig details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch appconfig details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Appconfig added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add appconfig: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Appconfig updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update appconfig: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Appconfig partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update appconfig: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Appconfig deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete appconfig: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Business Details
class BusinessDetailsAPI(ModelViewSet):
    queryset = Businessdetails.objects.all()
    serializer_class = BusinessdetailSerializer

    def list(self, request, *args, **kwargs):
        try:
            bdetails = Businessdetails.objects.all()
            serializer = self.get_serializer(bdetails, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Business Details",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = (
                "An error occurred while fetching business details: {}".format(str(e))
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Business details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch business details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Business details added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add business details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Business details updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update business details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Business details partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update business details: {}".format(
                str(e)
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Business details deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete business details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Businesses
class BusinessesAPI(ModelViewSet):
    queryset = Businesses.objects.all()
    serializer_class = BusinessesSerializer

    def list(self, request, *args, **kwargs):
        try:
            business = Businesses.objects.all()
            serializer = self.get_serializer(business, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Businesses",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = (
                "An error occurred while fetching all businesses: {}".format(str(e))
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Business details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch business details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Business added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add business: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Business updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update business: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Business partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update business: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Business deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete business: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Client Details
class ClientDetailsAPI(ModelViewSet):
    queryset = Clientdetails.objects.all()
    serializer_class = ClientdetailSerializer

    def list(self, request, *args, **kwargs):
        try:
            client = Clientdetails.objects.all()
            serializer = self.get_serializer(client, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Client details",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "An error occurred while fetching all clients: {}".format(
                str(e)
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Client details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch client details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Client added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add client: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Client details updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update client details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Client partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update client: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Client deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete client: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Developers
class DevelopersAPI(ModelViewSet):
    queryset = Developers.objects.all()
    serializer_class = DeveloperSerializer

    def list(self, request, *args, **kwargs):
        try:
            developer = Developers.objects.all()
            serializer = self.get_serializer(developer, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Developers",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = (
                "An error occurred while fetching all developers: {}".format(str(e))
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Developer details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch developer details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            developerpassword = request.data.get("developerpassword")
            hashpassword = make_password(developerpassword)
            request.data["developerpassword"] = hashpassword
            # print(check_password('Actual Password', 'encrypted password'))
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Developer added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add developer: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Developer updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update developer: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Developer partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update developer: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Developer deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete developer: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Estimatedetails
class EstimatedetailAPI(ModelViewSet):
    queryset = Estimatedetails.objects.all()
    serializer_class = EstimatedetailSerializer

    def list(self, request, *args, **kwargs):
        try:
            estimate = Estimatedetails.objects.all()
            serializer = self.get_serializer(estimate, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Estimates",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "An error occurred while fetching all estimates: {}".format(
                str(e)
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Estimate details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch estimate details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Estimate added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add estimate: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Estimate updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update estimate: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Estimate partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update estimate: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Estimate deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete estimate: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Plydetails
class PlydetailsAPI(ModelViewSet):
    queryset = Plydetails.objects.all()
    serializer_class = PlydetailSerializer

    def list(self, request, *args, **kwargs):
        try:
            ply = Plydetails.objects.all()
            serializer = self.get_serializer(ply, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Ply",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "An error occurred while fetching all ply: {}".format(
                str(e)
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Ply details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch ply details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Ply added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add ply: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Ply updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update ply: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Ply partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update ply: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Ply deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete ply: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Subscription
class SubscriptionDetailsAPI(ModelViewSet):
    queryset = Subscriptiondetails.objects.all()
    serializer_class = SubscriptiondetailSerializer

    def list(self, request, *args, **kwargs):
        try:
            subs = Subscriptiondetails.objects.all()
            serializer = self.get_serializer(subs, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Subscriptions",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = (
                "An error occurred while fetching all subscriptions: {}".format(str(e))
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Subscription details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch subscription details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Subscription added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add subscription: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Subscription updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update subscription: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Subcription partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update subcription: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Subscription deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete subscription: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Transaction
class TransactionAPI(ModelViewSet):
    queryset = Transactiondetails.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request, *args, **kwargs):
        try:
            transaction = Transactiondetails.objects.all()
            serializer = self.get_serializer(transaction, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Transactions",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = (
                "An error occurred while fetching all transactions: {}".format(str(e))
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Transaction details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch transaction details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Transaction added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add transaction: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Transaction updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update transaction: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Trasaction partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update transaction: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "Transaction deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete transaction: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for User Details
class UserdetailAPI(ModelViewSet):
    queryset = Userdetails.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        try:
            user = Userdetails.objects.all()
            serializer = self.get_serializer(user, many=True)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "All Users",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "An error occurred while fetching all users: {}".format(
                str(e)
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "User details fetch successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to fetch user details: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        try:
            userpassword = request.data.get("userpassword")
            hashpassword = make_password(userpassword)
            request.data["userpassword"] = hashpassword
            # print(check_password('Actual Password', 'encrypted password'))
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "User added successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_201_CREATED)
        except Exception as e:
            error_message = "Failed to add user: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "User updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to update user: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "User partially updated successfully",
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to partially update user: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_204_NO_CONTENT,
                "message": "User deleted successfully",
            }
            return Response(api_response, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_message = "Failed to delete user: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


# API for Estimates and clients for Specific BusinessID
class SpecificBusinessAPI(generics.ListAPIView):
    serialiazer_class = EstimatedetailSerializer

    def get_queryset(self):
        businessid = self.kwargs["businessid"]
        return Estimatedetails.objects.filter(businessid=businessid)
    

# API for user and admin
class UserDetailsView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        mobileno = self.request.query_params.get('mobileno')
        androidid = self.request.query_params.get('androidid')
        business_id = self.request.query_params.get('business_id')

        # Verify mobileno and androidid
        user = Userdetails.objects.filter(mobileno=mobileno, androidid=androidid).first()

        if user:
            # Check user role based on business_id
            if user.businessid == int(business_id):
                if user.userrole == 'admin':
                    # Display all records under that business id
                    queryset = Userdetails.objects.filter(businessid=business_id)
                else:
                    # Display record of that specific business id for user
                    queryset = Userdetails.objects.filter(businessid=business_id, userid=user.userid)
                return queryset
            else:
                return Userdetails.objects.none()  # Return an empty queryset if the user doesn't have access to this business_id
        else:
            return Userdetails.objects.none()  # Return an empty queryset if user credentials are invalid
import os
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Q, Max
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from urllib.parse import unquote
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
                "status" : "sucess",
                "code" : status.HTTP_200_OK,
                "message": "Base64 code stored successfully",
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        file_name = "Image_Code.txt"
        code_file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        try:
            with open(code_file_path, "r") as code_file:
                base64_code = code_file.read()

            response_data = {
                "status" : "success",
                "code" : status.HTTP_200_OK,
                "base64_code": base64_code,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except FileNotFoundError:
            error_data = {
                "status" : "error",
                "code" : status.HTTP_404_NOT_FOUND,
                "message": "File not found",
            }

            return Response(error_data, status=status.HTTP_404_NOT_FOUND)

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
            error_message = ("An error occurred while fetching administrators: {}".format(str(e)))
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            adminpassword = request.data.get("adminpassword")
            hashpassword = make_password(adminpassword)
            request.data["adminpassword"] = hashpassword
            # print(check_password('Actual Password', 'encrypted password'))
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
            adminpassword = request.data.get("adminpassword")
            hashpassword = make_password(adminpassword)
            request.data["adminpassword"] = hashpassword
            # print(check_password('Actual Password', 'encrypted password'))
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
                "code": status.HTTP_200_OK,
                "message": "Administrator deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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
                "code": status.HTTP_200_OK,
                "message": "Appconfig deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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
            contact_no = request.data.get('contactno')
            # Check if contactno already exists in Businessdetails
            existing_business = Businessdetails.objects.filter(contactno=contact_no).exists()
            if existing_business:
                error_response = {
                    "status": "error",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": f"Business with contactno {contact_no} already exists",
                }
                return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

            last_business = Businessdetails.objects.aggregate(Max('businessid'))
            last_business_id = last_business['businessid__max']

            # If the table is empty, set the initial businessid to 1
            if last_business_id is None:
                new_business_id = 1000000
            else:
                new_business_id = last_business_id + 1

            request.data['status'] = "Trial"
            request.data['multiuser'] = 0
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(businessid=new_business_id)  # Assuming 'businessid' is a field in your serializer
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
                "code": status.HTTP_200_OK,
                "message": "Business details deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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
                "code": status.HTTP_200_OK,
                "message": "Business deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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
            business_id = request.data.get("businessid")

            existing_clients = Clientdetails.objects.filter(businessid=business_id)
            max_client_id = existing_clients.aggregate(Max('clientid'))['clientid__max']

            if max_client_id is None:
                new_client_id = int(f"{business_id}00001")
            else:
                new_client_id = max_client_id + 1

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(clientid=new_client_id)

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
                "code": status.HTTP_200_OK,
                "message": "Client deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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
            developerpassword = request.data.get("developerpassword")
            hashpassword = make_password(developerpassword)
            request.data["developerpassword"] = hashpassword
            # print(check_password('Actual Password', 'encrypted password'))
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
            developerpassword = request.data.get("developerpassword")
            hashpassword = make_password(developerpassword)
            request.data["developerpassword"] = hashpassword
            # print(check_password('Actual Password', 'encrypted password'))
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
                "code": status.HTTP_200_OK,
                "message": "Developer deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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
            business_id = request.data.get("businessid")
            user_id = request.data.get("userid")
            client_id = request.data.get("clientid")

            existing_estimates = Estimatedetails.objects.filter(businessid=business_id, userid=user_id, clientid=client_id)
            max_estimate_id = existing_estimates.aggregate(Max('estimateid'))['estimateid__max']

            if max_estimate_id is None:
                new_estimate_id = int(f"{business_id}00001")
            else:
                new_estimate_id = max_estimate_id + 1

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(estimateid=new_estimate_id)

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
                "code": status.HTTP_200_OK,
                "message": "Estimate deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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
                "code": status.HTTP_200_OK,
                "message": "Ply deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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
                "code": status.HTTP_200_OK,
                "message": "Subscription deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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

    def retrieve(self, request, businessid, pk, *args, **kwargs):
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
            last_transaction = Transactiondetails.objects.aggregate(Max('transactionid'))
            last_transaction_id = last_transaction['transactionid__max']

            if last_transaction_id is None:
                new_transaction_id = 1
            else:
                new_transaction_id = last_transaction_id + 1

            request.data['transactionid'] = new_transaction_id  # Assuming 'transactionid' needs to be provided in the request data

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            transaction_instance = serializer.save()  # Save transaction and get the instance

            business_id = transaction_instance.businessid  # Assuming 'businessid' is a field in Transactiondetails
            business_details = Businessdetails.objects.get(businessid=business_id)

            # Assuming 'transactiondate' and 'subscriptiondate' are fields in respective models
            business_details.subscriptiondate = transaction_instance.transactiondate
            business_details.save()

            api_response = {
                "status": "success",
                "code": status.HTTP_201_CREATED,
                "message": "Transaction added successfully.",
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

    def update(self, request, businessid, pk, *args, **kwargs):
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

    def partial_update(self, request, businessid, pk, *args, **kwargs):
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

    def destroy(self, request, businessid, pk, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Transaction deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
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
            business_id = request.data.get("businessid")
            # userpassword = request.data.get("userpassword")
            # Assuming other fields such as androidid, deviceinfo are obtained similarly

            existing_users = Userdetails.objects.filter(businessid=business_id)
            max_user_id = existing_users.aggregate(Max('userid'))['userid__max']

            if max_user_id is None:
                new_user_id = int(f"{business_id}01")
            else:
                new_user_id = max_user_id + 1

            business = Businessdetails.objects.get(businessid=business_id)

            last_two_digits = int(str(new_user_id)[-2:])

            if last_two_digits == 1:
                username = business.businessname
                mobileno = business.contactno
                userrole = 'Admin'
            else:
                # Retrieve username, mobileno, and other required fields from the request
                username = request.data.get("username")
                mobileno = request.data.get("mobileno")
                userrole = 'User'

            user_data = {
                'userid': new_user_id,
                'businessid': business_id,
                'userpassword': 'dsbox@123',  # Use the provided userpassword
                'username': username,  # Use the determined username
                'mobileno': mobileno,  # Use the determined mobileno
                'userrole': userrole,
                'useraccess': 2,
                'androidid': request.data.get("androidid"),  # Get androidid from request
                'deviceinfo': request.data.get("deviceinfo"),  # Get deviceinfo from request
                'status': 'Active'
            }

            serializer = self.get_serializer(data=user_data)
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
            userpassword = request.data.get("userpassword")
            hashpassword = make_password(userpassword)
            request.data["userpassword"] = hashpassword
            # print(check_password('Actual Password', 'encrypted password'))
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
            userpassword = request.data.get("userpassword")
            hashpassword = make_password(userpassword)
            request.data["userpassword"] = hashpassword
            # print(check_password('Actual Password', 'encrypted password'))
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
                "code": status.HTTP_200_OK,
                "message": "User deleted successfully",
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to delete user: {}".format(str(e))
            error_response = {
                "status": "error",
                "code": status.HTTP_400_BAD_REQUEST,
                "message": error_message,
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

# API for Client List by ClientID, BusinessID
class GetClientByB(generics.ListAPIView):
    serializer_class = ClientdetailSerializer

    def get_queryset(self):
        # client_id = self.kwargs["clientid"]
        # user_id = self.kwargs["userid"]
        business_id = self.kwargs["businessid"]
        # return Clientdetails.objects.filter(clientid=client_id, userid=user_id)
        return Clientdetails.objects.filter(businessid=business_id)

    def list(self, request, *args, **kwargs):
        # client_id = self.kwargs["clientid"]
        # user_id = self.kwargs["user_id"]
        business_id = self.kwargs["businessid"]
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': f'Client list under {business_id}',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'status': 'failure',
                'code': status.HTTP_404_NOT_FOUND,
                'message': f'Client not found',
                'data': []
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
    
# API for Estimates by UserID and BusinessID
class GetEstimatesByUB(generics.ListAPIView):
    serializer_class = EstimatedetailSerializer

    def get_queryset(self):
        business_id = self.kwargs.get("businessid")
        user_id = self.kwargs.get("userid")
        queryset = Userdetails.objects.filter(businessid=business_id, userid=user_id)
        return queryset

    def get(self, request, *args, **kwargs):
        business_id = self.kwargs.get("businessid")
        user_id = self.kwargs.get("userid")

        try:
            user = Userdetails.objects.get(userid=user_id)

            if user.userrole == "Admin":
                queryset = Estimatedetails.objects.filter(businessid=user.businessid)
            elif user.userrole == "User":
                queryset = Estimatedetails.objects.filter(businessid=user.businessid, userid=user_id)
            else:
                return Response({'status': 'error', 'message': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(queryset, many=True)
            data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': f'Estimates for {business_id} by user {user_id}',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)

        except Userdetails.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Estimatedetails.DoesNotExist:
            return Response({'status': 'error', 'message': 'Estimates not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API for Estimates by ClientID
class GetEstimatesByClient(generics.ListAPIView):
    serializer_class = EstimatedetailSerializer

    def get_queryset(self):
        client_id = self.kwargs["clientid"]
        return Estimatedetails.objects.filter(clientid=client_id)

    def list(self, request, *args, **kwargs):
        client_id = self.kwargs["clientid"]
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': f'Estimates for ClientID: {client_id}',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'status': 'failure',
                'code': status.HTTP_404_NOT_FOUND,
                'message': f'No estimates for ClientID: {client_id}',
                'data': []
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

# API for User by deviceinfo and mobilenumber
class GetUserDetails(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        mobile_no = self.kwargs.get("mobileno")
        device_info = self.kwargs.get("deviceinfo")
        
        # Decode URL-encoded parameters to handle spaces properly
        device_info = unquote(device_info)
        
        # Remove leading and trailing spaces from the device_info value
        device_info = device_info.strip()

        # Split the device_info string by spaces and create a query for each word
        device_info_query = Q()
        for word in device_info.split():
            device_info_query &= Q(deviceinfo__icontains=word)

        queryset = Userdetails.objects.filter(mobileno=mobile_no).filter(device_info_query)
        return queryset

    def get(self, request, *args, **kwargs):
        mobile_no = self.kwargs.get("mobileno")
        device_info = self.kwargs.get("deviceinfo")
        
        # Decode URL-encoded parameters for response message
        trimmed_device_info = unquote(device_info).strip()

        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        if queryset.exists():
            data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': f'Record under {mobile_no} and {trimmed_device_info}',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)

        data = {
            'status': 'error',
            'code': status.HTTP_404_NOT_FOUND,
            'message': f'No record for {mobile_no} and {trimmed_device_info}',
            'data': []
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)

# API for Admin home page
class AdminHomeAPI(generics.ListAPIView):
    serializer_class = BusinessdetailSerializer  

    def get_serializer(self, *args, **kwargs):
        return None  # Override get_serializer method to return None

    def get(self, request, *args, **kwargs):
        try:
            total_count = Businessdetails.objects.count()
            active_count = Businessdetails.objects.filter(status="Active").count()
            trial_count = Businessdetails.objects.filter(status="Trial").count()

            today = datetime.now().date()
            current_week_start = today - timedelta(days=today.weekday())
            current_week_end = current_week_start + timedelta(days=6)
            past_week_start = current_week_start - timedelta(days=7)
            past_week_end = current_week_start - timedelta(days=1)

            current_week_records = self.get_queryset().filter(activationdate__range=(current_week_start, current_week_end))
            past_week_records = self.get_queryset().filter(activationdate__range=(past_week_start, past_week_end))

            current_week_data = self.get_records_per_day(current_week_records, current_week_start, current_week_end)
            past_week_data = self.get_records_per_day(past_week_records, past_week_start, past_week_end)

            response_data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'All businesses information',
                'data': {
                    'totalBusiness': total_count,
                    'activeBusiness': active_count,
                    'trialBusiness': trial_count,
                    'currentWeekRecords': current_week_data,
                    'pastWeekRecords': past_week_data,
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Exception occurred:", e)
            error_message = "Failed to retrieve business details."
            response_data = {
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': error_message,
                'data': None
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        return Businessdetails.objects.all()

    def get_records_per_day(self, queryset, start_date, end_date):
        date_records = {}
        current_date = start_date
        while current_date <= end_date:
            day_name = current_date.strftime('%A').lower()  # Get the day name from the date
            count = queryset.filter(activationdate=current_date).count()
            date_records[day_name] = count
            current_date += timedelta(days=1)
        return date_records

# API based on subscription for Admin
class AdminHomeAPI2(generics.ListAPIView):
    serializer_class = BusinessdetailSerializer  

    def get_queryset(self):
        return Businessdetails.objects.order_by('-subscriptiondate') # for descending order
        # return Businessdetails.objects.order_by('subscriptiondate') # for ascending order

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            response_data = {
                'status' : 'success',
                'code' : status.HTTP_200_OK,
                'messege' : 'Business Details based on subscription date',
                'data' : serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "Failed to retrieve business details."
            response_data = {
                'status': 'error',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': error_message,
                'data': None
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# API for Admin login
class AdminLoginAPI(generics.ListAPIView):
    queryset = Administrators.objects.all()
    serializer_class = AdministratorsSerializer

    def get(self, request, adminname, adminpassword, *args, **kwargs):
        if adminname and adminpassword:
            try:
                # Perform a case-sensitive check in Python after retrieving the user
                admin = Administrators.objects.get(adminname__iexact=adminname)
                
                # Ensure case sensitivity using Python check
                if admin.adminname == adminname:
                    stored_password = admin.adminpassword

                    # Check if the provided password matches the stored encrypted password
                    if check_password(adminpassword, stored_password):
                        return Response({'message': 'Valid User'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Invalid user'}, status=status.HTTP_401_UNAUTHORIZED)
            except Administrators.DoesNotExist:
                return Response({'message': 'Invalid user'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'Please provide both adminname and adminpassword'}, status=status.HTTP_400_BAD_REQUEST)
        
# API for subscriptions which are ending soon
class SubscriptionEndingSoon(generics.ListAPIView):
    serializer_class = TransactionSerializer
    
    def get(self, request):
        try:
            # Get current date
            current_date = datetime.now().date()

            # Retrieve transactions
            transactions = Transactiondetails.objects.all()

            # Collect transactions ending soon
            ending_soon = []
            for transaction in transactions:
                # Calculate the end date by adding duration days to the transaction date
                end_date = transaction.transactiondate + timedelta(days=transaction.duration)
                
                # Calculate remaining days by subtracting current date from the end date
                remaining_days = (end_date - current_date).days
                
                # Check if remaining days are within the range of 1 to 7
                if 1 <= remaining_days <= 7:
                    # Retrieve business details related to this transaction
                    business_records = Businessdetails.objects.filter(businessid=transaction.businessid)
                    for record in business_records:
                        ending_soon.append({
                            'business_id': record.businessid,
                            'business_name': record.businessname,
                            'contact_no': record.contactno,
                            'email': record.email,
                            'subscription_date': record.subscriptiondate,
                            'remaining_days' : remaining_days,
                            # Include other necessary fields from Businessdetails
                            # Add more fields as required
                        })

            if ending_soon:
                return Response({
                    'status': 'success',
                    'code': 200,
                    'message': 'Subscriptions ending soon',
                    'data': ending_soon
                })
            else:
                return Response({
                    'status': 'fail',
                    'code': 404,
                    'message': 'No businesses which are expiring soon',
                    'data': []
                })

        except Exception as e:
            # Handle other potential exceptions
            return Response({
                'status': 'error',
                'code': 500,
                'message': 'An error occurred',
                'data': str(e)
            })

# API for subuser list
class GetSubUserList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        business_id = self.kwargs.get('businessid')
        if business_id is not None:
            queryset = Userdetails.objects.filter(businessid=business_id)
            return queryset
        else:
            return Userdetails.objects.none()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            data = {
                "status": "success",
                "code": 200,
                "message": "User fetched successfully",
                "data": serializer.data
            }
        else:
            data = {
                "status": "error",
                "code": 404,
                "message": "No Users found for the provided businessid",
                "data": []
            }
        return Response(data)
    
# API for subscription for specific business
class SubscriptionforBusiness(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        try:
            business_id = self.kwargs.get("businessid")

            if business_id is None:
                return Response({
                    'status': 'fail',
                    'code': 400,
                    'message': 'Business ID not provided',
                    'data': []
                })

            # Get current date
            current_date = datetime.now().date()

            # Retrieve transactions for the specified business_id
            transactions = Transactiondetails.objects.filter(businessid=business_id)

            # Initialize a dictionary to store unique end dates and remaining days
            subscription_details = {}

            # Iterate through transactions to collect unique end dates and remaining days
            for transaction in transactions:
                # Calculate the end date by adding duration days to the transaction date
                end_date = transaction.transactiondate + timedelta(days=transaction.duration)

                # Calculate remaining days by subtracting the current date from the end date
                remaining_days = (end_date - current_date).days

                # Add unique end date and remaining days to the dictionary
                if remaining_days > 0:
                    date_key = end_date.strftime("%Y-%m-%d")
                    if remaining_days <= 7:
                        subscription_details[date_key] = {
                            'end_date': end_date.strftime("%Y-%m-%d"),
                            'remaining_days': remaining_days
                        }
                    else:
                        subscription_details[date_key] = {
                            'end_date': end_date.strftime("%Y-%m-%d")
                        }

            # Create a list of subscription details from the dictionary
            subscription_details_list = list(subscription_details.values())

            # Create the response dictionary
            response_data = {
                'status': 'success',
                'code': 200,
                'message': f'Subscription details for business ID {business_id}',
                'data': subscription_details_list
            }

            # If no active subscriptions found, include a subscription status message
            if not response_data['data']:
                response_data['message'] = f'No active subscription found for business ID {business_id}'
                response_data['data'].append({
                    'subscription_status': 'Your subscription is ended'
                })

            return Response(response_data)

        except Exception as e:
            # Handle other potential exceptions
            return Response({
                'status': 'error',
                'code': 500,
                'message': 'An error occurred',
                'data': str(e)
            })

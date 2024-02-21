import os
from datetime import datetime, timedelta
from django.conf import settings
from django.db.models import Max, Count, Q
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
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
    AdminLoginSerializer,
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
                "status": "success",
                "code": status.HTTP_200_OK,
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
                "status": "success",
                "code": status.HTTP_200_OK,
                "base64_code": base64_code,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except FileNotFoundError:
            error_data = {
                "status": "error",
                "code": status.HTTP_404_NOT_FOUND,
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
            # Extract starting index from the request query parameters
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Number of records per page

            # Ensure ordering by primary key for consistent pagination
            self.queryset = self.queryset.order_by('pk')

            # Use Django Paginator to get the subset of records
            paginator = Paginator(self.queryset, limit)
            page_number = (start_index // limit) + 1  # Calculate page number based on starting index

            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                return Response({"message": "No more records available"}, status=status.HTTP_200_OK)

            paginated_business = page.object_list
            paginated_serializer = self.get_serializer(paginated_business, many=True)

            # Get total count of records
            total_records = paginator.count

            # Get count of estimates for each BusinessID
            estimate_counts = Estimatedetails.objects.values('businessid').annotate(EstimateCount=Count('estimateid'))

            # Map the estimate counts to the corresponding businesses
            for business_data in paginated_serializer.data:
                business_id = business_data['businessid']
                estimate_count = next((item['EstimateCount'] for item in estimate_counts if item['businessid'] == business_id), 0)
                business_data['estimate_count'] = estimate_count

            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "total_records": total_records,
                "start_index": start_index,
                "limit": limit,
                "message": f"Businessdetails starting from index {start_index}",
                "data": paginated_serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = (
                "An error occurred while fetching businesses: {}".format(str(e))
            )
            error_response = {
                "status": "error",
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": error_message,
            }
            return Response(
                error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    def search(self, request, *args, **kwargs):
        try:
            search_term = request.query_params.get('search_term')
            if not search_term:
                return Response({"message": "Please provide a search term"}, status=status.HTTP_400_BAD_REQUEST)

            # Perform case-insensitive search by name or mobile number
            search_results = Businessdetails.objects.filter(
                Q(businessname__icontains=search_term) | Q(contactno__icontains=search_term)
            )

            # Extract start index and limit from the request query parameters
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Default limit is 50

            # Ensure ordering by primary key for consistent pagination
            search_results = search_results.order_by('pk')

            # Use Django Paginator to get the subset of records
            paginator = Paginator(search_results, limit)
            page_number = (start_index // limit) + 1  # Calculate page number based on starting index

            try:
                paginated_search_results = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_search_results = paginator.page(1)
            except EmptyPage:
                return Response({"message": "No more records available"}, status=status.HTTP_200_OK)

            serializer = self.get_serializer(paginated_search_results, many=True)

            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": f"Search results for '{search_term}'",
                "start_index": start_index,
                "limit": limit,
                "total_records": paginator.count,
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = (
                "An error occurred while searching businesses: {}".format(str(e))
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
            last_business = Businessdetails.objects.aggregate(Max('businessid'))
            last_business_id = last_business['businessid__max']

            # If the table is empty, set the initial businessid to 1
            if last_business_id is None:
                new_business_id = 1000000
            else:
                new_business_id = last_business_id + 1

            request.data['marginlength'] = '50'
            request.data['marginwidth'] = '20'
            request.data['brustingfactor'] = '14'
            request.data['gsm'] = '150'
            request.data['rate'] = '24'
            request.data['flutefactor'] = '1.5'
            request.data['waste'] = '3'
            request.data['conversionrate'] = '10'
            request.data['profit'] = '15'
            request.data['tax'] = '18'
            request.data['status'] = "Trial"
            request.data['multiuser'] = 0
            request.data['estimatenote'] = "1.Valid for 15 days only.-2.Taxes extra as applicable, if not mentioned in quotation.-3.Minimum order quantity 1000. If less than 1000, then transport charges extra."

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(businessid=new_business_id)
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
            # Extract starting index from the request query parameters
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Number of records per page

            # Ensure ordering by primary key for consistent pagination
            self.queryset = self.queryset.order_by('pk')

            # Use Django Paginator to get the subset of records
            paginator = Paginator(self.queryset, limit)
            page_number = (start_index // limit) + 1  # Calculate page number based on starting index

            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                return Response({"message": "No more records available"}, status=status.HTTP_200_OK)

            paginated_businesses = page.object_list
            paginated_serializer = self.get_serializer(paginated_businesses, many=True)

            # Get total count of records
            total_records = paginator.count

            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "total_records": total_records,
                "start_index": start_index,
                "limit": limit,
                "message": f"Businesses starting from index {start_index}",
                "data": paginated_serializer.data,
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
            # Extract starting index from the request query parameters
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Number of records per page

            # Ensure ordering by primary key for consistent pagination
            self.queryset = self.queryset.order_by('pk')

            # Use Django Paginator to get the subset of records
            paginator = Paginator(self.queryset, limit)
            page_number = (start_index // limit) + 1  # Calculate page number based on starting index

            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                return Response({"message": "No more records available"}, status=status.HTTP_200_OK)

            paginated_client = page.object_list
            paginated_serializer = self.get_serializer(paginated_client, many=True)

            # Get total count of records
            total_records = paginator.count

            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "total_records" : total_records,
                "start_index" : start_index,
                "limit" : limit,
                "message": f"Client details starting from index {start_index}",
                "data": paginated_serializer.data,
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
            # Extract starting index from the request query parameters
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Number of records per page

            # Ensure ordering by primary key for consistent pagination
            self.queryset = self.queryset.order_by('pk')

            # Use Django Paginator to get the subset of records
            paginator = Paginator(self.queryset, limit)
            page_number = (start_index // limit) + 1  # Calculate page number based on starting index

            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                return Response({"message": "No more records available"}, status=status.HTTP_200_OK)

            paginated_estimates = page.object_list
            paginated_serializer = self.get_serializer(paginated_estimates, many=True)

            # Get total count of records
            total_records = paginator.count

            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "total_records": total_records,
                "start_index": start_index,
                "limit": limit,
                "message": f"Estimates starting from index {start_index}",
                "data": paginated_serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = "An error occurred while fetching paginated estimates: {}".format(
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

            # Get the maximum estimateid for the given business, user, and client
            existing_estimates = Estimatedetails.objects.filter(businessid=business_id)
            max_estimate_id = existing_estimates.aggregate(Max("estimateid"))["estimateid__max"]

            # Generate a new estimateid by incrementing the maximum one (or use a default if no records exist)
            new_estimate_id = max_estimate_id + 1 if max_estimate_id is not None else int(f"{business_id}00001")

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
            # Extract starting index from the request query parameters
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Number of records per page

            # Ensure ordering by primary key for consistent pagination
            self.queryset = self.queryset.order_by('pk')

            # Use Django Paginator to get the subset of records
            paginator = Paginator(self.queryset, limit)
            page_number = (start_index // limit) + 1  # Calculate page number based on starting index

            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                return Response({"message": "No more records available"}, status=status.HTTP_200_OK)

            paginated_transaction = page.object_list
            paginated_serializer = self.get_serializer(paginated_transaction, many=True)

            # Get total count of records
            total_records = paginator.count

            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "total_records": total_records,
                "start_index": start_index,
                "limit": limit,
                "message": f"Transactions starting from index {start_index}",
                "data": paginated_serializer.data,
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

            request.data['transactionid'] = new_transaction_id
            request.data['status'] = 'Active'

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            transaction_instance = serializer.save()

            transaction = Transactiondetails.objects.get(businessid=business_id)
            business_id = transaction.businessid
            business_details = Businessdetails.objects.get(businessid=business_id)

            # Assuming 'transactiondate' and 'subscriptiondate' are fields in respective models
            business_details.subscriptiondate = transaction.transactiondate
            business_details.status = 'Active'  # Updating status to 'Active'
            business_details.save()

            # Update user access for all users related to the business
            Userdetails.objects.filter(businessid=business_id).update(useraccess=2)

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
            # Extract starting index from the request query parameters
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Number of records per page
            
            # Ensure ordering by primary key for consistent pagination
            self.queryset = self.queryset.order_by('-pk')

            # Use Django Paginator to get the subset of records
            paginator = Paginator(self.queryset, limit)
            page_number = (start_index // limit) + 1  # Calculate page number based on starting index

            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                return Response({"message": "No more records available"}, status=status.HTTP_200_OK)

            paginated_user = page.object_list
            paginated_serializer = self.get_serializer(paginated_user, many=True)

            # Get total count of records
            total_records = paginator.count

            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "total_records": total_records,
                "start_index": start_index,
                "limit": limit,
                "message": f"Users starting from index {start_index}",
                "data": paginated_serializer.data,
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
        
    def search(self, request, *args, **kwargs):
        try:
            search_term = request.query_params.get('search_term')
            if not search_term:
                return Response({"message": "Please provide a search term"}, status=status.HTTP_400_BAD_REQUEST)

            # Perform case-insensitive search by name or mobile number
            search_results = Userdetails.objects.filter(
                Q(username__icontains=search_term) | Q(mobileno__icontains=search_term)
            )

            # Extract start index and limit from the request query parameters
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Default limit is 50

            # Ensure ordering by primary key for consistent pagination
            search_results = search_results.order_by('pk')

            # Use Django Paginator to get the subset of records
            paginator = Paginator(search_results, limit)
            page_number = (start_index // limit) + 1  # Calculate page number based on starting index

            try:
                paginated_search_results = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_search_results = paginator.page(1)
            except EmptyPage:
                return Response({"message": "No more records available"}, status=status.HTTP_200_OK)

            serializer = self.get_serializer(paginated_search_results, many=True)

            api_response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": f"Search results for '{search_term}'",
                "start_index": start_index,
                "limit": limit,
                "total_records": paginator.count,
                "data": serializer.data,
            }
            return Response(api_response, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = (
                "An error occurred while searching user: {}".format(str(e))
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
            mobile_no = request.data.get("mobileno")

            existing_user = Userdetails.objects.filter(mobileno=mobile_no).first()

            if existing_user:
                existing_user_data = {
                        "businessid": existing_user.businessid,
                        "userid": existing_user.userid,
                        "userpassword": existing_user.userpassword,
                        "username": existing_user.username,
                        "mobileno": existing_user.mobileno,
                        "userrole": existing_user.userrole,
                        "useraccess": existing_user.useraccess,
                        "androidid": existing_user.androidid,
                        "deviceinfo": existing_user.deviceinfo,
                        "status": existing_user.status,
                    }
                api_response = {
                    "status": "error",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "message": "Mobile number already exists",
                    "existing_user_data": existing_user_data,
                }
                return Response(api_response)

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
                mobileno = request.data.get("mobileno")
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
                'status': business.status,
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


# API for Client List by BusinessID
class GetClientByB(generics.ListAPIView):
    serializer_class = ClientdetailSerializer

    def get_queryset(self):
        business_id = self.kwargs["businessid"]
        return Clientdetails.objects.filter(businessid=business_id)

    def list(self, request, *args, **kwargs):
        business_id = self.kwargs["businessid"]
        queryset = self.get_queryset()

        # Pagination
        start_index = int(request.query_params.get('start_index', 0))
        limit = 50  # Default limit is 50

        paginator = Paginator(queryset, limit)
        page_number = (start_index // limit) + 1

        try:
            paginated_queryset = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_queryset = paginator.page(1)
        except EmptyPage:
            paginated_queryset = paginator.page(paginator.num_pages)

        serializer = self.get_serializer(paginated_queryset, many=True)

        if queryset.exists():
            data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': f'Client list under {business_id}',
                'start_index': start_index,
                'limit': limit,
                'total_records': paginator.count,
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

    def list(self, request, *args, **kwargs):
        try:
            business_id = self.kwargs.get("businessid")
            user_id = self.kwargs.get("userid")

            user = Userdetails.objects.get(userid=user_id)

            if user.userrole == "Admin":
                queryset = Estimatedetails.objects.filter(businessid=user.businessid)
            elif user.userrole == "User":
                queryset = Estimatedetails.objects.filter(businessid=user.businessid, userid=user_id)
            else:
                return Response({'status': 'error', 'message': 'Invalid user role'}, status=status.HTTP_400_BAD_REQUEST)

            # Pagination
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Default limit is 50

            paginator = Paginator(queryset, limit)
            page_number = (start_index // limit) + 1

            try:
                paginated_queryset = paginator.page(page_number)
            except PageNotAnInteger:
                paginated_queryset = paginator.page(1)
            except EmptyPage:
                paginated_queryset = paginator.page(paginator.num_pages)

            serializer = self.get_serializer(paginated_queryset, many=True)

            data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': f'Estimates for {business_id} by user {user_id}',
                'start_index': start_index,
                'limit': limit,
                'total_records': paginator.count,
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
        android_id = self.kwargs.get("androidid")
        queryset = Userdetails.objects.filter(mobileno=mobile_no, androidid=android_id)
        return queryset
    
    def get(self, request, *args, **kwargs):
        mobile_no = self.kwargs.get("mobileno")
        android_id = self.kwargs.get("androidid")
        
        queryset = self.get_queryset()

        if queryset.exists():
            user = queryset.first()
            if user.useraccess == 3:
                data = {
                    'status': 'error',
                    'code': status.HTTP_200_OK,
                    'message': 'User has been blocked!!! Please contact admin.',
                }
                return Response(data, status=status.HTTP_200_OK)
            
            elif user.androidid == "NewUser":
                data = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Your device has changed so you need to update your androidID',
                    'data': UserSerializer(user).data,
                }
                return Response(data, status=status.HTTP_200_OK)

            else:
                data = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': f'Record found for {mobile_no} and {android_id}',
                    'data': UserSerializer(user).data
                }
                return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'status': 'error',
                'code': status.HTTP_404_NOT_FOUND,
                'message': f'No record found for {mobile_no} and {android_id}',
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

            current_week_records = self.get_queryset().filter(
                activationdate__range=(current_week_start, current_week_end))
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


# API based on businessid in descending order for Admin
class AdminHomeAPI2(generics.ListAPIView):
    serializer_class = BusinessdetailSerializer

    def get_queryset(self):
        return Businessdetails.objects.order_by('-businessid')  # for descending order
        # return Businessdetails.objects.order_by('subscriptiondate') # for ascending order

    def list(self, request, *args, **kwargs):
        try:
            # Extract starting index from the request query parameters
            start_index = int(request.query_params.get('start_index', 0))
            limit = 50  # Number of records per page

            queryset = self.get_queryset()  # Get the queryset with correct ordering

            # Ensure ordering by primary key for consistent pagination
            queryset = queryset.order_by('-pk')

            # Use Django Paginator to get the subset of records
            paginator = Paginator(queryset, limit)
            page_number = (start_index // limit) + 1  # Calculate page number based on starting index

            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                return Response({"message": "No more records available"}, status=status.HTTP_200_OK)

            paginated_home = page.object_list
            paginated_serializer = self.get_serializer(paginated_home, many=True)

            # Get total count of records
            total_records = paginator.count
            
            response_data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'total_records': total_records,
                'start_index': start_index,
                'limit': limit,
                'message': 'Business Details',
                'data': paginated_serializer.data
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
class AdminLoginAPI(APIView):
    serializer_class = AdminLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            adminname = serializer.validated_data['adminname']
            adminpassword = serializer.validated_data['adminpassword']

            try:
                # Perform a case-sensitive check after retrieving the user
                admin = Administrators.objects.get(adminname=adminname)

                # Ensure case sensitivity for both adminname and password
                if admin.adminname == adminname and check_password(adminpassword, admin.adminpassword):
                    return Response({'message': 'Valid User'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except Administrators.DoesNotExist:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # In case of invalid serializer data, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                            'remaining_days': remaining_days,
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

            # Retrieve the latest transaction for the specified business_id
            latest_transaction = Transactiondetails.objects.filter(businessid=business_id).order_by(
                '-transactiondate').first()

            if not latest_transaction:
                # If no transaction found, fetch activation date for the business_id
                activation_date = Businessdetails.objects.filter(businessid=business_id).values_list('activationdate', flat=True).first()
                if activation_date:
                    # If activation date exists, add 4 days to it for trial period
                    trial_end_date = activation_date + timedelta(days=4)
                    remaining_days = max((trial_end_date - current_date).days, 0)
                    status = 'Trial' if remaining_days > 0 else 'Expired'

                    # Update status in both Userdetails and Businessdetails
                    Userdetails.objects.filter(businessid=business_id).update(status=status)
                    Businessdetails.objects.filter(businessid=business_id).update(status=status)

                    # Create the response dictionary for trial period
                    response_data = {
                        'status': 'success',
                        'code': 200,
                        'message': f'Trial subscription for business ID {business_id}',
                        'data': [{
                            'subscription_date': activation_date,
                            'end_date': trial_end_date.strftime("%Y-%m-%d"),
                            'remaining_days': remaining_days,
                            'status': status
                        }]
                    }
                    return Response(response_data)

                else:
                    return Response({
                        'status': 'fail',
                        'code': 400,
                        'message': f'No transactions found and activation date not available for business ID {business_id}',
                        'data': []
                    })

            # If there are transactions, proceed with the existing logic
            end_date = latest_transaction.transactiondate + timedelta(days=latest_transaction.duration)
            remaining_days = max((end_date - current_date).days, 0)

            status = 'Expired' if remaining_days == 0 else ('Trial' if remaining_days <= 4 else 'Active')


            # Check if remaining_days is 0 and update 'useraccess' for all users under the businessid
            if remaining_days == 0:
                Userdetails.objects.filter(businessid=business_id, useraccess__lt=3).update(useraccess=1, status='Expired')

            else:
                Userdetails.objects.filter(businessid=business_id, useraccess__lt=3).update(status=status)

            response_data = {
                'status': 'success',
                'code': 200,
                'message': f'Subscription details for business ID {business_id}',
                'data': [{
                    'subscription_date': latest_transaction.transactiondate,
                    'end_date': end_date.strftime("%Y-%m-%d"),
                    'remaining_days': remaining_days,
                    'status': status
                }]
            }

            return Response(response_data)

        except Exception as e:
            return Response({
                'status': 'error',
                'code': 500,
                'message': 'An error occurred',
                'data': str(e)
            })

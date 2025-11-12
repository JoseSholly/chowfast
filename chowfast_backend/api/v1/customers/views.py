from customers.models import Customer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .response_serializers import (
    CustomerCreationSuccessSerializer,
    DuplicatePhoneErrorSerializer,
    ResponseCustomerInfoSerializer,
)
from .serializers import CustomerSerializer


class CreateCustomerView(APIView):
    serializer_class = CustomerSerializer
    http_method_names = ["post"]
    """
    Create a new customer.
    """

    @swagger_auto_schema(
        tags=["Customers"],
        operation_summary="Create a new Customer Account",
        request_body=CustomerSerializer,
        responses={
            # Success response uses the new wrapper serializer
            status.HTTP_201_CREATED: CustomerCreationSuccessSerializer,
            # Custom error response uses the specific error serializer
            status.HTTP_400_BAD_REQUEST: DuplicatePhoneErrorSerializer,
            # Note: For the default DRF validation errors (if serializer.is_valid() fails),
            # drf-yasg will often generate a useful generic 400 response automatically.
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get("phone_number")

            if Customer.objects.filter(phone_number=phone).exists():
                return Response(
                    {"error": "A customer with this phone number already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            customer = serializer.save()
            data = self.serializer_class(customer).data
            return Response(
                {
                    "status": "success",
                    "message": "Customer created successfully.",
                    "data": data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveCustomerView(APIView):
    """
    Retrieve a specific customer or all customers.
    """

    @swagger_auto_schema(
        tags=["Customers"],
        operation_summary="Get customer account",
        responses={
            # Success response uses the new wrapper serializer
            status.HTTP_201_CREATED: ResponseCustomerInfoSerializer,
            # Custom error response uses the specific error serializer
            status.HTTP_400_BAD_REQUEST: DuplicatePhoneErrorSerializer,
            # Note: For the default DRF validation errors (if serializer.is_valid() fails),
            # drf-yasg will often generate a useful generic 400 response automatically.
        },
    )
    def get(self, request, customer_id=None, *args, **kwargs):
        if customer_id:
            try:
                customer = Customer.objects.get(customer_id=customer_id)
            except Customer.DoesNotExist:
                return Response(
                    {"error": "Customer not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        data = serializer.data
        return Response(
            {
                "status": "success",
                "message": "Customer retrieved successfully.",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )


class UpdateCustomerView(APIView):
    """
    Update an existing customer by customer_id.
    """

    serializer_class = CustomerSerializer
    http_method_names = ["put"]

    @swagger_auto_schema(
        tags=["Customers"],
        operation_summary="Get Customer information",
        request_body=CustomerSerializer,
        responses={
            # Success response uses the new wrapper serializer
            status.HTTP_201_CREATED: CustomerCreationSuccessSerializer,
        },
    )
    def put(self, request, customer_id, *args, **kwargs):
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(
                {
                    "status": "success",
                    "message": "Customer updated successfully.",
                    "data": data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.urls import path

from .views import CreateCustomerView, RetrieveCustomerView, UpdateCustomerView

urlpatterns = [
    path("customers/register", CreateCustomerView.as_view(), name="create_customer"),
    path("customers/<str:customer_id>/", RetrieveCustomerView.as_view(), name="retrieve_customer"),
    path("customers/<str:customer_id>/update/", UpdateCustomerView.as_view(), name="update_customer"),
]

from django.urls import path

from .views import CreateCustomerView, RetrieveCustomerView, UpdateCustomerView

urlpatterns = [
    path("register/", CreateCustomerView.as_view(), name="create_customer"),
    path("<str:customer_id>/", RetrieveCustomerView.as_view(), name="retrieve_customer"),
    path("<str:customer_id>/update/", UpdateCustomerView.as_view(), name="update_customer"),
]

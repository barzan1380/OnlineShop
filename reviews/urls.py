from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path("submit-review/",views.SubmitReviewView.as_view(),name="submit-review")
]
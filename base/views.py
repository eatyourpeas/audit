from django.shortcuts import render

from .models import BaseSurvey

# Create your views here.

from django.http import HttpResponse


def index(request):
    surveys = BaseSurvey.objects.all()

    return render(
        request=request, template_name="home.html", context={"surveys": surveys}
    )


def create_base_survey(request):
    """
    POST request to create new survey
    """
    print("hello")
    survey_title = request.POST.get("survey-title")
    print(survey_title)
    context = {"surveys": None}
    return render(
        request=request, template_name="templates/survey-title.html", context=context
    )

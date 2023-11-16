from django.shortcuts import render

from .models import BaseSurvey, Section
from .forms import SectionForm


def index(request):
    surveys = BaseSurvey.objects.all()

    return render(
        request=request, template_name="home.html", context={"surveys": surveys}
    )


def create_base_survey(request):
    """
    POST request to create new survey
    """
    survey_title = request.POST.get("survey-title")
    BaseSurvey.objects.create(
        title=survey_title,
        is_ongoing=False)
    context = {"surveys": BaseSurvey.objects.all()}
    return render(
        request=request, template_name="survey-table.html", context=context
    )

def delete_base_survey(request, survey_id):
    """
    POST request to delete survey
    """
    BaseSurvey.objects.filter(pk=survey_id).delete()
    context = {"surveys": BaseSurvey.objects.all()}
    return render(
        request=request, template_name="survey-table.html", context=context
    )

def edit_base_survey(request, survey_id):
    """
    GET request to edit survey page
    """
    if request.method == 'POST':
        form = SectionForm(request.POST)
        section_title = request.POST.get('section_title')
        if form.is_valid():
            base_survey = BaseSurvey.objects.filter(pk=survey_id).get()
            form.save()
    else:
        form = SectionForm()
    context = {
        "survey": BaseSurvey.objects.filter(pk=survey_id).get(),
        "form": form
    }
    return render(
        request=request, template_name="edit-survey-table.html", context=context
    )


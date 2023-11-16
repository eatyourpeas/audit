from django.forms import Form

from .models import Section

class SectionForm(Form):
    class Meta:
        model=Section
        fields="__all__"
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db.models.constraints import UniqueConstraint
from django.db.models.functions import Lower

QUESTION_TYPES=(
    ("FREE_TEXT", "Free text"),
    ("MULTIPLE_CHOICE_SINGLE", "Multiple choice - single answer"),
    ("MULTIPLE_CHOICE_MULTIPLE", "Multiple choice - multiple answer"),
    ("YES_NO", "Yes/No"),
    ("YES_NO_OTHER", "Yes/No/Other"),
    ("YES_NO_UNCERTAIN", "Yes/No/Uncertain"),
    ("YES_NO_NA", "Yes/No/Not applicable"),
)

class BaseSurveyUser(AbstractUser):
    """
    User model. Overrides the Django base user but retains the core django user functions
    This is also set in AUTH_USER_MODEL in settings.py
    Note username is reset to email as the default
    """

    username=None

    first_name = models.CharField(
        _("First name"),
        help_text=_("Enter your first name"),
        max_length=150
    )
    
    surname = models.CharField(
        _("Surname"),
        help_text=_("Enter your surname"),
        max_length=150
    )

    email = models.EmailField(
        _("Email address"),
        help_text=_("Enter your email address"),
        unique=True
    )

    is_superuser = models.BooleanField(
        default=False
    )
    
    is_staff = models.BooleanField(
        # allows access to the admin area
        default=False
    )

    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "surname"]

    class Meta:
        verbose_name = _("Base Survey User")
        verbose_name_plural = _("Base Survey Users")
        constraints = [
            UniqueConstraint(
                Lower("email"),
                name="user_email_ci_uniqueness"
            )
        ]
    
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.surname}"

    def __str__(self) -> str:
        return self.get_full_name

class BaseSurvey(models.Model):
    """
    Each survey has a parent model
    """

    title = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True, default=None)
    end_date = models.DateField(null=True, blank=True, default=None)
    is_ongoing = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Base Survey")
        verbose_name_plural = _("Base Surveys")

    def __str__(self) -> str:
        return self.name


class Section(models.Model):
    """
    A survey has many sections
    """
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    help_text = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)

    # relationships
    survey = models.ForeignKey(to=BaseSurvey, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Survey Section")
        verbose_name_plural = _("Survey Sections")
    
    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    """
    Survey questions
    """
    text = models.CharField(max_length=100)
    help_text = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    survey_reference = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Base Survey Question")
        verbose_name_plural = _("Base Survey Questions")
    
    def __str__(self) -> str:
        return self.text

class SectionQuestion(models.Model):
    """
    Link model between Survey Section and Question
    One Survey Section can have many questions, one question can be part of many sections
    """
    
    # relationships
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Base Survey SectionQuestion")
        verbose_name_plural = _("Base Survey SectionQuestions")
    
    def __str__(self) -> str:
        return f"Link for question `{self.question}` in section `{self.section}`"

class QuestionType(models.Model):
    """
    Model describing types of question
    """
    type = models.CharField(choices=QUESTION_TYPES, max_length=50)

    # relationships
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Question type")
        verbose_name_plural = _("Question types")

    def __str__(self) -> str:
        return self.type
        

class QuestionOptions(models.Model):
    """
    Available options for a given question
    """
    option_text = models.CharField(max_length=100)
    help_text = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    survey_reference = models.CharField(max_length=100)

    # relationships
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Question option")
        verbose_name_plural = _("Question options")

    def __str__(self) -> str:
        return self.option_text

class BaseResponse(models.Model):
    """
    Represents a user response to a single survey. Comprises many answers.
    One user can respond to many surveys.
    """
    survey_started_date = models.DateTimeField(blank=True, null=True, default=None)
    survey_last_updated = models.DateTimeField(blank=True, null=True, default=None)
    survey_completed_date = models.DateTimeField(blank=True, null=True, default=None)
    survey_complete = models.BooleanField(default=False)
    
    # relationships
    survey = models.ForeignKey(to=BaseSurvey, on_delete=models.CASCADE)
    base_survey_user = models.ForeignKey(to=BaseSurveyUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Base Survey response")
        verbose_name_plural = _("Base Survey responses")

    def __str__(self) -> str:
        return f"Response by {self.base_survey_user} to survey `{self.survey}`"

class Answer(models.Model):
    """
    Answer to a question
    This may be free text in a text box, selection of an MCQ or a dropdown
    One question may have many answers
    """
    text = models.CharField(max_length=500, blank=True, null=True, default=None)
    integer_selection = models.IntegerField(blank=True, null=True, default=None)
    character_selection = models.IntegerField(blank=True, null=True, default=None)

    # relationships
    response = models.ForeignKey(to=BaseResponse, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self) -> str:
        return f"Answer to question `{self.question}`"

class BaseSurveyUserBaseSurvey(models.Model):
    """
    Link table between BaseSurveyUser and BaseSurvey
    """

    # relationships
    base_survey_user = models.ForeignKey(to=BaseSurveyUser, on_delete=models.CASCADE)
    base_survey = models.ForeignKey(to=BaseSurvey, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Base Survey User/Base Survey")
        verbose_name_plural = _("Base Survey User/Base Surveys")

    def __str__(self) -> str:
        return f"{self.base_survey_user}'s submission to survey `{self.base_survey}`"
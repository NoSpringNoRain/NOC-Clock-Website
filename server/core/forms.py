from django import forms
from django.contrib.auth.password_validation import password_validators_help_text_html
from django.core.validators import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

import re


def validate(input):
    if input <= 0:
        raise ValidationError('Input value must be > 0')


class JobSubmitForm(forms.Form):
    job_name = forms.CharField(label='Job name',
                               max_length=100,
                               required=False)

    age = forms.IntegerField(label='Age',
                             required=False,
                             validators=[validate])

    SEX_CHOICES = (
        ('0', 'N/A'),
        ('1', 'Male'),
        ('2', 'Female'),
        ('3', 'Other')
    )
    sex = forms.ChoiceField(widget=forms.Select, choices=SEX_CHOICES,
                            label='Gender', required=False)

    RACE_CHOICES = (
        ('0', 'N/A'),
        ('1', 'White'),
        ('2', 'Black/African American American Indian/Alaska'),
        ('3', 'Native'),
        ('4', 'Hispanic/Latinx'),
        ('5', 'Asian'),
        ('6', 'Middle Eastern'),
        ('7', 'Other')
    )
    race = forms.ChoiceField(widget=forms.Select, choices=RACE_CHOICES,
                             label='Race', required=False)

    EDU_CHOICES = (
        ('0', 'N/A'),
        ('1', 'High school, but did not graduate'),
        ('2', 'High school graduate'),
        ('3', 'Attended some college'),
        ('4', 'College graduate or higher'),
    )
    education_level = forms.ChoiceField(widget=forms.Select, choices=EDU_CHOICES,
                                        label='Education Level',
                                        required=False)

    FAM_CHOICES = (
        ('0', 'N/A'),
        ('1', 'YES'),
        ('2', 'NO'),
        ('3', 'Not Sure')
    )
    family_history = forms.ChoiceField(widget=forms.Select, choices=FAM_CHOICES,
                                       label='Do you have a first-degree relative '
                                             '(mother, father, sister, brother) living or deceased with '
                                             'a memory problem?', required=False)

    DIAG_CHOICES = (
        ('0', 'N/A'),
        ('1', 'YES'),
        ('2', 'NO'),
        ('3', 'Not Sure')
    )
    diagnosis_history = forms.ChoiceField(widget=forms.Select, choices=DIAG_CHOICES,
                                          label='Have you ever been diagnosed with a'
                                                'specific memory problem?', required=False)

    height = forms.CharField(label='Candidate Height (ft/inches)',
                             help_text='Enter your height, e.g. 5\'5\'\'', required=False)

    weight = forms.FloatField(label='Candidate Weight (pounds)',
                              help_text='Enter your weight, e.g. 150',
                              validators=[validate], required=False)

    EXE_CHOICES = (
        ('0', 'N/A'),
        ('1', 'Rarely/Never'),
        ('2', '1 time each week'),
        ('3', '2-3 times each week'),
        ('4', '4 or more times each week')
    )
    exercise_frequency = forms.ChoiceField(widget=forms.Select, choices=EXE_CHOICES,
                                           label='How often do you exercise or walk'
                                                 'for more than 10 minutes (without stopping)?',required=False)
    ALC_CHOICES = (
        ('0', 'N/A'),
        ('1', 'Rarely/Never'),
        ('2', 'Occasionally'),
        ('3', 'Weekly'),
        ('4', 'Daily')
    )
    alcohol_frequency = forms.ChoiceField(widget=forms.Select, choices=ALC_CHOICES,
                                          label='How often do you drink alcoholic beverages?',required=False)

    CIG_CHOICES = (
        ('0', 'N/A'),
        ('1', 'Rarely/Never'),
        ('2', 'Less than 5 years'),
        ('3', '5-9 years'),
        ('4', '10-20 years'),
        ('5', 'More than 20 years')
    )
    smoking_year = forms.ChoiceField(widget=forms.Select, choices=CIG_CHOICES,
                                     label='How long have you been smoking cigarette or pipes'
                                           'during your entire life?', required=False)

    img = forms.ImageField(label="Upload your clock drawing", required=False)



    def clean(self):
        cleaned_data = super().clean()
        # s1, s2 = cleaned_data.get('term1'), cleaned_data.get('term2')
        # if (s1 is not None) and (s2 is not None) and s2 % s1 != 0:
        #     self.add_error('term2', 'Term 2 must be a multiple of Term 1')

        return cleaned_data


class SettingsForm(forms.Form):
    current_password = forms.CharField(label='Current password',
                                       max_length=100,
                                       required=True,
                                       help_text='Please enter your current password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control _password'}))

    password = forms.CharField(label='Password',
                               max_length=100,
                               required=True,
                               validators=[validate_password],
                               help_text=password_validators_help_text_html(),
                               widget=forms.PasswordInput(attrs={'class': 'form-control _password'}))


class AcademicEmailField(forms.EmailField):
    def validate(self, value):
        super().validate(value)
        # List based on Wikipedia (https://en.wikipedia.org/wiki/.edu_(second-level_domain) and https://en.wikipedia.org/wiki/.edu_(second-level_domain))
        tld_good = (r'\.edu$', r'\.edu\.[a-z]+$', r'\.ac\.[a-z]+$')
        if not any(re.match(r'^.*@.*' + tld, value) for tld in tld_good):
            raise ValidationError('Your e-mail must belong to an academic domain (.edu, .edu.*, .ac.*)')
        if User.objects.filter(email__exact=value).exists():
            raise ValidationError('Provided email is already in the database')


class SignUpForm(forms.Form):
    email = AcademicEmailField(label='E-mail *',
                               required=True,
                               max_length=1000,
                               help_text='Please, provide a valid academic e-mail address (.edu, .edu.*, .ac.*), we will use it to send you your password',
                               widget=forms.EmailInput(attrs={'class': 'form-control',
                                                              'style': 'width: 40ch'}))

    first_name = forms.CharField(label='First Name',
                                 max_length=1000,
                                 required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'style': 'width: 40ch'}))

    last_name = forms.CharField(label='Last Name',
                                max_length=1000,
                                required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'style': 'width: 40ch'}))


def username_not_exists_validator(value):
    if not User.objects.filter(username__exact=value).exists():
        raise ValidationError('Sorry, we couldn\'t find the e-mail you provided')


class PasswordResetForm(forms.Form):
    username = forms.CharField(label='E-mail',
                               required=True,
                               max_length=1000,
                               help_text='Please, enter your e-mail address',
                               validators=[username_not_exists_validator],
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'style': 'width: 40ch'}))

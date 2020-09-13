from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, ButtonHolder
from .models import User, Analytics, UserActivity


def get_choices():
    """ get choices from queryset """
    queryset = User.objects.values_list('username', flat=True).order_by('date_joined')
    lst = []

    for i, key in enumerate(queryset):
        lst.append((str(i), key))

    return tuple(lst)


class BaseForm(forms.ModelForm):

    class Meta:
        model = Analytics
        fields = ('like_amount',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'

        css_class = 'form-group col-md-12 mb-1'
        self.helper.layout = Layout(
            Row(
                Column(HTML('<a href="/sn/api/user/">User list</a>'), css_class=css_class),
                Column(HTML('<a href="/sn/api/post/">Post list</a>'), css_class=css_class),
                Column(HTML('<a href="/sn/api/like/">Like list</a>'), css_class=css_class),
                Column(HTML('<a href="/sn/api/dislike/">Dislike list</a>'), css_class=css_class),
                Column(HTML('<a href="/sn/api/analytics/">Analytics: Likes</a>'), css_class=css_class),
                Column(HTML('<a href="/sn/api/user_activity/">Analytics: User activity</a>'), css_class=css_class),
                css_class='form-row'
            ),
        )


class AnalyticsForm(forms.ModelForm):

    class Meta:
        model = Analytics
        fields = ('like_amount', 'date_from', 'date_to')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in ('like_amount',):
            self.fields[key].required = False
            self.fields[key].disabled = True

        self.fields['date_from'] = forms.DateField(
            widget=forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d',
            )
        )

        self.fields['date_to'] = forms.DateField(
            widget=forms.TextInput(
                attrs={'type': 'date'},
            )
        )

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('date_from', css_class='form-group col-md-6 mb-0'),
                Column('date_to', css_class='form-group col-md-6 mb-0'),
                Column('like_amount', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                HTML('<a class="btn btn-secondary" href="/sn/api" %}>Back</a>'),
                Submit('submit', 'Submit', css_class='button white ml-5'),
            ),
        )


class UserActivityForm(forms.ModelForm):

    class Meta:
        model = UserActivity
        fields = ('user_list', 'last_login', 'last_request')

    def __init__(self, *args, **kwargs):
        self.choices = get_choices()
        super().__init__(*args, **kwargs)
        self.fields['user_list'] = forms.ChoiceField(choices=get_choices())

        for key in ('last_login', 'last_request'):
            self.fields[key].required = False
            self.fields[key].disabled = True

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('user_list', css_class='form-group col-md-12 mb-0'),
                Column('last_login', css_class='form-group col-md-6 mb-0'),
                Column('last_request', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            ButtonHolder(
                HTML('<a class="btn btn-secondary" href="/sn/api" %}>Back</a>'),
                Submit('submit', 'Submit', css_class='button white ml-5'),
            ),
        )

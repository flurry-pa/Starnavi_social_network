from datetime import datetime, timedelta, timezone

from django.shortcuts import render
from django.views.generic import CreateView
from .models import User, Post, Like, Analytics, UserActivity
from .forms import BaseForm, AnalyticsForm, UserActivityForm
from bot.logger import logger

FMRT = '%Y-%m-%d %H:%M:%S %Z'


def _process_form(form):
    """ get data from the POST request and process it """
    if form.is_valid():
        kwargs = {}

        for key in form.cleaned_data:
            kwargs.update({key: str(form.cleaned_data[key])})

        return kwargs

    else:
        logger.warning(f'Error: form is invalid:\n{form}')


class BaseCreateView(CreateView):
    form_class = BaseForm
    template_name = 'api/base_form.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unbound_form = BaseForm()

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.unbound_form})


class AnalyticsCreateView(CreateView):
    model = Analytics
    form_class = AnalyticsForm
    template_name = 'api/analytics_form.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unbound_form = AnalyticsForm()

    def post(self, request, *args, **kwargs):
        fn = 'AnalyticsCreateView, post() '

        try:
            form = AnalyticsForm(request.POST)

        except IndexError as err:
            logger.warning(f'{fn}Error: {err}\nrequest.POST: {request.POST}')
            return render(request, 'api/analytics/', {'form': self.unbound_form})

        data_from_form = _process_form(form)
        date_from = data_from_form['date_from']
        date_to = data_from_form['date_to']
        date_from = datetime.strptime(f'{date_from} 00:00:00+0000', '%Y-%m-%d %H:%M:%S%z')  # aware datetime (UTC zone)
        date_to = datetime.strptime(f'{date_to} 00:00:00+0000', '%Y-%m-%d %H:%M:%S%z') + timedelta(days=1)

        data_to_form = data_from_form.copy()
        data_to_form.update({
            'like_amount': Like.objects.filter(date__gte=date_from, date__lte=date_to).count(),
        })

        form = AnalyticsForm(initial=data_to_form)
        return render(request, 'api/analytics_form.html', {'form': form})


class UserActivityCreateView(CreateView):
    model = UserActivity
    form_class = UserActivityForm
    template_name = 'api/user_activity_form.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unbound_form = UserActivityForm()

    def post(self, request, *args, **kwargs):
        fn = 'UserActivityCreateView, post(): '

        try:
            form = UserActivityForm(request.POST)

        except IndexError as err:
            logger.warning(f'{fn}Error: {err}\nrequest.POST: {request.POST}')
            return render(request, 'api/user_activity/', {'form': self.unbound_form})

        choices = form.choices
        data_from_form = _process_form(form)
        id_combobox = int(data_from_form['user_list'])
        username = choices[id_combobox][1]
        values = User.objects.filter(username=username).values
        uid = list(values('id'))[0]['id']

        last_login = list(values('last_login'))[0]['last_login']
        date_joined = list(values('date_joined'))[0]['date_joined']
        zero_time = datetime(1970, 1, 1, tzinfo=timezone.utc)
        last_login = zero_time if last_login is None else list(values('last_login'))[0]['last_login']
        date_joined = zero_time if date_joined is None else list(values('date_joined'))[0]['date_joined']
        last_login_join = max(last_login, date_joined)
        last_login_join = last_login_join.strftime(FMRT) if last_login_join != zero_time else 'n/a'

        values = list(Post.objects.filter(author_id=uid).order_by('-pub_date').values('pub_date'))
        last_post = values[0]['pub_date'] if len(values) > 0 else zero_time

        values = list(Like.objects.filter(user_id=uid).order_by('-date').values('date'))
        last_like = values[0]['date'] if len(values) > 0 else zero_time
        last_post_like = max(last_post, last_like)
        last_post_like = last_post_like.strftime(FMRT) if last_post_like != zero_time else 'n/a'

        data_to_form = data_from_form.copy()
        data_to_form.update({
            'last_login': last_login_join,
            'last_request': last_post_like,
        })
        form = UserActivityForm(initial=data_to_form)
        return render(request, self.template_name, {'form': form})

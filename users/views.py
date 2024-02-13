from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib.auth import login as django_login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import UpdateView

from tts.text_to_speech import AudioConverter

from .forms import AnonymousHomeTTSForm, UserProfileForm
from .models import CustomUser, Subscription
from django.contrib import messages
from datetime import datetime, timedelta

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def index_redirect(request):
    return redirect(reverse('home'))


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    if 'userinfo' in token:
        userinfo = token['userinfo']
        email = userinfo['email']
        auth0_id = userinfo['sub']

        user, created = CustomUser.objects.get_or_create(auth0_id=auth0_id, email=email)
        user.save()
        django_login(request, user)
    return redirect(request.build_absolute_uri(reverse("home")))


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def logout(request):
    request.session.clear()
    return redirect(reverse('home'))


class HomeView(View):
    template_name = 'users/home.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        user_info = None
        if 'user' in request.session:
            token = request.session['user']
            if 'userinfo' in token:
                user_info = token['userinfo']
        form = AnonymousHomeTTSForm()
        context = {'user_info': user_info, 'user': user, 'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = AnonymousHomeTTSForm(request.POST, request.FILES)
        audio_file_url = None
        fail = False
        audio_converter = AudioConverter()
        if form.is_valid():
            instance = form.save(commit=False)
            text = form.cleaned_data['text']
            if len(text) < 500:
                output_file = audio_converter.text_to_speech(
                    text=text,
                    output_file=f"{text.split()[0]}.mp3",
                )
            else:
                fail = True
            if not fail:
                audio_file_url = f"{settings.MEDIA_URL}{output_file}"
                instance.audiofile = output_file
                instance.save()
        else:
            return render(request, self.template_name, {
                'form': form,
                'audio_file_url': audio_file_url,
                'fail': fail
            }
                          )
        return render(request, self.template_name, {
            'form': form,
            'audio_file_url': audio_file_url,
            'fail': fail
        }
                      )


class UserProfileView(View):
    model = CustomUser
    template_name = 'users/profile.html'
    form_class = UserProfileForm

    def get(self, request, *args, **kwargs):
        user_profile = CustomUser.objects.get(pk=request.user.pk)
        subscription = user_profile.subscription_set.filter(is_active=True).first()
        messages_for_user = messages.get_messages(request)
        return render(
            request,
            self.template_name,
            {
                'user_profile': user_profile,
                'messages_for_user': messages_for_user,
                'subscription': subscription
            }
        )


class EditProfileView(UpdateView):
    template_name = 'users/edit_profile.html'

    def get(self, request, *args, **kwargs):
        user_profile = CustomUser.objects.get(pk=request.user.pk)
        form = UserProfileForm(instance=user_profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_profile = CustomUser.objects.get(pk=request.user.pk)
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', kwargs={'pk': user_profile.pk}))
        return render(request, self.template_name, {'form': form})


class SubscriptionView(View):
    template_name = 'users/subscription.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        duration = int(request.POST.get('duration'))
        start_date = datetime.now()
        end_date = start_date + timedelta(days=duration)
        end_date = end_date.replace(
            hour=start_date.hour,
            minute=start_date.minute,
            second=start_date.second,
            microsecond=start_date.microsecond
        )
        existing_subscription = Subscription.objects.filter(user=request.user, is_active=True).first()
        if existing_subscription:
            existing_subscription.end_date += timedelta(days=duration)
            existing_subscription.save()
        else:
            Subscription.objects.create(
                user=request.user,
                start_date=start_date,
                end_date=end_date,
                is_active=True,
                payment_status=True,
            )

        request.user.is_premium = True
        request.user.save()
        messages.success(request, 'Subscription purchased successfully!')
        return redirect(reverse('profile', kwargs={'pk': request.user.pk}))

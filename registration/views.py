from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect


from registration.forms import UserForm
from profiles.forms import ProfileForm
from profiles.slugify import unique_slugify


def register(request):
    registered = False

    # Messy to include profile stuff here
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        profile_form = ProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            unique_slugify(profile, user.username)
            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request,
                  'registration/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                # If account is valid and active
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used
                return HttpResponse("Your ChrApp account is disabled - please contact the site admin!")
        else:
            # Incorrect login details
            print("Invalid login details.")
            return HttpResponse("Invalid login details supplied.")

    # Request is not a POST so display login form
    else:
        # No context variables to pass to templates system
        return render(request, 'registration/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

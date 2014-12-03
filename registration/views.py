from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404


from guardian.shortcuts import assign_perm


from registration.forms import UserForm, InviteFormSet
from registration.models import Invitation
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

            # Give user permission to view and edit own profile
            assign_perm('profiles.view_profile', user, profile)
            assign_perm('profiles.change_profile', user, profile)

            registered = True

            # Invitation stuff
            if 'invitation' in request.session:
                # Retrieve invitation object
                invitation = Invitation.objects.get(
                    id=request.session['invitation'])

                # Delete the used invitation from the database and session
                invitation.delete()
                del request.session['invitaion']

            # Log user in after registration
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            login(request, user)

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


@login_required
def invite(request):
    if request.method == 'POST':
        formset = InviteFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)

            for instance in instances:
                instance.key = User.objects.make_random_password(20)
                instance.sender = request.user
                instance.save()
                instance.send()

            # invitation = Invitation(
            #     to_name=formset.cleaned_data['to_name'],
            #     to_email=formset.cleaned_data['to_email'],
            #     key=User.objects.make_random_password(20),
            #     sender=request.user
            #     )
            # invitation.save()
            # invitation.send()
            return HttpResponseRedirect(reverse('invite'))
    else:
        previous_invites = Invitation.objects.all()
        formset = InviteFormSet(queryset=Invitation.objects.none())

    variables = RequestContext(request, {
        'formset': formset,
        'previous_invites': previous_invites,
        })
    return render_to_response('registration/friend_invites.html', variables)


def accept(request, key):
    invitation = get_object_or_404(Invitation, key__exact=key)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect(reverse('register'))

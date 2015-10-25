from profile.models import Profile


# User details pipeline
def create_profile(strategy, details, response, user=None, *args, **kwargs):
    print('hi')
    if user:
        print('there is a user')
        if kwargs['is_new']:
            print('user is new')
            attrs = {'user': user}
            Profile.objects.create(user=user)
            print('profile created for {}'.format(user.first_name))

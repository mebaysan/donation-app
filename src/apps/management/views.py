from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode

User = get_user_model()


def password_reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        form = SetPasswordForm(user)
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            # todo: update password change view styles
            # todo: update email template to send in rendered html format
            # todo: fix password change screen
            if form.is_valid():
                print(form.cleaned_data)
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                return redirect('management:password_reset_ok')

        return render(request, 'management/reset_password.html', {
            'form': form,
            'validlink': True,
            'uidb64': uidb64,
            'token': token,
            'errors': form.errors if form.errors else None
        })
    else:
        return render(request, 'management/reset_password.html', {'validlink': False})


def password_reset_complete(request):
    return render(request, 'management/reset_password_complete.html')

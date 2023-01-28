from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login as dj_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import auth
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.donor.models import DonationCategory, DonationItem
from apps.payment.helpers.payment_provider.payment_provider_factory import PaymentProviderFactory

User = get_user_model()


def index(request):
    categories = DonationCategory.objects.filter(is_published=True).all()
    items = DonationItem.objects.filter(is_published=True).all()
    context = {
        'categories': categories,
        'items': items
    }
    return render(request, 'index.html', context=context)


@require_http_methods(["POST"])
@csrf_exempt
def transaction_success(request):
    provider = PaymentProviderFactory.get_payment_provider()
    HttpResponse(provider.approve_payment(request))


@require_http_methods(["POST"])
@csrf_exempt
def transaction_fail(request):
    return HttpResponse(request)


@login_required
def cart(request):
    if request.method == 'POST':
        provider = PaymentProviderFactory.get_payment_provider()
        return provider.make_payment(request)
    return render(request, 'cart.html')


@login_required
@require_http_methods(['POST'])
def cart_update(request):

    return redirect('web:index')


@require_http_methods(['POST'])
def register(request):
    name = request.POST.get('registerName', None)
    surname = request.POST.get('registerSurname', None)
    gender = request.POST.get('registerGender', None)
    email = request.POST.get('registerEmail', None)
    phone_number = request.POST.get('registerPhone', None)
    country = request.POST.get('registerCountry', None)
    city = request.POST.get('registerCity', None)
    state = request.POST.get('registerState', None)
    password = request.POST.get('registerPassword', None)
    password_again = request.POST.get('registerPasswordAgain', None)
    is_approved_to_be_in_touch = request.POST.get('registerIsApprovedToBeInTouch', False)
    if is_approved_to_be_in_touch == 'on':
        is_approved_to_be_in_touch = True

    if password != password_again:
        # Passwords do not match
        messages.error(request, 'Parolalar eşleşmiyor!')
        return redirect('web:login')

    # Create a new user instance
    try:
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
            last_name=surname,
            phone_number=phone_number,
            gender=gender,
            country=country,
            city=city,
            state=state,
            is_approved_to_be_in_touch=is_approved_to_be_in_touch
        )
        donor_group = Group.objects.filter(name='Donor').first()
        user.groups.add(donor_group)
        user.save()
        messages.success(request, 'Kaydınız başarıyla oluşturuldu. Giriş Yapabilirsiniz.')
        return redirect('web:login')
    except Exception as e:
        messages.error(request, f'Kayıt olurken bir hata meydana geldi. Lütfen tekrar deneyin.')
        return redirect('web:login')


def login(request):
    if request.user.is_authenticated:
        return redirect('web:index')
    if request.method == "POST":
        email = request.POST.get("loginEmail", None)
        password = request.POST.get("loginPassword", None)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            dj_login(request, user)
            messages.add_message(
                request, messages.SUCCESS, f"Başarıyla giriş yaptınız."
            )
            return redirect("web:index")
        else:
            messages.add_message(
                request, messages.ERROR, "Kullanıcı bulunamadı."
            )
        return redirect('web:login')
    return render(request, 'auth.html')


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "Başarıyla çıkış yaptınız.")
    return redirect('web:index')


@login_required
def profile(request):
    return render(request, 'profile.html')


@require_http_methods(['POST'])
def profile_update(request):
    name = request.POST.get('profileUpdateName', None)
    surname = request.POST.get('profileUpdateSurname', None)
    gender = request.POST.get('profileUpdateGender', None)
    email = request.POST.get('profileUpdateEmail', None)
    phone_number = request.POST.get('profileUpdatePhone', None)
    country = request.POST.get('profileUpdateCountry', None)
    city = request.POST.get('profileUpdateCity', None)
    state = request.POST.get('profileUpdateState', None)
    is_approved_to_be_in_touch = request.POST.get('profileUpdateIsApprovedToBeInTouch', False)
    if is_approved_to_be_in_touch == 'on':
        is_approved_to_be_in_touch = True

    # Create a new user instance
    try:
        request.user.username = email
        request.user.email = email
        request.user.first_name = name
        request.user.last_name = surname
        request.user.phone_number = phone_number
        request.user.gender = gender
        request.user.country = country
        request.user.city = city
        request.user.state = state
        request.user.is_approved_to_be_in_touch = is_approved_to_be_in_touch

        request.user.save()

        messages.success(request, 'Profiliniz başarıyla güncellendi.')
        return redirect('web:profile')
    except Exception as e:
        messages.error(request, f'Profil güncellenirken bir hata meydana geldi. Lütfen tekrar deneyin.')
        return redirect('web:profile')


@require_http_methods(['POST'])
@login_required
def password_update(request):
    password = request.POST.get('profileUpdatePassword', None)
    password_again = request.POST.get('profileUpdatePasswordAgain', None)

    if password != password_again:
        # Passwords do not match
        messages.error(request, 'Parolalar eşleşmiyor!')
        return redirect('web:profile')

    # Create a new user instance
    try:
        request.user.set_password(password)
        request.user.save()
        messages.success(request, 'Parolanız başarıyla güncellendi.')
        return redirect('web:profile')
    except Exception as e:
        messages.error(request, f'Parola güncellenirken bir hata meydana geldi. Lütfen tekrar deneyin.')
        return redirect('web:profile')

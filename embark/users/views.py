# pylint: disable=R1705
__copyright__ = 'Copyright 2021-2024 Siemens Energy AG, Copyright 2021 The AMOS Projects, Copyright 2021 Siemens AG'
__author__ = 'YulianaPoliakova, Garima Chauhan, p4cx, Benedikt Kuehne, VAISHNAVI UMESH, m-1-k-3'
__license__ = 'MIT'

import builtins
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail

from users.forms import LoginForm, SignUpForm, ResetForm
from users.models import User

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def user_main(request):
    user = get_user(request)
    logger.debug("Account settings for %s", user)
    #   return render(request, 'user/index.html', {"timezones": settings.TIMEZONES, "server_tz": settings.TIME_ZONE, 'user': user})
    return render(request, 'user/index.html', {"timezones": settings.TIMEZONES, "server_tz": settings.TIME_ZONE})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        logger.debug(request.POST)
        try:
            user = get_user(request)
            signup_form = SignUpForm(data=request.POST)
            if signup_form.is_valid():
                username = signup_form.cleaned_data.get('username')
                password = signup_form.cleaned_data.get('password2')
                email = signup_form.cleaned_data.get('email')
                user = User.objects.create(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                logger.debug('User created')
                token = default_token_generator.make_token(user)
                current_site = get_current_site(request)
                mail_subject = 'Activate your EMBArk account.'
                message = render_to_string('user/email_template_activation.html', context={
                    'username': user.username,
                    'domain': current_site.domain,
                    'uid': user.id,
                    'token': token,
                })
                if settings.EMAIL_ACTIVE is True:
                    send_mail(mail_subject, message, 'system@' + settings.DOMAIN, [email])
                    messages.success(request, 'Registration successful. Please check your email to activate')
                    return redirect(reverse('embark-activate-user', kwargs={'uuid': user.id}))
                else:
                    logger.debug("Registered, redirecting to login")
                    if activate_user(user, token):
                        messages.success(request, 'Registration successful.')
                        return redirect(reverse('embark-login'))
                    else:
                        raise ValidationError("Activation Error")
        except builtins.Exception as error:
            logger.exception('Wide exception in Signup: %s', error)
            messages.error(request, 'Something went wrong when signing up the user.')
    else:
        signup_form = SignUpForm()
    return render(request, 'user/register.html', {'form': signup_form})


@require_http_methods(["GET", "POST"])
def embark_login(request):
    if request.method == "POST":
        try:
            login_form = LoginForm(request=request, data=request.POST)
            logger.debug(login_form)
            if login_form.is_valid():
                logger.debug('form valid')
                user = login_form.get_user()
                if user:
                    logger.debug('User authenticated')
                    login(request, user)
                    logger.debug('User logged in')
                    request.session["django_timezone"] = user.timezone
                    # messages.success(request, str(user.username) + ' timezone set to : ' + str(user.timezone))
                    return redirect('embark-uploader-home')
                logger.debug('User could not be authenticated')
            logger.debug('Form errors: %s', str(login_form.errors))
        except ValidationError as valid_error:
            logger.error("Exception in value: %s ", valid_error)
            messages.error(request, 'User is deactivated')
        except builtins.Exception as error:
            logger.exception('Wide exception in Signup: %s', error)
            messages.error(request, 'Something went wrong when logging in the user.')
    login_form = LoginForm()
    return render(request, 'user/login.html', {'form': login_form})


@login_required(login_url='/' + settings.LOGIN_URL)
def embark_logout(request):
    logout(request=request)
    logger.debug("Logout user %s", request)
    messages.success(request, 'Logout successful.')
    return redirect('embark-login')


@login_required(login_url='/' + settings.LOGIN_URL)
@require_http_methods(["GET", "POST"])
def password_change(request):   # TODO adapt t
    if request.method == "POST":
        logger.debug(request.POST)
        user = get_user(request)

        data = {k: v[0] for k, v in dict(request.POST).items()}
        logger.debug(data)
        try:
            body = {k: v[0] for k, v in dict(request.POST).items()}
            try:
                old_password = body['oldPassword']
                new_password = body['newPassword']
                confirm_password = body['confirmPassword']

                if user.check_password(old_password):
                    if old_password == new_password:
                        logger.debug('New password = old password')
                        messages.error(request, 'New password matches the old password')
                        return render(request, 'user/passwordChange.html')
                    if new_password == confirm_password:
                        user.set_password(new_password)
                        user.save()
                        authenticate(request, username=user.username, password=new_password)
                        login(request, user)
                        logger.debug('New password set, user authenticated')
                        messages.success(request, 'Password change successful.')
                        return render(request, 'user/passwordChangeDone.html')
                    else:
                        logger.debug('Passwords do not match')
                        messages.error(request, 'Passwords do not match.')
                        return render(request, 'user/passwordChange.html')
                else:
                    logger.debug('Old password is incorrect')
                    messages.error(request, 'Old password is incorrect.')
                    return render(request, 'user/passwordChange.html')
            except KeyError:
                logger.exception('Missing keys from data-passwords')
                messages.error(request, 'Some fields are empty!')
                return render(request, 'user/passwordChange.html')
        except builtins.Exception as error:
            logger.exception('Wide exception in Password Change: %s', error)
            messages.error(request, 'Something went wrong when changing the password for the user.')
            return render(request, 'user/passwordChange.html')
    return render(request, 'user/passwordChange.html')


@csrf_exempt
@login_required(login_url='/' + settings.LOGIN_URL)
@require_http_methods(["GET", "POST"])
def acc_delete(request):
    if request.method == "POST":
        logger.debug('disabling account')
        user = get_user(request)
        email = user.email
        token = default_token_generator.make_token(user)
        current_site = get_current_site(request)
        mail_subject = 'Delete your EMBArk account.'
        message = render_to_string('user/email_template_deactivation.html', context={
            'user': user,
            'username': user.username,
            'domain': current_site.domain,
            'uid': user.id,
            'token': token,
        })
        if settings.EMAIL_ACTIVE is True:
            send_mail(mail_subject, message, 'system@' + settings.DOMAIN, [email])
            messages.success(request, 'Please check your email to confirm deletion')
            return redirect(reverse('embark-deactivate-user', kwargs={'uuid': user.id}))
        else:
            logger.debug(' %s Account: %s disabled', timezone.now().strftime("%H:%M:%S"), user)
            user.username = user.get_username() + '_disactivated_' + timezone.now().strftime(
                "%H:%M:%S")     # workaround for not duplicating entry users_user.username
            user.is_active = False
            user.save()
            messages.success(request, 'Account successfully deleted.')
            return redirect('embark-login')
    return render(request, 'user/accountDelete.html')


@require_http_methods(["GET"])
def deactivate(request, user_id):   # TODO
    logger.debug("deactivating user with id : %s", user_id)
    return render(request, 'user/login.html')


@require_http_methods(["GET"])
@login_required(login_url='/' + settings.LOGIN_URL)
def get_log(request, log_type, lines):      # FIXME move to admin
    """
    View takes a get request with following params:
    1. log_type: selector of log file (daphne, migration, mysql_db, redis_db, uwsgi, web)
    2. lines: lines in log file
    Args:
        request: HTTPRequest instance

    Returns:

    """
    log_file_list = ["daphne", "migration", "mysql_db", "redis_db", "uwsgi", "web"]
    log_file = log_file_list[int(log_type)]
    file_path = f"{settings.BASE_DIR}/logs/{log_file}.log"
    logger.info('Load log file: %s', file_path)
    try:
        with open(file_path, encoding='utf-8') as file_:
            try:
                buffer_ = 500
                lines_found = []
                block_counter = -1

                while len(lines_found) <= lines:
                    try:
                        file_.seek(block_counter * buffer_, 2)
                    except IOError:
                        file_.seek(0)
                        lines_found = file_.readlines()
                        break

                    lines_found = file_.readlines()
                    block_counter -= 1

                result = lines_found[-(lines + 1):]
            except builtins.Exception as error:
                logger.exception('Wide exception in logstreamer: %s', error)

        return render(request, 'user/log.html', {'header': log_file + '.log', 'log': ''.join(result), 'username': request.user.username})
    except IOError:
        return render(request, 'user/log.html', {'header': 'Error', 'log': file_path + ' not found!', 'username': request.user.username})


@require_http_methods(["POST"])
@login_required(login_url='/' + settings.LOGIN_URL)
def set_timezone(request):
    if request.method == "POST":
        user = get_user(request)
        new_timezone = request.POST["timezone"]
        request.session["django_timezone"] = new_timezone
        user.timezone = new_timezone
        user.save()
        messages.success(request, str(user.username) + ' timezone set to : ' + str(new_timezone))
        return redirect("..")
    else:
        messages.error(request, 'Timezone could not be set')
        return redirect("..")


def activate_user(user, token):
    """
    activates user with token
    """
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return True
    return False


@require_http_methods(["GET"])
@login_required(login_url='/' + settings.LOGIN_URL)
def activate(request, user_id, token):
    """
    activation page + form request
    activates user through the usage of token
    """
    try:
        user = User.objects.get(id=user_id)
        if activate_user(user, token):
            login(request, user)
            messages.success(request, str(user.username) + 'activated')
        else:
            messages.error(request, "Token invalid - maybe it expired?")
    except ValueError as val_error:
        logger.error("%s in token %s", val_error, token)
    return redirect(reverse('embark-MainDashboard'))


@require_http_methods(["GET", "POST"])
def reset_password(request):
    if request.method == 'POST':
        reset_form = ResetForm(request.POST)
        if reset_form.is_valid():
            logger.debug('Form is valid')
            reset_form.save(request=request)
            messages.success(request, 'Send Password reset request')
    reset_form = ResetForm()
    admin_email = User.objects.get(username='admin').email
    return render(request, 'user/lostPassword.html', {'form': reset_form, 'email_setting': settings.EMAIL_ACTIVE, 'admin_email': admin_email})

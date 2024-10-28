import redis
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

REDIS_URL = settings.REDIS_URL


def send_password_reset_email(user_email, reset_link):
    """
    Sends an email to the user with a link to reset their password.
    """
    subject = "Password Reset Request - Connectix"
    html_message = render_to_string(
        "password_reset_mail.html", {"reset_link": reset_link}
    )
    plain_message = strip_tags(html_message)
    from_email = "no-reply@connectix.com"
    send_mail(
        subject, plain_message, from_email, [user_email], html_message=html_message
    )


def send_magic_link_email(user_email, magic_link):
    """
    Sends an email to the user with a link to reset their password.
    """
    subject = "Magic Link - Connectix"
    html_message = render_to_string("magic_link_mail.html", {"magic_link": magic_link})
    plain_message = strip_tags(html_message)
    from_email = "no-reply@connectix.com"
    send_mail(
        subject, plain_message, from_email, [user_email], html_message=html_message
    )


def get_redis_client():
    return redis.from_url(REDIS_URL)

from django.conf import settings
from django.core.mail import send_mail


# ============================================================
# EMAIL VERIFICATION
# ============================================================

def send_verification_email(user, token):

    verification_url = (
        f"{settings.FRONTEND_URL}"
        f"/verify-email?token={token}"
    )

    print("\n" + "=" * 80)
    print("ZEVORA EMAIL VERIFICATION")
    print("=" * 80)
    print(f"User: {user.email}")
    print("Verification URL:")
    print(verification_url)
    print("=" * 80 + "\n")

    send_mail(
        subject="Verify your ZEVORA account",
        message=(
            f"Hello {user.first_name or user.username},\n\n"
            f"Welcome to ZEVORA!\n\n"
            f"Please verify your ZEVORA account by opening "
            f"the link below:\n\n"
            f"{verification_url}\n\n"
            f"This link expires in 24 hours.\n\n"
            f"If you did not create a ZEVORA account, "
            f"you can safely ignore this email.\n\n"
            f"Regards,\n"
            f"ZEVORA Team"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            user.email
        ],
        fail_silently=False,
    )


# ============================================================
# PASSWORD RESET
# ============================================================

def send_password_reset_email(user, token):

    reset_url = (
        f"{settings.FRONTEND_URL}"
        f"/reset-password?token={token}"
    )

    print("\n" + "=" * 80)
    print("ZEVORA PASSWORD RESET")
    print("=" * 80)
    print(f"User: {user.email}")
    print("Reset URL:")
    print(reset_url)
    print("=" * 80 + "\n")

    send_mail(
        subject="Reset your ZEVORA password",
        message=(
            f"Hello {user.first_name or user.username},\n\n"
            f"We received a request to reset your "
            f"ZEVORA password.\n\n"
            f"Reset your password here:\n"
            f"{reset_url}\n\n"
            f"This link expires in 30 minutes.\n\n"
            f"If you did not request this, "
            f"you can safely ignore this email.\n\n"
            f"Regards,\n"
            f"ZEVORA Team"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            user.email
        ],
        fail_silently=False,
    )
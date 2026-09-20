from django.core import signing


# ============================================================
# SALTS
# ============================================================

PASSWORD_RESET_SALT = "zevora-password-reset"
EMAIL_VERIFICATION_SALT = "zevora-email-verification"


# ============================================================
# EMAIL VERIFICATION TOKEN
# ============================================================

def create_verification_token(user):
    """
    Create a signed token for email verification.
    Token expires after 24 hours.
    """

    return signing.dumps(
        {
            "user_id": user.id,
            "email": user.email,
        },
        salt=EMAIL_VERIFICATION_SALT,
    )


def verify_verification_token(token):
    """
    Verify email verification token.

    Token is valid for 24 hours.
    """

    return signing.loads(
        token,
        salt=EMAIL_VERIFICATION_SALT,
        max_age=60 * 60 * 24,
    )


# ============================================================
# PASSWORD RESET TOKEN
# ============================================================

def create_password_reset_token(user):
    """
    Create a signed password reset token.
    """

    return signing.dumps(
        {
            "user_id": user.id,
            "email": user.email,
        },
        salt=PASSWORD_RESET_SALT,
    )


def verify_password_reset_token(token):
    """
    Verify password reset token.

    Token is valid for 30 minutes.
    """

    return signing.loads(
        token,
        salt=PASSWORD_RESET_SALT,
        max_age=60 * 30,
    )
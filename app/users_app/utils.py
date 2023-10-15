from password_strength import PasswordPolicy


def validate_password_strength(password):
    # Define a password policy
    policy = PasswordPolicy.from_names(
        length=8,
        uppercase=1,
        numbers=1,
        special=1,
    )
    errors = policy.test(password)
    return len(errors) == 0

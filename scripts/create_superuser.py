from django.contrib.auth import get_user_model

def main():
    User = get_user_model()
    email = 'simaclaverly@gmail.com'
    pw = '..,,'

    u = User.objects.filter(email=email).first()
    if u is None:
        # Create superuser with username derived from email local part
        username = email.split('@')[0]
        u = User.objects.create_superuser(username, email, pw)
        print('created', u.username)
    else:
        # Update existing user to be a superuser and set password
        u.username = email.split('@')[0]
        u.is_staff = True
        u.is_superuser = True
        u.set_password(pw)
        u.save()
        print('updated', u.username)

if __name__ == '__main__':
    main()

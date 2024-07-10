from django.db import models
import bcrypt


class MyUserModelManager(models.Manager):
    def create(self, **kwargs):
        """
        Intercept user creation to has password
        """
        plain_passwd = kwargs.get('password')
        if plain_passwd:
            hashed_pwd = MyUserModelManager.hash_password(plain_passwd)
            kwargs['password'] = hashed_pwd

        # Create the user instance
        new_user = super().create(**kwargs)  # here, the object is created

        return new_user  # return instance

    @staticmethod
    def hash_password(plain_pwd: str):
        """
        Hash password before user creation
        """
        try:
            hashed_pwd = bcrypt.hashpw(plain_pwd.encode(), bcrypt.gensalt())
            return hashed_pwd.decode()
        except Exception as exc:
            print(f'error hashing password: {exc}')
            raise Exception(
                "Could not hash password, check problems!."
            ) from exc

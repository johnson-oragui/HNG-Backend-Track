from django.db import models
import bcrypt


class MyUserModelManager(models.Manager):
    def create(self, **kwargs):
        """
        Intercept user creation to has password
        """
        from organisation.models import Organisation
        from user_organisation.models import UserOrganisation
        plain_passwd = kwargs.get('password')
        if plain_passwd:
            hashed_pwd = MyUserModelManager.hash_password(plain_passwd)
            kwargs['password'] = hashed_pwd

        # Create the user instance
        new_user = super().create(**kwargs)  # here, the object is created
        description = f"{new_user.first_name} is the Greatest"

        # Create the organisation with user's firstName
        organisation = Organisation.objects.create(name=new_user.first_name,
                                                   owner_email=new_user.email,
                                                   description=description)

        # Assuming kwargs includes a "role" parameter
        role = kwargs.get('role', 'owner')  # Default to "owner" if not provided

        # Create user-organisation association
        user_org = UserOrganisation.objects.create(user=new_user,
                                                   organisation=organisation,
                                                   role=role)

        return new_user  # return instance

    @staticmethod
    def hash_password(plain_pwd: str):
        """
        Hash password before user creation
        """
        if not plain_pwd or not isinstance(plain_pwd, str) or plain_pwd.strip() == '':
            raise ValueError("password must be a string")
        try:
            salt = bcrypt.gensalt()
            encoded_pwd = plain_pwd.encode()

            hashed_pwd = bcrypt.hashpw(encoded_pwd, salt=salt)

            return hashed_pwd
        except Exception as exc:
            print(f'error hashing password: {exc}')
            raise Exception(
                "Could not hash password, check problems!."
            ) from exc

    def get_user_by_email_or_id(self, email=None, user_id=None):
        """
        Retrieve user with email or user_id
        """
        try:
            if email and not user_id:
                user = self.filter(email=email)
                if user:
                    return user
                else:
                    return
            if user_id and not email:
                user = self.filter(user_id=user_id)
                if user:
                    return user
                else:
                    return
            if user_id and email:
                user = self.filter(user_id=user_id, email=email)
                if user:
                    return user
                else:
                    return
        except Exception as exc:
            print(f'error retrieving user by email or id: {exc}')
            return

    def update_user(self, data: dict = None):
        """
        Update a user
        """
        if not data or not isinstance(data, dict):
            raise ValueError(f"{data} is empty or not a dictionary")

        try:
            updated_usser = self.update(**data)
            return updated_usser
        except Exception as exc:
            print(f'error updating user: {exc}')
            raise Exception("could not update user") from exc

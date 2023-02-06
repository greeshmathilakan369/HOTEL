from django.contrib.auth.base_user import BaseUserManager



# class CustomUserManager(BaseUserManager):
#     """
#     Custom user model where the email address is the unique identifier
#     and has an is_admin field to allow access to the admin app 
#     """
    

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_active', True)
#         extra_fields.setdefault('role', 1)
#         is_superuser=True

#         if extra_fields.get('role') != 1:
#             raise ValueError('Superuser must have role of Global Admin')
#         return self.create_user(email, password, **extra_fields)


class CustomUserManager(BaseUserManager):
    def create_user(self, email,first_name,role,last_name,password=None):
        
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            role=role,
            last_name=last_name
            # address=address,
            # phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None):
        
        user = self.create_user(
            email,
            password=password,
            
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
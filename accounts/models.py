from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_student_user(self, email, first_name, second_name, phone_number, city, location, password=None, password2=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            second_name = second_name,
            phone_number = phone_number,
            city = city,
            location = location,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_company_user(self, email, company_name, description, city, location, password=None, password2=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            company_name = company_name,
            description = description,
            city = city,
            location = location,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    
    objects = UserManager()
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_student(self):
        try:
            return self.student is not None
        except Student.DoesNotExist:
            return False

    @property
    def is_company(self):
        try:
            return self.company is not None
        except Company.DoesNotExist:
            return False

# Here we use Inheritance for creating the multi-users

class Company(User):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        parent_link=True,
        related_name='company',
    )
    company_name = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    location = models.ForeignKey('Location', on_delete=models.PROTECT)


    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companys')

class Student(User):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        parent_link=True,
        related_name='student',
    )
    first_name = models.CharField(max_length=256)
    second_name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=256)
    city = models.ForeignKey('City', on_delete=models.PROTECT)
    location = models.ForeignKey('Location', on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

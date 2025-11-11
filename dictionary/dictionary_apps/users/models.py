from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models
from django.utils import timezone


from datetime import timedelta

from dictionary.dictionary_apps.common.models import BaseModel, UserRole

DEFAULT_USER_ROLE = 2
DEFAULT_USER_ADMIN_ROLE = 1
class BaseUserManager(BUM):
    def authenticate(self, email=None, password=None):
        try:
            user = self.get(email=email)
        except BaseUser.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def create_user(self, email, is_active=True, user_role=DEFAULT_USER_ROLE, is_admin=False, username=None,
                    name=None, surname=None, phone=None, password=None, score=None, chat_id=None,
                    telegram_username=None):
        if not email:
            raise ValueError("Users musr have email address")

        user = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            user_role=UserRole.objects.get(id=user_role),
            name=name,
            surname=surname,
            username=username,
            phone=phone,
            chat_id=chat_id,
            telegram_username=telegram_username,


        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            user_role=DEFAULT_USER_ADMIN_ROLE,
            password=password,

        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    MAX_LIFES = 5
    name = models.CharField(max_length=100, blank=True, null=True, default='')
    surname = models.CharField(max_length=100, blank=True, null=True, default='')
    username = models.CharField(max_length=100, blank=True, null=True, default='', unique=True)
    email = models.EmailField(
        verbose_name='email_address',
        max_length=255,
        unique=True,
    )
    registration_date = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True, null=True, default='')
    last_login_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    user_role = models.ForeignKey(UserRole, related_name='user_role', on_delete=models.CASCADE, default=2)
    chat_id = models.IntegerField(blank=True, null=True, default=0)
    telegram_username = models.CharField(blank=True, null=True, default=None, max_length=100)
    user_bot_pass = models.CharField(max_length=100, blank=True, null=True, default='')
    score = models.IntegerField(blank=True, null=True, default=0)
    lifes = models.IntegerField(blank=True, null=True, default=5)
    last_life_update = models.DateTimeField(default=timezone.now)#null=True, blank=True)
    user_bot_id = models.IntegerField(blank=True, null=True, default=0)
    user_bot_pass = models.CharField(max_length=100, blank=True, null=True, default='')


    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="baseuser_set",  # Уникальное имя для обратной связи
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="baseuser_set",  # Уникальное имя для обратной связи
        related_query_name="user",
    )
    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin#True if self.user_role.id == 4 else False

    def restore_lifes(self):
        print('RESTORE')
        if self.email == 'aleshinaolg@gmail.com' or self.email == 'alex@gmail.com':
            self.lifes = 1000
            self.save(update_fields=['lifes', 'last_life_update', 'last_login_date'])
        if self.lifes >= self.MAX_LIFES:
            return

        now_update = timezone.now()
        if self.last_life_update is None:
            self.last_life_update = now_update
            self.last_login_date = now_update
            self.save(update_fields=['last_life_update', 'last_login_date'])
            return
        elasped = now - self.last_life_update
        hours_passred = int(elasped.total_seconds() // 3600)

        if hours_passred > 0:
            print(self.email)

            self.lifes = min(self.lifes + hours_passred, self.MAX_LIFES)
            self.last_life_update += timedelta(hours=hours_passred)
            self.save(update_fields=['lifes', 'last_life_update'])

















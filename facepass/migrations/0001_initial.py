# Generated by Django 3.2.4 on 2021-07-30 21:17

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('face_signature', models.JSONField(blank=True, default=str)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AllowedInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(choices=[('firstname', 'Firstname'), ('lastname', 'Lastname'), ('email', 'Email'), ('birthdate', 'Birthdate'), ('age', 'Age'), ('address', 'Address'), ('city', 'City'), ('country', 'Country'), ('postal_code', 'Postal Code'), ('ssn', 'Ssn'), ('phone_number', 'Phone Number'), ('credit_card_number', 'Credit Card Number')], max_length=200, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('api_key', models.CharField(blank=True, default=None, max_length=30, null=True, unique=True)),
                ('success_url', models.URLField(blank=True, default=None, null=True)),
                ('error_url', models.URLField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_profiles', to=settings.AUTH_USER_MODEL)),
                ('requested_information', models.ManyToManyField(blank=True, default=None, related_name='company_profiles', to='facepass.AllowedInformation')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('lastname', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True)),
                ('birthdate', models.DateTimeField(blank=True, default=None, null=True)),
                ('age', models.IntegerField(blank=True, default=None, null=True)),
                ('address', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('country', models.CharField(blank=True, default=None, max_length=200, null=True)),
                ('postal_code', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('ssn', models.CharField(blank=True, default=None, max_length=16, null=True)),
                ('phone_number', models.CharField(blank=True, default=None, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format:         '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('credit_card_number', models.CharField(blank=True, default=None, max_length=16, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('owner', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='personal_information', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_restricted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('allowed_information', models.ManyToManyField(blank=True, default=None, related_name='passes', to='facepass.AllowedInformation')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passes', to='facepass.companyprofile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Passes',
            },
        ),
    ]

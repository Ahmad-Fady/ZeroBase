from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Student, Company

class AddUserForm(forms.ModelForm):
    """
    New User Form. Requires password confirmation.
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email','staff','is_active','admin',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UpdateUserForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'password', 'is_active',
            'staff','admin'
        )

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = ('email','staff','is_active','admin','last_login')
    list_filter = ('staff','is_active','admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ('first_name', 'second_name', 'gender', 'role', 'resume', 'phone_number', 'organizationName','organizationStrength', 'organizationType',)}),
        ('Permissions', {'fields': ('is_active', 'staff','admin')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ()
    ordering = ('email',)
    filter_horizontal = ()

class AddStudentForm(forms.ModelForm):
    """
    New User Form. Requires password confirmation.
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = Student
        fields = ('email', 'first_name', 'second_name','phone_number', 'city', 'location',)

    # this function checks that the location is in the right city
    def clean_location(self):
        city = self.cleaned_data['city']
        location = self.cleaned_data['location']
        if location.city != city:
            raise forms.ValidationError("The location is not in this city")
        return location

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UpdateStudentForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Student
        fields = (
            'email', 'password','first_name', 'second_name', 'phone_number', 'city', 'location',
        )

    def clean_password(self):
# Password can't be changed in the admin
        return self.initial["password"]

class StudentAdmin(BaseUserAdmin):
    form = UpdateStudentForm
    add_form = AddStudentForm

    list_display = ('email','first_name', 'second_name', 'phone_number', 'city', 'location',)
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'second_name', 'phone_number', 'city', 'location',)}),
        # ('Permissions', {'fields': ('is_active', 'staff','admin')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email','first_name', 'second_name', 'phone_number', 'city', 'location', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ()
    ordering = ('email','first_name', 'second_name')
    filter_horizontal = ()

class AddCompanyForm(forms.ModelForm):
    """
    New User Form. Requires password confirmation.
    """
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm password', widget=forms.PasswordInput
    )

    class Meta:
        model = Company
        fields = ('email','company_name','description', 'city', 'location',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UpdateCompanyForm(forms.ModelForm):
    """
    Update User Form. Doesn't allow changing password in the Admin.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Company
        fields = (
            'email', 'password','company_name','description', 'city', 'location',
        )

    def clean_password(self):
# Password can't be changed in the admin
        return self.initial["password"]

class CompanyAdmin(BaseUserAdmin):
    form = UpdateCompanyForm
    add_form = AddCompanyForm

    list_display = ('email','company_name','description')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('company_name', 'description', 'city', 'location',)}),
        # ('Permissions', {'fields': ('is_active', 'staff','admin')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email','company_name','description', 'password1',
                    'password2'
                )
            }
        ),
    )
    search_fields = ()
    ordering = ('email','company_name','description')
    filter_horizontal = ()

admin.site.register(User,UserAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Company,CompanyAdmin)


# admin.site.register(Student)
# admin.site.register(Company)

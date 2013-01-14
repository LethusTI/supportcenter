# -*- coding: utf-8 -*

from itertools import chain

from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
from mongotools.forms import MongoForm

from lethusbox.django.forms import FilterForm

from models import User, UnidadeProfile
from constants import PERMISSIONS
from widgets import PermissionSelect, ActionSelect

def base36encode(number):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    base36 = ''
    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]

class UserCreationForm(MongoForm):
    """
    Formulário de Criação de usuário.
    possui senha e senha de confirmação
    """
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput)

    def clean_username(self):
        """
        Checa se o usuáio é único no banco de dados
        """
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        """
        Compara as duas senhas
        """
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        """
        Salva o usuário e seta a senha
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user

    class Meta:
        document = User
        fields = ("username",)

class UserChangeForm(MongoForm):
    """
    Formulário de Alteração do usuário
    """
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    class Meta:
        document = User

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

class AuthenticationForm(forms.Form):
    """
    Formulário para Login
    """
    username = forms.CharField(label=_("Username"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                _("Your Web browser doesn't appear to have cookies enabled. "
                  "Cookies are required for logging in."))

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=75)

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(
                                email__iexact=email,
                                is_active=True
                            )
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        from django.core.mail import send_mail
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            t = loader.get_template(email_template_name)

            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': base36encode(int(str(user.pk), 16)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            send_mail(_("Password reset on %s") % site_name,
                t.render(Context(c)), from_email, [user.email])

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without
    entering the old password
    """
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class PasswordChangeForm(SetPasswordForm):
    """
    Formulário para um usuário alterar sua propria senha
    """
    old_password = forms.CharField(label=_("Old password"), widget=forms.PasswordInput)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("Your old password was entered incorrectly. Please enter it again."))
        return old_password

PasswordChangeForm.base_fields.keyOrder = ['old_password', 'new_password1', 'new_password2']

class AdminPasswordChangeForm(forms.Form):
    """
    Formulário para um Administrador alterar a senha de um usuário
    """
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (again)"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'minlength':'4'})
        self.fields['password2'].widget.attrs.update({'minlength':'4',
                                                      'equalTo':'#id_password1'})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        """
        Saves the new password.
        """
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user

class AccountForm(MongoForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['email'].widget.attrs['class'] = 'email'

    class Meta:
        fields = ('first_name', 'last_name', 'email')
        document = User

class SuperUserForm(MongoForm):
    full_name = forms.CharField(label="Nome completo", required=True)

    def __init__(self, *args, **kwargs):
        super(SuperUserForm, self).__init__(*args, **kwargs)

        self.fields.insert(0, 'full_name', self.fields['full_name'])

        if self.instance:
            self.initial['full_name'] = self.instance.get_full_name()

    def clean_username(self):
        username = self.cleaned_data["username"]
        filter_args = {'username': username}

        if self.instance and self.instance.pk:
            filter_args['pk__ne'] = self.instance.pk

        if User.objects(**filter_args).count() > 0:
            raise forms.ValidationError(
                "Já existe um usuário com esse nome por favor escolha outro.")

        return username

    def save(self, *args, **kwargs):
        obj = super(SuperUserForm, self).save(commit=False)

        parts = self.cleaned_data['full_name'].split(' ', 1)

        if len(parts) == 2:
            obj.first_name, obj.last_name = parts
        else:
            obj.first_name = parts[0]
            obj.last_name = None

        obj.is_superuser = True

        if kwargs.pop('commit', True):
            obj.save()

        return obj

    class Meta:
        document = User
        fields = ('username', 'email', 'is_active')

class AddSuperUserForm(SuperUserForm):
    password1 = forms.CharField(required=True, label="Senha",
        widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(required=True, label="Confirmar Senha",
        widget=forms.PasswordInput(render_value=True))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("A confirmação da senha não confere, verifique.")
        return password2

    def save(self, *args, **kwargs):
        obj = super(AddSuperUserForm, self).save(commit=False)
        obj.set_password(self.cleaned_data["password1"])

        if kwargs.pop('commit', True):
            obj.save()

        return obj

    class Meta:
        document = User
        fields = ('username', 'email', 'is_active')

class UnidadeProfileForm(MongoForm):
    full_name = forms.CharField(label="Nome completo", required=True)
    permissions = forms.MultipleChoiceField(
        label=u" ",
        choices=list(chain(*[[(i, i) for i in x]
                             for x in PERMISSIONS.values()])),
        widget=PermissionSelect(attrs={'class':'permission'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super(UnidadeProfileForm, self).__init__(*args, **kwargs)

        self.fields.insert(0, 'full_name', self.fields['full_name'])

        if self.instance:
            self.initial['full_name'] = self.instance.get_full_name()
            self.initial['permissions'] = self.instance.permissions or None

    def save(self, *args, **kwargs):
        obj = super(UnidadeProfileForm, self).save(commit=False)

        parts = self.cleaned_data['full_name'].split(' ', 1)

        if len(parts) == 2:
            obj.first_name, obj.last_name = parts
        else:
            obj.first_name = parts[0]
            obj.last_name = None

        obj.permissions = self.cleaned_data.get('permissions', None) or None

        if kwargs.pop('commit', True):
            obj.save()

        return obj

    class Meta:
        document = UnidadeProfile
        fields = ('username', 'email', 'is_active', 'unidade')

class AddUnidadeProfileForm(UnidadeProfileForm):
    password1 = forms.CharField(required=True, label="Senha",
        widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(required=True, label="Confirmar Senha",
        widget=forms.PasswordInput(render_value=True))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("A confirmação da senha não confere, verifique.")
        return password2

    def save(self, *args, **kwargs):
        obj = super(AddUnidadeProfileForm, self).save(commit=False)
        obj.set_password(self.cleaned_data["password1"])

        if kwargs.pop('commit', True):
            obj.save()

        return obj

    class Meta:
        document = UnidadeProfile
        fields = ('username', 'email', 'is_active', 'unidade')

class HistoricFilterForm(FilterForm):                         
    module = forms.ChoiceField(label="Módulo",
                               choices=(), widget=forms.Select,
                               required=False)

    action = forms.ChoiceField(label="Ação",
                               choices=(), required= False)


    def __init__(self, data, filter_module, filter_action, *args, **kwargs):
        super(HistoricFilterForm, self).__init__(data, *args, **kwargs)

        self.fields['module'].choices = ([('', 'Todos módulos')] +
                                         [(x, y) for x, y in filter_module()])

        self.fields['action'].choices = ([('', 'Todas ações')] +
                                         [(x, y)
                                          for x, y in filter_action()])

        self.fields['action'].widget = ActionSelect(filter_module = filter_module,
                                                    filter_action = filter_action)

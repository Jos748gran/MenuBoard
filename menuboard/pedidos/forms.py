from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from pedidos.models import Plato, Mesa, Cliente, Pedido, Mesero, PersonalCocina, ItemPedido
from util.models import UserProfile

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    cedula = forms.CharField(max_length=10, required=True)
    telefono = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                cedula=self.cleaned_data['cedula'],
                telefono=self.cleaned_data['telefono'],
            )
            clientes_group, created = Group.objects.get_or_create(name='Clientes')
            user.groups.add(clientes_group)
            Cliente.objects.create(
                nombre=user.username,
                cedula=self.cleaned_data['cedula'],
                telefono=self.cleaned_data['telefono'],
            )
        return user

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'precio','imagen']

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['capacidad',]

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre','cedula','telefono',]

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente','estado','mesa','item_pedido_list',]

class MeseroForm(forms.ModelForm):
    class Meta:
        model = Mesero
        fields = ['nombre','cedula','telefono',]

class PersonalCocinaForm(forms.ModelForm):
    class Meta:
        model = PersonalCocina
        fields = ['nombre','cedula','telefono',]

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['cliente','plato','cantidad','observacion',]

class ItemPedidoFormMod(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['cantidad','observacion',]

class OrdenarPedidoForm(forms.Form):
    es_para_llevar = forms.BooleanField(required=False, label='Para llevar')
    mesa_ocupada = forms.ModelChoiceField(queryset=Mesa.objects.filter(esta_disponible=True), required=False, label='Mesa')
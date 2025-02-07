from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from pedidos.models import Plato, Mesa, Cliente, Pedido, Mesero, PersonalCocina, ItemPedido


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

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
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
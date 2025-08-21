from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Patient, Doctor, Consultation

User = get_user_model()  

# Formulaires d'authentification personnalisés
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Entrez votre nom d'utilisateur"
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe'
        })
    )

# Formulaires d'inscription spécifiques
class PatientRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'address')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Labels en français
        self.fields['username'].label = "Nom d’utilisateur"
        self.fields['email'].label = "Adresse e-mail"
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"
        self.fields['phone_number'].label = "Numéro de téléphone"
        self.fields['address'].label = "Adresse complète"
        # self.fields['first_name'].label = "Prenom"
        # self.fields['last_name'].label = "Nom"
        self.fields['username'].error_messages = {
            'required' : 'Le nom d\'utilisateur\' est obligatoire ',
            'invalid'  : 'selectionner un nom d\'utilisateur valide '
        }   
        self.fields['email'].error_messages = {
            'required' : 'L\'email d\'utilisateur\' est obligatoire ',
            'invalid'  : 'selectionner un email d\'utilisateur valide '
        }  
        self.fields['password1'].error_messages = {
            'required' : 'le mot de passe est obligatoire ',
            'invalid'  : 'selectionner mot de passe valide '
        }  
        self.fields['password2'].error_messages = {
            'required' : 'Le mot de passe est obligatoire ',
            'invalid'  : 'selectionner un mot de passe valide '
        }  
        self.fields['address'].error_messages = {
            'required' : 'L\'adresse d\'utilisateur\' est obligatoire ',
            'invalid'  : 'selectionner une adresse valide '
        }              
        self.fields['phone_number'].error_messages = {
            'required' : 'Le numero d\'utilisateur\' est obligatoire ',
            'invalid'  : 'selectionner un numero valide '
        }  

        # Placeholders pour guider l'utilisateur
        placeholders = {
            'username': 'Entrez votre nom d’utilisateur',
            'email': 'exemple@mail.com',
            'password1': 'Votre mot de passe sécurisé',
            'password2': 'Répétez votre mot de passe',
            'phone_number': 'Ex: +224 620 00 00 00',
            'address': 'Votre adresse complète',
            # 'last_name' : 'Entrez votre nom',
            # 'first_name' : 'Entrez votre prenom',
        }

        # Appliquer style Bootstrap et fond clair à tous les champs
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg rounded-3',
                    'placeholder': placeholders.get(name, ''),
                    'rows': 3,
                    'style': 'background-color: #f9f9f9; border: 1px solid #ddd;'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg rounded-3',
                    'placeholder': placeholders.get(name, ''),
                    'style': 'background-color: #f9f9f9; border: 1px solid #ddd;'
                }) 
        

class DoctorRegistrationForm(UserCreationForm):
    specialty = forms.CharField(max_length=100)
    license_number = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'specialty', 'license_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Custom labels
        self.fields['username'].label = "Nom d’utilisateur"
        self.fields['email'].label = "Adresse e-mail"
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmer le mot de passe"
        self.fields['specialty'].label = "Spécialité"
        self.fields['license_number'].label = "Numéro de licence"

        # Placeholders & Bootstrap classes
        placeholders = {
            'username': 'Entrez votre nom d’utilisateur',
            'email': 'exemple@mail.com',
            'password1': 'Votre mot de passe sécurisé',
            'password2': 'Répétez votre mot de passe',
            'specialty': 'Votre spécialité médicale',
            'license_number': 'Numéro d’enregistrement professionnel',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control form-control-lg rounded-3',
                'placeholder': placeholders.get(field_name, ''),
                'style': 'background-color: #f9f9f9; border: 1px solid #ddd;'
            })    

# Formulaire pour les consultations
class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['doctor', 'date', 'notes', 'duration', 'payment_amount']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Labels en français
        self.fields['doctor'].label = "Choix Docteur"
        self.fields['notes'].label = "Note"
        self.fields['duration'].label = "Durée de Consultation"
        self.fields['payment_amount'].label = "Montant Net"    
        
        self.fields['doctor'].error_messages = {
            'required' : 'La selection du docteur est obligatoire ',
            'invalid'  : 'selectionner un docteur valide '
        }  
        self.fields['notes'].error_messages = {
            'required' : 'La note est obligatoire ',
            'invalid'  : 'selectionner une note valide '
        }  
        self.fields['duration'].error_messages = {
            'required' : 'La durée est obligatoire ',
            'invalid'  : 'selectionner une durée valide '
        } 
        self.fields['payment_amount'].error_messages = {
            'required' : 'Le montant net est obligatoire ',
            'invalid'  : 'selectionner un motant valide '
        } 
        # Placeholders pour guider l'utilisateur
        placeholders = {
            'note': 'Veuillez saisir votre note',
            'duration' : 'Entrez la dure ',
            'payment_amount' : 'Net a payer',    
        }
            
        # Appliquer style Bootstrap et fond clair à tous les champs
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg rounded-3',
                    'placeholder': placeholders.get(name, ''),
                    'rows': 3,
                    'style': 'background-color: #f9f9f9; border: 1px solid #ddd;'
                })
            else:
                field.widget.attrs.update({
                    'class': 'form-control form-control-lg rounded-3',
                    'placeholder': placeholders.get(name, ''),
                    'style': 'background-color: #f9f9f9; border: 1px solid #ddd;'
                })     
        
class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',  # <-- ici !
            'placeholder': 'Votre adresse email'
        })
    )        
# # forms.py (in your app directory, e.g., myapp/forms.py)

# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import User, Patient, Doctor, Consultation

# class PatientRegistrationForm(UserCreationForm):
#     phone_number = forms.CharField(max_length=15)
#     address = forms.CharField(widget=forms.Textarea)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'address')

# class DoctorRegistrationForm(UserCreationForm):
#     specialty = forms.CharField(max_length=100)
#     license_number = forms.CharField(max_length=50)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2', 'specialty', 'license_number')

# class ConsultationForm(forms.ModelForm):
#     class Meta:
#         model = Consultation
#         fields = ['doctor', 'date', 'notes', 'duration', 'payment_amount']
#         widgets = {
#             'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }
        
        
        
        
#         #Seconde 
# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.CharField(label="Nom d'utilisateur", max_length=254)
#     password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

# class ConsultationForm(forms.ModelForm):
#     class Meta:
#         model = Consultation
#         fields = ['date', 'status', 'payment_amount', 'payment_status']        
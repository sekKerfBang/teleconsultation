from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import PatientRegistrationForm, DoctorRegistrationForm, ConsultationForm, CustomAuthenticationForm, CustomPasswordResetForm
from .models import User, Patient, Doctor, Consultation
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

User = get_user_model()

# Vue pour la page "À propos"
def about_us(request):
    return render(request, 'idea/about-us.html')

# Vue personnalisée pour la connexion
class CustomLoginView(LoginView):
    template_name = 'idea/login.html'  # Ton template basé sur base.html
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True  # Évite que l'utilisateur déjà connecté voie la page de login

    def get_success_url(self):
        """
        Redirection après connexion selon le rôle utilisateur.
        """
        user = self.request.user
        if hasattr(user, 'is_patient') and user.is_patient:
            return reverse_lazy('utilisateur:patient_dashboard')
        elif hasattr(user, 'is_doctor') and user.is_doctor:
            return reverse_lazy('utilisateur:doctor_dashboard')
        return reverse_lazy('utilisateur:home')

    def form_valid(self, form):
        """
        Gestion personnalisée après connexion.
        """
        # user = form.get_user()
        # login(self.request, user)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(self.request, username = username , password = password)
            if user is not None:
                login(self.request, user)
                messages.success(self.request, f"Bienvenue, {user.username} 👋")
                return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        """
        Gestion personnalisée en cas d'échec de connexion.
        """
        messages.error(self.request, "Nom d'utilisateur ou mot de passe incorrect ❌")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        """
        Si déjà connecté → rediriger directement.
        """
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)



# Vues pour l'inscription
def register_patient(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.save()
            print('============= verif register patient ========== ')


            # Créer le profil Patient lié à l'utilisateur
            Patient.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )

            messages.success(request, "Inscription réussie ! Veuillez vous connecter.")
            return redirect('utilisateur:login')
        else:
            messages.success(request, "Inscription non reussi, veuillez recommencez  ")
    else:
        form = PatientRegistrationForm()
    return render(request, 'idea/register_patient.html', {'form': form})


def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_doctor = True
            user.save()
            Doctor.objects.create(user=user, specialty=form.cleaned_data['specialty'], license_number=form.cleaned_data['license_number'])
            messages.success(request, "Inscription réussie ! Veuillez vous connecter.")
            return redirect('utilisateur:login')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'idea/register_doctor.html', {'form': form})

# Déconnexion
def custom_logout(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('utilisateur:login')

# Tableau de bord patient
@login_required
def patient_dashboard(request):
    if not request.user.is_patient:
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect('utilisateur:login')
    consultations = Consultation.objects.filter(patient__user=request.user)
    return render(request, 'idea/patient_dashboard.html', {'consultations': consultations})

# Tableau de bord médecin
@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor:
        messages.error(request, "Vous n'êtes pas autorisé à accéder à cette page.")
        return redirect('utilisateur:login')
    consultations = Consultation.objects.filter(doctor__user=request.user).order_by("-date")
    return render(request, 'idea/doctor_dashboard.html', {'consultations': consultations})

@login_required
def update_consultation_status(request, consultation_id, status):
    consultation = get_object_or_404(Consultation, id=consultation_id)

    # Vérification : seul le patient ou le médecin concerné peut agir
    if not (request.user == consultation.patient.user or request.user == consultation.doctor.user):
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cette consultation.")

    # Mise à jour du statut
    consultation.status = status
    consultation.save()

    # Redirection selon le rôle
    if hasattr(request.user, 'doctor'):
        return redirect('utilisateur:doctor_dashboard')
    else:
        return redirect('utilisateur:patient_dashboard')
# def update_consultation_status(request, consultation_id, new_status):
#     consultation = get_object_or_404(Consultation, id=consultation_id)

#     # Vérification que c’est bien le médecin qui modifie
#     if hasattr(request.user, "doctor") and consultation.doctor.user == request.user:
#         consultation.status = new_status
#         consultation.save()
#         messages.success(request, f"Statut mis à jour : {consultation.get_status_display()}")
#     else:
#         messages.error(request, "Action non autorisée.")

#     return redirect("utilisateur:doctor_dashboard")

# Liste des consultations
class ConsultationListView(ListView):
    model = Consultation
    template_name = 'idea/consultation_list.html'
    context_object_name = 'consultations'

    def get_queryset(self):
        if self.request.user.is_patient:
            return Consultation.objects.filter(patient__user=self.request.user)
        elif self.request.user.is_doctor:
            return Consultation.objects.filter(doctor__user=self.request.user)
        return Consultation.objects.none()

# Création d'une consultation
class ConsultationCreateView(CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'idea/consultation_form.html'
    success_url = reverse_lazy('utilisateur:patient_dashboard')

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient
        form.instance.doctor = Doctor.objects.filter(user__is_doctor=True).first()  # À ajuster selon ta logique
        messages.success(self.request, "Consultation créée avec succès !")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_patient:
            messages.error(request, "Vous devez être un patient connecté pour créer une consultation.")
            return redirect('utilisateur:login')
        return super().dispatch(request, *args, **kwargs)

# Vues personnalisées pour la réinitialisation de mot de passe
class CustomPasswordResetView(PasswordResetView):
    template_name = 'idea/password_reset.html'
    email_template_name = 'idea/password_reset_email.html'
    success_url = reverse_lazy('utilisateur:password_reset_done')
    form_class = CustomPasswordResetForm
    
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name).strip()
        # Rendu du template HTML
        html_content = render_to_string(email_template_name, context)
        text_content = strip_tags(html_content)  # Version texte brut comme fallback
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email]) # type: ignore
        msg.attach_alternative(html_content, "text/html")
        msg.send()



class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'idea/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'idea/password_reset_confirm.html'
    success_url = reverse_lazy('utilisateur:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'idea/password_reset_complete.html'

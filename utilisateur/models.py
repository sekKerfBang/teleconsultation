from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Modèle d'utilisateur personnalisé hérité de AbstractUser
class User(AbstractUser):
    is_patient = models.BooleanField(default=False)  # Indique si l'utilisateur est un patient
    is_doctor = models.BooleanField(default=False)   # Indique si l'utilisateur est un médecin

    def __str__(self):
        return self.username  # Représentation textuelle de l'utilisateur

# Modèle pour les patients, lié à User via une relation OneToOne
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # Lien unique vers User
    phone_number = models.CharField(max_length=15)  # Numéro de téléphone du patient
    address = models.TextField()  # Adresse physique du patient

    def __str__(self):
        return f"Patient: {self.user.username}"  # Représentation textuelle

# Modèle pour les médecins, lié à User via une relation OneToOne
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # Lien unique vers User
    specialty = models.CharField(max_length=100)  # Spécialité médicale (ex. cardiologue)
    license_number = models.CharField(max_length=50)  # Numéro de licence professionnelle

    def __str__(self):
        return f"Dr. {self.user.username}"  # Représentation textuelle

# Modèle pour les consultations, reliant patients et médecins
class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Référence au patient
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)    # Référence au médecin
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création
    updated_at = models.DateTimeField(auto_now=True)  # Date de mise à jour
    notes = models.TextField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'En attente'),
            ('in_progress', 'En cours'),  # <-- AJOUTER CE STATUT
            ('completed', 'Terminée'),
        ],
        default='pending'
    )
    payment_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # Montant à payer
    payment_status = models.CharField(
        max_length=20,
        choices=[('unpaid', 'Non payé'), ('paid', 'Payé')],  # Statut du paiement
        default='unpaid'
    )
    video_link = models.URLField(blank=True, null=True)  # Lien vers la vidéoconférence (ex. Jitsi)

    def __str__(self):
        return f"Consultation {self.patient} avec {self.doctor} le {self.date}"  # Représentation textuelle
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['doctor', 'date'], name='unique_doctor_date')
        ]
        
    def save(self, *args, **kwargs):
        if not self.video_link:
            unique_room_id = uuid.uuid4().hex  # Générer un ID unique
            self.video_link = f"https://meet.jit.si/{unique_room_id}"
        super().save(*args, **kwargs)    
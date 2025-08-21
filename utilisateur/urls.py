from django.urls import path
from .views import (
    CustomLoginView, register_patient, register_doctor, custom_logout,
    patient_dashboard, doctor_dashboard, ConsultationListView, ConsultationCreateView,
    CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView, about_us, update_consultation_status
)

app_name = 'utilisateur'

urlpatterns = [
    path('', CustomLoginView.as_view(), name='home'),  # Page d'accueil redirigée vers login
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/patient/', register_patient, name='register_patient'),
    path('register/doctor/', register_doctor, name='register_doctor'),
    path('logout/', custom_logout, name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('patient/dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path("consultations/<int:consultation_id>/status/<str:new_status>/", update_consultation_status, name="update_consultation_status"),
    path('consultations/', ConsultationListView.as_view(), name='consultation_list'),
    path('consultations/create/', ConsultationCreateView.as_view(), name='consultation_create'),
    path('about-us/', about_us, name='about_us'),
]
# from django.urls import path
# from .views import (about_us, CustomLoginView, register_patient, register_doctor, custom_logout,
#     CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
#     patient_dashboard, doctor_dashboard, ConsultationListView, ConsultationCreateView)



# app_name = 'utilisateur'

# urlpatterns = [
#     path('', CustomLoginView.as_view(), name='home'),  # Page d'accueil redirigée vers login
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('register/patient/', register_patient, name='register_patient'),
#     path('register/doctor/', register_doctor, name='register_doctor'),
#     path('logout/', custom_logout, name='logout'),
#     path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
#     path('patient/dashboard/', patient_dashboard, name='patient_dashboard'),
#     path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
#     path('consultations/', ConsultationListView.as_view(), name='consultation_list'),
#     path('consultations/create/', ConsultationCreateView.as_view(), name='consultation_create'),
#     # path('about-us/', lambda request: render(request, 'about_us.html'), name='about_us'),  #
#     path('about-us/', about_us, name='about_us'),
    
#     # ## Juste une simulation des Urls  
#     # path('login/', CustomLoginView.as_view(), name='login'),
#     # path('register/patient/', register_patient, name='register_patient'),
#     # path('register/doctor/', register_doctor, name='register_doctor'),
#     # path('logout/', custom_logout, name='logout'),
#     # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
#     # path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
#     # path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     # path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
#     # path('patient/dashboard/', patient_dashboard, name='patient_dashboard'),
#     # path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
#     # path('consultations/', ConsultationListView.as_view(), name='consultation_list'),
#     # path('consultations/create/', ConsultationCreateView.as_view(), name='consultation_create'),
    
# ]

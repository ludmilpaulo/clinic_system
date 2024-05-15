from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from .models import DoctorProfile, PatientProfile, Document, ConsultationCategory

from rest_framework import generics, permissions

from .serializers import DoctorProfileSerializer

class DoctorProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        doctor_id = self.kwargs['doctor_id']
        return DoctorProfile.objects.get(pk=doctor_id)


@api_view(['POST'])
def custom_signup(request, format=None):
    print("Received data:", request.data)
    if request.method == 'POST':
        try:
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")
            user_type = request.data.get("user_type")

            name = request.data.get("name")
            surname = request.data.get("surname")
            phone_number = request.data.get("phone_number")
            id_number_or_passport = request.data.get("id_number_or_passport")
            gender = request.data.get("gender")
            date_of_birth = request.data.get("date_of_birth")
            address = request.data.get("address")

            print("Validating inputs...")
            if not username or not email or not password or not user_type:
                print("Validation error: Missing fields")
                return JsonResponse({"error": "All fields are required"}, status=400)

            if not name or not surname or not phone_number or not id_number_or_passport or not gender or not date_of_birth or not address:
                print("Validation error: Missing profile fields")
                return JsonResponse({"error": "All profile fields are required"}, status=400)

            print("Checking for existing username and email...")
            if User.objects.filter(username=username).exists():
                print("Validation error: Username exists")
                return JsonResponse({"error": "Username already exists"}, status=400)
            if User.objects.filter(email=email).exists():
                print("Validation error: Email registered")
                return JsonResponse({"error": "Email already registered"}, status=400)

            print("Creating user...")
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            if user_type == 'doctor':
                specialty = request.data.get("specialty")
                years_of_experience = request.data.get("years_of_experience")


                if not specialty or not years_of_experience:
                    print("Validation error: Missing doctor fields")
                    return JsonResponse({"error": "All doctor fields are required"}, status=400)


                print("Creating doctor profile...")
                doctor_profile = DoctorProfile.objects.create(
                    user=user,
                    name=name,
                    surname=surname,
                    phone_number=phone_number,
                    id_number_or_passport=id_number_or_passport,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    address=address,
                    specialty=specialty,
                    years_of_experience=years_of_experience

                )

                print("Handling document uploads...")
                documents = request.FILES.getlist('documents')
                for document in documents:
                    Document.objects.create(user=user, document=document)

                print("Sending welcome email to doctor...")
                send_mail(
                    subject='Welcome to the Clinic Platform',
                    message=(
                        'Dear Doctor, welcome to our platform. Your account will be activated in 78 hours pending background checks. '
                        'If you have any other supporting documents, please respond to this email with the attached documents.'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )

            else:
                print("Creating patient profile...")
                PatientProfile.objects.create(
                    user=user,
                    name=name,
                    surname=surname,
                    phone_number=phone_number,
                    id_number_or_passport=id_number_or_passport,
                    gender=gender,
                    date_of_birth=date_of_birth,
                    address=address
                )

                print("Sending welcome email to patient...")
                send_mail(
                    subject='Welcome to the Clinic Platform',
                    message='Dear Patient, welcome to our platform.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )

            print("Creating token...")
            token, _ = Token.objects.get_or_create(user=user)

            print("Signup successful")
            return JsonResponse({
                "message": "Signup successful",
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "status": 201
            }, status=201)

        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)




@api_view(['POST'])
def custom_login(request, format=None):
    print("Received data:", request.data)
    if request.method == 'POST':
    
        try:
            username_or_email = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(request, username=username_or_email, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                login(request, user)
                return JsonResponse({"message": "Login successful",
                                     'token':token.key,
                                        'user_id':user.pk,
                                        'username':user.username,
                                     }, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)




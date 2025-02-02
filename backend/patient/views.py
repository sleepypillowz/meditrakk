from supabase import create_client
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientSerializer, PatientRegistrationSerializer


from django.views.decorators.csrf import csrf_exempt
import json
from queueing.models import Patient, TemporaryStorageQueue
from datetime import datetime

# Supabase credentials
url = 'https://wczowfydbgmwbotbxaxa.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indjem93ZnlkYmdtd2JvdGJ4YXhhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUxNzU1MjUsImV4cCI6MjA1MDc1MTUyNX0.5JxhYLqY3q6y2ti9Cn3R6-UBJFisPDOvUYxYQ_DgGSE'  # Make sure you use the correct key
supabase = create_client(url, key)

class PatientListView(APIView):
    def get(self, request):
        try:
            response = supabase.table("patient_patient").select(
                "*",
                "queueing_temporarystoragequeue(id, priority_level, status, created_at)"
            ).execute()
            
            print(response)  # Debugging: Print full response
            if hasattr(response, 'error') and response.error:
                return Response({"error": response.error.message}, status=status.HTTP_400_BAD_REQUEST)

            patients = response.data if hasattr(response, 'data') else response
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PatientRegister(APIView):
    def post(self, request):
        # Deserialize the data with the PatientRegistrationSerializer
        patient = PatientRegistrationSerializer(data=request.data)
        
        if patient.is_valid():
            validated_data = patient.validated_data

            # Convert date_of_birth to string (YYYY-MM-DD) if it's not None
            if validated_data.get("date_of_birth"):
                validated_data["date_of_birth"] = validated_data["date_of_birth"].strftime("%Y-%m-%d")

            try:
                # Insert data into Patient table using Django ORM
                patient = Patient.objects.create(
                    first_name=validated_data.get('first_name', ''),
                    middle_name=validated_data.get('middle_name', ''),
                    last_name=validated_data['last_name'],
                    email=validated_data['email'],
                    phone_number=validated_data['phone_number'],
                    date_of_birth=datetime.strptime(validated_data['date_of_birth'], '%Y-%m-%d').date(),
                    complaint=validated_data.get('complaint'),
                    street_address=validated_data.get('street_address', ''),
                    barangay=validated_data.get('barangay', ''),
                    municipal_city=validated_data.get('municipal_city', '')
                )

                # After inserting, you can also create the TemporaryStorageQueue entry
                priority_level = validated_data.get('priority', 'Regular')                
                TemporaryStorageQueue.objects.create(
                    patient=patient,
                    priority_level=priority_level,
                    status='Waiting'
                )
                
                # Respond with success if everything went well
                patient_serializer = PatientRegistrationSerializer(patient)
                return Response(patient_serializer.data, status=status.HTTP_201_CREATED)


            except Exception as e:
                # Handle unexpected errors during insertion
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        # If serializer is not valid
        return Response({"errors": patient.errors}, status=status.HTTP_400_BAD_REQUEST)

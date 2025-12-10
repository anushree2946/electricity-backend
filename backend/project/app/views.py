from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Applicant, Connection, Status

from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from datetime import datetime
import json
import pandas as pd


# ---------------------------------------
# HEALTH CHECK
# ---------------------------------------
def health_check(request):
    return JsonResponse({"status": "backend_running"})


# ---------------------------------------
# SIGNUP
# ---------------------------------------
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "Account created successfully!"}, status=201)

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ---------------------------------------
# LOGIN
# ---------------------------------------
@csrf_exempt
def session_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = authenticate(username=data.get("username"), password=data.get("password"))

        if user:
            login(request, user)
            return JsonResponse({"message": "Login successful", "user": user.username})

        return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ---------------------------------------
# LOGOUT
# ---------------------------------------
@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})


# ---------------------------------------
# UPLOAD CSV
# ---------------------------------------
def uploaddata(request):
    try:
        filepath = "electricity_board_case_study.csv"
        df = pd.read_csv(filepath, encoding="latin-1")

        for _, row in df.iterrows():
            applicant, _ = Applicant.objects.get_or_create(
                Applicant_Name=row["Applicant_Name"],
                Gender=row["Gender"],
                District=row["District"],
                State=row["State"],
                Pincode=row["Pincode"],
                Ownership=row["Ownership"],
                GovtID_Type=row["GovtID_Type"],
                ID_Number=row["ID_Number"],
                Category=row["Category"],
            )

            status_obj, _ = Status.objects.get_or_create(Status_Name=row["Status"])

            Connection.objects.get_or_create(
                Applicant=applicant,
                Load_Applied=row["Load_Applied"],
                Date_of_Application=datetime.strptime(row["Date_of_Application"], "%d-%m-%Y"),
                Status=status_obj,
                Reviewer_ID=row["Reviewer_ID"],
                Reviewer_Name=row["Reviewer_Name"],
                Reviewer_Comments=row["Reviewer_Comments"],
            )

        return HttpResponse("CSV uploaded successfully!")

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


# ---------------------------------------
# FETCH / FILTER TABLE DATA
# ---------------------------------------
def get_connections(request):

    search = request.GET.get("search", "").strip()
    start_date = parse_date(request.GET.get("start_date") or "")
    end_date = parse_date(request.GET.get("end_date") or "")

    queryset = Connection.objects.select_related("Applicant", "Status").all()

    if search:
        queryset = queryset.filter(id__icontains=search)

    if start_date and end_date:
        queryset = queryset.filter(Date_of_Application__range=[start_date, end_date])

    paginator = Paginator(queryset, 50)
    page = request.GET.get("page", 1)
    connections = paginator.get_page(page)

    data = [
        {
            "id": c.id,
            "Load_Applied": c.Load_Applied,
            "Date_of_Application": c.Date_of_Application.strftime("%Y-%m-%d"),
            "Status": c.Status.Status_Name,
            "Reviewer_ID": c.Reviewer_ID,
            "Reviewer_Name": c.Reviewer_Name,
            "Reviewer_Comments": c.Reviewer_Comments,

            "Applicant": {
                "Applicant_Name": c.Applicant.Applicant_Name,
                "Gender": c.Applicant.Gender,
                "District": c.Applicant.District,
                "State": c.Applicant.State,
                "Pincode": c.Applicant.Pincode,
                "Ownership": c.Applicant.Ownership,
                "GovtID_Type": c.Applicant.GovtID_Type,
                "ID_Number": c.Applicant.ID_Number,
                "Category": c.Applicant.Category,
            }
        }
        for c in connections
    ]

    return JsonResponse({
        "data": data,
        "total_pages": paginator.num_pages,
        "current_page": connections.number,
    })


# ---------------------------------------
# UPDATE RECORD
# ---------------------------------------
@csrf_exempt
def update_applicant(request, id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            connection = Connection.objects.get(id=id)
            applicant = connection.Applicant

            applicant.Applicant_Name = data["applicant"]["name"]
            applicant.save()

            return JsonResponse({"message": "Updated successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)

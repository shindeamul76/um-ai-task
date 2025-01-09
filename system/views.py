from django.shortcuts import render

# Create your views here.


from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        connection.ensure_connection()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    app_status = "healthy"

    return JsonResponse({
        "status": "ok" if db_status == "healthy" and app_status == "healthy" else "error",
        "database": db_status,
        "application": app_status
    })
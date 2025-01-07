from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import math
import json

# Home view
def home(request):
    return render(request, 'map_app/home.html')

# View to handle buffer creation
def create_buffer(request):
    if request.method == "GET":
        # Extract coordinates and radius from GET parameters
        lat = float(request.GET.get('lat', 0))
        lng = float(request.GET.get('lng', 0))
        radius = float(request.GET.get('radius', 0))

        # Example logic for returning buffer data
        buffer_data = {
            'center': {'lat': lat, 'lng': lng},
            'radius': radius,  # In meters
        }

        return JsonResponse(buffer_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

# Proximity query for nearby points of interest (POIs)
@csrf_exempt
def proximity_query(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lat = data.get('lat')
        lng = data.get('lng')
        radius = data.get('radius')  # Radius in meters

        # Perform proximity query using PostGIS
        with connection.cursor() as cursor:
            query = """
                SELECT name, ST_AsGeoJSON(geom) AS geom
                FROM pois
                WHERE ST_DWithin(
                    ST_SetSRID(ST_Point(%s, %s), 4326)::geography,
                    geom::geography,
                    %s
                );
            """
            cursor.execute(query, [lng, lat, radius])
            results = cursor.fetchall()

             # Format results for the response
        attractions = [{"name": row[0], "geom": json.loads(row[1])} for row in results]
        return JsonResponse({"attractions": attractions})

    return JsonResponse({"error": "Invalid request method"}, status=400)
def documentation(request):
    return render(request, 'map_app/documentation.html')
def about(request):
    return render(request, 'map_app/about.html')

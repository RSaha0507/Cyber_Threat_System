from ip2geotools.databases.noncommercial import DbIpCity

def get_geo_location(ip):
    try:
        response = DbIpCity.get(ip, api_key="free")
        return {
            "ip": ip,
            "city": response.city,
            "country": response.country,
            "lat": response.latitude,
            "lon": response.longitude
        }
    except:
        return None

import jwt

from app.core.config.settings import get_settings


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjciLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lIjoic3RyaW5nIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoidXNlckBleGFtcGxlLmNvbSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IlVzZXIiLCJleHAiOjE3ODgxODc5MjYsImlzcyI6IkVtcGxveWVlX1Byb2oiLCJhdWQiOiJFbXBsb3llZUFQSVVzZXJzIn0.tyMVW2i_8xyyo1UqTf80lpfLkVp5YIIhhw_syoTIsD4"


settings = get_settings()

try:
    payload = jwt.decode(
        TOKEN,
        settings.jwt_secret_key,
        algorithms=["HS256"],
        issuer=settings.jwt_issuer,
        audience=settings.jwt_audience,
    )

    print("\nJWT authentication successful!")
    print("--------------------------------")
    print("User ID :", payload.get(
        "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"
    ))
    print("Username:", payload.get(
        "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"
    ))
    print("Email   :", payload.get(
        "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
    ))
    print("Role    :", payload.get(
        "http://schemas.microsoft.com/ws/2008/06/identity/claims/role"
    ))

except jwt.ExpiredSignatureError:
    print("Token has expired")

except jwt.InvalidTokenError as ex:
    print("Invalid token:", ex)
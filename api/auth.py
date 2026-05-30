import base64

# Credentials for Basic Authentication 
VALID_USERS = {
    "admin": "momo2026",
}

def check_basic_auth(handler):
    """
    Reads the Authorization header, decodes Base64 credentials,
    and checks them against VALID_USERS.
    Returns True if valid, False otherwise.
    """
    auth_header = handler.headers.get("Authorization", "")

    if not auth_header.startswith("Basic "):
        return False

    try:
        encoded = auth_header[6:]  # strip "Basic "
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)
        return VALID_USERS.get(username) == password
    except Exception:
        return False


def require_auth(handler):
    """
    Call at the top of every do_GET/POST/PUT/DELETE method.
    Sends a 401 response and returns False if not authenticated.
    Returns True if the request may proceed.
    """
    if not check_basic_auth(handler):
        handler.send_response(401)
        handler.send_header("WWW-Authenticate", 'Basic realm="MoMo API"')
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(b'{"error": "Unauthorized: invalid or missing credentials"}')
        return False
    return True
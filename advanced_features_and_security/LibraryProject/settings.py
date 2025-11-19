# SECURITY: Turn off debug in production
DEBUG = False

# Browser security protections
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# Ensure cookies are sent over HTTPS only
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

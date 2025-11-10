"""
Task 2 Step 4: Implement Content Security Policy (CSP)
Set up a Content Security Policy header to reduce the risk of XSS attacks
by specifying which domains can be used to load content in your application.
"""


class CSPMiddleware:
    """
    Custom middleware to set Content Security Policy headers.
    This reduces the risk of XSS attacks by specifying which domains
    can be used to load content in the application.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Task 2 Step 4: Set Content Security Policy header
        # This policy allows:
        # - 'self' - same origin
        # - 'unsafe-inline' for styles (can be restricted further in production)
        # - 'unsafe-inline' for scripts (should be restricted in production)
        # For production, consider using nonces or hashes instead of 'unsafe-inline'
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        response['Content-Security-Policy'] = csp_policy
        
        return response


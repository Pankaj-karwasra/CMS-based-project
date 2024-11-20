# app/middleware.py

'''class AdminUserSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for the custom admin path
        if request.path.startswith('/custom_admin/'):
            request.session.set_expiry(0)  # Admin sessions expire when the browser is closed
        else:
            request.session.set_expiry(None)  # Other users have a normal session expiration
        response = self.get_response(request)
        return response'''

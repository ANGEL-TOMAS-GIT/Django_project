# Create middleware.py in warehouse folder
# warehouse/middleware.py
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class ForceDefaultLanguageMiddleware(MiddlewareMixin):
    """
    Force default language based on user preference or header
    """
    def process_request(self, request):
        # Check for language in session or cookie
        lang = request.GET.get('lang')
        if lang and lang in ['en', 'es']:
            translation.activate(lang)
            request.session[translation.LANGUAGE_SESSION_KEY] = lang
        elif translation.LANGUAGE_SESSION_KEY in request.session:
            translation.activate(request.session[translation.LANGUAGE_SESSION_KEY])
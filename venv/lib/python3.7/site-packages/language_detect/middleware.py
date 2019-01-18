# -*- coding: utf-8 -*-

from django_six import MiddlewareMixin

class BrowserLanguageDetectionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        lng = request.META.get('LANGUAGE', request.META.get('LANG'))
        if lng:
            request.browser_language = lng
        else:
            request.browser_language = None
        
        return None

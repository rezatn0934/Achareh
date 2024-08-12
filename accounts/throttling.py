from rest_framework.throttling import SimpleRateThrottle


class PhoneRateThrottle(SimpleRateThrottle):
    scope = 'phone'

    def get_cache_key(self, request, view):
        """
        Return a cache key for the request, based on the phone number.
        """
        phone = request.data.get('phone')
        if not phone:            
            phone = request.data.get('usernamephone')
            if not phone:
                return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': phone
        }

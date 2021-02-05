from ipware import get_client_ip as get_ip


def get_client_ip(request):
    '''x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip'''
    client_ip, is_routable = get_ip(request)
    if client_ip is None:
        return None
    else:
        print(client_ip)
        return client_ip
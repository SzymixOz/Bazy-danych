def navigation_items(request):
    items = [
        {'url': '/reservationSystem', 'label': 'Home'},
        {'url': '/reservationSystem/about', 'label': 'About'},
    ]
    return {'navigation_items': items}

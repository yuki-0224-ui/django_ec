def default_context(request):
    return {
        'DEFAULT_PRODUCT_IMAGE': {
            'src': 'https://dummyimage.com/600x700/dee2e6/6c757d.jpg',
            'alt': '商品画像なし'
        },
        'DEFAULT_PRODUCT_THUMBNAIL': {
            'src': 'https://dummyimage.com/450x300/dee2e6/6c757d.jpg',
            'alt': '商品画像なし'
        },
    }

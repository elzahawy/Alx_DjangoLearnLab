# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'blog/static']

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'blog/templates'],
        'APP_DIRS': True,
        ...
    },
]

# HTTPS Deployment Configuration Guide

This document provides instructions for configuring HTTPS and secure redirects in a production Django deployment.

## Task 3: HTTPS and Secure Redirects Implementation

### Django Settings Configuration

All HTTPS-related settings are configured in `settings.py`:

```python
# HTTPS Redirect
SECURE_SSL_REDIRECT = True

# HSTS Settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security Headers
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
```

## Web Server Configuration

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Certificate Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Proxy to Django
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /path/to/your/staticfiles/;
    }

    # Media files
    location /media/ {
        alias /path/to/your/media/;
    }
}
```

### Apache Configuration Example

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key

    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"

    # Proxy to Django
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    ProxyPreserveHost On

    # Static files
    Alias /static /path/to/your/staticfiles
    <Directory /path/to/your/staticfiles>
        Require all granted
    </Directory>

    # Media files
    Alias /media /path/to/your/media
    <Directory /path/to/your/media>
        Require all granted
    </Directory>
</VirtualHost>
```

## SSL/TLS Certificate Setup

### Using Let's Encrypt (Free SSL)

1. **Install Certbot**:
   ```bash
   sudo apt-get update
   sudo apt-get install certbot python3-certbot-nginx  # For Nginx
   # OR
   sudo apt-get install certbot python3-certbot-apache  # For Apache
   ```

2. **Obtain Certificate**:
   ```bash
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   # OR
   sudo certbot --apache -d yourdomain.com -d www.yourdomain.com
   ```

3. **Auto-renewal**:
   Certbot automatically sets up renewal. Test with:
   ```bash
   sudo certbot renew --dry-run
   ```

### Using Commercial SSL Certificate

1. Purchase SSL certificate from a Certificate Authority (CA)
2. Generate Certificate Signing Request (CSR)
3. Submit CSR to CA and receive certificate files
4. Configure web server with certificate files

## Django Settings for Reverse Proxy

If using a reverse proxy (Nginx/Apache), you may need to configure:

```python
# In settings.py
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

This tells Django to trust the `X-Forwarded-Proto` header from the proxy.

## Testing HTTPS Configuration

### 1. Test SSL Redirect
- Visit `http://yourdomain.com` - should redirect to `https://yourdomain.com`

### 2. Test HSTS
- Check browser developer tools → Network → Headers
- Look for `Strict-Transport-Security` header

### 3. Test Secure Cookies
- Check browser developer tools → Application → Cookies
- Verify cookies have `Secure` flag set

### 4. Test Security Headers
Use online tools:
- [Security Headers](https://securityheaders.com/)
- [SSL Labs](https://www.ssllabs.com/ssltest/)

## Development vs Production

### Development (No HTTPS)
Set in `settings.py`:
```python
DEBUG = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

### Production (With HTTPS)
Set in `settings.py`:
```python
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Security Review Checklist

- [ ] SSL/TLS certificate installed and valid
- [ ] HTTP to HTTPS redirect working
- [ ] HSTS header present and configured
- [ ] Secure cookie flags enabled
- [ ] Security headers configured
- [ ] All forms use CSRF tokens
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured
- [ ] Secret key stored in environment variable
- [ ] Database credentials secured
- [ ] Static files served securely
- [ ] Media files access controlled

## Troubleshooting

### Issue: Too Many Redirects
**Solution**: Check if `SECURE_SSL_REDIRECT` is set while behind a proxy. Configure `SECURE_PROXY_SSL_HEADER`.

### Issue: Cookies Not Working
**Solution**: In development, set `SESSION_COOKIE_SECURE = False` and `CSRF_COOKIE_SECURE = False`.

### Issue: Mixed Content Warnings
**Solution**: Ensure all resources (CSS, JS, images) are loaded via HTTPS.

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [OWASP Security Headers](https://owasp.org/www-project-secure-headers/)


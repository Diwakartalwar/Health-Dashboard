from django.core.management.base import BaseCommand
from django.test import Client
from django.urls import get_resolver, URLPattern, URLResolver
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Scan and report broken links in the project'

    def get_all_urls(self, urlpatterns, prefix=''):
        """Recursively extract all URL patterns"""
        urls = []
        
        for pattern in urlpatterns:
            if isinstance(pattern, URLResolver):
                new_prefix = prefix + str(pattern.pattern)
                urls.extend(self.get_all_urls(pattern.url_patterns, new_prefix))
            elif isinstance(pattern, URLPattern):
                url = prefix + str(pattern.pattern)
                urls.append(url)
        
        return urls

    def handle(self, *args, **options):
        client = Client()
        resolver = get_resolver()
        urls = self.get_all_urls(resolver.url_patterns)
        
        # Filter testable URLs
        test_urls = []
        for url in urls:
            url_str = str(url)
            if '^' not in url_str and '(?P' not in url_str and '<' not in url_str:
                if not url_str.startswith('media/') and not url_str.startswith('static/'):
                    test_urls.append(url_str)
        
        self.stdout.write(self.style.SUCCESS(f"\n{'='*70}"))
        self.stdout.write(self.style.SUCCESS(f"Scanning {len(test_urls)} URLs"))
        self.stdout.write(self.style.SUCCESS(f"{'='*70}\n"))
        
        broken = []
        working = []
        
        # Create test user
        try:
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(username='testuser', password='testpass123')
            client.force_login(user)
            self.stdout.write(self.style.SUCCESS(f"✓ Logged in as: {user.username}\n"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠ Could not create test user: {e}\n"))
        
        for url in sorted(set(test_urls)):
            try:
                response = client.get(f'/{url}', follow=True)
                
                if response.status_code == 404:
                    broken.append((url, "404 Not Found"))
                    self.stdout.write(self.style.ERROR(f"✗ /{url} (404)"))
                elif response.status_code == 500:
                    broken.append((url, "500 Server Error"))
                    self.stdout.write(self.style.ERROR(f"✗ /{url} (500)"))
                elif 300 <= response.status_code < 400:
                    working.append(url)
                    self.stdout.write(self.style.WARNING(f"→ /{url} ({response.status_code})"))
                else:
                    working.append(url)
                    self.stdout.write(self.style.SUCCESS(f"✓ /{url} ({response.status_code})"))
                    
            except Exception as e:
                broken.append((url, str(e)))
                self.stdout.write(self.style.ERROR(f"✗ /{url} ({str(e)[:50]})"))
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n{'='*70}"))
        self.stdout.write(self.style.SUCCESS(f"SUMMARY"))
        self.stdout.write(self.style.SUCCESS(f"{'='*70}"))
        self.stdout.write(f"✓ Working: {len(working)}")
        self.stdout.write(f"✗ Broken:  {len(broken)}")
        self.stdout.write(f"Total:     {len(working) + len(broken)}\n")
        
        if broken:
            self.stdout.write(self.style.ERROR("BROKEN LINKS:"))
            self.stdout.write(self.style.ERROR("-" * 70))
            for url, reason in broken:
                self.stdout.write(f"  /{url}")
                self.stdout.write(f"    → {reason}\n")

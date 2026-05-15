from django.db import models

class Course(models.Model):
    CATEGORY_CHOICES = [
        ('Integration', 'Integrationskurse'),
        ('Beruf', 'Berufssprachkurse'),
        ('Spezial', 'Spezialkurse (z.B. telc C1, Akademische Heilberufe)'),
        ('Orientierung', 'Erstorientierungskurse (EOK)'),
        ('Nachhilfe', 'Schülerförderung / Nachhilfe'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Kurstitel")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Integration', verbose_name="Kategorie")
    description = models.TextField(verbose_name="Beschreibung")
    duration = models.CharField(max_length=100, verbose_name="Dauer / Startdatum")
    price = models.CharField(max_length=100, verbose_name="Kosten / Förderung")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Vor- und Nachname")
    email = models.EmailField(verbose_name="E-Mail")
    phone = models.CharField(max_length=20, verbose_name="Telefonnummer", blank=True, null=True)
    message = models.TextField(verbose_name="Nachricht")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")

    def __str__(self):
        return f"Nachricht von {self.name} - {self.created_at.strftime('%Y-%m-%d')}"

class Registration(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Ausstehend'),
        ('Confirmed', 'Bestätigt'),
        ('Waitlisted', 'Warteliste'),
        ('Cancelled', 'Storniert'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='registrations', verbose_name="Kurs")
    first_name = models.CharField(max_length=100, verbose_name="Vorname")
    last_name = models.CharField(max_length=100, verbose_name="Nachname")
    email = models.EmailField(verbose_name="E-Mail")
    phone = models.CharField(max_length=20, verbose_name="Telefonnummer", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Registriert am")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.course.title} ({self.get_status_display()})"

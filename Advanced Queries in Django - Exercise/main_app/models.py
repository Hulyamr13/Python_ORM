from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.db.models import Count, Q


class RealEstateListingManager(models.Manager):
    def by_property_type(self, property_type):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price, max_price):
        return self.filter(price__gte=min_price, price__lte=max_price)

    def with_bedrooms(self, bedrooms_count):
        return self.filter(bedrooms=bedrooms_count)

    def popular_locations(self):
        return (
            self.values('location')
            .annotate(location_count=Count('location'))
            .order_by('location_count', 'location')[:2]
        )


class RealEstateListing(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('House', 'House'),
        ('Flat', 'Flat'),
        ('Villa', 'Villa'),
        ('Cottage', 'Cottage'),
        ('Studio', 'Studio'),
    ]

    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    location = models.CharField(max_length=100)

    objects = RealEstateListingManager()

    def __str__(self):
        return f"{self.get_property_type_display()} in {self.location}"


class VideoGameManager(models.Manager):
    def games_by_genre(self, genre):
        return self.filter(genre=genre)

    def recently_released_games(self, year):
        return self.filter(release_year__range=(year, 2023))

    def highest_rated_game(self):
        highest_rated = self.all().order_by('-rating').first()
        return highest_rated

    def lowest_rated_game(self):
        lowest_rated = self.all().order_by('rating').first()
        return lowest_rated

    def average_rating(self):
        from django.db.models import Avg
        avg_rating = self.aggregate(Avg('rating'))['rating__avg']
        if avg_rating is not None:
            return round(avg_rating, 1)
        else:
            return 0.0


class VideoGame(models.Model):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('RPG', 'RPG'),
        ('Adventure', 'Adventure'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
    ]

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES)
    release_year = models.PositiveIntegerField(validators=[MinValueValidator(1990), MaxValueValidator(2023)])
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    objects = VideoGameManager()

    def clean(self):
        if self.rating < 0.0 or self.rating > 10.0:
            raise ValidationError("The rating must be between 0.0 and 10.0")

        if self.release_year < 1990 or self.release_year > 2023:
            raise ValidationError("The release year must be between 1990 and 2023")

    def __str__(self):
        return self.title


class BillingInfo(models.Model):
    address = models.CharField(max_length=255)


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50)
    billing_info = models.ForeignKey(BillingInfo, on_delete=models.CASCADE)

    @classmethod
    def get_invoices_with_prefix(cls, prefix):
        return cls.objects.filter(invoice_number__startswith=prefix)

    @classmethod
    def get_invoices_sorted_by_number(cls):
        return cls.objects.all().order_by('invoice_number')

    @classmethod
    def get_invoice_with_billing_info(cls, invoice_number):
        return cls.objects.select_related('billing_info').get(invoice_number=invoice_number)


class Technology(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    technologies_used = models.ManyToManyField(Technology)

    def get_programmers_with_technologies(self):
        return Programmer.objects.prefetch_related('projects__technologies_used').filter(projects=self)


class Programmer(models.Model):
    name = models.CharField(max_length=100)
    projects = models.ManyToManyField(Project)

    def get_projects_with_technologies(self):
        return Project.objects.prefetch_related('technologies_used').filter(programmer=self)


class TaskManager(models.Manager):
    def overdue_high_priority_tasks(self):
        return self.filter(priority='High', is_completed=False, completion_date__gt=models.F('creation_date'))

    def completed_mid_priority_tasks(self):
        return self.filter(priority='Medium', is_completed=True)

    def search_tasks(self, query):
        from django.db.models import Q
        return self.filter(Q(title__icontains=query) | Q(description__icontains=query))

    def recent_completed_tasks(self, days):
        cutoff_date = date.today() - timedelta(days=days)
        return self.filter(is_completed=True, completion_date__gte=cutoff_date)


class Task(models.Model):
    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    is_completed = models.BooleanField(default=False)
    creation_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)

    objects = TaskManager()


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    difficulty_level = models.IntegerField()
    duration_minutes = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()

    @classmethod
    def get_long_and_hard_exercises(cls):
        return cls.objects.filter(duration_minutes__gt=30, difficulty_level__gte=10)

    @classmethod
    def get_short_and_easy_exercises(cls):
        return cls.objects.filter(duration_minutes__lt=15, difficulty_level__lt=5)

    @classmethod
    def get_exercises_within_duration(cls, min_duration, max_duration):
        return cls.objects.filter(duration_minutes__gte=min_duration, duration_minutes__lte=max_duration)

    @classmethod
    def get_exercises_with_difficulty_and_repetitions(cls, min_difficulty, min_repetitions):
        return cls.objects.filter(difficulty_level__gte=min_difficulty, repetitions__gte=min_repetitions)
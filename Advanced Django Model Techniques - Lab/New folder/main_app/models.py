from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MaxValueValidator, MinValueValidator


def validate_menu_categories(value):
    if "Appetizers" not in value or "Main Course" not in value or "Desserts" not in value:
        raise ValidationError('The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')


class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(limit_value=2, message="Name must be at least 2 characters long."),
            MaxLengthValidator(limit_value=100, message="Name cannot exceed 100 characters.")
        ]
    )
    location = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(limit_value=2, message="Location must be at least 2 characters long."),
            MaxLengthValidator(limit_value=200, message="Location cannot exceed 200 characters.")
        ]
    )
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(limit_value=0, message="Rating must be at least 0.00."),
            MaxValueValidator(limit_value=5, message="Rating cannot exceed 5.00.")
        ]
    )


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(validators=[validate_menu_categories])
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        related_name='menus'
    )


class ReviewMixin(models.Model):
    reviewer_name = models.CharField(max_length=100)
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=5)])

    class Meta:
        abstract = True  # Make the mixin class abstract so that it cannot be instantiated on its own.
        ordering = ['-rating']

    def __str__(self):
        return f"{self.reviewer_name} - {self.rating}"


class RestaurantReview(ReviewMixin, models.Model):
    reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    review_content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(limit_value=5)]
    )

    class Meta:
        ordering = ['-rating']
        verbose_name = "Restaurant Review"
        verbose_name_plural = "Restaurant Reviews"
        unique_together = ('reviewer_name', 'restaurant')


class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(max_length=100)

    class Meta:
        ordering = ['-rating']
        verbose_name = "Food Critic Review"
        verbose_name_plural = "Food Critics Reviews"


class MenuReview(models.Model):
    reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(
        'Menu',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(limit_value=5)])

    class Meta:
        ordering = ['-rating']
        verbose_name = "Menu Review"
        verbose_name_plural = "Menu Reviews"
        unique_together = ('reviewer_name', 'menu')
        indexes = [
            models.Index(fields=['menu'], name='main_app_menu_review_menu_id')
        ]

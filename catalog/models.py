from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    # Category model
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('catalog:cakes_category', args=[self.slug])

    class Meta:
        ordering = ('category_name',)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name


class Cake(models.Model):
    # Cake model
    category = models.ForeignKey(Category, related_name="cakes", on_delete=models.CASCADE)
    cake_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()
    size = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cakes/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    composition = models.TextField(null=True, blank=True, default="Will be added soon")
    poster_img = models.ImageField(upload_to='cakes_selected/', null=True)
    selected = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('catalog:single_cake', args=[self.slug])

    def get_average_rating(self):
        average_score = 0.0
        if self.cake_to_review.count() > 0:
            total_score = sum([review.rating for review in self.cake_to_review.all()])
            average_score = total_score / self.cake_to_review.count()

        return round(average_score, 1)

    class Meta:
        ordering = ('cake_name',)
        verbose_name_plural = "cakes"

    def __str__(self):
        return self.cake_name


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='reviews', blank=True, null=True)
    cake = models.ForeignKey(Cake, related_name="cake_to_review", verbose_name="cake_review", on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    author = models.CharField(max_length=50)
    review = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ('-created',)


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=50)
    subject = models.TextField(max_length=1000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

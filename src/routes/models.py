from datetime import time
import re
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from mySite import settings
from django.db.models import Avg, Count
import requests

ROUTE_RATE_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

COMMENT_RATE_CHOICES = [
        (-1, '-1'),
        (1, '1'),
    ]

class CustomValidator():
    def validate_route_url(value):
        if re.search('^(https://)?maps.openrouteservice.org/#/.*$', value) == None:
            raise ValidationError('Podany adres url jest nieprawidłowy.')
        if re.search('^(https://)?maps.openrouteservice.org/#/directions/'
            + '([^/]+/){2}(^/]+/)*data/([0-9]+,)*[0-9]+$', value) == None:
            raise ValidationError('Podana trasa jest nieprawidłowa.')
        if re.search('null', value) != None:
            raise ValidationError('Trasa nie może zawierać pustego punktu.')
        if re.search('Your%20location', value) != None:
            raise ValidationError('Trasa nie może zawierać jako punktu aktualnej lokalizacji.')

class Route(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Użytkownik:')
    url = models.TextField(verbose_name='Adres url trasy:', null=False, blank=False, validators=[CustomValidator.validate_route_url])
    name = models.CharField(verbose_name='Nazwa trasy:', null=False, blank=False, max_length=100)
    description = models.TextField(verbose_name='Opis trasy:', null=True, blank=True)
    is_published = models.BooleanField(verbose_name='Opublikować?', null=False, blank=False, default=False)
    is_deleted = models.BooleanField(verbose_name='Usunąć?', null=False, blank=False, default=False)
    date_published = models.DateTimeField(verbose_name='Data publikacji:', null=True, blank=True, editable=False)
    date_created = models.DateTimeField(verbose_name='Data utworzenia:', null=False, blank=False, editable=False)
    last_modyfied = models.DateTimeField(verbose_name='Data modyfikacji:', null=True, blank=True)

    class Meta:
        verbose_name = "Trasa"
        verbose_name_plural = "Trasy"
        get_latest_by = '-date_created'
        unique_together = [['created_by', 'name']]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.last_modyfied = timezone.now()
        if self.date_published == None and self.is_published == True:
            self.date_published = timezone.now()
        return super(Route, self).save(*args, **kwargs)

    def avgRate(self):
        rate = RouteRate.objects.filter(referenced_route=self.id, is_deleted=False).aggregate(Avg('rate'))
        rate = rate['rate__avg']
        if rate != None:
            rate = '{:.1f}'.format(rate)
        else:
            rate = 'Brak ocen'
        return rate

    def isLiked(self, *args):
        liked = FavoriteRoute.objects.filter(created_by=args[0], referenced_route=self.id, is_deleted=False)
    
        if len(liked) > 0:
            return True
        else:
            return False

    def getWaypoints(self):
        url = ''
        waypoints = re.split('(https://)?maps.openrouteservice.org/#/directions/', self.url)
        if len(waypoints) == 3:
            url = waypoints[2]
        else:
            url = waypoints[1]
        waypoints = re.split('/data/', url)
        url = waypoints[0]
        waypoints = re.sub('/', '|', url)
        return waypoints

    def getWeather(self, waypoints):
        url = "https://visual-crossing-weather.p.rapidapi.com/forecast"
        querystring = {"aggregateHours":"24","location":waypoints,"contentType":"json","unitGroup":"metric",
            "shortColumnNames":"True", 'forecastDays': 7, 'extendedStats': "True"}

        headers = {
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com",
            'x-rapidapi-key': settings.x_rapidapi_key
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if not 'locations' in response.json():
            return None
        else:
            response = response.json()['locations']
        return response

class FavoriteRoute(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Użytkownik:')
    referenced_route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Trasa:')
    is_deleted = models.BooleanField(verbose_name='Usunąć?', null=False, blank=False, default=False)
    date_created = models.DateTimeField(verbose_name='Data utworzenia:', null=False, blank=False, editable=False)
    last_modyfied = models.DateTimeField(verbose_name='Data modyfikacji:', null=True, blank=True)

    class Meta:
        verbose_name = "Ulubiona trasa"
        verbose_name_plural = "Ulubione trasy"
        get_latest_by = '-date_created'
        unique_together = [['created_by', 'referenced_route']]
        
    def __str__(self):
        return self.referenced_route.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.last_modyfied = timezone.now()
        return super(FavoriteRoute, self).save(*args, **kwargs)

class RouteRate(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Użytkownik:')
    referenced_route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Trasa:')
    rate = models.IntegerField(verbose_name='Ocena:', null=False, blank=False, choices=ROUTE_RATE_CHOICES, default=5)
    is_deleted = models.BooleanField(verbose_name='Usunąć?', null=False, blank=False, default=False)
    date_created = models.DateTimeField(verbose_name='Data utworzenia:', null=False, blank=False, editable=False)
    last_modyfied = models.DateTimeField(verbose_name='Data modyfikacji:', null=True, blank=True)

    class Meta: 
        verbose_name = "Ocena trasy"
        verbose_name_plural = "Oceny tras"
        get_latest_by = '-date_created'
        unique_together = [['created_by', 'referenced_route']]

    def __str__(self):
        return str(self.created_by.username) + ' - ' + str(self.referenced_route.name) + ' - ' +  str(self.rate)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.last_modyfied = timezone.now()
        return super(RouteRate, self).save(*args, **kwargs)

class Comment(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Użytkownik:')
    referenced_route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Trasa:')
    content = models.TextField(verbose_name='Treść komentarza:', null=False, blank=False)
    is_deleted = models.BooleanField(verbose_name='Usunąć?', null=False, blank=False, default=False)
    date_created = models.DateTimeField(verbose_name='Data utworzenia:', null=False, blank=False, editable=False)
    last_modyfied = models.DateTimeField(verbose_name='Data modyfikacji:', null=True, blank=True)

    class Meta:
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"
        get_latest_by = '-date_created'

    def __str__(self):
        return self.content

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.last_modyfied = timezone.now()
        return super(Comment, self).save(*args, **kwargs)

    def sumRate(self, *args, **kwargs):
        goodRate = CommentRate.objects.filter(referenced_comment=self.id, is_deleted=False, rate=1).aggregate(Count('rate'))
        badRate = CommentRate.objects.filter(referenced_comment=self.id, is_deleted=False, rate=-1).aggregate(Count('rate'))
        goodRate = goodRate['rate__count']
        badRate = badRate['rate__count']
        return goodRate - badRate

class CommentRate(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Użytkownik:')
    referenced_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Komentarz:')
    rate = models.IntegerField(verbose_name='Ocena:', null=False, blank=False, choices=COMMENT_RATE_CHOICES, default=1)
    is_deleted = models.BooleanField(verbose_name='Usunąć?', null=False, blank=False, default=False)
    date_created = models.DateTimeField(verbose_name='Data utworzenia:', null=False, blank=False, editable=False)
    last_modyfied = models.DateTimeField(verbose_name='Data modyfikacji:', null=True, blank=True)

    class Meta: 
        verbose_name = "Ocena komentarza"
        verbose_name_plural = "Oceny komentarzy"
        get_latest_by = '-date_created'
        unique_together = [['created_by', 'referenced_comment']]

    def __str__(self):
        return str(self.created_by.username) + ' - ' + str(self.referenced_comment.id) + ' - ' +  str(self.rate)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = timezone.now()
        self.last_modyfied = timezone.now()
        return super(CommentRate, self).save(*args, **kwargs)
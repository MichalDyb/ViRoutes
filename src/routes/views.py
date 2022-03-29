from datetime import datetime
from re import search, sub
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, render
from django.views import View
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib import messages
from django.utils.timezone import make_aware
import pytz

class MyProfileView(LoginRequiredMixin, View):
    template_name = 'routes/my-profile.html'   
    title = 'Mój profil | Trasy | '                       
  
    def get(self, request, *args, **kwargs):
        numberRouteNotPublished = Route.objects.filter(created_by=request.user, is_deleted=False, is_published=False).aggregate(Count('id'))['id__count']
        numberRoutePublished = Route.objects.filter(created_by=request.user, is_deleted=False, is_published=True).aggregate(Count('id'))['id__count']
        numberFavorite = FavoriteRoute.objects.filter(created_by=request.user, is_deleted=False).aggregate(Count('id'))['id__count']
        numberComment = Comment.objects.filter(created_by=request.user, is_deleted=False).aggregate(Count('id'))['id__count']
        return render(request, self.template_name, {'title': self.title, 'numberRouteNotPublished': numberRouteNotPublished, 'numberRoutePublished': numberRoutePublished, 'numberFavorite': numberFavorite, 'numberComment': numberComment})

class AddRouteTutorialView(LoginRequiredMixin, View):
    template_name = 'routes/add-route-tutorial.html'   
    title = 'Poradnik wyznaczania trasy | Mój profil | Trasy | '                       
  
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title})

class AddRouteView(LoginRequiredMixin, View):
    template_name = 'routes/add-route.html'   
    title = 'Dodaj trasę | Moje trasy | Mój profil | Trasy | '                       
    form = AddRouteForm()          

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'title': self.title, 'form': self.form})

    def post(self, request, *args, **kwargs):
        form = AddRouteForm(data=request.POST)
        if form.is_valid():
            check_name = Route.objects.filter(name=form.cleaned_data['name'], is_deleted=False)
            if len(check_name) > 0:
                messages.error(request, 'Trasa o nazwie "' + form.cleaned_data['name'] + '" została już dodana przez tego użytkownika.')
                return render(request, self.template_name, {'title': self.title, 'form': form})
            route = form.save(commit=False)
            route.created_by = request.user
            route.save()
            messages.info(request, 'Nowa trasa o nazwie "' + form.cleaned_data['name'] + '" została dodana.')
            return render(request, self.template_name, {'title': self.title, 'form': AddRouteForm()})
        return render(request, self.template_name, {'title': self.title, 'form': form})

class MyRoutesView(LoginRequiredMixin, View):
    template_name = 'routes/my-routes.html'   
    title = 'Moje trasy | Mój profil | Trasy | '
    form = RouteRateForm()            
  
    def get(self, request, page_number=None, *args, **kwargs):
        routes = Route.objects.filter(created_by=request.user, is_deleted=False).order_by('-date_created')
        routes_per_page = 5
        last_page = len(routes) % routes_per_page
        full_pages = int(len(routes)/routes_per_page) + int(last_page > 0)
        
        if page_number == None:
            page_number = 1
        else:
            page_number = int(page_number)

        if full_pages == 0:
            full_pages = 1

        if page_number > 1 and page_number > full_pages or page_number < 1:
            raise Http404

        if page_number < full_pages:
            page_routes = routes[(page_number - 1) * routes_per_page:page_number * routes_per_page]
        elif page_number == full_pages:
            if len(routes) == 0:
                page_routes = routes
            elif last_page == 0:
                page_routes = routes[(page_number - 1) * routes_per_page:page_number * routes_per_page]
            else:
                page_routes = routes[(page_number - 1) * routes_per_page:(page_number - 1) * routes_per_page + last_page]

        previous_page = page_number - 1
        next_page = page_number + 1
        if page_number == 1:
            previous_page = full_pages
        if page_number == full_pages:
            next_page = 1

        return render(request, self.template_name, {'title': self.title, 'form':self.form, 'current_page': page_number, 'full_pages': full_pages, 'previous_page':previous_page, 'next_page':next_page , 'page_routes': page_routes})

class MyCommentsView(LoginRequiredMixin, View):
    template_name = 'routes/my-comments.html'   
    title = 'Moje komentarze | Mój profil | Trasy | '                       

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(created_by=request.user, is_deleted=False).order_by('-date_created')
        return render(request, self.template_name, {'title': self.title, 'page_comments':comments})

class EditRouteFullView(LoginRequiredMixin, View):
    template_name = 'routes/edit-route-full.html'   
    title = 'Edytuj trasę | Moje trasy | Mój profil | Trasy | '                       

    def get(self, request, route, next_url, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.is_published == True or my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        form = EditRouteFullForm(instance=my_route)  
        return render(request, self.template_name, {'title': self.title, 'form': form, 'route': route, 'next_url': next_url})

    def post(self, request, route, next_url, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.is_published == True or my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        form = EditRouteFullForm(data=request.POST, instance=my_route)
        if form.is_valid():
            check_name = Route.objects.filter(created_by=my_route.created_by, name=form.cleaned_data['name'], is_deleted=False).exclude(id=my_route.id)
            if len(check_name) > 0:
                messages.error(request, 'Trasa o nazwie "' + form.cleaned_data['name'] + '" została już dodana przez tego użytkownika.')
                return render(request, self.template_name, {'title': self.title, 'form': form, 'route': route, 'next_url': next_url})
            route = form.save(commit=False)
            route.save()
            messages.info(request, 'Trasa o nazwie "' + form.cleaned_data['name'] + '" została zmodyfikowana.')
            return redirect(next_url)
        return render(request, self.template_name, {'title': self.title, 'form': form, 'route': route, 'next_url': next_url})

class EditRouteView(LoginRequiredMixin, View):
    template_name = 'routes/edit-route.html'   
    title = 'Edytuj trasę | Moje trasy | Mój profil | Trasy | '                       

    def get(self, request, route, next_url, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.is_published == False or my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        form = EditRouteForm(instance=my_route)  
        return render(request, self.template_name, {'title': self.title, 'form': form, 'route': route, 'next_url': next_url})

    def post(self, request, route, next_url, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.is_published == False or my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        form = EditRouteForm(data=request.POST, instance=my_route)
        if form.is_valid():
            check_name = Route.objects.filter(created_by=my_route.created_by, name=form.cleaned_data['name'], is_deleted=False).exclude(id=my_route.id)
            if len(check_name) > 0:
                messages.error(request, 'Trasa o nazwie "' + form.cleaned_data['name'] + '" została już dodana przez tego użytkownika.')
                return render(request, self.template_name, {'title': self.title, 'form': form, 'route': route, 'next_url': next_url})
            route = form.save(commit=False)
            route.save()
            messages.info(request, 'Trasa o nazwie "' + form.cleaned_data['name'] + '" została zmodyfikowana.')
            return redirect(next_url)
        return render(request, self.template_name, {'title': self.title, 'form': form, 'route': route, 'next_url': next_url})

class DeleteRouteView(LoginRequiredMixin, View):
    template_name = 'routes/delete-route.html'   
    title = 'Usuń trasę | Moje trasy | Mój profil | Trasy | ' 

    def get(self, request, route, next_url, confirmed=None, *args, **kwargs):
        my_route = Route.objects.filter(id=route, created_by=request.user, is_deleted=False, is_published=False)
        if len(my_route) != 1:
            raise Http404
        my_route = my_route[0]
        if confirmed == None:
            return render(request, self.template_name, {'title': self.title, 'route': route, 'next_url': next_url, 'route_name':my_route.name})
        if confirmed == 'yes':
            my_route.is_deleted = True
            my_route.save()
            messages.info(request, 'Trasa o nazwie "' + my_route.name + '" została usunieta.')
            return redirect(next_url)

        if confirmed != 'no':
            raise Http404
        return redirect(next_url)

class AddFavoriteRouteView(LoginRequiredMixin, View):
    template_name = 'routes/my-routes.html'   
    title = 'Dodaj trasę do ulubionych | Moje trasy | Mój profil | Trasy | '

    def get(self, request, route, next_url, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        liked = FavoriteRoute.objects.filter(created_by=request.user.id, referenced_route=my_route.id, is_deleted=True)
        if len(liked) == 1:
            liked[0].is_deleted = False
            liked[0].save()
        else:
            newRoute = FavoriteRoute(created_by=request.user, referenced_route=my_route)
            newRoute.save()
        messages.info(request, 'Trasa o nazwie "' + my_route.name + '" została dodana do ulubionych.')
        return redirect(next_url)

class DeleteFavoriteRouteView(LoginRequiredMixin, View):
    template_name = 'routes/my-routes.html'   
    title = 'Usuń trasę z ulubionych | Moje trasy | Mój profil | Trasy | ' 

    def get(self, request, route, next_url, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        liked = FavoriteRoute.objects.filter(created_by=request.user.id, referenced_route=my_route.id, is_deleted=False)
        if len(liked) == 1:
            liked[0].is_deleted = True
            liked[0].save()
        else:
            raise Http404
        messages.info(request, 'Trasa o nazwie "' + my_route.name + '" została usunieta z ulubionych.')
        return redirect(next_url)

class AddRouteRateView(View):
    template_name = 'routes/my-routes.html'   
    title = 'Dodaj ocene trasy | Moje trasy | Mój profil | Trasy | '

    def post(self, request, route, next_url, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if not request.user.is_authenticated:
            messages.info(request, 'Aby ocenić trasę musisz być zalogowany.')
            return redirect(next_url)
        if my_route.is_published == False and my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        form = RouteRateForm(data=request.POST)
        if not form.is_valid():
            messages.error(request, 'Ocena trasy nie została dodana. Podane dane są nieprawidłowe.')
            return redirect(next_url)
        rated = RouteRate.objects.filter(created_by=request.user, referenced_route=my_route, is_deleted=False)
        if len(rated) == 1:
            rated[0].rate = form.cleaned_data['rate']
            rated[0].save()
            messages.info(request, 'Ocena trasy "' + my_route.name + '" została zmieniona.')
            return redirect(next_url)
        rated = RouteRate.objects.filter(created_by=request.user, referenced_route=my_route, is_deleted=True)
        if len(rated) == 1:
            rated[0].is_deleted = False
            rated[0].rate = form.cleaned_data['rate']
            rated[0].save()
        else:
            newRouteRate = RouteRate(created_by=request.user, referenced_route=my_route, rate=form.cleaned_data['rate'])
            newRouteRate.save()
        messages.info(request, 'Ocena trasy "' + my_route.name + '" została dodana.')
        return redirect(next_url)

class AddRouteCommentView(View):
    template_name = 'routes/my-routes.html'   
    title = 'Dodaj komentarz | Moje trasy | Mój profil | Trasy | '

    def post(self, request, route, next_url, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if not request.user.is_authenticated:
            messages.info(request, 'Aby dodać komentarz musisz być zalogowany.')
            return redirect(next_url)
        if my_route.is_published == False and my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        form = CommentForm(data=request.POST)
        if not form.is_valid():
            messages.error(request, 'Komentarz nie został dodany, podane dane są nieprawidłowe.')
            return redirect(next_url)
        
        newComment = Comment(created_by=request.user, referenced_route=my_route, content=form.cleaned_data['content'])
        newComment.save()
        messages.info(request, 'Nowy komentarz został dodany.')
        return redirect(next_url)

class AddCommentRateView(View):
    template_name = 'routes/my-routes.html'   
    title = 'Dodaj ocene komentarza | Moje trasy | Mój profil | Trasy | '

    def get(self, request, comment, rate, next_url, *args, **kwargs):
        my_comment = get_object_or_404(Comment, id=comment)
        if not request.user.is_authenticated:
            messages.info(request, 'Aby ocenić komentarz musisz być zalogowany.')
            return redirect(next_url)
        if my_comment.is_deleted == True or my_comment.referenced_route.is_published == False and my_comment.referenced_route.created_by != request.user or my_comment.referenced_route.is_deleted == True:
            raise Http404
        rated = CommentRate.objects.filter(created_by=request.user, referenced_comment=my_comment, is_deleted=False)
        if len(rated) == 1:
            rated[0].rate = rate
            rated[0].save()
            messages.info(request, 'Ocena komentarza została zmieniona.')
            return redirect(next_url)
        rated = CommentRate.objects.filter(created_by=request.user, referenced_comment=my_comment, is_deleted=True)
        if len(rated) == 1:
            rated[0].is_deleted = False
            rated[0].rate = rate
            rated[0].save()
        else:
            newRouteRate = CommentRate(created_by=request.user, referenced_comment=my_comment, rate=rate)
            newRouteRate.save()
        messages.info(request, 'Ocena komentarza została dodana.')
        return redirect(next_url)

class MyRouteDetailView(LoginRequiredMixin, View):
    template_name = 'routes/my-route-detail.html'   
    title = 'Szczegóły trasy | Moje trasy | Mój profil | Trasy | '                       

    def get(self, request, route, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        form = CommentForm()
        comments = Comment.objects.filter(referenced_route=my_route, is_deleted=False).order_by('date_created')
        return render(request, self.template_name, {'title': self.title, 'form': form, 'form2': RouteRateForm, 'page_route': my_route, 'page_comments':comments , 'route': route})

class MyRouteWeatherView(LoginRequiredMixin, View):
    template_name = 'routes/my-route-weather.html'   
    title = 'Warunki pogodowe | Moje trasy | Mój profil | Trasy | '                       

    def get(self, request, route, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        locations = my_route.getWeather(my_route.getWaypoints())
        return render(request, self.template_name, {'title': self.title, 'page_route': my_route, 'route': route, 'locations': locations})

class FavoriteRoutesView(LoginRequiredMixin, View):
    template_name = 'routes/favorite-routes.html'   
    title = 'Ulubione trasy | Mój profil | Trasy | '
    form = RouteRateForm()            
  
    def get(self, request, page_number=None, *args, **kwargs):
        routes = Route.objects.filter(is_deleted=False, favoriteroute__created_by=request.user, 
            favoriteroute__is_deleted=False).order_by('-date_created')

        routes_per_page = 5
        last_page = len(routes) % routes_per_page
        full_pages = int(len(routes)/routes_per_page) + int(last_page > 0)
        
        if page_number == None:
            page_number = 1
        else:
            page_number = int(page_number)

        if full_pages == 0:
            full_pages = 1

        if page_number > 1 and page_number > full_pages or page_number < 1:
            raise Http404

        if page_number < full_pages:
            page_routes = routes[(page_number - 1) * routes_per_page:page_number * routes_per_page]
        elif page_number == full_pages:
            if len(routes) == 0:
                page_routes = routes
            elif last_page == 0:
                page_routes = routes[(page_number - 1) * routes_per_page:page_number * routes_per_page]
            else:
                page_routes = routes[(page_number - 1) * routes_per_page:(page_number - 1) * routes_per_page + last_page]

        previous_page = page_number - 1
        next_page = page_number + 1
        if page_number == 1:
            previous_page = full_pages
        if page_number == full_pages:
            next_page = 1

        return render(request, self.template_name, {'title': self.title, 'form':self.form, 'current_page': page_number, 'full_pages': full_pages, 'previous_page':previous_page, 'next_page':next_page , 'page_routes': page_routes})

class FavoriteRouteDetailView(LoginRequiredMixin, View):
    template_name = 'routes/favorite-route-detail.html'   
    title = 'Szczegóły trasy | Ulubione trasy | Mój profil | Trasy | '                       

    def get(self, request, route, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        checkLiked = FavoriteRoute.objects.filter(created_by=request.user, referenced_route=my_route, is_deleted=False)
        if len(checkLiked) != 1:
            raise Http404
        form = CommentForm()
        comments = Comment.objects.filter(referenced_route=my_route, is_deleted=False).order_by('date_created')
        return render(request, self.template_name, {'title': self.title, 'form': form, 'form2': RouteRateForm, 'page_route': my_route, 'page_comments':comments , 'route': route})

class FavoriteRouteWeatherView(LoginRequiredMixin, View):
    template_name = 'routes/favorite-route-weather.html'   
    title = 'Warunki pogodowe | Ulubione trasy | Mój profil | Trasy | '                       

    def get(self, request, route, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.created_by != request.user or my_route.is_deleted == True:
            raise Http404
        checkLiked = FavoriteRoute.objects.filter(created_by=request.user, referenced_route=my_route, is_deleted=False)
        if len(checkLiked) != 1:
            raise Http404
        locations = my_route.getWeather(my_route.getWaypoints())
        return render(request, self.template_name, {'title': self.title, 'page_route': my_route, 'route': route, 'locations': locations})

class RoutesView(View):
    template_name = 'routes/published-routes.html'   
    title = 'Opublikowane trasy | Trasy | '
    form = RouteRateForm()            
  
    def get(self, request, page_number=None, *args, **kwargs):
        routes = Route.objects.filter(is_deleted=False, is_published=True).order_by('-date_created')
        routes_per_page = 5
        last_page = len(routes) % routes_per_page
        full_pages = int(len(routes)/routes_per_page) + int(last_page > 0)
        
        if page_number == None:
            page_number = 1
        else:
            page_number = int(page_number)

        if full_pages == 0:
            full_pages = 1

        if page_number > 1 and page_number > full_pages or page_number < 1:
            raise Http404

        if page_number < full_pages:
            page_routes = routes[(page_number - 1) * routes_per_page:page_number * routes_per_page]
        elif page_number == full_pages:
            if len(routes) == 0:
                page_routes = routes
            elif last_page == 0:
                page_routes = routes[(page_number - 1) * routes_per_page:page_number * routes_per_page]
            else:
                page_routes = routes[(page_number - 1) * routes_per_page:(page_number - 1) * routes_per_page + last_page]

        previous_page = page_number - 1
        next_page = page_number + 1
        if page_number == 1:
            previous_page = full_pages
        if page_number == full_pages:
            next_page = 1

        return render(request, self.template_name, {'title': self.title, 'form':self.form, 'current_page': page_number, 'full_pages': full_pages, 'previous_page':previous_page, 'next_page':next_page , 'page_routes': page_routes})

class RouteDetailView(View):
    template_name = 'routes/published-route-detail.html'   
    title = 'Szczegóły trasy | Opublikowane trasy | Trasy | '                       

    def get(self, request, route, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.is_deleted == True or my_route.is_published == False:
            raise Http404
        form = CommentForm()
        comments = Comment.objects.filter(referenced_route=my_route, is_deleted=False).order_by('date_created')
        return render(request, self.template_name, {'title': self.title, 'form': form, 'form2': RouteRateForm, 'page_route': my_route, 'page_comments':comments , 'route': route})

class RouteWeatherView(View):
    template_name = 'routes/published-route-weather.html'   
    title = 'Warunki pogodowe | Opublikowane trasy | Trasy | '                       

    def get(self, request, route, *args, **kwargs):
        my_route = get_object_or_404(Route, id=route)
        if my_route.is_deleted == True or my_route.is_published == False:
            raise Http404
        locations = my_route.getWeather(my_route.getWaypoints())
        return render(request, self.template_name, {'title': self.title, 'page_route': my_route, 'route': route, 'locations': locations})

class SearchRoutesView(View):
    template_name = 'routes/published-search-routes.html'   
    title = 'Wyszukaj trase | Opublikowane trasy | Trasy | '
    form = RouteRateForm()         
  
    def get(self, request, page_number=None, *args, **kwargs):
        searchForm = SearchForm(data=request.GET)

        routes = Route.objects.filter(is_deleted=False, is_published=True).order_by('-date_created')

        if request.GET.get('name'):
            routes = routes.filter(name__icontains=request.GET.get('name'))
        if request.GET.get('author'):
            routes = routes.filter(created_by__username__icontains=request.GET.get('author'))
        if request.GET.get('date'):
            subDate = re.split('-', request.GET.get('date'))
            tz = pytz.timezone('Europe/Helsinki')

            date = timezone.datetime(year=int(subDate[0]), month=int(subDate[1]), day=int(subDate[2]))
            date = make_aware(date, tz, True)

            if request.GET.get('datetype') == '1':
                routes = routes.filter(date_published__lt=date)
            if request.GET.get('datetype') == '2':
                routes = routes.filter(date_published__gt=date)

        if request.GET.get('sort') == '1':
            if request.GET.get('sorttype') == '1':
                routes = routes.order_by('-date_published')
            if request.GET.get('sorttype') == '2':
                routes = routes.order_by('date_published')

        if request.GET.get('sort') == '2':
            if request.GET.get('sorttype') == '1':
                routes = routes.order_by('-name')
            if request.GET.get('sorttype') == '2':
                routes = routes.order_by('name')

        if request.GET.get('sort') == '3':
            if request.GET.get('sorttype') == '1':
                routes = routes.order_by('-created_by__username')
            if request.GET.get('sorttype') == '2':
                routes = routes.order_by('created_by__username')

        routes_per_page = 5
        last_page = len(routes) % routes_per_page
        full_pages = int(len(routes)/routes_per_page) + int(last_page > 0)
        
        if page_number == None:
            page_number = 1
        else:
            page_number = int(page_number)

        if full_pages == 0:
            full_pages = 1

        if page_number > 1 and page_number > full_pages or page_number < 1:
            raise Http404

        if page_number < full_pages:
            page_routes = routes[(page_number - 1) * routes_per_page:page_number * routes_per_page]
        elif page_number == full_pages:
            if len(routes) == 0:
                page_routes = routes
            elif last_page == 0:
                page_routes = routes[(page_number - 1) * routes_per_page:page_number * routes_per_page]
            else:
                page_routes = routes[(page_number - 1) * routes_per_page:(page_number - 1) * routes_per_page + last_page]

        previous_page = page_number - 1
        next_page = page_number + 1
        if page_number == 1:
            previous_page = full_pages
        if page_number == full_pages:
            next_page = 1

        getData = '?'
        for i in request.GET:
            getData += i + '=' + request.GET.get(i) + '&' 

        return render(request, self.template_name, {'title': self.title, 'form':self.form, 'searchForm':searchForm, 'current_page': page_number, 'full_pages': full_pages, 'previous_page':previous_page, 'next_page':next_page , 'page_routes': page_routes, 'getData': getData[:len(getData)-1]})
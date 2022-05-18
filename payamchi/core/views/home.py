from django.shortcuts import render
from django import views
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, views.View):

    def get(self, request):
        return render(request, 'core/home.html', {})

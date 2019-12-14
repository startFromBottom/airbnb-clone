from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from . import models


def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = (
        models.Room.objects.all()
    )  # Queryset : lazy (not load real data from db in this moment)
    paginator = Paginator(room_list, per_page=10, orphans=5)

    try:
        # not have to handling exceptions but customizing less
        # rooms = paginator.get_page(page)
        rooms = paginator.page(int(page))
        return render(request, "rooms/home.html", {"page": rooms})
    except EmptyPage:
        return redirect("/")

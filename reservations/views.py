import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from reviews import forms as review_forms
from django.contrib.auth.decorators import login_required
from . import models
from users import models as user_models


class CreateError(Exception):
    pass


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        # create reservation
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = review_forms.CreateReviewForm
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


@login_required
def edit_reservation(request, pk, verb):

    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


@login_required
def see_reservations(request, pk):

    try:
        # HOST
        request.session["is_hosting"]
        reservations = models.Reservation.objects.filter(room__host__pk=pk)

    except KeyError:
        # GUEST
        try:
            reservations = models.Reservation.objects.filter(guest__pk=pk)

        except models.Reservation.DoesNotExist:
            return redirect(reverse("core:home"))

    except models.Reservation.DoesNotExist:
        return redirect(reverse("core:home"))

    return render(
        request, "reservations/reservation_see.html", {"reservations": reservations}
    )


@login_required
def see_edit_reservation(request, guest_pk, r_pk, verb):

    print("알라딘 === ", verb)

    reservation = models.Reservation.objects.get_or_none(pk=r_pk)
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    elif verb == "delete":
        models.Reservation.objects.get(pk=r_pk).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:see", kwargs={"pk": guest_pk}))

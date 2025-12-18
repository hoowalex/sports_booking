from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Training
from django.utils import timezone


def index(request):
    recent = Training.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    return render(request, 'index.html', {'recent_trainings': recent})

def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def training_list(request):
    trainings = Training.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'trainings.html', {'trainings': trainings})


@login_required
def join_training(request, training_id):
    training = get_object_or_404(Training, id=training_id)

    # Перевіряємо, чи користувач уже записаний
    if request.user in training.participants.all():
        messages.info(request, "Ви вже записані на це тренування.")
    # Перевіряємо, чи є вільні місця
    elif training.participants.count() < training.max_participants:
        training.participants.add(request.user)
        messages.success(request, f"Ви успішно записалися на {training.title}!")
    else:
        messages.error(request, "На жаль, усі місця вже зайняті.")

    return redirect('trainings')


@login_required
def create_training(request):
    if request.user.role not in ['trainer', 'admin']:
        return redirect('trainings')

    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        max_p = request.POST.get('max_participants', 15)
        Training.objects.create(
            title=title,
            date=date,
            max_participants=max_p,  # Зберігаємо в БД
            trainer=request.user
        )
        return redirect('trainings')

    return render(request, 'create_training.html')


# Додайте ці функції до вашого booking/views.py

@login_required
@login_required
def profile(request):
    now = timezone.now()

    # Тренування, які ще не відбулися
    upcoming_trainings = request.user.joined_trainings.filter(date__gte=now).order_by('date')

    # Тренування, які вже завершилися
    past_trainings = request.user.joined_trainings.filter(date__lt=now).order_by('-date')

    # Якщо користувач тренер — його власні тренування (майбутні)
    created_trainings = None
    if request.user.role in ['trainer', 'admin']:
        created_trainings = Training.objects.filter(trainer=request.user).order_by('date')

    return render(request, 'profile.html', {
        'upcoming_trainings': upcoming_trainings,
        'past_trainings': past_trainings,
        'created_trainings': created_trainings
    })


@login_required
def leave_training(request, training_id):
    training = get_object_or_404(Training, id=training_id)
    if request.user in training.participants.all():
        training.participants.remove(request.user)

    # Повертаємо користувача на ту сторінку, де він був (список або профіль)
    return redirect(request.META.get('HTTP_REFERER', 'trainings'))


@login_required
def delete_training(request, training_id):
    training = get_object_or_404(Training, id=training_id)

    # Перевірка: тільки тренер цього заняття або адмін можуть видаляти
    if request.user == training.trainer or request.user.role == 'admin':
        training.delete()
        messages.success(request, "Тренування успішно видалено.")
    else:
        messages.error(request, "У вас немає прав для видалення цього тренування.")

    return redirect('trainings')



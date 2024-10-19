from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, RecipeStep
from .forms import RecipeForm, RecipeStepForm

from django.shortcuts import render, redirect
from .models import Recipe, RecipeStep
from .forms import RecipeForm, RecipeStepForm

def index(request):
    # Tüm tarifleri al
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, "index.html", {'recipes': recipes})

def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()  # Tarifi kaydet
            return redirect('index')  # Ana sayfaya yönlendir
    else:
        form = RecipeForm()

    return render(request, 'create_recipe.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import Recipe, RecipeStep


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    steps = RecipeStep.objects.filter(recipe=recipe)

    step_times = []
    chef_busy_until = 0  # Şefin meşgul olduğu zamanı takip etmek için

    # Adımların başlama ve bitiş sürelerini hesapla
    for step in steps:
        if step.occupies_chef:
            start_time = chef_busy_until
        else:
            start_time = 0  # Şef gerektirmeyen adımlar 0'dan başlayabilir

        # Bitiş süresi
        end_time = start_time + step.duration

        # Şef meşgulse, zamanı güncelle
        if step.occupies_chef:
            chef_busy_until = end_time

        # Adımı ve hesaplanan süreleri listeye ekle
        step_times.append({
            'step': step,
            'start_time': start_time,
            'end_time': end_time,
        })

    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'step_times': step_times,
    })


def add_recipe_step(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    if request.method == 'POST':
        form = RecipeStepForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.recipe = recipe  # Adımı tarif ile ilişkilendir
            step.save()  # Adımı kaydet
            return redirect('recipe_detail', recipe_id=recipe.id)  # Tarif detayına yönlendir
    else:
        form = RecipeStepForm()

    return render(request, 'add_recipe_step.html', {'form': form, 'recipe': recipe})



def recipe_list(request):
    # Tüm tarifleri alıyoruz ve her bir tarife bağlı adımlara da erişiyoruz
    recipes = Recipe.objects.prefetch_related('steps').all()

    context = {
        'recipes': recipes,  # Tarifler ve adımlar context'e ekleniyor
    }

    return render(request, 'recipe_list.html', context)


def calculate_time(steps):
    results = []
    step_times = {}
    chef_busy_until = 0

    while steps:
        current_batch = []  # İşlenecek adımlar

        for step in steps:
            # Ön koşulları kontrol et
            if step.prerequisites.exists():
                if not all(prerequisite in step_times for prerequisite in step.prerequisites.all()):
                    continue  # Ön koşullar tamamlanmadı

            # Adımın başlangıç zamanını hesapla
            if step.occupies_chef:
                # Eğer adım şef gerektiriyorsa
                start_time = chef_busy_until
            else:
                # Şef gerektirmiyorsa, başlangıç zamanı 0'dan başlar
                start_time = 0

            # Ön koşul bitiş zamanlarını kontrol et
            if step.prerequisites.exists():
                prerequisite_end_times = [
                    step_times[prerequisite]['end_time']
                    for prerequisite in step.prerequisites.all()
                    if prerequisite in step_times
                ]
                if prerequisite_end_times:
                    start_time = max(start_time, max(prerequisite_end_times))

            # Adımın bitiş zamanını hesapla
            end_time = start_time + step.duration

            # Mevcut adımı ekle
            current_batch.append((step, start_time, end_time))

            # Şef meşgulse, zamanı güncelle
            if step.occupies_chef:
                chef_busy_until = end_time

        # Mevcut adımları işle
        for step, start, end in current_batch:
            step_times[step] = {'start_time': start, 'end_time': end}
            results.append(f"'{step.name}' starts at minute {start} and ends at minute {end}.")

        # İşlenen adımları listeden çıkar
        steps = [step for step in steps if step not in [s for s, _, _ in current_batch]]

    return results

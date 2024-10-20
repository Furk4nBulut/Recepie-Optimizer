from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, RecipeStep
from .forms import RecipeForm, RecipeStepForm
from .utils import calculate_time
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




def recipe_list(request):
    # Tüm tarifleri alıyoruz ve her bir tarife bağlı adımlara da erişiyoruz
    recipes = Recipe.objects.prefetch_related('steps').all()

    context = {
        'recipes': recipes,  # Tarifler ve adımlar context'e ekleniyor
    }

    return render(request, 'recipe_list.html', context)




from django.shortcuts import get_object_or_404, redirect


def optimize_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)  # Get the recipe using recipe_id

    if request.method == 'POST':
        form = RecipeStepForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.recipe = recipe  # Assign the recipe
            step.save()  # Save the step with the assigned recipe
            return redirect('optimize_recipe', recipe_id=recipe_id)
    else:
        form = RecipeStepForm()

    steps = RecipeStep.objects.filter(recipe=recipe)  # Get steps for the recipe

    # Zaman hesaplamayı çalıştır
    results = []
    if steps:
        results = calculate_time(steps)

    return render(request, 'optimize.html', {'form': form, 'steps': steps, 'results': results, 'recipe': recipe})

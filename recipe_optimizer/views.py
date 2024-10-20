from .utils import calculate_time
from .forms import RecipeForm, RecipeStepForm
from django.shortcuts import render,get_object_or_404, redirect
from .models import Recipe, RecipeStep
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, RecipeStep
from .forms import RecipeStepForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, RecipeStep


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




def recipe_list(request):
    # Tüm tarifleri alıyoruz ve her bir tarife bağlı adımlara da erişiyoruz
    recipes = Recipe.objects.prefetch_related('steps').all()

    context = {
        'recipes': recipes,  # Tarifler ve adımlar context'e ekleniyor
    }

    return render(request, 'recipe_list.html', context)


def optimize_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)  # Get the recipe using recipe_id

    if request.method == 'POST':
        form = RecipeStepForm(request.POST, recipe=recipe)  # Pass the recipe instance
        if form.is_valid():
            step = form.save(commit=False)
            step.recipe = recipe  # Assign the recipe
            step.save()  # Save the step with the assigned recipe

            # Save the prerequisites (ManyToMany field)
            form.save_m2m()  # This saves the ManyToMany relationships

            return redirect('optimize', recipe_id=recipe_id)
    else:
        form = RecipeStepForm(recipe=recipe)  # Pass the recipe instance

    steps = RecipeStep.objects.filter(recipe=recipe)  # Get steps for the recipe

    # Time calculation
    results = []
    if steps:
        results = calculate_time(steps)

    return render(request, 'optimize.html', {'form': form, 'steps': steps, 'results': results, 'recipe': recipe})


def edit_step(request, recipe_id, step_id=None):
    recipe = get_object_or_404(Recipe, pk=recipe_id)  # Get the recipe based on the recipe_id

    if step_id:
        # If step_id is provided, we're editing an existing step
        step = get_object_or_404(RecipeStep, pk=step_id, recipe=recipe)
    else:
        # Otherwise, we're adding a new step
        step = None

    if request.method == 'POST':
        # If the request is POST, process the form data
        form = RecipeStepForm(request.POST, instance=step, recipe=recipe)
        if form.is_valid():
            step = form.save(commit=False)
            step.recipe = recipe  # Link the step to the current recipe
            step.save()  # Save the step

            # Save the many-to-many field (prerequisites)
            form.save_m2m()

            return redirect('optimize_recipe', recipe_id=recipe_id)
    else:
        # If GET, display the empty or populated form
        form = RecipeStepForm(instance=step, recipe=recipe)

    return render(request, 'edit_step.html', {
        'form': form,
        'recipe': recipe,
        'step': step
    })

def delete_step(request, recipe_id, step_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    step = get_object_or_404(RecipeStep, pk=step_id, recipe=recipe)

    if request.method == 'POST':
        step.delete()  # Delete the step from the database
        return redirect('optimize_recipe', recipe_id=recipe_id)

    return render(request, 'confirm_delete.html', {'recipe': recipe, 'step': step})

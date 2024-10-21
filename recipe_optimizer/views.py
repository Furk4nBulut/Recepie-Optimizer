from .utils import calculate_time
from .forms import RecipeForm, RecipeStepForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, RecipeStep
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    """
    Retrieves all recipes and renders them on the index page.

    :param request: The HTTP request object.
    :returns: Renders the 'index.html' template with a list of all recipes ordered by creation date.
    """
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, "index.html", {'recipes': recipes})


def create_recipe(request):
    """
    Handles the creation of a new recipe.

    If the request method is POST and the form is valid, saves the recipe and redirects to the index page.
    Otherwise, displays the form for creating a recipe.

    :param request: The HTTP request object.
    :returns: Renders the 'create_recipe.html' template with the recipe form.
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RecipeForm()

    return render(request, 'create_recipe.html', {'form': form})


def recipe_list(request):
    """
    Retrieves all recipes and their related steps and renders them on the recipe list page.

    :param request: The HTTP request object.
    :returns: Renders the 'recipe_list.html' template with a list of all recipes and their steps.
    """
    recipes = Recipe.objects.prefetch_related('steps').all()

    return render(request, 'recipe_list.html', {'recipes': recipes})


def optimize_recipe(request, recipe_id):
    """
    Handles the optimization of a recipe by adding steps and calculating the time for each step.

    :param request: The HTTP request object.
    :param recipe_id: The ID of the recipe to be optimized.
    :returns: Renders the 'optimize.html' template with the form to add steps, the list of steps, and time calculation results.
    :raises Http404: If the recipe with the given ID does not exist.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        form = RecipeStepForm(request.POST, recipe=recipe)
        if form.is_valid():
            step = form.save(commit=False)
            step.recipe = recipe
            step.save()
            form.save_m2m()

            return redirect('optimize_recipe', recipe_id=recipe_id)
    else:
        form = RecipeStepForm(recipe=recipe)

    steps = RecipeStep.objects.filter(recipe=recipe)
    results, last_end_time = calculate_time(steps) if steps else ([], 0)

    return render(request, 'optimize.html', {
        'form': form,
        'steps': steps,
        'results': results,
        'last_end_time': last_end_time,
        'recipe': recipe
    })


def edit_step(request, recipe_id, step_id=None):
    """
    Edits an existing step or adds a new step to a recipe.

    :param request: The HTTP request object.
    :param recipe_id: The ID of the recipe to which the step belongs.
    :param step_id: The ID of the step to be edited (if any).
    :returns: Renders the 'edit_step.html' template with the form for editing or adding a step.
    :raises Http404: If the recipe or step does not exist.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    step = get_object_or_404(RecipeStep, pk=step_id, recipe=recipe) if step_id else None

    if request.method == 'POST':
        form = RecipeStepForm(request.POST, instance=step, recipe=recipe)
        if form.is_valid():
            step = form.save(commit=False)
            step.recipe = recipe
            step.save()
            form.save_m2m()

            return redirect('optimize_recipe', recipe_id=recipe_id)
    else:
        form = RecipeStepForm(instance=step, recipe=recipe)

    return render(request, 'edit_step.html', {
        'form': form,
        'recipe': recipe,
        'step': step
    })


def delete_step(request, recipe_id, step_id):
    """
    Deletes a specific step from a recipe.

    :param request: The HTTP request object.
    :param recipe_id: The ID of the recipe to which the step belongs.
    :param step_id: The ID of the step to be deleted.
    :returns: Redirects to the optimize recipe page after deletion.
    :raises Http404: If the recipe or step does not exist.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    step = get_object_or_404(RecipeStep, pk=step_id, recipe=recipe)

    if request.method == 'POST':
        step.delete()
        return redirect('optimize_recipe', recipe_id=recipe_id)

    return render(request, 'confirm_delete.html', {'recipe': recipe, 'step': step})


def delete_recipe(request, recipe_id):
    """
    Deletes a specific recipe.

    :param request: The HTTP request object.
    :param recipe_id: The ID of the recipe to be deleted.
    :returns: Redirects to the index page after deletion.
    :raises Http404: If the recipe does not exist.
    """
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.method == 'POST':
        recipe.delete()
        return redirect('index')

    return render(request, 'confirm_delete.html', {'recipe': recipe})


def recipe_json(request, recipe_id):
    """
    Returns the recipe and its steps in JSON format, with an option to download.

    :param request: The HTTP request object.
    :param recipe_id: The ID of the recipe to retrieve.
    :returns: A JSON response containing the recipe and its steps. Optionally, allows downloading as a JSON file.
    :raises Http404: If the recipe does not exist.
    """
    recipe = Recipe.objects.get(id=recipe_id)
    steps = RecipeStep.objects.filter(recipe=recipe)

    data = {
        'recipe': {
            'id': recipe.id,
            'name': recipe.name,
            'description': recipe.description,
            'steps': [
                {
                    'id': step.id,
                    'name': step.name,
                    'duration': step.duration,
                    'occupies_chef': step.occupies_chef,
                    'prerequisites': [prereq.name for prereq in step.prerequisites.all()]
                }
                for step in steps
            ]
        }
    }

    results, last_end_time = calculate_time(steps)
    data['optimization_results'] = results
    data['total_time'] = last_end_time

    if request.GET.get('download'):
        response = HttpResponse(
            json.dumps(data, indent=4),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="recipe_{recipe_id}.json"'
        return response

    return JsonResponse(data)


@csrf_exempt
def upload_json(request):
    if request.method == 'POST':
        try:
            json_file = request.FILES['json-file']
            json_data = json.load(json_file)

            recipe_data = json_data.get('recipe')
            if not recipe_data:
                return JsonResponse({'success': False, 'error': 'Invalid JSON format'})

            recipe, created = Recipe.objects.update_or_create(
                name=recipe_data['name'],
                defaults={
                    'description': recipe_data['description']
                }
            )

            for step_data in recipe_data.get('steps', []):
                prerequisite_names = step_data.get('prerequisites', [])
                prerequisites = RecipeStep.objects.filter(name__in=prerequisite_names, recipe=recipe)

                step, created = RecipeStep.objects.update_or_create(
                    recipe=recipe,
                    name=step_data['name'],
                    defaults={
                        'duration': step_data['duration'],
                        'occupies_chef': step_data['occupies_chef']
                    }
                )
                step.prerequisites.set(prerequisites)
                step.save()

            return JsonResponse({'success': True})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
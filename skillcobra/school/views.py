from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from skillcobra.school.apis.serializers import CourseCurriculumSerializer
from skillcobra.school.forms import CourseCurriculumForm
from skillcobra.school.forms import CreateCourseCurriculumLectureForm

from .models import CourseCurriculum, Lecture


# Create your views here.
@login_required
@require_POST
@csrf_exempt
def delete_course_module(request, module_pk):
    profile = get_user(request).user_profile
    module = get_object_or_404(
        CourseCurriculum,
        course__tutor=profile,
        pk=module_pk,
    )
    module.delete()
    return JsonResponse({"success": True},safe=False, status=204)
# Create your views here.
@login_required
@require_POST
@csrf_exempt
def update_course_module(request, module_pk):
    profile = get_user(request).user_profile
    module = get_object_or_404(
        CourseCurriculum,
        course__tutor=profile,
        pk=module_pk,
    )
    form = CourseCurriculumForm(request.POST, instance=module)
    if form.is_valid():
        form.save()
        return JsonResponse(
            {"details": "module update successful", "success": True},
            safe=False, status=200)
    return JsonResponse(
        {"details": "Something went went while updating the form"},
        safe=False, status=400)

@login_required
@require_POST
@csrf_exempt
def create_course_module_lecture(request, module_pk):
    profile = get_user(request).user_profile
    module = get_object_or_404(
        CourseCurriculum,
        course__tutor=profile,
        pk=module_pk,
    )
    form = CreateCourseCurriculumLectureForm(request.POST, request.FILES)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.module_lecture = module
        instance.save()
        form.save(commit=True)
        return JsonResponse(
            {"details": "module update successful", "success": True},
            safe=False, status=201)
    return JsonResponse(
        {"details": "Something went went while updating the form"},
        safe=False, status=400)


@login_required
@require_POST
@csrf_exempt
def update_lecture_view(request, module_pk, lecture_pk):

    # profile = get_user(request).user_profile
    module = get_object_or_404(
        Lecture,
        pk=lecture_pk,
        module_lecture__pk=module_pk,
    )
    # form = CreateCourseCurriculumLectureForm(request.POST, request.FILES)
    # if form.is_valid():
    #     instance = form.save(commit=False)
    #     instance.module_lecture = module
    #     instance.save()
    #     form.save(commit=True)
    #     return JsonResponse(
    #         {"details": "module update successful", "success": True},
    #         safe=False, status=201)
    
    return JsonResponse(
        {"details": "Something went went while updating the form"},
        safe=False, status=400)

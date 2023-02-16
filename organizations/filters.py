# import django_filters
# from django_filters import CharFilter, ChoiceFilter, ModelChoiceFilter
# from .models import *
# from organizations.models import *
# from django import forms
# from django.forms.widgets import TextInput, ChoiceWidget, Select
#
#
# class institutionFilter(django_filters.FilterSet):
#     #course_short = django_filters.ModelMultipleChoiceFilter(queryset=Courses.objects.select_related('category').all().order_by('course_short'), required=True,
#                                                            # widget=forms.Select)
#     #name = CharFilter(field_name='name', lookup_expr="icontains", label='Name',
#                      # widget=TextInput(attrs={'placeholder': 'Search Universites'}))
#     class_name = django_filters.ModelChoiceFilter(queryset=Organization.objects.all().order_by('name'),required=True,empty_label="Select Class",
#     widget=forms.Select)
#     building = django_filters.ModelChoiceFilter(queryset=Building.objects.all(),required=True, empty_label="Select Board/Exam/Uni",
#                                                     widget=forms.Select)
#
#     #category = django_filters.ChoiceFilter(choices=CATEGORY_CHOICES, required=False, widget=forms.Select)
#
#     class Meta:
#         model = Organization
#         fields = ['class_name', 'building']
#         widgets = {
#             #'category': forms.Select(),
#             #'country': forms.Select(),
#
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(institutionFilter, self).__init__(*args, **kwargs)
#         self.form['building'].queryset = Building.objects.none()
#         # at sturtup user doesn't push Submit button, and QueryDict (in data) is empty
#         if self.data == {}:
#             self.queryset = self.queryset.none()
#         else:
#             self.queryset.all()
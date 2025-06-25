# widgets.py- users/widgets.py
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'widgets/custom_file_input.html'




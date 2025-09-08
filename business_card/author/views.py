from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .models import Contact, PortFolio
from .forms import ContactForm
from .tasks import send_email_task


User = get_user_model()


def get_user():
    return User.objects.first()


def home(request):
    """Home page has context with meaning "user"."""
    return render(request, "author/home.html", {"user": get_user()})


class PortfolioLiveView(ListView):
    """
    To display works in a list.
    
    Has a context with the value:
    - projects: all objects of model PortFolio filtered by user and sorted by data from newest to oldest
    """
    model = PortFolio
    template_name = "author/portfolio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["projects"] = PortFolio.objects.filter(user=get_user()).order_by("-created_at")
        return context


class ContactCreateView(TemplateView):
    """
    Contact presentation and contact form.

    Has a context with the value:
    - contact: takes one object from model Contact per user
    - form: the form with the name is ContactForm not related to the model in any way
    - errors: a form is created if validation fails

    Method post sends form data to an email address.
    """
    model = Contact
    template_name = "author/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact"] = get_object_or_404(Contact, user=get_user())
        context["form"] = ContactForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            message = ""

            for field, value in form.cleaned_data.items():
                if field != 'file':
                    message += f"{field}: {value}\n"

            uploaded_file = request.FILES.get('file')

            if uploaded_file:
                file_path = default_storage.save(f"temp/{uploaded_file.name}", ContentFile(uploaded_file.read()))
            else:
                file_path = None
                
            send_email_task.delay(
                subject="messages from business card sites",
                message=message,
                email=["dmitriymorkov83@gmail.com"],
                file_path=file_path,
                )

            return self.render_to_response(
                self.get_context_data(success=True, form=ContactForm())
            )
        
        return self.render_to_response(self.get_context_data(form=form, errors=form.errors.values))
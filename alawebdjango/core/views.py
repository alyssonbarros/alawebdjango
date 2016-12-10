from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View, TemplateView


from alawebdjango.core.forms import ContactForm


class IndexView(TemplateView):

    template_name = 'index.html'


index = IndexView.as_view()


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            body = render_to_string('contact_email.txt',
                                    form.cleaned_data)

            mail.send_mail('Confirmação de contato',
                           body,
                           'arbarros372@gmail.com',
                           ['arbarros372@gmail.com', form.cleaned_data['email']])

            messages.success(request, 'Contato realizado com sucesso!')

            return HttpResponseRedirect('/contato/')
        else:
            return render(request, 'contact.html',
                          {'form': form})

    else:
        context = {'form': ContactForm()}
        return render(request, 'contact.html', context)


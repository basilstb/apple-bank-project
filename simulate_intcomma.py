import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.template import Template, Context

t = Template("{% load humanize %}{{ amount|intcomma }}")
c = Context({'amount': '100.00'})
print(t.render(c))

c2 = Context({'amount': 100.00})
print(t.render(c2))

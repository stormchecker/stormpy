{#- Only list the members that belong to this module (see stormpy_autosummary.py) -#}
{%- set families = filter_api_members(fullname, template_families(fullname)) -%}
{%- set template_funcs = filter_api_members(fullname, template_functions(fullname)) -%}
{%- set attributes = filter_api_members(fullname, attributes) | reject('in', families + template_funcs) | list -%}
{%- set functions = (filter_api_members(fullname, functions) + template_funcs) | unique | sort | list -%}
{%- set classes = filter_api_members(fullname, classes) -%}
{%- set exceptions = filter_api_members(fullname, exceptions) -%}
{%- set classes = (classes + families) | unique | sort | list -%}
{{ fullname | escape | underline}}

.. automodule:: {{ fullname }}

   {% block attributes %}
   {%- if attributes %}
   .. rubric:: {{ _('Module Attributes') }}

   .. autosummary::
      :toctree:
   {% for item in attributes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {%- endblock %}

   {%- block functions %}
   {%- if functions %}
   .. rubric:: {{ _('Functions') }}

   .. autosummary::
      :toctree:
      :template: autosummary/apifunction.rst
   {% for item in functions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {%- endblock %}

   {%- block classes %}
   {%- if classes %}
   .. rubric:: {{ _('Classes') }}

   .. autosummary::
      :toctree:
      :template: autosummary/apiclass.rst
   {% for item in classes %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {%- endblock %}

   {%- block exceptions %}
   {%- if exceptions %}
   .. rubric:: {{ _('Exceptions') }}

   .. autosummary::
      :toctree:
      :template: autosummary/class.rst
   {% for item in exceptions %}
      {{ item }}
   {%- endfor %}
   {% endif %}
   {%- endblock %}

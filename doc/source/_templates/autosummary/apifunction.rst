{% set alias = canonical_api_alias(fullname) %}
{% if alias %}
{{ objname | escape | underline }}

.. currentmodule:: {{ module }}

.. py:function:: {{ objname }}
   :canonical: {{ alias }}

   Alias of :func:`{{ alias }}`. See its canonical page for parameters and examples.
{% elif objname in template_functions(module) %}
{% include 'autosummary/templatefunction.rst' %}
{% else %}
{% include 'autosummary/function.rst' %}
{% endif %}

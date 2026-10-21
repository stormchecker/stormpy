{% set alias = canonical_api_alias(fullname) %}
{% if alias %}
{{ objname | escape | underline }}

.. currentmodule:: {{ module }}

.. py:class:: {{ objname }}
   :canonical: {{ alias }}

   Alias of :class:`{{ alias }}`. See its canonical page for constructors and members.
{% elif objname in template_families(module) %}
{% include 'autosummary/templateclass.rst' %}
{% else %}
{% include 'autosummary/class.rst' %}
{% endif %}

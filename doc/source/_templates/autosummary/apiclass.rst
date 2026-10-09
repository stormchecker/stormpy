{% if objname in template_families(module) %}
{% include 'autosummary/templateclass.rst' %}
{% else %}
{% include 'autosummary/class.rst' %}
{% endif %}

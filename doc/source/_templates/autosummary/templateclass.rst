{% set info = template_info(fullname) %}
{{ objname | escape | underline }}

.. currentmodule:: {{ module }}

.. py:class:: {{ objname }}[{{ info.parameters }}]{{ info.constructors[0] if info.constructors else '' }}
{% for signature in info.constructors[1:] %}             {{ objname }}[{{ info.parameters }}]{{ signature }}
{% endfor %}

   {% for description, specializations in info.descriptions %}
   {% if info.descriptions | length > 1 %}For {{ specializations | join(', ') }}:{% endif %}
   {{ description | indent(3) }}
   {% endfor %}

   Template arguments:
   {% for name, kind in info.kinds %}
   * ``{{ name }}`` ({{ kind }})
   {%- endfor %}

   Available specializations:

   {% for args in info.instantiations %}
   * ``{{ objname }}[{{ args }}]``
   {%- endfor %}

   {% if info.deduction %}{{ info.deduction }}{% endif %}

   {% if info.constructor_variants %}
   Constructor signatures vary by specialization:
   {% for specialization, signature in info.constructor_variants %}
   * ``{{ specialization }}{{ signature }}``
   {%- endfor %}
   {% endif %}

Members
-------

{{ info.members }}

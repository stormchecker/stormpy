"""Sphinx-only support for documenting stormpy template families.

The runtime metadata provides the registrations; pybind docstrings supply the
member signatures. Never infer a generic annotation from a single concrete
signature: fixed types stay concrete; unresolved native signatures are omitted.
"""

import inspect
import re
import sys
from difflib import SequenceMatcher

import stormpy
from stormpy._template import TemplateClass


def argument_name(argument):
    """Use public exports rather than the defining module of a native type."""
    cls = argument if isinstance(argument, type) else type(argument)
    if cls.__module__ == "builtins":
        name = cls.__qualname__
    else:
        # Only these public namespaces own template argument types. In
        # particular, do not search loaded modules or expose private classes.
        namespaces = (stormpy, stormpy.storage)
        aliases = (f"{module.__name__}.{key}" for module in namespaces for key, value in vars(module).items() if not key.startswith("_") and value is cls)
        name = min(aliases, key=lambda s: (s.count("."), len(s), s), default=f"{cls.__module__}.{cls.__qualname__}")
    return name if isinstance(argument, type) else f"{name}.{argument.name}" if hasattr(argument, "name") else repr(argument)


def specialization_name(family, inst):
    return f"{family.__name__}[{', '.join(argument_name(arg) for arg in inst.arguments)}]"


def deduction_description(family):
    """Describe built-in constructor guides using their argument metadata."""
    metadata = family.metadata
    guide = metadata.deduction_guide
    if guide == "deduce_default":
        args = family._deduction_guide(family, (), {})
        return f"The default specialization is ``{family.__name__}[{', '.join(argument_name(arg) for arg in args)}]``."
    if guide not in ("deduce_from_object", "deduce_from_first_argument") or metadata.deduction_source is None:
        return None
    source = metadata.deduction_source
    position = ("first", "second", "third")[source.position] if 0 <= source.position < 3 else f"position {source.position} (zero-based)"
    description = f"The specialization can be inferred from the {position} positional constructor argument"
    if source.keywords:
        keywords = " or ".join(f"``{keyword}``" for keyword in source.keywords)
        description += f" (alternatively, the {keywords} keyword argument)"
    description += "."
    if guide == "deduce_from_object":
        try:
            args = family._deduction_guide(family, (), {})
        except TypeError:
            pass
        else:
            args = args if isinstance(args, tuple) else (args,)
            description += f" If none is supplied, ``{family.__name__}[{', '.join(argument_name(arg) for arg in args)}]`` is selected."
    return description


def member_doc(member):
    if isinstance(member, (staticmethod, classmethod)):
        member = member.__func__
    return inspect.getdoc(member) or ""


def _unresolved(line):
    """Native C++ or private implementation types are not public API types."""
    return "::" in line or bool(re.search(r"(?:^|\.)_[A-Za-z]", line))


def _split_arguments(text):
    """Split pybind arguments without splitting inside nested type arguments."""
    args, start, depth = [], 0, 0
    for i, char in enumerate(text):
        if char in "<([":
            depth += 1
        elif char in ">)]":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(text[start:i].strip())
            start = i + 1
    args.append(text[start:].strip())
    return args


def _public_signature(line):
    """Drop unresolvable annotations, not the overload they occur in."""
    match = re.fullmatch(r"(?P<prefix>(?:\d+\. )?\w+)\((?P<args>.*)\) -> (?P<return>.*)", line)
    if not match:
        return line
    args = _split_arguments(match["args"])
    for i, arg in enumerate(args):
        name, separator, annotation = arg.partition(": ")
        if separator:
            typ, default_separator, default = annotation.partition(" = ")
            if _unresolved(typ):
                args[i] = name + (" = " + default if default_separator else "")
    result = match["return"]
    signature = f"{match['prefix']}({', '.join(args)})" + (" -> " + result if not _unresolved(result) else "")
    # pybind prints object defaults using their process-specific memory address.
    return re.sub(r"(?<= = )<[^<>]* object at 0x[0-9a-fA-F]+>", "...", signature)


def signature_lines(doc, name):
    """Find pybind's leading single or numbered overload signatures."""
    lines = doc.splitlines()
    return [i for i, line in enumerate(lines) if re.fullmatch(rf"(?:\d+\. )?{re.escape(name)}\(.*\)(?: -> .*)?", line)]


def generic_docs(family, entries, families, name):
    """Generalize signature tokens only if they vary between specializations."""
    if name == "property":
        return entries
    result = []
    for inst, doc in entries:
        # Map each concrete spelling to (generic spelling, fixed spelling).
        replacements = {}
        for arg, param in zip(inst.arguments, family.metadata.parameters):
            if isinstance(arg, type):
                for spelling in (argument_name(arg), f"{arg.__module__}.{arg.__qualname__}"):
                    replacements[spelling] = (param.name, spelling)
        for other in families:
            for spec in other.metadata.instantiations:
                params = [
                    next((param.name for value, param in zip(inst.arguments, family.metadata.parameters) if value is arg), argument_name(arg))
                    for arg in spec.arguments
                ]
                replacements[spec.native_name] = (
                    f"{other.canonical_name}[{', '.join(params)}]",
                    f"{other.canonical_name}[{', '.join(argument_name(arg) for arg in spec.arguments)}]",
                )
        pattern = re.compile(r"(?<![\w.])(?:" + "|".join(re.escape(key) for key in sorted(replacements, key=len, reverse=True)) + r")(?![\w.])")
        lines = doc.splitlines()
        indexes = signature_lines(doc, name)
        for i in indexes:
            line = lines[i]
            # Only compare the corresponding signature, never unrelated prose.
            other_lines = [
                other_doc.splitlines()[i]
                for other_inst, other_doc in entries
                if other_inst != inst and len(other_doc.splitlines()) > i and i in signature_lines(other_doc, name)
            ]
            blocks = [SequenceMatcher(None, line, other, autojunk=False).get_matching_blocks() for other in other_lines]

            def replace(match):
                token = match.group()
                self_type = token == inst.native_name and re.search(r"\bself:\s*$", line[: match.start()])
                varies = any(not any(b.a <= match.start() and match.end() <= b.a + b.size for b in group) for group in blocks)
                generic, fixed = replacements[token]
                return generic if self_type or varies else fixed

            normalized = pattern.sub(replace, line)
            lines[i] = _public_signature(normalized)
        # pybind's overload heading is not useful without all signatures.
        lines = [line for line in lines if line != "Overloaded function." and line != f"{name}(*args, **kwargs)"]
        result.append((inst, "\n".join(lines).strip()))
    return result


def constructors(family, families):
    """Return common class signatures, or signatures grouped by specialization."""
    entries = [(inst, member_doc(inspect.getattr_static(inst.implementation, "__init__"))) for inst in family.metadata.instantiations]
    entries = [(inst, doc) for inst, doc in entries if doc != inspect.getdoc(object.__init__)]
    groups = {}
    for inst, doc in generic_docs(family, entries, families, "__init__"):
        signatures = []
        for i in signature_lines(doc, "__init__"):
            line = re.sub(r"^\d+\. ", "", doc.splitlines()[i])
            args = _split_arguments(line[line.index("(") + 1 : line.rindex(")")])
            if args and args[0].split(":", 1)[0] == "self":
                args.pop(0)
            signatures.append(f"({', '.join(args)})")
        if signatures:
            groups.setdefault(tuple(signatures), []).append(inst)
    if len(groups) == 1 and len(next(iter(groups.values()))) == len(family.metadata.instantiations):
        return next(iter(groups)), []
    variants = []
    for signatures, insts in groups.items():
        for inst in insts:
            for signature in signatures:
                concrete = signature
                for param, arg in zip(family.metadata.parameters, inst.arguments):
                    concrete = re.sub(rf"\b{re.escape(param.name)}\b", argument_name(arg), concrete)
                variants.append((specialization_name(family, inst), concrete))
    return (), variants


def render_members(family, families):
    """Render the union of specialization members, marking conditional ones."""
    instantiations = family.metadata.instantiations
    names = sorted({name for inst in instantiations for name in dir(inst.implementation) if not name.startswith("_")})
    lines = []
    for name in names:
        entries = []
        descriptor = None
        for inst in instantiations:
            if not hasattr(inst.implementation, name):
                continue
            member = inspect.getattr_static(inst.implementation, name)
            if member is getattr(object, name, None) or (name == "__init__" and member_doc(member) == inspect.getdoc(object.__init__)):
                continue
            if descriptor is None:
                descriptor = member
            entries.append((inst, member_doc(member)))
        if not entries:
            continue
        kind = "property" if isinstance(descriptor, property) else "method" if callable(descriptor) or isinstance(descriptor, classmethod) else "attribute"
        variants = {}
        for inst, doc in generic_docs(family, entries, families, "property" if kind == "property" else name):
            variants.setdefault(doc, []).append(inst)
        signatures = [name]
        if kind == "method" and len(variants) == 1:
            first_doc = next(iter(variants))
            doc_lines = first_doc.splitlines()
            indexes = signature_lines(first_doc, name)
            if indexes and all(not _unresolved(doc_lines[i]) for i in indexes):
                signatures = [re.sub(r"^\d+\. ", "", doc_lines[i]) for i in indexes]
                variants = {"\n".join(line for i, line in enumerate(doc_lines) if i not in indexes).strip(): next(iter(variants.values()))}
        lines.append(f".. py:{kind}:: {family.__name__}.{signatures[0]}")
        for signature in signatures[1:]:
            lines.append(f"               {family.__name__}.{signature}")
        if isinstance(descriptor, staticmethod):
            lines.append("   :staticmethod:")
        elif isinstance(descriptor, classmethod):
            lines.append("   :classmethod:")
        lines.append("")
        if len(entries) != len(instantiations):
            available = ", ".join(f"``{specialization_name(family, inst)}``" for inst, _ in entries)
            lines.extend([f"   Available only for: {available}.", ""])
        for doc, instances in variants.items():
            if len(variants) > 1:
                labels = ", ".join(f"``{specialization_name(family, inst)}``" for inst in instances)
                lines.extend([f"   For {labels}:", ""])
            for paragraph in doc.split("\n\n"):
                if not paragraph.strip():
                    continue
                if " -> " in paragraph or re.match(rf"^(?:\d+\. )?{re.escape(name)}\(", paragraph):
                    lines.extend(["   .. code-block:: text", ""])
                    lines.extend("      " + line for line in paragraph.splitlines())
                else:
                    lines.extend("   " + line for line in paragraph.splitlines())
                lines.append("")
    return "\n".join(lines)


def template_families(module):
    """Public families owned by this module, excluding re-exports."""
    return sorted(name for name, obj in vars(sys.modules[module]).items() if isinstance(obj, TemplateClass) and obj.canonical_name == f"{module}.{name}")


def template_info(fullname):
    module, _, name = fullname.rpartition(".")
    family = getattr(sys.modules[module], name)
    metadata = family.metadata
    descriptions = {}
    for inst in metadata.instantiations:
        description = inspect.getdoc(inst.implementation)
        if description:
            descriptions.setdefault(description, []).append(", ".join(argument_name(arg) for arg in inst.arguments))
    families = {
        id(obj): obj
        for module_name, module_obj in list(sys.modules.items())
        if module_name.startswith("stormpy") and module_obj is not None
        for obj in vars(module_obj).values()
        if isinstance(obj, TemplateClass)
    }
    common_constructors, constructor_variants = constructors(family, families.values())
    return {
        "constructors": common_constructors,
        "constructor_variants": constructor_variants,
        "descriptions": list(descriptions.items()),
        "deduction": deduction_description(family),
        "parameters": ", ".join(p.name for p in metadata.parameters),
        "kinds": [(p.name, p.kind) for p in metadata.parameters],
        "instantiations": [", ".join(argument_name(arg) for arg in inst.arguments) for inst in metadata.instantiations],
        "members": render_members(family, families.values()),
    }


def setup(app):
    """Register the project-local Sphinx extension."""
    return {"parallel_read_safe": True, "parallel_write_safe": True}

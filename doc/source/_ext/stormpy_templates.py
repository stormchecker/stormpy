"""Sphinx-only support for documenting stormpy template families.

The runtime metadata provides the registrations; pybind docstrings supply the
member signatures. Never infer a generic annotation from a single concrete
signature: fixed types stay concrete; unresolved native signatures are omitted.
"""

import builtins
import inspect
import re
import sys
from difflib import SequenceMatcher

import stormpy
from stormpy._template import _TemplateClass, _TemplateFunction
from stormpy_autosummary import is_developer_api_page, public_api_modules


def argument_name(argument, namespaces=None):
    """Use public exports rather than the defining module of a native type."""
    cls = argument if isinstance(argument, type) else type(argument)
    if cls.__module__ == "builtins":
        name = cls.__qualname__
    else:
        # Only these public namespaces own template argument types. In
        # particular, do not search loaded modules or expose private classes.
        if namespaces is None:
            namespaces = public_api_modules()
        aliases = (f"{module.__name__}.{key}" for module in namespaces for key in module.__all__ if getattr(module, key) is cls)
        name = min(aliases, key=lambda s: (s.rpartition(".")[0] == "stormpy", s.count("."), len(s), s), default=f"{cls.__module__}.{cls.__qualname__}")
    return name if isinstance(argument, type) else f"{name}.{argument.name}" if hasattr(argument, "name") else repr(argument)


def specialization_name(family, inst):
    return f"{family.__name__}[{', '.join(argument_name(arg) for arg in inst.arguments)}]"


def deduction_description(family):
    """Describe built-in deduction guides using their argument metadata."""
    metadata = family.metadata
    guide = metadata.deduction_guide
    if guide == "deduce_default":
        args = family._deduction_guide(family, (), {})
        return f"The default specialization is ``{family.__name__}[{', '.join(argument_name(arg) for arg in args)}]``."
    if guide not in ("deduce_from_object", "deduce_from_first_argument") or metadata.deduction_source is None:
        return None
    source = metadata.deduction_source
    position = ("first", "second", "third")[source.position] if 0 <= source.position < 3 else f"position {source.position} (zero-based)"
    context = "function" if isinstance(family, _TemplateFunction) else "constructor"
    description = f"The specialization can be inferred from the {position} positional {context} argument"
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
    args, start, depth, quote, escaped = [], 0, 0, None, False
    for i, char in enumerate(text):
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char in "<([":
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
    # Stabilize defaults even when a function has no return annotation.
    line = re.sub(r"<[^<>]* object(?: at 0x[0-9a-fA-F]+)?>", "...", line)
    match = re.fullmatch(r"(?P<prefix>(?:\d+\. )?\w+)\((?P<args>.*)\)(?: -> (?P<return>.*))?", line)
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
    return f"{match['prefix']}({', '.join(args)})" + (" -> " + result if result and not _unresolved(result) else "")


def signature_lines(doc, name):
    """Find pybind's leading single or numbered overload signatures."""
    lines = doc.splitlines()
    return [i for i, line in enumerate(lines) if re.fullmatch(rf"(?:\d+\. )?{re.escape(name)}\(.*\)(?: -> .*)?", line)]


def generic_docs(family, entries, families, name):
    """Generalize signature tokens only if they vary between specializations."""
    if name == "property":
        return entries
    aliases = _public_type_names()
    result = []
    for inst, doc in entries:
        # Map each concrete spelling to (generic spelling, fixed spelling).
        replacements = {native: (public, public) for native, public in aliases.items()}
        for arg, param in zip(inst.arguments, family.metadata.parameters):
            if isinstance(arg, type):
                for spelling in (argument_name(arg), f"{arg.__module__}.{arg.__qualname__}"):
                    replacements[spelling] = (param.name, spelling)
        # Published families share their native classes with developer families.
        # Apply public spellings last so raw bindings never hide a public alias.
        for other in sorted(families, key=lambda obj: (".developer" not in obj.canonical_name, obj.canonical_name)):
            if isinstance(other, _TemplateFunction):
                continue
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

            normalized = pattern.sub(replace, line) if replacements else line
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


def constructor_descriptions(family, families):
    """Include __init__ prose in the class body, like autoclass_content='both'."""
    entries = [(inst, member_doc(inspect.getattr_static(inst.implementation, "__init__"))) for inst in family.metadata.instantiations]
    entries = [(inst, doc) for inst, doc in entries if doc != inspect.getdoc(object.__init__)]
    descriptions = {}
    for inst, doc in generic_docs(family, entries, families, "__init__"):
        indexes = set(signature_lines(doc, "__init__"))
        description = "\n".join(line for i, line in enumerate(doc.splitlines()) if i not in indexes).strip()
        if description:
            descriptions.setdefault(description, []).append(specialization_name(family, inst))
    return [
        (description, specializations if len(specializations) != len(family.metadata.instantiations) else [])
        for description, specializations in descriptions.items()
    ]


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
            doc = member_doc(member)
            implementation = member.__func__ if isinstance(member, (staticmethod, classmethod)) else member
            if callable(implementation) and not signature_lines(doc, name):
                try:
                    signature = _python_function_signature(implementation, name)
                except (TypeError, ValueError):
                    pass
                else:
                    doc = f"{signature}\n\n{doc}".strip()
            entries.append((inst, doc))
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
                if re.match(rf"^(?:\d+\. )?{re.escape(name)}\(", paragraph):
                    lines.extend(["   .. code-block:: text", ""])
                    lines.extend("      " + line for line in paragraph.splitlines())
                else:
                    lines.extend("   " + line for line in paragraph.splitlines())
                lines.append("")
    return "\n".join(lines)


def template_families(module):
    """Public families owned by this module, excluding re-exports."""
    return sorted(
        name
        for name, obj in vars(sys.modules[module]).items()
        if isinstance(obj, _TemplateClass) and not isinstance(obj, _TemplateFunction) and obj.canonical_name == f"{module}.{name}"
    )


def template_functions(module):
    """Template functions owned by this module, excluding re-exports."""
    return sorted(name for name, obj in vars(sys.modules[module]).items() if isinstance(obj, _TemplateFunction) and obj.canonical_name == f"{module}.{name}")


def _loaded_template_classes():
    return tuple(
        {
            id(obj): obj
            for module_name, module_obj in list(sys.modules.items())
            if module_name.startswith("stormpy") and module_obj is not None
            for obj in vars(module_obj).values()
            if isinstance(obj, _TemplateClass) and not isinstance(obj, _TemplateFunction)
        }.values()
    )


def _public_type_names():
    """Map native non-template types to their public or developer exports."""
    aliases, exports = {}, {}
    namespaces = public_api_modules()
    for module_name, module in list(sys.modules.items()):
        if not module_name.startswith("stormpy") or module is None or any(part.startswith("_") for part in module_name.split(".")):
            continue
        for name, obj in vars(module).items():
            if name.startswith("_") or not isinstance(obj, type) or not obj.__module__.startswith("stormpy"):
                continue
            if hasattr(module, "__all__") and name not in module.__all__:
                continue
            native_name = f"{obj.__module__}.{obj.__qualname__}"
            public_name = argument_name(obj, namespaces)
            alias = public_name if public_name != native_name else f"{module_name}.{name}"
            aliases.setdefault(native_name, []).append(alias)
            exports[f"{module_name}.{name}"] = native_name
    preferred = {native: min(names, key=lambda name: (".developer" in name, name.count("."), len(name), name)) for native, names in aliases.items()}
    return {**preferred, **{export: preferred[native] for export, native in exports.items()}}


def _function_annotation(annotation, implementation):
    """Resolve Python forward annotations in the original function's namespace."""
    if isinstance(annotation, _TemplateClass):
        return annotation.canonical_name
    text = annotation if isinstance(annotation, str) else inspect.formatannotation(annotation)
    namespace = getattr(inspect.unwrap(implementation), "__globals__", {})

    def resolve(match):
        name, *attributes = match.group().split(".")
        obj = namespace.get(name, getattr(builtins, name, None))
        for attribute in attributes:
            obj = getattr(obj, attribute, None)
        if isinstance(obj, _TemplateClass):
            return obj.canonical_name
        return argument_name(obj) if isinstance(obj, type) else match.group()

    return re.sub(r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*", resolve, text)


def _python_function_signature(implementation, name):
    signature = inspect.signature(implementation)
    parameters = list(signature.parameters.values())
    args = []
    for i, parameter in enumerate(parameters):
        if parameter.kind == inspect.Parameter.KEYWORD_ONLY and (
            i == 0 or parameters[i - 1].kind not in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.VAR_POSITIONAL)
        ):
            args.append("*")
        arg = str(parameter.replace(annotation=inspect.Parameter.empty, default=inspect.Parameter.empty))
        if parameter.annotation is not inspect.Parameter.empty:
            arg += ": " + _function_annotation(parameter.annotation, implementation)
        if parameter.default is not inspect.Parameter.empty:
            default = parameter.default
            default_text = argument_name(default) if isinstance(default, type) or hasattr(default, "name") else repr(default)
            arg += " = " + default_text
        args.append(arg)
        if parameter.kind == inspect.Parameter.POSITIONAL_ONLY and (i + 1 == len(parameters) or parameters[i + 1].kind != inspect.Parameter.POSITIONAL_ONLY):
            args.append("/")
    result = f"{name}({', '.join(args)})"
    if signature.return_annotation is not inspect.Signature.empty:
        result += " -> " + _function_annotation(signature.return_annotation, implementation)
    return result


def template_function_info(fullname):
    module, _, name = fullname.rpartition(".")
    family = getattr(sys.modules[module], name)
    aliases = _public_type_names()
    alias_pattern = re.compile(r"(?<![\w.])(?:" + "|".join(re.escape(key) for key in sorted(aliases, key=len, reverse=True)) + r")(?![\w.])")
    entries = []
    for inst in family.metadata.instantiations:
        doc = member_doc(inst.implementation)
        native_name = inst.implementation.__name__
        lines = doc.splitlines()
        for i in signature_lines(doc, native_name):
            lines[i] = re.sub(rf"^((?:\d+\. )?){re.escape(native_name)}\(", rf"\g<1>{name}(", lines[i])
        doc = "\n".join(lines)
        if not signature_lines(doc, name):
            try:
                signature = _python_function_signature(inst.implementation, name)
            except (TypeError, ValueError):
                pass
            else:
                doc = f"{signature}\n\n{doc}"
        lines = doc.splitlines()
        for i in signature_lines(doc, name):
            if aliases:
                lines[i] = alias_pattern.sub(lambda match: aliases[match.group()], lines[i])
            lines[i] = re.sub(r"<[^<>]* object(?: at 0x[0-9a-fA-F]+)?>", "...", lines[i])
        doc = "\n".join(lines)
        entries.append((inst, doc))
    overloads, signatures = {}, []
    for inst, doc in generic_docs(family, entries, _loaded_template_classes(), name):
        lines = doc.splitlines()
        indexes = signature_lines(doc, name)
        current_signatures = []
        for position, start in enumerate(indexes):
            signature = re.sub(r"^\d+\. ", "", lines[start])[len(name) :]
            end = indexes[position + 1] if position + 1 < len(indexes) else len(lines)
            description = "\n".join(lines[start + 1 : end]).strip()
            specializations = overloads.setdefault((signature, description), [])
            specialization = specialization_name(family, inst)
            if specialization not in specializations:
                specializations.append(specialization)
            current_signatures.append(signature)
        if not indexes:
            overloads.setdefault(("", doc), []).append(specialization_name(family, inst))
        signatures.append(tuple(dict.fromkeys(current_signatures)))
    common = signatures[0] if signatures and all(group == signatures[0] for group in signatures) else ()
    return {
        "parameters": ", ".join(p.name for p in family.metadata.parameters),
        "kinds": [(p.name, p.kind) for p in family.metadata.parameters],
        "signatures": common,
        "deduction": deduction_description(family),
        "instantiations": [specialization_name(family, inst) for inst in family.metadata.instantiations],
        "overloads": [
            {
                "signature": signature,
                "description": description,
                "specializations": specializations if len(specializations) != len(family.metadata.instantiations) else [],
            }
            for (signature, description), specializations in overloads.items()
        ],
    }


def template_info(fullname):
    module, _, name = fullname.rpartition(".")
    family = getattr(sys.modules[module], name)
    metadata = family.metadata
    descriptions = {}
    for inst in metadata.instantiations:
        description = inspect.getdoc(inst.implementation)
        if description:
            descriptions.setdefault(description, []).append(", ".join(argument_name(arg) for arg in inst.arguments))
    families = _loaded_template_classes()
    common_constructors, constructor_variants = constructors(family, families)
    return {
        "constructors": common_constructors,
        "constructor_variants": constructor_variants,
        "constructor_descriptions": constructor_descriptions(family, families),
        "descriptions": list(descriptions.items()),
        "deduction": deduction_description(family),
        "parameters": ", ".join(p.name for p in metadata.parameters),
        "kinds": [(p.name, p.kind) for p in metadata.parameters],
        "instantiations": [", ".join(argument_name(arg) for arg in inst.arguments) for inst in metadata.instantiations],
        "members": render_members(family, families),
    }


def template_docstring(app, what, name, obj, options, lines):
    """Use native family descriptions, not the template wrapper's docstring."""
    if not isinstance(obj, _TemplateClass):
        return
    if isinstance(obj, _TemplateFunction):
        descriptions = dict.fromkeys(overload["description"] for overload in template_function_info(obj.canonical_name)["overloads"] if overload["description"])
    else:
        descriptions = dict.fromkeys(description for inst in obj.metadata.instantiations if (description := inspect.getdoc(inst.implementation)))
    lines[:] = "\n\n".join(descriptions).splitlines()


def _normalize_public_signature(line):
    """Publish known native types before omitting unresolved annotations."""
    aliases = _public_type_names()
    for family in sorted(_loaded_template_classes(), key=lambda obj: (".developer" not in obj.canonical_name, obj.canonical_name)):
        for inst in family.metadata.instantiations:
            aliases[inst.native_name] = f"{family.canonical_name}[{', '.join(argument_name(arg) for arg in inst.arguments)}]"
    if aliases:
        pattern = re.compile(r"(?<![\w.])(?:" + "|".join(re.escape(key) for key in sorted(aliases, key=len, reverse=True)) + r")(?![\w.])")
        line = pattern.sub(lambda match: aliases[match.group()], line)
    return _public_signature(line)


def _native_overloads(what, obj):
    """Read pybind's numbered signatures, excluding its placeholder signature."""
    if isinstance(obj, _TemplateClass) or what not in {"class", "exception", "method", "function"}:
        return []
    constructor = what in {"class", "exception"}
    native_name = "__init__" if constructor else getattr(obj, "__name__", "")
    doc = member_doc(obj.__init__ if constructor else obj)
    if "Overloaded function." not in doc or not native_name:
        return []
    lines = doc.splitlines()
    return [lines[i] for i in signature_lines(doc, native_name) if re.match(r"\d+\. ", lines[i])]


def public_signature(app, what, name, obj, options, signature, return_annotation):
    """Render native overloads as signatures, normalizing public type names."""
    developer_page = is_developer_api_page(app.env.docname)
    overloads = _native_overloads(what, obj)
    if overloads:
        signatures = []
        for line in overloads:
            if not developer_page:
                line = _normalize_public_signature(line)
            match = re.fullmatch(r"\d+\. \w+\((.*)\)(?: -> (.*))?", line)
            arguments = _split_arguments(match[1])
            if what in {"class", "exception", "method"} and arguments[0].split(":", 1)[0] in {"self", "cls"}:
                arguments.pop(0)
            result = f"({', '.join(arguments)})"
            if match[2] and what not in {"class", "exception"}:
                result += f" -> {match[2]}"
            signatures.append(result)
        # Sphinx 9's new autodoc renderer prefixes only the first line of an
        # event-supplied signature; the legacy renderer prefixes every line.
        if not getattr(app.config, "autodoc_use_legacy_class_based", True):
            module = max((module for module in sys.modules if name.startswith(module + ".")), key=len, default="")
            relative_name = name[len(module) + 1 :] if module else name
            signatures[1:] = [relative_name + sig for sig in signatures[1:]]
        return "\n".join(signatures), None
    if not signature or developer_page:
        return
    line = "signature" + signature + (f" -> {return_annotation}" if return_annotation else "")
    normalized = _normalize_public_signature(line)
    match = re.fullmatch(r"signature(\(.*\))(?: -> (.*))?", normalized)
    return match.groups() if match else None


def public_docstring(app, what, name, obj, options, lines):
    """Keep overload prose in the body; signatures are rendered separately."""
    overloads = _native_overloads(what, obj)
    if overloads:
        # Sphinx may already have consumed the leading *args/**kwargs line.
        native_name = overloads[0].split("(", 1)[0].split(". ", 1)[1]
        indexes = set(signature_lines("\n".join(lines), native_name))
        lines[:] = [line for i, line in enumerate(lines) if i not in indexes and line != "Overloaded function."]
    if isinstance(obj, _TemplateClass) or is_developer_api_page(app.env.docname):
        return
    names = {name.rsplit(".", 1)[-1], getattr(obj, "__name__", "")}
    if what == "class":
        names.add("__init__")
    indexes = {i for native_name in names if native_name for i in signature_lines("\n".join(lines), native_name)}
    for i in indexes:
        lines[i] = _normalize_public_signature(lines[i])


def public_type_references(app, doctree):
    """Resolve native annotations through their published public API aliases.

    Apply this after autodoc parses signatures so constructors, overloads,
    return types and explicit type roles all use the same mapping.
    """
    from docutils import nodes
    from sphinx.addnodes import desc_signature, pending_xref

    aliases = _public_type_names()
    if is_developer_api_page(app.env.docname):
        # Public re-exports have no separate developer page. Keep other
        # developer targets unchanged, including backend-specific formulas.
        aliases = {native: public for native, public in aliases.items() if "developer" not in public.split(".")}
    for reference in doctree.findall(pending_xref):
        if reference.get("refdomain") != "py":
            continue
        target = reference.get("reftarget")
        public = aliases.get(target, target)
        if public == target:
            continue
        reference["reftarget"] = public
        if not reference.get("refexplicit"):
            for text in list(reference.findall(nodes.Text)):
                if str(text) == target:
                    text.parent.replace(text, nodes.Text(public))
    # Sphinx retains unparseable C++ annotations as plain signature text.
    # Normalize their type spellings too, even when it cannot create a link.
    aliases = {native: public for native, public in aliases.items() if native != public}
    if aliases:
        pattern = re.compile(r"(?<![\w.])(?:" + "|".join(re.escape(key) for key in sorted(aliases, key=len, reverse=True)) + r")(?![\w.])")
        for signature in doctree.findall(desc_signature):
            for text in list(signature.findall(nodes.Text)):
                public = pattern.sub(lambda match: aliases[match.group()], str(text))
                if public != str(text):
                    text.parent.replace(text, nodes.Text(public))


def setup(app):
    """Register the project-local Sphinx extension."""
    app.setup_extension("sphinx.ext.autodoc")
    app.connect("autodoc-process-docstring", template_docstring)
    app.connect("autodoc-process-docstring", public_docstring)
    app.connect("autodoc-process-signature", public_signature)
    app.connect("doctree-read", public_type_references)
    return {"parallel_read_safe": True, "parallel_write_safe": True}

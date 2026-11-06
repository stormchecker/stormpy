"""Developer tasks for stormpy.

Run ``nox -l`` to list all sessions and ``nox -s <session>`` to run one.

Sessions that need stormpy itself run in the current Python environment (``venv_backend="none"``),
because installing stormpy into a fresh virtual environment requires a full C++ build.
Install the development dependencies beforehand with ``pip install -v .[dev]``.
"""

import sys
from pathlib import Path

import nox

ROOT = Path(__file__).parent
DOC_DIR = ROOT / "doc"

# Do not run anything by default, only list the available sessions
nox.options.sessions = []


def doc_pages() -> list[str]:
    """Return the documentation pages written in MyST Markdown that are paired with Jupyter notebooks via jupytext."""
    pages = []
    for path in sorted(DOC_DIR.rglob("*.md")):
        with path.open(encoding="utf-8") as f:
            if any(line.startswith("jupytext:") for line in f):
                pages.append(str(path.relative_to(ROOT)))
    return pages


@nox.session(venv_backend="none")
def format(session: nox.Session) -> None:
    """Format all C++ files, all Python files and the Python code in the documentation."""
    session.run("bash", "resources/scripts/auto-format.sh", external=True)
    session.run(sys.executable, "-m", "black", ".")
    session.run("jupytext", "--sync", "--pipe", f"{sys.executable} -m black {{}}", *doc_pages())


@nox.session(venv_backend="none")
def check_format_doc(session: nox.Session) -> None:
    """Check that all Python code in the documentation is formatted with black."""
    session.run("jupytext", "--pipe", f"{sys.executable} -m black --check --diff {{}}", *doc_pages())


@nox.session(venv_backend="none")
def check_doc(session: nox.Session) -> None:
    """Perform roundtrip check for the documentation and execute all code cells."""
    pages = doc_pages()
    session.run("jupytext", "--to", "ipynb", "--test-strict", *pages)
    tmp = Path(session.create_tmp())
    for page in pages:
        script = tmp / (Path(page).stem + ".py")
        session.run("jupytext", "--quiet", "--to", "py:percent", "--output", str(script), page)
        session.log(f"Executing {page}")
        session.run(sys.executable, str(script))


@nox.session(venv_backend="none")
def tests(session: nox.Session) -> None:
    """Run all tests."""
    session.run(sys.executable, "-m", "pytest", *session.posargs)


@nox.session(venv_backend="none")
def check(session: nox.Session) -> None:
    """Perform all checks: documentation formatting, documentation execution and tests."""
    session.notify("check_format_doc")
    session.notify("check_doc")
    session.notify("tests", posargs=session.posargs)


@nox.session(venv_backend="none")
def notebooks(session: nox.Session) -> None:
    """Create Jupyter notebooks from the MyST files in the documentation."""
    session.run("jupytext", "--to", "notebook", *doc_pages())


@nox.session(venv_backend="none")
def clean_notebooks(session: nox.Session) -> None:
    """Remove all generated Jupyter notebooks."""
    for notebook in DOC_DIR.rglob("*.ipynb"):
        notebook.unlink()


@nox.session(venv_backend="none")
def doc(session: nox.Session) -> None:
    """Build the documentation."""
    session.run(sys.executable, "-m", "sphinx", "-M", "html", "doc/source", "doc/build", *session.posargs)

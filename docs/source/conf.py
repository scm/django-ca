# This file is part of django-ca (https://github.com/mathiasertl/django-ca).
#
# django-ca is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# django-ca is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along with django-ca. If not, see
# <http://www.gnu.org/licenses/>.

"""Sphinx configuration."""

import os
import sys
from typing import Any, Dict, List

import sphinx_rtd_theme
from sphinx.addnodes import document, pending_xref
from sphinx.application import Sphinx

try:
    from sphinxcontrib import spelling
except ImportError:
    spelling = None


sys.path.insert(0, os.path.dirname(__file__))

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('.'))

_BASE_DIR = os.path.dirname(os.path.abspath(__name__))
_ROOT_DIR = os.path.dirname(os.path.dirname(_BASE_DIR))
_SRC_DIR = os.path.join(_ROOT_DIR, "ca")
_FIXTURES = os.path.join(_SRC_DIR, "django_ca", "tests", "fixtures")
sys.path.insert(0, _SRC_DIR)
sys.path.insert(0, _ROOT_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ca.settings")

import django  # NOQA: E402
from django.conf import settings  # NOQA: E402

from devscripts import config  # NOQA: E402
from devscripts.versions import get_last_version  # NOQA: E402

settings.configure(
    SECRET_KEY="dummy",
    BASE_DIR=_SRC_DIR,
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django_ca",
    ],
    FIXTURES_DIR=_FIXTURES,
)
django.setup()


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinx.ext.autosummary",
    # Enable Celery task docs: https://docs.celeryproject.org/en/latest/userguide/sphinx.html
    "celery.contrib.sphinx",
    "numpydoc",
    "sphinx_inline_tabs",
    "sphinx_jinja",
    "sphinxcontrib.openapi",
    "sphinxcontrib.jquery",
    "django_ca_sphinx",
]

if spelling is not None:
    from django_ca_sphinx.spelling import URIFilter, MagicWordsFilter, TypeHintsFilter  # isort:skip

    extensions.append("sphinxcontrib.spelling")
    spelling_exclude_patterns = ["**/generated/*.rst"]
    spelling_filters = [URIFilter, MagicWordsFilter, TypeHintsFilter]
    # spelling_show_suggestions = True

numpydoc_show_class_members = False
autodoc_inherit_docstrings = False
manpages_url = "https://manpages.debian.org/{page}.{section}"


# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "django-ca"
copyright = "2016 - 2023, Mathias Ertl"
author = "Mathias Ertl"

import django_ca  # NOQA: E402

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
release = version = django_ca.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns: List[str] = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = "alabaster"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'h', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'r', 'sv', 'tr'
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = "django-cadoc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements: Dict[Any, Any] = {}  # Note: we don't use this at all

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, "django-ca.tex", "django-ca Documentation", "Mathias Ertl", "manual"),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "django-ca", "django-ca Documentation", [author], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "django-ca",
        "django-ca Documentation",
        author,
        "django-ca",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

autodoc_mock_imports = [
    "OpenSSL",
    "acme",
    "freezegun",
    "josepy",
    "pyvirtualdisplay",
    "selenium",
]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "cg": ("https://cryptography.io/en/stable/", None),
    "django": (
        "https://docs.djangoproject.com/en/%s/" % config.DJANGO[-1],
        "https://docs.djangoproject.com/en/%s/_objects/" % config.DJANGO[-1],
    ),
    "acme": ("https://acme-python.readthedocs.io/en/stable/", None),
    "josepy": ("https://josepy.readthedocs.io/en/stable/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

rst_epilog = f"""
.. |minimum-python| replace:: {config.PYTHON_RELEASES[0]}
.. |Extension| replace:: :py:class:`~cg:cryptography.x509.Extension`
.. |ExtensionType| replace:: :py:class:`~cg:cryptography.x509.ExtensionType`
.. |Name| replace:: :py:class:`~cg:cryptography.x509.Name`
.. |RelativeDistinguishedName| replace:: :py:class:`~cg:cryptography.x509.RelativeDistinguishedName`
.. _RFC 5280: https://datatracker.ietf.org/doc/html/rfc5280
"""

html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# reusable variables for contexts below
_ca_default_hostname = "ca.example.com"
_tls_cert_root = "/etc/certs/"

# Jinja template contexts
jinja_contexts = {
    "full-requirements-from-source": {
        "base": "Python",
        "how:": "installed via APT",
    },
    "full-requirements-in-docker": {
        "base": "Docker",
        "how:": "each in a separate Docker container",
    },
    "manage-as-py": {"manage": "python manage.py"},
    "manage-in-docker-compose": {
        "manage": "docker compose exec backend manage",
        "shared": True,
        "console_include": "include/quickstart_with_docker_compose/setup-cas.yaml",
        "context": "quickstart-with-docker-compose",
        "path": "~/ca/",
    },
    "manage-from-source": {"manage": "django-ca"},
    "requirements-as-py": {},
    "requirements-in-docker": {},
    "requirements-in-docker-compose": {},
    "requirements-from-source": {},
    "guide-source-where-to-go": {
        "ca_default_hostname": _ca_default_hostname,
        "ca_url_path": "",
        "shared": False,
        "guide": "from-source",
        "manage": "django-ca",
        "user": "root",
    },
    "quickstart-with-docker": {
        "backend_host": "backend",
        "ca_default_hostname": _ca_default_hostname,
        "docker_tag": "mathiasertl/django-ca",
        "frontend_host": "frontend",
        "network": "django-ca",
        "nginx_host": "nginx",
        "postgres_host": "postgres",
        "postgres_password": "password",
        "redis_host": "redis",
        "secret_key": "changeme",
    },
    "quickstart-with-docker-compose": {
        "ca_default_hostname": _ca_default_hostname,
        "ca_url_path": "",
        "postgres_host": "db",
        "postgres_password": "mysecretpassword",
        "privkey_path": f"{_tls_cert_root}live/{_ca_default_hostname}/privkey.pem",
        "pubkey_path": f"{_tls_cert_root}live/{_ca_default_hostname}/fullchain.pem",
        "dhparam_name": "dhparam.pem",
        "certbot_root": "/etc/letsencrypt/",
        "tls_cert_root": _tls_cert_root,
        "validation": False,  # True when run as automatic validation
        "sphinx": True,  # Yes, we render for Sphinx documentation
    },
    "quickstart-from-source": {
        "ca_default_hostname": _ca_default_hostname,
        "ca_url_path": "",
    },
    "guide-as-app-where-to-go": {
        "ca_default_hostname": _ca_default_hostname,
        "ca_url_path": "ca/",
        "shared": False,
        "guide": "as-app",
        "manage": "manage.py",
    },
    "guide-docker-compose-where-to-go": {
        "ca_default_hostname": _ca_default_hostname,
        "ca_url_path": "",
        "shared": True,
        "guide": "with-docker-compose",
        "manage": "docker compose exec backend manage",
        "path": "~/ca/",
    },
}
jinja_globals = {"version": version, "last_version": str(get_last_version())}
jinja_filters = {
    "basename": os.path.basename,
}

qualname_overrides = {
    "mappingproxy": "python:types.MappingProxyType",
    "MappingProxyType": "python:types.MappingProxyType",
    "django.core.files.storage.base.Storage": "django.core.files.storage.FileSystemStorage",
    "cryptography.hazmat.bindings._rust.ObjectIdentifier": "cg:cryptography.x509.ObjectIdentifier",
    "cryptography.x509.extensions.ExtendedKeyUsage": "cg:cryptography.x509.ExtendedKeyUsage",
    # x509.GeneralName fixes a build error with the typehints in constants.GENERAL_NAME_TYPES. The error seems
    # to disappear once the typehint is unquoted, which is possible with Python 3.9. It's likely that this
    # override can be removed once support for Python 3.8 is dropped.
    "x509.GeneralName": "cg:cryptography.x509.GeneralName",  # pragma: only py<3.9
    # Django documents HttpRequest and HttpResponse under re-exported path names:
    "django.http.request.HttpRequest": "django:django.http.HttpRequest",
    "django.http.response.HttpResponse": "django:django.http.HttpResponse",
}

# Ignore (not so important) classes where the documented name does not match the documented name.
nitpick_ignore = [
    # When literals are used in typehints, Sphinx does not find the reference to the literal and errors with:
    #
    #   docstring of django_ca.constants....:1:py:class reference target not found: <name-of-literal>
    #
    # Note that the above message does *not* contain the full class path, just the variable name and also
    # claims a type of "class", when "attr" would be correct. The full path can be "fixed" with
    # `qualname_overrides` above, but that does not fix the error. Setting "reftype" to "attr" in
    # `resolve_canonical_names()` below also works, but you still get the same error.
    ("py:class", "OtherNames"),
    ("py:class", "KeyUsages"),
    ("py:class", "GeneralNames"),
    # asn1crypto is really used only for OtherNames, so we do not link it
    ("py:class", "asn1crypto.core.Primitive"),
    # Pydantic root model signature does not currently work
    ("py:class", "RootModelRootType"),
]


# NOINSPECTION NOTE: app is passed by the caller, but we don't need it.
# noinspection PyUnusedLocal
def resolve_canonical_names(app: Sphinx, doctree: document) -> None:
    """Resolve canonical names of types to names that resolve in intersphinx inventories.

    Projects often document functions/classes under a name that is re-exported. For example, cryptography
    documents "Certificate" under ``cryptography.x509.Certificate``, but it's actually implemented in
    ``cryptography.x509.base.Certificate`` (and re-exported in x509.py).

    When Sphinx encounters typehints it tries to create links to the types, looking up types from external
    projects using ``sphinx.ext.intersphinx``. The lookup for such re-exported types fails because Sphinx
    tries to look up the object in the implemented ("canonical") location.

    .. seealso::

        * https://github.com/sphinx-doc/sphinx/issues/4826 - solves this with the "canonical" directive
        * https://github.com/pyca/cryptography/pull/7938 - where this was fixed for cryptography
        * https://www.sphinx-doc.org/en/master/extdev/appapi.html#events - sphinx api docs
        * https://stackoverflow.com/a/62301461 - source of this hack

    """
    pending_xrefs = doctree.traverse(condition=pending_xref)
    for node in pending_xrefs:
        alias = node.get("reftarget", None)

        if alias is not None and alias in qualname_overrides:
            # This does set the type to attr in the error message, but does not fix the build error with
            # typehints described in nitpick_ignore either:
            # if alias == "KeyUsages":
            #     node["reftype"] = "attr"
            node["reftarget"] = qualname_overrides[alias]


def setup(app: Sphinx) -> None:
    """Add hook functions to Sphinx hooks."""
    app.connect("doctree-read", resolve_canonical_names)

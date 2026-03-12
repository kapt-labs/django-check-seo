![Django Check SEO](https://user-images.githubusercontent.com/45763865/114545606-72178380-9c5c-11eb-99dd-1088bb2a0bd9.png)

*Replacing some features of Yoast or SEMrush for Django & Django-CMS users.*

In other words, django-check-seo will tell you if you have problems concerning a broad range of SEO aspects of your pages.


[![PyPI](https://img.shields.io/pypi/v/django-check-seo?color=%232a2)](https://pypi.org/project/django-check-seo/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/django-check-seo?color=%232a2)](https://pypi.org/project/django-check-seo/) [![GitHub last commit](https://img.shields.io/github/last-commit/kapt-labs/django-check-seo)](https://github.com/kapt-labs/django-check-seo)

----

# Requirements

- Python 3.8+ & Django 2.2+  
    > *Still using Python 2? Version <0.6 [from this branch](https://github.com/kapt-labs/django-check-seo/tree/python2) is for you!*
- Django Check SEO relies on Django site framework + define a new permission
- beautifulsoup4 (>= 4.7.0)
- htmx (a version is included in Django Check SEO static files)

# Install


1. Install the module from [PyPI](https://pypi.org/project/django-check-seo/):
    ```
    python3 -m pip install django-check-seo
    ```

2. Add it in your `INSTALLED_APPS`:
    ```
        "django_check_seo",
    ```

3. Add this in your `urls.py` *(add it before the `cms.urls` line if you're using django CMS)*:
    ```
        path("django-check-seo/", include("django_check_seo.urls")),
    ```
4. Update your Django Site objet with a working url (website url for prod env, localhost:8000 for your dev environment).

5. Add `testserver` to your `ALLOWED_HOSTS` (django-check-seo uses the Test Framework in order to get content, instead of doing a regular HTTP request).

6. Add the permission (`use_django_check_seo`) to the users/groups you want to let access Django Check SEO.

7. *(optional) Configure the settings (see [config](#config) below).*

8. ![that's all folks!](https://i.imgur.com/o2Tcd2E.png)

----

# Misc

This application may be used with or without `django-cms` (a "Check SEO" button will appear in the CMS toolbar if you're using django-cms).

If you're not using Django CMS (only Django), here's the link format to access your pages reports (with or without using i18n):

```
https://example.com/django-check-seo/?page=/example-page/
https://example.com/fr/django-check-seo/?page=/example-page/
```

----

# Settings

## Keywords handling ![**new in 2.0.0**](https://img.shields.io/badge/new_in-2.0.0-green)

Keywords are discovered via a configurable function. Set it's import path in your settings:

```py
# Default: read from html page <meta name="keywords" content="..."> (comma-separated)
DJANGO_CHECK_SEO_KEYWORDS_DISCOVERY_METHOD = "django_check_seo.utils.keywords_discovery.meta_keywords"
```

To use keywords stored in the database (models `Page` and `Keyword` from Django Check SEO), set this instead:

```py
DJANGO_CHECK_SEO_KEYWORDS_DISCOVERY_METHOD = "django_check_seo.utils.keywords_discovery.model_keywords"
# Set/update keywords through Django Check SEO page:
DJANGO_CHECK_SEO_KEYWORDS_EDITABLE = True
```

You're free to implement your own solution to handle keywords.

## Select main content (exclude header/footer/...)

Since django-check-seo will count things like number of words on the main content and the number of internal links, it is important to only select the *main* content of the page (an address in the footer is not the main content of your page).

Django-check-seo use a string (named `DJANGO_CHECK_SEO_EXCLUDE_CONTENT`) of [css selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors) to exclude unwanted html nodes from the html content:

```py
DJANGO_CHECK_SEO_EXCLUDE_CONTENT = "tag, .class, #id, tag > .child_class"
```

> **Example**: See [this issue's comment](https://github.com/kapt-labs/django-check-seo/issues/35#issuecomment-593429870) for an example.  
> You can find a reference table of css selectors explained [here](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors#Reference_table_of_selectors) (on mdn docs).

## Basic config

The basic config (used by default) is located in [`django-check-seo/conf/settings.py`](https://github.com/kapt-labs/django-check-seo/blob/master/django_check_seo/conf/settings.py#L5-L15) and looks like this:
```python
DJANGO_CHECK_SEO_SETTINGS = {
    "content_words_number": [300, 600],
    "internal_links": 1,
    "external_links": 1,
    "meta_title_length": [30, 60],
    "meta_description_length": [50, 160],
    "keywords_in_first_words": 50,
    "max_link_depth": 3,
    "max_url_length": 70,
}
```

If you need to change something, just define a dict named `DJANGO_CHECK_SEO_SETTINGS` in your settings.py.

### *Custom config example:*

If you put this in your `settings.py` file:

```python
DJANGO_CHECK_SEO_SETTINGS = {
    "internal_links": 25,
    "meta_title_length": [15,30],
}
```

Then this will be the settings used by the application:

```python
DJANGO_CHECK_SEO_SETTINGS = {
    "content_words_number": [300, 600],
    "internal_links": 25,  # 1 if using default settings
    "external_links": 1,
    "meta_title_length": [15,30],  # [30, 60] if using default settings
    "meta_description_length": [50, 160],
    "keywords_in_first_words": 50,
    "max_link_depth": 3,
    "max_url_length": 70,
}
```

*Want to know more ? See the wiki page [Config explained](https://github.com/kapt-labs/django-check-seo/wiki/Config-explained).*

## Templates

The `django_check_seo/default.html` template have an `<aside>` block named `seo_aside` that you can replace if you want, using the `extends` & `{% block seo_aside %}` instructions, like this:

```jinja2
{% extends "django_check_seo/default.html" %}

{% block seo_aside %}
    Hi!
{% endblock seo_aside %}
```
> This template will remplace all the `About`/`Documentation` & `Raw data` (content on the `<aside>` block) by "Hi!".

----

# Want a screenshot?

![screenshot](https://i.imgur.com/hJGDvtw.png)

*Other (older) screenshots and videos are available on the [wiki](https://github.com/kapt-labs/django-check-seo/wiki/Medias).*

----

# Unit tests

They are located in `tests` folder.

```sh
# Create test venv & install dependencies
python3 -m venv .venv && . .venv/bin/activate && python3 -m pip install django bs4 lxml djangocms-page-meta requests pytest pytest-django pytest-cov unidecode
```

## Launch tests

```sh
# Souce venv, launch tests (including coverage)
. .venv/bin/activate && python3 -m pytest -s --cov-config=.coveragerc --cov=django_check_seo --cov-report term-missing
```

----

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
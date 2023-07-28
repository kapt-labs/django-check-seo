![Django Check SEO](https://user-images.githubusercontent.com/45763865/114545606-72178380-9c5c-11eb-99dd-1088bb2a0bd9.png)

*Replacing some features of Yoast or SEMrush for Django & Django-CMS users.*

In other words, django-check-seo will tell you if you have problems concerning a broad range of SEO aspects of your pages.

----

[![PyPI](https://img.shields.io/pypi/v/django-check-seo?color=%232a2)](https://pypi.org/project/django-check-seo/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/django-check-seo?color=%232a2)](https://pypi.org/project/django-check-seo/) [![GitHub last commit](https://img.shields.io/github/last-commit/kapt-labs/django-check-seo)](https://github.com/kapt-labs/django-check-seo)

----

# Install

*(compatible with django >= 1.8.15 & python >= 2.7)*

1. Install the module from [PyPI](https://pypi.org/project/django-check-seo/):
    ```
    python3 -m pip install django-check-seo
    ```

2. Add it in your `INSTALLED_APPS`:
    ```
        "django_check_seo",
    ```

3. Add this in your `urls.py` *(if you're using django-cms, put it before the `cms.urls` line or it will not work)*:
    ```
        path("django-check-seo/", include("django_check_seo.urls")),
    ```
    * *Or add this if you're still using `url` (you shouldn't):*
        ```
            url(r"^django-check-seo/", include("django_check_seo.urls")),
        ```

4. Update your Django [Site](https://i.imgur.com/pNRsKs7.png) object parameters with a working url (here's an [example](https://i.imgur.com/IedF3xE.png) for dev environment).

5. Add `testserver` to your `ALLOWED_HOSTS` list in your settings.py (django-check-seo uses the Test Framework in order to get content, instead of doing an HTTP request).

6. *(optional) Configure the settings (see [config](#config)).*

7. ![that's all folks!](https://i.imgur.com/o2Tcd2E.png)

----

# Misc

This application needs `beautifulsoup4` (>=4.7.0) and `djangocms_page_meta` *(==0.8.5 if using django < 1.11)*. It may be used with or without `django-cms` (a django-check-seo button will appear in the topbar if you're using django-cms).

If you're not using Django CMS (only Django), here's the link format to access your pages reports:

```
https://example.com/django-check-seo/?page=/example-page/
  -> will check https://example.com/example-page/

https://example.com/fr/django-check-seo/?page=/example-page/
  -> will check https://example.com/example-page/
     (using localized url (if you add django-check-seo in i18n_patterns))
```

----

# Config

## Basic settings

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

### *Custom settings example:*

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

*Want to know more ? See the wiki page [Settings explained](https://github.com/kapt-labs/django-check-seo/wiki/Settings-explained).*

----

## Select main content (exclude header/footer/...)

Since django-check-seo will count things like number of words on the main content and the number of internal links, it is important to only select the *main* content of the page (an address in the footer is not the main content of your page).

Django-check-seo use a string (named `DJANGO_CHECK_SEO_EXCLUDE_CONTENT`) of [css selectors](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors) to exclude unwanted html nodes from the html content:

```
DJANGO_CHECK_SEO_EXCLUDE_CONTENT = "tag, .class, #id, tag > .child_class"
```

*You can find a reference table of css selectors explained [here](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors#Reference_table_of_selectors) (on mdn docs).*

## *Example: See [this issue's comment](https://github.com/kapt-labs/django-check-seo/issues/35#issuecomment-593429870) for an example.*

----

# Want a screenshot?

![screenshot](https://i.imgur.com/hJGDvtw.png)

*Other (older) screenshots and videos are available on the [wiki](https://github.com/kapt-labs/django-check-seo/wiki/Medias).*

----

# Unit tests

They are located in `tests` folder.

The file `launch_tests.sh` is here to manage tests launching for you. You only need `python3-venv` (for python3 venv) and `virtualenv` (for **python2** venv) in order to make it work.

----

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

----

# Interested in finding out more?

Take a look at the [wiki](https://github.com/kapt-labs/django-check-seo/wiki/):

 * [List & explanations of all checks](https://github.com/kapt-labs/django-check-seo/wiki/Description-of-the-checks)
 * [How to add a check?](https://github.com/kapt-labs/django-check-seo/wiki/How-to-add-a-check%3F)
 * ...

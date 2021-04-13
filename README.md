![Django Check SEO](https://user-images.githubusercontent.com/45763865/114545606-72178380-9c5c-11eb-99dd-1088bb2a0bd9.png)

Replacing some features of Yoast or SEMrush for django CMS users.

In other words, django-check-seo will tell you if you have problems concerning a broad range of SEO aspects of your pages.

----

[![PyPI](https://img.shields.io/pypi/v/django-check-seo?color=%232a2)](https://pypi.org/project/django-check-seo/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/django-check-seo?color=%232a2)](https://pypi.org/project/django-check-seo/) [![GitHub last commit](https://img.shields.io/github/last-commit/kapt-labs/django-check-seo)](https://github.com/kapt-labs/django-check-seo)

----

# Installation

The following instructions are for an installation on a djangocms-based website using python >= 3 & django >= 2, or for a djangocms-based website using python >= 2.7 & django >= 1.8.15.

 1. Install module using pipenv:
 ```
 pipenv install django-check-seo
 ```
 * *Or pip:*
 ```
 pip install django-check-seo
 ```
 2. Add it to your installed apps:
 ```
     "django_check_seo",
 ```
 3. [Add it](https://user-images.githubusercontent.com/45763865/72879105-83453f00-3cfc-11ea-8f1f-933ce7af4964.png) to your `urls.py` *(before `url(r'^', include('cms.urls')),` or it will not work)*:
 ```
     url(r"^django-check-seo/", include("django_check_seo.urls")),
 ```
 * *Or add this if you're using path:*
 ```
     path("django-check-seo/", include("django_check_seo.urls")),
 ```
 4. Update your [site](https://i.imgur.com/pNRsKs7.png) parameters with correct url (*[example](https://i.imgur.com/IedF3xE.png)* for dev environment)

 5. *(optional) Configure the settings, and/or force http instead of https, and/or add authentification (see [config](#config)).*

 6. ![that's all folks!](https://i.imgur.com/o2Tcd2E.png)

----

# Prerequisites

This application need `beautifulsoup4` (>=4.7.0), `requests`, `djangocms` & `djangocms_page_meta` *(==0.8.5 if using django < 1.11)*.

----

# Config

## Basic settings

Basic config (used by default) is in [`django-check-seo/conf/settings.py`](https://github.com/kapt-labs/django-check-seo/blob/master/django_check_seo/conf/settings.py#L5-L15):
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
    "internal_links": 25,
    "external_links": 1,
    "meta_title_length": [15,30],
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

### *Example:*

See [this issue comment](https://github.com/kapt-labs/django-check-seo/issues/35#issuecomment-593429870) for an example.

----

## Use `http` instead of `https`

By default, the application will attempt to make requests in https.

To enable plain http queries, you can add a variable named `DJANGO_CHECK_SEO_FORCE_HTTP` set to `True` in your settings.py.

### *Example:*

```python
# Force HTTP
DJANGO_CHECK_SEO_FORCE_HTTP = True

# Force HTTPS (default case, same as not defining the variable)
DJANGO_CHECK_SEO_FORCE_HTTP = False
```

----

## Authentication

The website you want to test may require a prior connection due to a .htaccess file (or may use [wsgi-basic-auth](https://github.com/mvantellingen/wsgi-basic-auth)), which prevents django-check-seo from accessing its html code.

To prevent this, you can specify the login informations (username/password) in the `DJANGO_CHECK_SEO_AUTH` dictionnary (in your website settings).

This dictionary must contain two keys named `user` and `pass`.

### *Example:*

 * In `mywebsite/settings.py`:
 ```python
 DJANGO_CHECK_SEO_AUTH = {
     "user": os.getenv("HTACCESS_USER"),
     "pass": os.getenv("HTACCESS_PASS"),
 }
 ```

 * In `.env` file:
 ```
 export HTACCESS_USER=myusername
 export HTACCESS_PASS=mypassword

 WSGI_AUTH_CREDENTIALS=$HTACCESS_USER:$HTACCESS_PASS
 ```

### Authentication and redirections

When you _really_ want django-check-seo to follow a redirection and you _really_ want to authenticate on the redirected site using the `DJANGO_CHECK_SEO_AUTH` credentials, you can set this config var to `True` in your site settings:

```
DJANGO_CHECK_SEO_AUTH_FOLLOW_REDIRECTS = True
```

***Warning!** This could be considered a bad practice to allow this by default, because if you create a redirection on your (authenticated-only accessible) website, then the destination website will have access to the credentials by reading the `Authorization` header (see [CVE-2014-1829](https://nvd.nist.gov/vuln/detail/CVE-2014-1829)). See [this issue](https://github.com/kapt-labs/django-check-seo/issues/43#issue-839650874) for a valid usecase.*

----

# Want a screenshot?

![screenshot](https://i.imgur.com/hJGDvtw.png)

*Other screenshots and videos are available on the [wiki](https://github.com/kapt-labs/django-check-seo/wiki/Medias).*

----

# Unit tests

They are located in `tests` folder.

The file `launch_tests.sh` is here to manage tests launching for you. You only need `python3-venv` (for python3 venv) and `virtualenv` (for **python2** venv) in order to make it work ([example video](https://up.l3m.in/files/1584462369-launch_tests.webm)).

----

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

----

# Interested in finding out more?

Take a look at the [wiki](https://github.com/kapt-labs/django-check-seo/wiki/):

 * [List & explanations of all checks](https://github.com/kapt-labs/django-check-seo/wiki/Description-of-the-checks)
 * [How to add a check?](https://github.com/kapt-labs/django-check-seo/wiki/How-to-add-a-check%3F)
 * ...

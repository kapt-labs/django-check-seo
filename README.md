![Django Check SEO](https://user-images.githubusercontent.com/45763865/69130297-8def1800-0ab0-11ea-8e3f-973e0f97a080.png)

Replacing some features of Yoast or SEMrush for django CMS users.

In other words, django-check-seo will tell you if you have problems concerning a broad range of SEO aspects of your pages.

----

## Installation

 1. Install module using pipenv:
 ```
 pipenv install django-check-seo
 ```
 * *Or pip:*
 ```
 pip install django-check-seo
 ```
 2. [Add it](https://i.imgur.com/clmjJoE.mp4) to your installed apps:
 ```
     "django-check-seo.apps.DjangoCheckSEOConfig",
 ```
 3. [Add it](https://user-images.githubusercontent.com/45763865/72879105-83453f00-3cfc-11ea-8f1f-933ce7af4964.png) to your `urls.py` *(before `url(r'^', include('cms.urls')),` or it will not work)*:
 ```
     url(r"^django-check-seo/", include("django-check-seo.urls")),
 ```
 * *Or add this if you're using path:*
 ```
     path("django-check-seo/", include("django-check-seo.urls")),
 ```
 4. Update your [site](https://i.imgur.com/pNRsKs7.png) parameters with correct url (*[example](https://i.imgur.com/IedF3xE.png)* for dev environment)

 5. ![https://i.imgur.com/o2Tcd2E.png](https://i.imgur.com/o2Tcd2E.png)

----

## Prerequisites

This application need `beautifulsoup4`, `requests`, `djangocms` & `djangocms_page_meta`.

----

## Config

### Basic settings

Basic config (used by default) is in [`django-check-seo/conf/settings.py`](https://github.com/kapt-labs/django-check-seo/blob/93110f7713d89768a474a704b30dac1536f8b7b9/django-check-seo/conf/settings.py#L6-L15):
```python
SEO_SETTINGS = {
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

If you need to change something, just define it in your `mywebsite/settings.py` file in a dict named `DJANGO_CHECK_SEO_SETTINGS`.

#### *Example:*

If you put this in your `settings.py` file:

```python
DJANGO_CHECK_SEO_SETTINGS = {
    "internal_links": 25,
    "meta_title_length": [15,30],
}
```

Then this will be the settings used by the application:

```python
SEO_SETTINGS = {
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

### Authentication

The website you want to test may require a prior connection due to a .htaccess file (or may use [wsgi-basic-auth](https://github.com/mvantellingen/wsgi-basic-auth)), which prevents django-check-seo from accessing its html code.

To prevent this, you can specify the login informations (username/password) in the `DJANGO_CHECK_SEO_AUTH` dictionnary (in your website settings).

This dictionary must contain two keys named `user` and `pass`.

#### *Example:*

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

----

## Want a screenshot?

![screenshot](https://user-images.githubusercontent.com/45763865/72882024-2b113b80-3d02-11ea-8507-6cb48f9f34b3.png)

*Other screenshots and videos are available on the [wiki](https://github.com/kapt-labs/django-check-seo/wiki/Medias).*

----

## Interested in finding out more?

Take a look at the [wiki](https://github.com/kapt-labs/django-check-seo/wiki/):

 * [List & explanations of all checks](https://github.com/kapt-labs/django-check-seo/wiki/Description-of-the-checks)
 * [How to add a check?](https://github.com/kapt-labs/django-check-seo/wiki/How-to-add-a-check%3F)
 * ...

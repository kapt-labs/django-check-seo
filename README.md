![Django Check SEO](https://user-images.githubusercontent.com/45763865/69130297-8def1800-0ab0-11ea-8e3f-973e0f97a080.png)

Replacing some features of Yoast or SEMrush for django CMS users.

In other words, django-check-seo will tell you if you have problems concerning a broad range of SEO aspects of your pages.

----

## Install

#### With pipenv

 * Add `django-check-seo = { git = 'https://github.com/kapt-labs/django-check-seo.git' }` to your Pipfile below `[packages]`, then run `pipenv install`,
 *or*
 * Execute `pipenv install git+https://github.com/kapt-labs/django-check-seo#egg=django-check-seo` in your working directory,

**and then**

 * add `django-check-seo.apps.DjangoCheckSEOConfig` to your `INSTALLED_APPS`,
   * *optional since django-check-seo do not uses the django applications features*
 * add `django-check-seo/static/django-check-seo/` to your `STATICFILES_DIRS`,
 * add the file [`cms_toolbars.py`](https://github.com/kapt-labs/django-check-seo/wiki/Toolbar-shortcut#cms_toolbarspy) inside your `django_project_name` folder,
 * add `url(r"^django-check-seo/", include("django-check-seo.urls")),` to your `urlpatterns` in `urls.py`,
 * export all the vars used in the application (or put them inside your [`.env`](https://gist.github.com/corentinbettiol/f1e4b6630b7ae9afe2f9023b2185f3db#file-env) file).

*Start your django CMS project, log in, you should see the "Check SEO..." button and everything should be okay.*

*[Example output](https://gist.github.com/corentinbettiol/f1e4b6630b7ae9afe2f9023b2185f3db) when setting up a project with django-check-seo.*

#### Without pipenv

*coming soon* 📝

----

## Prerequisites

You will need `djangocms` & `djangocms_page_meta` in order to made this application work.

----

## Want a screenshot or two?

![](https://i.imgur.com/ibjcb5U.png)

*Other screenshots and videos are available on the [wiki](https://github.com/kapt-labs/django-check-seo/wiki/Medias).*

----

## Interested in finding out more?

Take a look at the [wiki](https://github.com/kapt-labs/django-check-seo/wiki/):

 * [List & explanations of all checks](https://github.com/kapt-labs/django-check-seo/wiki/Description-of-the-checks)
 * [How to add a check?](https://github.com/kapt-labs/django-check-seo/wiki/How-to-add-a-check%3F)
 * ...

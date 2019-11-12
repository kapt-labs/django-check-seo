# django-check-SEO

Will tell you if you have problems concerning all SEO aspects of your pages.

----

### List of alerts raised
 * No meta keywords
 * No title tag
 * Title tag is too short
 * Title tag is too long
 * Title do not contain any keyword
 * Meta description is too short
 * Meta description is too long
 * No keyword in meta description
 * No meta description
 * Not enough internal links
 * Too many internal links
 * Not enough external links
 * Too many external links
 * Not enough keyword occurences
 * Too many keyword occurences
 * No keyword in URL
 * Too much h1 tags
 * No h1 tag
 * No keyword in h1
 * No h2 tag
 * No keyword in h2
 * Img lack alt tag
 * Too many levels in path
 * No keyword in first sentence

----

## Can I have a screenshot?

Yep, here it is:


![](https://i.imgur.com/3W0CK4b.png)

----

## Install

#### With pipenv

 * Add `django-check-seo = { git = 'https://github.com/kapt-labs/django-check-seo.git' }` to your Pipfile below `[packages]`, then run `pipenv install`,
 *or*
 * Execute `pipenv install git+https://github.com/kapt-labs/django-check-seo#egg=django-check-seo` in your working directory,

**and then**

 * add `django-check-seo` to your `INSTALLED_APPS`,
 * add the file [`cms_toolbars.py`](https://github.com/kapt-labs/django-check-seo/wiki/Toolbar-shortcut#cms_toolbarspy) inside your `django_project_name` folder,
 * add `url(r"^django-check-seo/", include("django-check-seo.urls")),` to your `urlpatterns` in `urls.py`,
 * export all the vars used in the application (or put them inside your `.env` file).

*Start your django CMS project, log in, you should see the "Check SEO..." button and everything should be okay.*
*[Example output](https://gist.github.com/corentinbettiol/f1e4b6630b7ae9afe2f9023b2185f3db) when setting up a project with django-check-seo.*

#### Without pipenv

*coming soon* 📝

## Prerequisites

You will need `djangocms` & `djangocms_page_meta` in order to made this application work.

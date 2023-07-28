Changelog
=========


v0.6.3 (2023-07-28)
-------------------

Bug fixes
~~~~~~~~~
- Fix #58 - remove unused load cms_tags [Corentin Bettiol]

Documentation
~~~~~~~~~~~~~
- Update changelog [Corentin Bettiol]


v0.6.2 (2023-04-19)
-------------------

Documentation
~~~~~~~~~~~~~
- Update changelog [Corentin Bettiol]

Other
~~~~~
- An issue when splitting the keywords [Ahmed Shawky]

  Keywords must be separated by ",  " a comma followed by two empty spaces, which will fail in most cases.
  Split by, then removing empty spaces should solve the issue



v0.6.1 (2023-04-18)
-------------------

Documentation
~~~~~~~~~~~~~
- Update readme [Corentin Bettiol]
- Update changelog [Corentin Bettiol]

Other
~~~~~
- Have the test-client follow redirects on requests [Marco Bonetti]


v0.6.0 (2023-03-03)
-------------------

Documentation
~~~~~~~~~~~~~
- Update readme [Corentin Bettiol]
- Update changelog [Corentin Bettiol]

Other
~~~~~
- #55 Support both new and old versions of Django still using
  ugettext_lazy [Marco Bonetti]
- Dont report missing description if we have exactly one [Marco Bonetti]
- Django 4: ugettext_lazy was removed in favor of gettext_lazy [Marco
  Bonetti]


v0.5.2 (2022-09-21)
-------------------

Bug fixes
~~~~~~~~~
- Fix python2 tests [Corentin Bettiol]

Maintenance
~~~~~~~~~~~
- Python2 (!!!) compat [Corentin Bettiol]
- Improve (?) django 3 compat [Corentin Bettiol]

  replace a check "startswith 2" by "> 1" in order to handle django
  version 3 and mor



v0.5.1 (2022-06-17)
-------------------

Bug fixes
~~~~~~~~~
- Fix #45 Meta description check is now working [Corentin Bettiol]


v0.5.0 (2022-06-14)
-------------------

Features
~~~~~~~~
- Fix #48 [Corentin Bettiol]

  Fix typo in comments.

  Update image check: image lacking alt tags are creating a "warning" and
  not an "error" anymore, since there are valid usecases where you won't
  add an alt tag (non-text content).

  Update of translations


Documentation
~~~~~~~~~~~~~
- Update readme [Corentin Bettiol]

  update pre-commit-confi

- Update changelog [Adrien Delhorme]

Other
~~~~~
- Remove requests as a requirement, use django.test.Client [Jeffrey de
  Lange]


v0.4.3 (2021-09-09)
-------------------

Documentation
~~~~~~~~~~~~~
- Update changelog [Adrien Delhorme]

Maintenance
~~~~~~~~~~~
- Correct MANIFEST.in [Adrien Delhorme]


v0.4.2 (2021-09-09)
-------------------

Bug fixes
~~~~~~~~~
- Display file name instead of string "image" [Adrien Delhorme]
- Misleading translation for image alt check [Adrien Delhorme]
- Correct handling of unicode strings [Adrien Delhorme]
- Check_keyword_url with accents [Adrien Delhorme]

  When the keywords contained accents and spaces and the url contained
  accents, the check was failing


Documentation
~~~~~~~~~~~~~
- Update AUTHORS file [Adrien Delhorme]
- Update logo in readme for dark theme [Corentin Bettiol]
- Update changelog [cb]

Maintenance
~~~~~~~~~~~
- Ignore .python-version file [Adrien Delhorme]


v0.4.1 (2021-08-23)
-------------------

Bug fixes
~~~~~~~~~
- Replace spaces by dash in keyword for url search [cb]

Documentation
~~~~~~~~~~~~~
- Update readme [cb]
- Update changelog [cb]


v0.4.0 (2021-03-25)
-------------------

Features
~~~~~~~~
- Add setting to allow authenticated requests to follow redirections
  [cb]

  * close #43
  * update black in .pre-commit-config & run blac


Bug fixes
~~~~~~~~~
- Use no-store instead of no-cache [cb]

  (more info here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control#cacheability



v0.3.7 (2021-01-06)
-------------------

Bug fixes
~~~~~~~~~
- Fix #42 [cb]

  *djangocms toolbar button now does not return a str containing a string representation of a byte string anymor

- Update broken setup.cfg [cb]
- Remove print [cb]


v0.3.6 (2020-09-14)
-------------------

Bug fixes
~~~~~~~~~
- No summary [cb]

  *fix python2 issue 'No module named unidecode



v0.3.5 (2020-09-14)
-------------------

Features
~~~~~~~~
- Fix launc_tests exit codes [cb]
- Update keyword matchin in URL [cb]

  *add tests for keywords in URL
  *update tests for h


Documentation
~~~~~~~~~~~~~
- Add CONTRIBUTING.md [cb]

  *Add contributing guidelines
  *Add AUTHORS.md file (list of contributors)
  *Edit README.md
  *Edit launch_tests.sh
  *Edit pre-commit confi


Maintenance
~~~~~~~~~~~
- Run flake8, isort & black [cb]

Tests
~~~~~
- Add tests for keywords in 1st paragraph [cb]
- Test url & content length [cb]
- Add tests *for internal & external links [cb]
- Add tests for check_keywords [cb]
- Fix failing tests in python2 [cb]

Other
~~~~~
- #40 [cb]

  *current url is now fetched using utf-8, which will not throw exception if accentuated char is foun

- Update pre-commit & launch_checks [cb]
- Update pre-commit [cb]
- +TEST [cb]

  *switch title kw check to the new method (using regex)
  *add tests for titl

- Add image tests remove unnecessary tags from test html [cb]
- Bug + add tests for h2 [cb]

  *fix bug where keyword was not found but green bold was added to part of the wor

- Add tests for meta description [cb]
- Add tests for check_description [cb]
- Update tests [cb]

  *remove some foldrs & files from coverage repor

- Update coding in test_h1.py (from latin-1 to utf-8) [cb]
- Bug in check_h1 [cb]

  *finished adding tests for check_h1.py, enhoy 100% coverage!
  *fix bug from previous commit (forgot parenthesis

- Add some h1 tests & fix bug [cb]

  fix h1 bug: no text was displayed in searched_in where all content was in the alt tag of an image (thx tests!



v0.3.4 (2020-03-24)
-------------------
- Bad strings in some regex [cb]


v0.3.3 (2020-03-24)
-------------------

Features
~~~~~~~~
- Add test skeleton (will soon add real unit tests) [cb]

Other
~~~~~
- #37, fix #38 [cb]

  * replace number by keywords that are found inside text
  * update regex used to count keyword occurences to accept some special chars (including @



v0.3.2 (2020-03-04)
-------------------

Maintenance
~~~~~~~~~~~
- Update README & check_title [cb]

  * fix typo README
  * fix check_title: case "empty title tag" was not handle


Other
~~~~~
- +MAINT: check_title [cb]

  * replace .string by .text
  * handle case where title tag exist but does not contain any text (display [no content])
  * add french translation for "[no content]



v0.3.1 (2020-03-03)
-------------------

Bug fixes
~~~~~~~~~
- Description was lowered but no keywords [cb]

  * "check my super duper description" does not contain "Super"
  * "check my super duper description" contain "super

- Empty links error [cb]

  * links with only newlines were considered as valid strings, now they should display their content tag instead (usually an img without alt tag

- Meta description error [cb]

  * .join() in python2 is not encoding-safe, so strings like "Thaïs" in meta description or h1 could lead to an erro

- Meta description searched_in [cb]

  * display lower() meta description to match with lower() keywords in searched_in var



v0.3.0 (2020-03-02)
-------------------
- +FIX+DOCS [cb]

  *add new DJANGO_CHECK_SEO_SEARCH_IN parameter (fix #30, #32 & #35)
  *fix error in searched_in for meta descriptions tests (fix #36

- Display arrows & update cursor for list of checks [cb]


v0.2.0 (2020-02-28)
-------------------

Documentation
~~~~~~~~~~~~~
- Mention custom djangocms-page-meta version for install on django <
  1.11 [cb]

Other
~~~~~
- & FEAT: [cb]

  * slugify urls & keywords (fix #33)
  * show what is wrong (or good) in the "searched in" sections (fix #34)
  * no more empty links in "searched in" sections :
  - you should see content of alt tag if it exists in an image in your link
  - if there is no image in your link, you should see the html code of the first chil

- Update default settings: [cb]

  set link depth to 4 instead of

- Correct typo, add colors in "searched in" sections [cb]


v0.1.1 (2020-02-05)
-------------------

Bug fixes
~~~~~~~~~
- Fix html tags order in template [cb]


v0.1.0 (2020-02-05)
-------------------

Features
~~~~~~~~
- Mention that the check is done on public page only [cb]

  * update translations
  * add cs



v0.0.12 (2020-02-05)
--------------------

Bug fixes
~~~~~~~~~
- Ignore title tags in body [cb]

  close #28: check for a title meta tag only inside <head></head



v0.0.11 (2020-02-04)
--------------------
- +FIXES: [cb]

  * MAINT: update README
  * FIX: update broken html in template file



v0.0.10 (2020-01-29)
--------------------
- (really) fix #27, remove old fogotten verify=False in request that
  created a warning when using auth parameters [cb]


v0.0.9 (2020-01-29)
-------------------

Format
~~~~~~
- Remove unwanted print [cb]


v0.0.8 (2020-01-29)
-------------------

Bug fixes
~~~~~~~~~
- Update manifest so template/ & static/ folders are included in the
  package [cb]

Documentation
~~~~~~~~~~~~~
- Update metadata in setup.cfg [cb]


v0.0.7 (2020-01-28)
-------------------
- + FEAT: * fix #27: requests are made using https (add parameter to
  force use of http) * add support for python 2.7 & django 1.8! (best
  feature ever) * bonus: fix strange folder name (with '-' instead of
  '_'), now you are able to just add 'django_check_seo' in your
  INSTALLED_APPS [cb]


v0.0.6 (2020-01-22)
-------------------

Maintenance
~~~~~~~~~~~
- Remove unnecessary print [cb]


v0.0.5 (2020-01-22)
-------------------

Documentation
~~~~~~~~~~~~~
- Update readme [cb]

  * clearer installation instructions
  * add config example
  * add auth example
  * update screensho


Other
~~~~~
- Bug in check_links (the check still used old os.environ['DOMAIN_NAME']
  instead of Site.objects.get_current().domain [cb]
- Add wsgi-basic-auth support [cb]

  close #2



v0.0.4 (2020-01-20)
-------------------

Documentation
~~~~~~~~~~~~~
- Update readme [cb]


v0.0.3 (2020-01-20)
-------------------
- Add flake8 & pre-commit config files, update gitignore [cb]


v0.0.2 (2020-01-20)
-------------------
- Update readme, remove unused files, add lxml parser in required
  packages [cb]


v0.0.1 (2020-01-20)
-------------------

Maintenance
~~~~~~~~~~~
- Add proper dependencies, update version & add bumpversion support
  close #26 [cb]

Other
~~~~~
- Add new translation [cb]
- Remove unused setting [cb]

  (keyword density is not used in any test

- Potential bug in different environments [cb]

  replace env DOMAIN_NAME by Site.objects.get_current(

- Update readme [cb]

  correct bs4 pacage name to beautifulsoup4
  remove unnecessary stuf

- Bug: add ending slash in url [cb]
- Update README: improve instruction [cb]
- Bug in check_keyword_url [cb]
- Bug in check_images.py: if there is no src or alt text, display
  ''unknown image'' [cb]
- Remove unused translation [cb]
- #22, update various checks, remove ''found title tag'' check (it was a
  duplicate check) [cb]
- Update translations, work on #22 [cb]
- Translation error, work on searched_in content for meta description
  checks [cb]
- #21 [cb]

  add em tags to all english terms in french translation
  create element.html templat

- Relative font import [cb]
- #20 [cb]

  add var with keywords in context
  display keywords in template
  add css for keywords lis

- Update translations [cb]
- Update translations [cb]
- #19 [cb]

  url check now use slugif

- #18 [cb]

  access to content is more secur

- Forgot to update version number [cb]
- Remove unnecessary file [cb]
- Remove forgotten print [cb]
- Bug [cb]

  keywords composed of multiple words were not found in meta title ta

- Bug [cb]

  keywords composed of multiple words were not found in url

- Bug in keyword_present_first_paragraph [cb]
- Remove unused imports [cb]
- Remove broken links check [cb]

  see https://github.com/kapt-labs/django-check-seo/wiki/Custom-Check

- #17, add cms_toolbars file [cb]

  check_links is now checking the full_url & the DOMAIN_NAME vars
  new cms_toolbars.py file is added, and now users do not need to create any file inside their projec

- Add new check - fix #16 [cb]

  check if no broken internal link is found using requests.status_cod

- Bug: the right content is now selected for a success description [cb]
- Bug: format improperly placed [cb]
- Update translations [cb]
- Bug of translation by adding a context [cb]
- Update translations [cb]
- Add issue templates [Corentin Bettiol]
- Links of fonts in design.css file [cb]
- Bug induced by fixing previous broken links bug [cb]
- Update readme: simplify install section [cb]
- Bug: static files were not loaded properly [cb]
- Broken links [cb]
- Update readme, update translations [cb]
- Update readme [cb]
- Update readme [cb]
- Bug in the url depth calculation [cb]
- Add doc for each check [cb]
- Bug in check_title where title tag exists but is empty [cb]
- Bug on check_h1 [cb]
- #12, fix #13, fix #15 [cb]

  add success list, display list under problems & warning lists
  progress and end of dictionary migration to new objects
  checks involving keywords should compare lowered strings no

- Add new successful checks, check_description.py now uses CustomList
  objects [cb]
- Progress on #12, fix #13 [cb]

  rename checks/ to checks_list/
  create site & custom_list classes inside checks/
  update translations (incomplete)
  update design (add green list for successful tests)
  add successful checks list that is displayed behind the two others
  beginning of the conversion process of problems & warning

- #8 [cb]

  update README (update screenshot, add link to gallery)
  add style
  update french translatio

- Add logo in application, update README [cb]

  add instructions on how to add static folder in dev mod

- Add logo [cb]
- #9 [cb]

  all descriptions are shorter no

- #10 [cb]

  see https://github.com/kapt-labs/django-check-seo/wiki/How-to-add-a-check%3F\#custom-checks to know how to add a chec

- Omission correction [cb]
- #11, work on #9 [cb]
- Work on #9 [cb]
- Add fr translation [cb]
- Update readme [cb]
- Update README, fix #7 (package application) [cb]

  create setup & manifest files, so now you should be able to install django-check-seo from this rep

- Bug in count_words_number.py [cb]
- #6 [cb]

  now the tests to exlude footer & menus are performed before extracting content in .container classe

- Improve #4, fix #5 [cb]

  - now all files are imported & functions are called automatically, so no need to import your module! Just drop the file in the folder and watch the magic happen
  - add factor of importance: after importing the files, the script executes the functions with the greatest importance firs

- Improve readability of html content, remove django app folder [cb]

  html content contained multiple carriage returns, so I removed them. But then it contained some joinedWords. So I updated the function to replace multiple carriage returns by spaces

- #4, improve code [cb]

  remove DjangoCheckSeo class
  add Site class
  split checks in multiple files in /checks folder
  each check is now launched by checks/launch_checks.py file (it should be easier to add your check without breaking all the code)
  each check has access to the Site instance (with some cool content in its vars)
  add a new <details> in the application page which will display formatted content without htm

- Add new check [cb]

  check 17: url is shorter than 'max_url_length' char

- Bug [cb]

  check for alt attribute in img tags was not functionnal and returned a keyerro

- Remove prints, correct division by zero error [cb]
- Wagnings to warnings, change the way keywords occurences checks work
  [cb]

  use percentage of words instead of an interva

- #2 [cb]

  number of links now trigger a warning instead of a proble

- Add new check, remove stop-words [cb]

  check 17: count words in main conten

- Remove mention of nltk [cb]
- Add list of features on readme, update text, add extracted content in
  context vars [cb]
- Add new check [cb]

  check 16: ensure that at least a keyword is in the first X words of conten

- Add new checks [cb]

  check 14:  ensure alt presence in images
  check 15: check path level

- Update screenshot in readme [cb]
- Add new checks [cb]

  check 10: keywords present in h2 tags (and h2 tags are present in page)
  check 11: meta description is present
  check 12: meta description length
  check 13: keywords present in meta descriptio

- Broken english [cb]
- Change template view, add new checks [cb]

  check 7: keyword is present in url
  check 8: h1 is present exactly 1 time
  check 9: keyword is present in h

- Add new checks [cb]

  check 5: number of internal & external links
  check 6: occurrence of keyword

- Use beautiful soup to parse html content, add firsts checks [cb]

  check 1: check if title is present on the page\ncheck 2: check title length\ncheck 3: get keywords\ncheck 4: check if at least a keyword is in page titl

- Add readme [cb]
- First run of black, isort & flake8, update gitignore, add comment [cb]
- Update name to reflect actual git repo name [cb]
- Initial commit [Corentin Bettiol]
- First commit, testing things [cb]




.. Generated by gitchangelog

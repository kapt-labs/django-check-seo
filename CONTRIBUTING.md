# Contributing

How can you contribute to this project ?

## Add issue

You can help by finding new issues & reporting them by creating [new issues](https://github.com/kapt-labs/django-check-seo/issues).

## Add code

You can help by picking an issue, or choosing to add a new test/feature (create an issue before you start coding).

0. Create a new issue, receive positive feedback.

1. Fork the repo, clone it.

2. Install pre-commit & unit tests dependencies.
    ```bash
    python3 -m pip install pre-commit python3-venv
    python2 -m pip install virtualenv
    ```

3. Install pre-commit hooks.
    ```bash
    pre-commit install
    ```

4. Create new branch.
    ```bash
    git checkout -b mybranch
    ```

5. Add your code.

6. (*Facultative*) Add tests ?

7. Add yourself in [AUTHORS.md](AUTHORS.md).

8. Commit, push.  
    *Make sure that pre-commit runs isort, black, flake8 & `launch_checks.sh`. [Example](https://github.com/kapt-labs/django-check-seo/commit/da1d0be5d3ebe6734585cd5dd7027186d432ccd0#commitcomment-38147459).*

9. Create a [Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

10. ![That's all folks!](https://i.imgur.com/o2Tcd2E.png)

----

### Commit description guidelines

We're using bluejava's [git-commit-guide](https://github.com/bluejava/git-commit-guide) for our commits description. Here's a quick reference:

![Reference git-commit-guide](https://raw.githubusercontent.com/bluejava/git-commit-guide/master/gitCommitMsgGuideQuickReference.png)

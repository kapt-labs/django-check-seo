#!/bin/bash

# django-check-seo super test-launching script
#
# Usage:
#    ./launch_tests.sh           activate venv (or create it & activate it),
#                                launch tests, deactivate venv
#    ./launch_tests.sh remove    remove folder "venv"
#    ./launch_tests.sh help      display this text


if [[ $1 == "remove" ]]; then

    if [[ -d "venv" ]]; then

        echo -e "\e[1;32m✅ test venv found\e[0m"
        echo -e "\e[2m➡ removing venv...\e[0m"
        rm -r venv
        echo -e "\e[1;32m✅ test venv removed successfully\e[0m"

    else

        echo -e "\e[1;31m❌ test venv not found\e[0m"
        echo -e "\e[1;32m✅ nothing to remove\e[0m"

    fi

else if [[ $1 == "help" ]]; then

    echo -e "django-check-seo super test-launching script"
    echo
    echo -e "Usage:"
    echo -e "    ./launch_tests.sh           \e[2mactivate venv (or create it & activate it), launch tests, deactivate venv\e[0m"
    echo -e "    ./launch_tests.sh remove    \e[2mremove folder \"venv\"\e[0m"
    echo -e "    ./launch_tests.sh help      \e[2mdisplay this text\e[0m"

else if [[ "$#" -gt 0 ]]; then

    echo "Wrong arg: try \"./launch_tests.sh help\" to get help."

else if [[ -d "venv" ]]; then

        echo -e "\e[1;32m✅ test venv found\e[0m"
                echo -e "\e[2m➡ launching tests...\e[0m"
        . venv/bin/activate && python3 -m pytest -s --cov=django_check_seo --cov-report term-missing && deactivate

else

    echo -e "\e[1;31m❌ test venv not found\e[0m"
    echo -e "\e[2m➡ creating venv...\e[0m"
    python3 -m venv venv 1>/dev/null && . venv/bin/activate && python3 -m pip install django bs4 lxml pytest pytest-django pytest-cov 1>/dev/null && deactivate
    echo -e "\e[1;32m✅ venv created successfully\e[0m"
    echo -e "\e[2m➡ launching tests...\e[0m"
    . venv/bin/activate && python3 -m pytest -s --cov=django_check_seo --cov-report term-missing && deactivate

fi fi fi fi

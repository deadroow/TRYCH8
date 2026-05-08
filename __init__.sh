#!/bin/bash

set -euo pipefail
source ./bash_scripts/utils/display.sh

create_bash_boilerplate(){
    mkdir -p bash_scripts/base/constants
    mkdir -p bash_scripts/tests
    mkdir -p bash_scripts/utils
    
    touch bash_scripts/base/constants/colors.sh
    touch bash_scripts/utils/display.sh
}

create_venv_boilerplate(){
    echo "________________"
    if [ ! -d ".venv" ]; then
        py -m venv .venv
        
        source .venv/Scripts/activate
        if [ ! -f "requirements.txt" ]; then
            pip install pylint pygame pytest
            pip freeze > requirements.txt
        else
            echo "[create_venv_bp] requirements.txt already exists"
            pip install -r requirements.txt
        fi
    else
        echo "[create_venv_bp] .venv already exists"
    fi
    echo "________________"
}

create_git_boilerplate(){
    echo "________________"
    if [ ! -d ".git" ]; then
        git init
        {
            echo ".venv/"
            echo "__pycache__/"
            echo ".vscode"
            echo ".DS_Store"
        } >> .gitignore
    else 
        echo "[create_git_bp] this is already a git repos"
    fi
    echo "________________"
}

create_app_boilerplate(){
    mkdir -p app/models app/utils app/decorators app/plugins
    touch app/models/__init__.py app/utils/__init__.py app/decorators/__init__.py app/plugins/__init__.py
}   

create_root_boilerplate(){
    touch pylint.toml
    touch .gitlab-ci.yml
    touch main.py
    touch Makefile
    mkdir -p docs/models docs/plan
    touch docs/models/chip8.puml docs/models/software.puml
    touch docs/plan/gantt.mw
    mkdir -p utils data/chip8_softwares decorators plugins
}

create_pre_boilerplate(){
    mkdir -p pre/models pre/utils pre/decorators pre/plugins
    touch pre/models/__init__.py pre/utils/__init__.py pre/decorators/__init__.py pre/plugins/__init__.py
}

ui (){
    echo "1) create_pre_boilerplate"
    echo "2) create_root_boilerplate"
    echo "3) create_app_boilerplate"
    echo "4) create_git_boilerplate"
    echo "5) create_venv_boilerplate"
    echo "6) bash_boilerplate"
    read -r -p "Make a choice: " choice
    case $choice in
        1) create_pre_boilerplate ;;
        2) create_root_boilerplate ;; 
        3) create_app_boilerplate ;; 
        4) create_git_boilerplate ;; 
        5) create_venv_boilerplate ;;
        6) create_bash_boilerplate ;; 
        *) display_msg "unknown choice" ;;
    esac
}

ui
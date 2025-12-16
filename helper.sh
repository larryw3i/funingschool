#!/bin/bash

project_dir=$(dirname "$(readlink -f "$0")")
venv_dir=${project_dir}/venv
src_dir=${project_dir}/src
fnschoo1_dir=${src_dir}/fnschoo1
db_cp_dir=${fnschoo1_dir}/.db_cp

if [[ ! -d ${venv_dir} ]]; then
    python3 \
        -m venv \
        venv \
        --system-site-packages
fi

. ${venv_dir}/bin/activate

copy_db() {
    db_path=${fnschoo1_dir}/db.sqlite3
    user_name=""
    if [ -z "$1" ]; then
        user_name="$(whoami)"
    else
        user_name="$1"
    fi
    if [ ! -d "${db_cp_dir}" ]; then
        mkdir -p ${db_cp_dir}
    fi
    db_copy_path=${db_cp_dir}/db.${user_name}.$(date +%Y%m%d%H%M%S).$(uuid).sqlite3
    cp ${db_path} ${db_copy_path}
    echo "'${db_path}' has been copied to '${db_copy_path}' ."
}

generate_code_txt() {
    code_out_path=${project_dir}/code.out.txt
    echo "" >${code_out_path}
    files=$(
        find src \
            -type d \( -name ".egg-info" -o -name "*.egg-info" \) -prune \
            -o -type f \( -name "*.py" -o -name "*.po" -o -name "*.html" -o -name "*.js" ! -name "*.min.js" \) -print
    )
    for f in ${files[@]}; do
        echo "File: ${f}" >>${code_out_path}
        cat ${f} >>${code_out_path}
    done
}

pack() {
    if [[ ! -f $(which twine) ]]; then
        pip install -U setuptools wheel build twine
    fi
    new_version=$(date +"%Y%m%d.8%H%M.8%S")
    sed -i "s/\(__version__ = \"\)[^\"]*\(\"\)/\1$new_version\2/g" ${fnschoo1_dir}/__init__.py
    echo "New version is ${new_version} ."
    cd ${fnschoo1_dir}
    python manage.py migrate
    python manage.py compilemessages
    cd ${project_dir}
    python -m build
}

pack_upload() {
    cd ${project_dir}
    rm -rf dist/*
    pack
    twine upload dist/*
}

format_code() {
    run_prettier() {
        if [[ "$(which prettier)" != *"/bin/prettier" ]]; then
            echo "Trying to install prettier ..."
            mkdir -p ${HOME}/.npm-global
            npm config set prefix "${HOME}/.npm-global"
            export PATH=${HOME}/.npm-global/bin:$PATH
            npm i -g prettier
        fi
        export PATH=${HOME}/.npm-global/bin:$PATH
        prettier \
            ${src_dir} \
            ${project_dir}/.djlintrc.json \
            ${project_dir}/.prettierrc.json \
            --config ${project_dir}/.prettierrc.json \
            --ignore-path ${project_dir}/.prettierignore \
            --write
    }

    run_djlint() {
        djlint_dir=$(find ${project_dir}/venv/lib/ -type d -name 'djlint')
        if [[ ! ${djlint_dir} ]]; then
            pip install djlint
        fi
        djlint \
            ${src_dir} \
            --reformat \
            --statistics \
            --configuration \
            ${project_dir}/.djlintrc.json
    }

    run_isort() {
        if [[ ! -x $(which isort) ]]; then
            echo 'Trying to install "isort"...'
            sudo apt install isort
        fi
        if [[ -x $(which isort) ]]; then
            isort \
                -l 80 \
                ${fnschoo1_dir} \
                ${project_dir}/manage.py
        fi
    }

    run_shfmt() {
        if [[ ! -x $(which shfmt) ]]; then
            echo 'Trying to install "shfmt"...'
            sudo apt install shfmt
        fi
        if [[ -x $(which shfmt) ]]; then
            shfmt \
                -i 4 \
                -l \
                -s \
                -w ${project_dir}
        fi
    }

    run_black() {
        if [[ ! -x $(which black) ]]; then
            echo "Trying to install $(black)..."
            sudo apt install black
        fi
        if [[ -x $(which black) ]]; then
            black \
                -l 80 \
                ${fnschoo1_dir} \
                ${project_dir}/manage.py
        fi
    }

    run_djlint
    run_shfmt
    run_isort
    run_black
    run_prettier
}

if [[ $# -eq 0 ]]; then
    echo "I'm helper of Project FUNINGSCHOOL."
else
    $1 ${@:2}
fi

# The end.

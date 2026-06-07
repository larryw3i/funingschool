#!/bin/bash

project_dir=$(dirname "$(readlink -f "$0")")
venv_dir=${project_dir}/venv
src_dir=${project_dir}/src
fnschoo1_dir=${src_dir}/fnschoo1
db_cp_dir=${fnschoo1_dir}/.db_cp
released_hashes_path=${project_dir}/release/SHA256es

pyhelper_name="helper"
pyhelper_dir=${project_dir}/${pyhelper_name}
pyhelper_locale_dir=${pyhelper_dir}/locale

fnschool_static_dir=${fnschoo1_dir}/static
fnschool_static_node_modules_dir=${fnschool_static_dir}/node_modules

if [[ ! -d ${venv_dir} ]]; then
    python \
        -m venv \
        --system-site-packages \
        venv
    . ${venv_dir}/bin/activate
    python -m helper project -d -i
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
            -type d \
            \( \
            -name ".egg-info" \
            -o -name "*.egg-info" \
            \) \
            -prune \
            -o \
            -type f \
            \( \
            -name "*.py" \
            -o -name "*.po" \
            -o -name "*.html" \
            -o -name "*.js" \
            ! -name "*.min.js" \
            \) \
            -print
    )
    for f in ${files[@]}; do
        echo "File: ${f}" >>${code_out_path}
        cat ${f} >>${code_out_path}
    done
}

cp_node_modules() {
    if [[ ! -f $(which npm) ]]; then
        echo "Try to instll npm and nodejs ."
        sudo apt install npm nodejs
    fi
    PWD_CP=${PWD}
    cd ${fnschool_static_dir}
    if [[ ! -d ${fnschool_static_node_modules_dir} ]]; then
        npm install
    fi
    _fnschool_static_node_modules_dir=${fnschool_static_node_modules_dir/%\/node_modules/\/_node_modules_}
    if [[ -d ${_fnschool_static_node_modules_dir} ]]; then
        rm -rfvv ${_fnschool_static_node_modules_dir}
    fi
    if [[ -d ${fnschool_static_node_modules_dir}/node_modules ]]; then
        rm -rfvv ${fnschool_static_node_modules_dir}/node_modules
    fi
    cd ${fnschool_static_node_modules_dir}
    module_files=$(
        find ${PWD} \
            -type f \
            \( \
            -path "*/@popperjs/*" \
            -o -path "*/bootstrap/*" \
            -o -path "*/jquery/*" \
            \) \
            \( \
            -name "*.min.js" \
            -o -name "*.min.js.map" \
            -o -name "*.min.css" \
            -o -name "*.min.css.map" \
            -o -name "*LICENSE*" \
            -o -name "*AUTHORS*" \
            \)
    )
    for m_file in ${module_files[@]}; do
        _m_file=${m_file/\/node_modules\//\/_node_modules_\/}
        _m_file=${_m_file/\/dist\//\/_dist_\/}
        mkdir -p $(dirname ${_m_file})
        cp -vv ${m_file} ${_m_file}
    done
    cd ${PWD_CP}
}

pack() {
    new_version=""
    if [ $# -eq 0 ]; then
        new_version="$(date +"%Y%m%d.8%H%M.8%S")"
    else
        new_version="${1}"
    fi
    fnschool_static_node_modules_dir_cp=${project_dir}/node_modules.cp
    cp_node_modules
    mv -vv ${fnschool_static_node_modules_dir} ${fnschool_static_node_modules_dir_cp}
    if [[ ! -f $(which twine) ]]; then
        pip install -U setuptools wheel build twine
    fi
    sed -i "s/\(__version__ = \"\)[^\"]*\(\"\)/\1$new_version\2/g" ${fnschoo1_dir}/__init__.py
    echo "New version is ${new_version} ."
    cd ${fnschoo1_dir}
    python manage.py migrate
    python manage.py compilemessages
    cd ${project_dir}
    python -m build
    mv -vv ${fnschool_static_node_modules_dir_cp} ${fnschool_static_node_modules_dir}
    echo "Generated new version is \"${new_version}\" ."
}

pack_upload() {
    pwd_cp=${PWD}
    released_hashes_cp_path=${released_hashes_path}.cp
    cd ${project_dir}
    rm -rf dist/*
    new_version="$(date +"%Y%m%d.8%H%M.8%S")"
    pack "${new_version}"
    cd dist
    sha256sum * >${released_hashes_cp_path}
    cat ${released_hashes_path} >>${released_hashes_cp_path}
    mv ${released_hashes_cp_path} ${released_hashes_path}
    cd ${project_dir}
    twine upload dist/*
    cd ${pwd_cp}
    echo "Updated new version is \"${new_version}\" ."
}

format_code() {
    run_prettier() {
        export PATH=${HOME}/.npm-global/bin:$PATH
        if [[ "$(which prettier)" != *"/bin/prettier" ]]; then
            echo "Trying to install prettier ..."
            mkdir -p ${HOME}/.npm-global
            npm config set prefix "${HOME}/.npm-global"
            export PATH=${HOME}/.npm-global/bin:$PATH
            npm i -g prettier
        fi
        echo "Starting prettier ..."
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
        echo "Starting djlint ..."
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
            echo "Starting isort ..."
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
            echo "Starting shfmt ..."
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
            echo "Starting black ..."
            black \
                -l 80 \
                --fast \
                ${fnschoo1_dir} \
                ${project_dir}/manage.py \
                ${pyhelper_dir}
        fi
    }

    run_djlint
    run_shfmt
    run_isort
    run_black
    run_prettier
}

xgettext_pyhelper() {
    pot_file=${pyhelper_locale_dir}/${pyhelper_name}.pot
    find ${pyhelper_dir} -name "*.py" -print | xgettext --language=Python -o ${pot_file} -f -
    if [[ ! -f ${pot_file} ]]; then
        echo "File \"${pot_file}\" not found."
        exit 1
    fi
    for d in $(ls ${pyhelper_locale_dir}); do
        lang=${d}
        d=${pyhelper_locale_dir}/${d}
        if [[ -d ${d} ]]; then
            lc_msg_dir=${d}/LC_MESSAGES
            po_file=${lc_msg_dir}/${pyhelper_name}.po
            if [[ ! -d ${lc_msg_dir} ]]; then
                mkdir -p ${lc_msg_dir}
            fi

            if [[ ! -f ${po_file} ]]; then
                msginit -i ${pot_file} -l ${lang}.UTF-8 -o ${po_file}
            else
                msgmerge --update -vv ${po_file} ${pot_file}
            fi

        fi
    done
}

msgfmt_pyhelper() {
    for d in $(ls ${pyhelper_locale_dir}); do
        lang=${d}
        d=${pyhelper_locale_dir}/${d}
        if [[ -d ${d} ]]; then
            lc_msg_dir=${pyhelper_locale_dir}/${lang}/LC_MESSAGES
            po_file=${lc_msg_dir}/${pyhelper_name}.po
            mo_file=${lc_msg_dir}/${pyhelper_name}.mo
            msgfmt -vv -o ${mo_file} ${po_file}
        fi
    done
}

run_xgettext() {
    xgettext_pyhelper
    python manage.py makemessages -a
}

run_msgfmt() {
    msgfmt_pyhelper
    python manage.py compilemessages
}

gen_doc() {
    msgfmt_pyhelper
    python -m helper docs -g
}

if [[ $# -eq 0 ]]; then
    echo "I'm helper of Project FUNINGSCHOOL."
else
    $1 ${@:2}
fi

# The end.

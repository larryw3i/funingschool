#!/bin/bash

project_dir=$(dirname "$(readlink -f "$0")")
venv_dir=${project_dir}/venv
src_dir=${project_dir}/src

if [[ ! -d ${venv_dir} ]]; then
    python3 -m venv venv --system-site-packages
fi

. ${venv_dir}/bin/activate

run_djlint() {
    djlint_dir=$(find ${project_dir}/venv/lib/ -type d -name 'djlint')
    if [[ ! ${djlint_dir} ]]; then
        pip install djlint
    fi
    djlint ${src_dir} \
        --reformat \
        --indent 2 \
        --statistics \
        --max-line-length 80 \
        --profile django

}

run_isort() {
    if [[ ! -x $(which isort) ]]; then
        echo 'Trying to install "isort"...'
        sudo apt install isort
    fi
    if [[ -x $(which isort) ]]; then
        isort -l 80 ${project_dir}
    fi
}

run_shfmt() {
    if [[ ! -x $(which shfmt) ]]; then
        echo 'Trying to install "shfmt"...'
        sudo apt install shfmt
    fi
    if [[ -x $(which shfmt) ]]; then
        shfmt -i 4 -l -s -w ${project_dir}
    fi
}

run_black() {
    if [[ ! -x $(which black) ]]; then
        echo "Trying to install $(black)..."
        sudo apt install black
    fi
    if [[ -x $(which black) ]]; then
        black -l 80 ${project_dir}
    fi
}

run_djlint
run_shfmt
run_isort
run_black

# The end.

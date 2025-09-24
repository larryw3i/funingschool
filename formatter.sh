#!/bin/bash

venv_dir=${PWD}/venv
src_dir=${PWD}/src

if [[ ! -d ${venv_dir} ]]; then
    python3 -m venv venv --system-site-packages
fi

. ${venv_dir}/bin/activate

run_djlint() {
    if [[ ! "$(find venv/lib/ -type d -name 'djlint')" ]]; then
        pip install djlint
    fi
    djlint ${src_dir} --reformat --indent 2 --statistics --max-line-length 80
}

run_shfmt() {
    if [[ ! -x $(which shfmt) ]]; then
        echo "Trying to install $(shfmt)..."
        sudo apt install shfmt
    fi
    if [[ -x $(which shfmt) ]]; then
        shfmt -i 4 -l -s -w ${PWD}
    fi
}

run_black() {
    if [[ ! -x $(which black) ]]; then
        echo "Trying to install $(black)..."
        sudo apt install black
    fi
    if [[ -x $(which black) ]]; then
        black -l 80 ${PWD}
    fi
}

run_djlint
run_shfmt
run_black

# The end.

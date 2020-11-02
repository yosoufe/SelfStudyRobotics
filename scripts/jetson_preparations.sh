#!/bin/bash
PYENV_LOCATION=`realpath ~/.pyenv`

if [ -d "$PYENV_LOCATION" ]; then
    echo "pyenv already exists at ${PYENV_LOCATION}!"
else
    git clone https://github.com/pyenv/pyenv.git $PYENV_LOCATION
    sudo apt-get update
    sudo apt-get install -y --no-install-recommends \
        make \
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        wget \
        curl \
        llvm \
        libncurses5-dev \
        xz-utils \
        tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libffi-dev \
        liblzma-dev
fi


if `grep -q "pyenv setup" ~/.bashrc`; then
    echo "pyenv already exits in ~/.bashrc"
    echo "If you need to update it, please remove it manually"
else
    echo 'Adding pyenv to ~/.bashrc'
    echo '' >> ~/.bashrc
    echo '' >> ~/.bashrc
    echo '# pyenv setup' >> ~/.bashrc
    echo "export PYENV_ROOT=${PYENV_LOCATION}" >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
    exec "$SHELL"
fi
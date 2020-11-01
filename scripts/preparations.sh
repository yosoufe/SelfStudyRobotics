#!/bin/bash
PYENV_LOCATION=`realpath ~/.pyenv`

if [ -d "$PYENV_LOCATION" ]; then
    echo "pyenv exists!"
else
    git clone https://github.com/pyenv/pyenv.git $PYENV_LOCATION
    cd $PYENV_LOCATION
fi


if `grep -q "pyenv setup" ~/.bashrc`; then
    echo "pyenv already in ~/.bashrc"
else
    echo 'Adding pyenv to ~/.bashrc'
    echo '' >> ~/.bashrc
    echo '' >> ~/.bashrc
    echo '# pyenv setup' >> ~/.bashrc
    echo 'export PYENV_ROOT="$PYENV_LOCATION"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
fi
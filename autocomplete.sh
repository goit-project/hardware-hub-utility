COLOR_HIGHLIGHT='\e[32;1m'
COLOR_ERROR='\e[31;1m'
COLOR_DEFAULT='\e[0m'
PATH_INSTALL='/usr/local/bin/epa'
PATH_SCRIPT=$(realpath "$0")
PATH_EPA=$(dirname "$PATH_SCRIPT")/epa
PATH_COMPLETE=$(dirname "$PATH_SCRIPT")/autocomplete
PATH_USER_HOME=$(eval echo ~$USER)
BASH_AUTOCOMPLETE_DO_LOAD=false
BASH_AUTOCOMPLETE_DO_INIT=false

# echo - highlight
echo_high () {
  echo -en $COLOR_HIGHLIGHT
  echo "${@:1}"
  echo -en $COLOR_DEFAULT
}

# echo - fatal error
echo_error () {
  echo -en $COLOR_ERROR
  echo "${@:1}"
  echo -en $COLOR_DEFAULT
}

# echo - general info
echo_info () {
  echo "${@:1}"
}

# autocomplete - zshell
echo_high ">>> Configuring autocomplete <<<"
if [[ $SHELL == *"zsh" ]]; then
  echo_info "Enabling bashautocomplete in ZSHELL"

  echo_info "Checking if bashcompinit autoload is set in '.zshrc'"
  if ! grep "^autoload *bashcompinit" "$PATH_USER_HOME/.zshrc" >/dev/null; then
    BASH_AUTOCOMPLETE_DO_LOAD=true
  fi

  echo_info "Checking if bashcompinit called in '.zshrc'"
  if ! grep "^bashcompinit" "$PATH_USER_HOME/.zshrc" >/dev/null; then
    BASH_AUTOCOMPLETE_DO_INIT=true
  fi


  if $BASH_AUTOCOMPLETE_DO_LOAD || $BASH_AUTOCOMPLETE_DO_INIT; then
    echo_info "Updating '.zshrc'"

    echo -e "\n# Enabling bash autocomplete functionality" >> "$PATH_USER_HOME/.zshrc"
    $BASH_AUTOCOMPLETE_DO_LOAD    && echo "autoload bashcompinit" >> "$PATH_USER_HOME/.zshrc" &&
      echo "'autoload bashcompinit >> ~/.zshrc'"
    $BASH_AUTOCOMPLETE_DO_INIT    && echo "bashcompinit"          >> "$PATH_USER_HOME/.zshrc" &&
      echo "'bashcompinit >> ~/.zshrc'"
  fi

  echo "Enabling argument completion for goit utility in ZSH"
  eval "$(register-python-argcomplete goit)"
fi


# autocomplete - bash
if [[ $SHELL == *"bash" ]]; then
  echo_info "Enabling autocomplete for goit utility in BASH"
  eval "$(register-python-argcomplete goit)"
fi

echo_info "Done"

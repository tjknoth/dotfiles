# P10k instant prompt
[[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]\
  &&\
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"

# Oh-my-zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"
plugins=(git)
source $ZSH/oh-my-zsh.sh

# PATH additions (conditional)
[[ -d "$HOME/.cargo/bin" ]] && path+="$HOME/.cargo/bin"
[[ -d "$HOME/.local/bin" ]] && path+="$HOME/.local/bin"
[[ -d "/Applications/Visual Studio Code.app" ]] && path+="/Applications/Visual
 Studio Code.app/Contents/Resources/app/bin"

# Secrets (not version controlled)
[[ -f ~/.secrets ]] && source ~/.secrets

# pyenv
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && path+="$PYENV_ROOT/bin"
command -v pyenv &>/dev/null && eval "$(pyenv init -)"

# nvm
export NVM_DIR="$HOME/.nvm"
[[ -s "$NVM_DIR/nvm.sh" ]] && source "$NVM_DIR/nvm.sh"

# ghcup
[[ -f "$HOME/.ghcup/env" ]] && source "$HOME/.ghcup/env"

# p10k
[[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh

unsetopt share_history
DEFAULT_USER=$USER

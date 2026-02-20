# Auto-attach to tmux over SSH (before p10k instant prompt to avoid console output warning)
# Skip if 'main' session already has an attached client (e.g. new tab)
if [[ -n "$SSH_CONNECTION" && -z "$TMUX" ]] && command -v tmux &>/dev/null && [[ -t 0 ]]; then
  if ! tmux has-session -t main 2>/dev/null || [[ -z "$(tmux list-clients -t main)" ]]; then
    exec tmux new-session -A -s main
  fi
fi

# P10k instant prompt
[[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]\
  &&\
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"

# Oh-my-zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"
export NVM_LAZY_LOAD=true
plugins=(git zsh-nvm)
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

# nvm (managed by zsh-nvm plugin above)

# ghcup
[[ -f "$HOME/.ghcup/env" ]] && source "$HOME/.ghcup/env"

# p10k
[[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh

unsetopt share_history
DEFAULT_USER=$USER

# Machine-local overrides (not version controlled)
[[ -f ~/.zshrc.local ]] && source ~/.zshrc.local

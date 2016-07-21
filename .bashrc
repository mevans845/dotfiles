source ~/.shrc

# Better history
export HISTCONTROL=ignoreboth
export HISTSIZE=1000
export HISTIGNORE="ls:pwd:exit"


# File navigation aliases
alias ..='cd ..'
alias _='cd -'
alias ls='ls -hF -G'  # add colors for filetype recognition
alias ll='ls -l -h'
alias la='ls -A'
alias du='du -kh' 
alias df='df -kTh'

# Colored output in grep
alias grep='grep --color=auto'

# Making solarized work with tmux
alias tmux="TERM=screen-256color-bce tmux"

# bash-completion
if [ -f /opt/local/etc/profile.d/bash_completion.sh ]; then
    . /opt/local/etc/profile.d/bash_completion.sh
fi

function _update_ps1()
{
  export PS1="$(~/powerline-shell.py $?)"
}

export PS1="\w "

# Poweline style bash prompt!
# export PROMPT_COMMAND="_update_ps1"

##########################################################################
# Git aliases (with bash completion!)                                    #
# Note: __git_complete is not a public function, so completion can break #
##########################################################################
function _make_git_alias()
{
    local shortname=$1
    local longname=$2
    shift
    local rest=""
    while [ $# -gt 0 ]; do
        rest=$rest" $1"
        shift
    done
    rest='git'$rest
    alias $shortname="$rest"

    if [[ $(_exists __git_complete) -ne 0 ]]; then
        __git_complete $shortname _git_$longname
    fi
}
_make_git_alias g1 log --oneline
_make_git_alias ga add
_make_git_alias gb branch
_make_git_alias gc commit
_make_git_alias gco checkout
_make_git_alias gcm commit -m
_make_git_alias gca commit -am
_make_git_alias gcl clone
_make_git_alias gd diff
_make_git_alias gf fetch
_make_git_alias gl log
_make_git_alias gp push
_make_git_alias gpu pull
_make_git_alias grm rm
_make_git_alias gst status

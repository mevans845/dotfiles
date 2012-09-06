# MacPorts Installer addition on 2012-09-03_at_00:20:36: adding an appropriate PATH variable for use with MacPorts.
export PATH=/opt/local/bin:/opt/local/sbin:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.

# Use vi mode for editing commands
set -o vi

# Opens files in a single MacVim server.
# Picks the first server in serverlist if there are multiple servers
function OpenInMacVim {
    server=$(mvim --serverlist | head -1)
    if [ -n "$server" ]; then
        if [ -z "$1" ]; then
            osascript -e 'tell application "MacVim" to activate' 
        else
            mvim --servername $server --remote-tab $@
        fi
    else
        mvim $@
    fi
}

if [[ $(command -v mvim > /dev/null 2>&1; echo $?) -eq 0 ]];
then
    alias vi='OpenInMacVim'
fi


# File navigation aliases
alias cd..='cd ..'
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

# Poweline style bash prompt!
export PROMPT_COMMAND="export PS1=\$(~/powerline-bash.py \$?)"
# For tmux powerline support
# export PS1="$PS1"'$([ -n "$TMUX" ] && tmux setenv TMUXPWD_$(tmux display -p "#I_#P") "$PWD")'

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
    __git_complete $shortname _git_$longname
}
_make_git_alias g1 log --oneline
_make_git_alias ga add
_make_git_alias gb branch
_make_git_alias gc checkout
_make_git_alias gcl clone
_make_git_alias gd diff
_make_git_alias gf fetch
_make_git_alias gl log
_make_git_alias gm commit -m
_make_git_alias gma commit -am
_make_git_alias gp push
_make_git_alias gpu pull
_make_git_alias gr rebase
_make_git_alias gs status


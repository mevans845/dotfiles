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

alias vi='OpenInMacVim'

# bash-completion
if [ -f /opt/local/etc/profile.d/bash_completion.sh ]; then
    . /opt/local/etc/profile.d/bash_completion.sh
fi

##
# Your previous /Users/shrey/.bash_profile file was backed up as /Users/shrey/.bash_profile.macports-saved_2012-09-03_at_00:20:36
##

# MacPorts Installer addition on 2012-09-03_at_00:20:36: adding an appropriate PATH variable for use with MacPorts.
export PATH=/opt/local/bin:/opt/local/sbin:$PATH
# Finished adapting your PATH environment variable for use with MacPorts.

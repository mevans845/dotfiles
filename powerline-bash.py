#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import os
import subprocess
import sys

class Powerline:
    def __init__(self):
        self.segments = []
        self.separator = '⮀'
        self.ESC = '\e'
        self.LSQ = '\\['
        self.RSQ = '\\]'
        self.clear_fg = self.LSQ + self.ESC + '[38;0m' + self.RSQ
        self.clear_bg = self.LSQ + self.ESC + '[48;0m' + self.RSQ

    def append(self, content, fg, bg):
        segment = {'content': str(content), 'fg': str(fg), 'bg': str(bg)}
        self.segments.append(segment)

    def color(self, prefix, code):
        return self.LSQ + self.ESC + '[' + prefix + ';5;' + code + 'm' + self.RSQ

    def fgcolor(self, code):
        return self.color('38', code)

    def bgcolor(self, code):
        return self.color('48', code)

    def draw(self):
        i=0
        line=''
        while i < len(self.segments)-1:
            s = self.segments[i]
            ns = self.segments[i+1]
            line += self.fgcolor(s['fg']) + self.bgcolor(s['bg']) + s['content']
            line += self.fgcolor(s['bg']) + self.bgcolor(ns['bg']) + self.separator
            i += 1
        s = self.segments[i]
        line += self.fgcolor(s['fg']) + self.bgcolor(s['bg']) + s['content']
        line += self.clear_bg + self.fgcolor(s['bg']) + self.separator + self.clear_fg
        return line

def get_git_branch():
    try:
        output = subprocess.check_output("git branch 2> /dev/null | grep -e '\*'", shell=True)
        return output[2:].rstrip()
    except subprocess.CalledProcessError:
        return ''

if __name__ == '__main__':
    last_cmd_error = sys.argv[1]

    p = Powerline()
    p.append(' ' + getpass.getuser().upper() + ' ', 250, 238)
    p.append(' \w ', 15, 237)

    git_branch = get_git_branch()
    if len(git_branch) > 0:
        p.append(' ' + git_branch + ' ', 0, 148)

    if int(last_cmd_error) == 0:
        p.append('\$', 7, 239)
    else:
        p.append('\$', 237, 130)

    print p.draw(),

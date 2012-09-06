#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

class Powerline:
    separator = '⮀'
    separator_thin="⮁"
    ESC = '\e'
    LSQ = '\['
    RSQ = '\]'
    clear_fg = LSQ + ESC + '[38;0m' + RSQ
    clear_bg = LSQ + ESC + '[48;0m' + RSQ

    def __init__(self):
        self.segments = []

    def append(self, content, fg, bg, separator=None, separator_fg=None):
      if separator == None:
        separator = self.separator
      if separator_fg == None:
        separator_fg = bg
      segment = {
          'content': str(content),
          'fg': str(fg),
          'bg': str(bg),
          'separator': str(separator),
          'separator_fg': str(separator_fg)
          }
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
            line += self.fgcolor(s['separator_fg']) + self.bgcolor(ns['bg']) + s['separator']
            i += 1
        s = self.segments[i]
        line += self.fgcolor(s['fg']) + self.bgcolor(s['bg']) + s['content']
        line += self.clear_bg + self.fgcolor(s['separator_fg']) + s['separator'] + self.clear_fg
        return line

def add_git_segment(powerline):
    try:
        branch = subprocess.check_output(
            "git branch 2> /dev/null | grep -e '\*'",
            shell=True).rstrip()[2:]
        p.append(' ' + branch + ' ', 22, 148)
    except subprocess.CalledProcessError:
      pass

# Show working directory with fancy separators
def add_cwd_segment(powerline):
    #p.append(' \w ', 15, 237)
    home = os.getenv('HOME')
    cwd = os.getcwd()
    if cwd.find(home) == 0:
      cwd = cwd.replace(home, '~', 1)
    names = cwd.split('/')
    for n in names[:-1]:
      powerline.append(' ' + n + ' ', 250, 237, Powerline.separator_thin, 244)
    powerline.append(' ' + names[-1] + ' ', 254, 237)

def add_root_indicator(powerline, error):
    bg = 236
    fg = 15
    if int(error) != 0:
        fg = 15
        bg = 161
    p.append(' \$ ', fg, bg)

if __name__ == '__main__':
    p = Powerline()
    p.append(' \u ', 250, 240)
    p.append(' \h ', 250, 238)
    add_cwd_segment(p)
    add_git_segment(p)
    add_root_indicator(p, sys.argv[1] if len(sys.argv) > 1 else 0)
    print p.draw(),

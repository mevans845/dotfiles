import os
import subprocess
import shlex
import sys


HOME_DIR = os.getenv("HOME")
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
OH_MY_ZSH_DIR = os.path.join(HOME_DIR, ".oh-my-zsh")


def is_linked(src_path, dest_path):
    try:
        return os.readlink(dest_path) == src_path
    except OSError:
        pass
    return False


def run_silent(command):
    return subprocess.run(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)


def run(command):
    return subprocess.run(shlex.split(command))


def run_shell(command):
    return subprocess.run(shlex.split(command), shell=True)


class Requirement(object):
    def is_satisfied(self):
        raise NotImplementedError()

    def install(self):
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__


class SymlinkRequirement(Requirement):
    def _get_paths():
        # Should yield (src, dest) pairs
        raise NotImplementedError()

    def is_satisfied(self):
        for src_path, dest_path in self._get_paths():
            assert os.path.exists(src_path), "%s doesn't exist" % src_path
            if is_linked(src_path, dest_path):
                continue
            return False
        return True

    def install(self):
        for src_path, dest_path in self._get_paths():
            if is_linked(src_path, dest_path):
                continue
            if os.path.exists(dest_path):
                if input("%s already exists. Replace? [y/N]: " %
                         dest_path) != "y":
                    continue
                os.remove(dest_path)
            os.symlink(src_path, dest_path)


class Brew(Requirement):
    def is_satisfied(self):
        ret = run_silent("brew bundle check")
        return ret.returncode == 0

    def install(self):
        run("brew bundle -v")


class Pip3(Requirement):
    packages = {
        "ipython"
    }

    def is_satisfied(self):
        import json
        ret = run_silent("pip3 list --format=json")
        json = json.loads(ret.stdout.decode("utf-8"))
        missing = self.packages - set(row["name"] for row in json)
        return not missing

    def install(self):
        run("pip3 install %s" % " ".join(self.packages))


class OhMyZsh(Requirement):
    def is_satisfied(self):
        return os.path.exists(OH_MY_ZSH_DIR)

    def install(self):
        import urllib.request
        filename, _ = urllib.request.urlretrieve(
            "https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/"
            "tools/install.sh")
        run("chmod u+x %s" % filename)
        run_shell(filename)


class OhMyZshCustomPlugins(SymlinkRequirement):
    def _get_paths(self):
        for plugin in ["git", "gitfast"]:
            plugin_dir = "custom/plugins/%s" % plugin
            yield os.path.join(SRC_DIR, "zsh", plugin_dir), \
                os.path.join(OH_MY_ZSH_DIR, plugin_dir)


class SublimeSyncing(SymlinkRequirement):
    def _get_paths(self):
        yield (os.path.join(HOME_DIR, "Dropbox/Sublime/User"),
               os.path.join(
                HOME_DIR,
                "Library/Application Support/Sublime Text 3/Packages/User"))


class Dotfiles(SymlinkRequirement):
    def _get_paths(self):
        filenames = [
            ".shrc",
            ".zshrc",
            ".vimrc",
            ".quip.shrc",
            ".quip.vimrc",
            ".slate.js"
        ]
        for filename in filenames:
            src_path = os.path.join(SRC_DIR, filename)
            dest_path = os.path.join(HOME_DIR, filename)
            yield src_path, dest_path


def main(dry_run=False):
    requirements = [
        Dotfiles(),
        Brew(),
        Pip3(),
        OhMyZsh(),
        OhMyZshCustomPlugins(),
        SublimeSyncing(),
    ]

    for requirement in requirements:
        if requirement.is_satisfied():
            print("%s: PASSED" % requirement)
        else:
            print("%s: FAILED" % requirement)
            if not dry_run:
                print("Installing %s" % requirement)
                requirement.install()

    still_failing = [requirement for requirement in requirements
                     if not requirement.is_satisfied()]

    if still_failing:
        print("Some requirements still failed:")
        for requirement in still_failing:
            print("  ", requirement)
        sys.exit(1)

    print("Setup complete")
    print("""
Now you need to:
    - Setup ssh keys
    - Install 1Password
    - Change default shell to zsh
    - Sign-in to Dropbox
    - Set iTerm2 to load preferences from ~/Dropbox/iTerm2
    - Activate Alfred, Sublime Text, 1Password
""")


if __name__ == "__main__":
    main()

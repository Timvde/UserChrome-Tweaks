#Contributing to UserChrome Tweaks

First of all, thank you for your interest in contributing! Here are some guidelines.

##Code style

* For indentation, 2 spaces are used.
* Comments that span multiple lines, have an empty first and last line, like so:
```
/*
 * Multi-line comment here.
 */
```
* Comment that span only a single line, can use the previous style, or be compacted in one line, where comment delimiters are separated from the comment with one space:
```
/* Single-line comment here. */
```
* If there are differences in the CSS used between platforms, please use separate, self-containing files. This might lead to duplicate code, but will ease the installation process.

Please try to follow these guidelines. By contributing to UserChrome Tweaks, you agree that your code will be adapted to follow these guidelines, if it does not already do so.

##Naming files

No CSS files will be placed at the top level. Suitable subdirectories will be created, with `misc` being a left-over subdirectory which contains miscellaneous tweaks that do not fit anywhere else.

Filename use snake-case. If a file contains platform-specific CSS, the platform is included as a suffix, i.e. `-Linux`, `-macOS`, `-Windows`. Suffixes are put in alphabetical order. Files that apply on all platforms, should not include a suffix.

## Licensing

This repository is licensed under GPLv3. For practical reasons, by contributing, you automatically agree that your code is relicensed as GPLv3. If the submitted code includes a copyright notice, it is adopted. If it doesn't, you certify that the code is written by yourself. Since GPL requires explicit attribution, your GitHub username is chosen in this case.

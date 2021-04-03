# A community maintained repository of userChrome.css tweaks for Firefox

Every file should only contain a single, specific tweak. No full themes or anything. Users of this repository should be able to easily combine the different tweaks into a setup of their liking.

Incompatibilities between different files can happen. There's not much we can do about it. Just keep this in mind.

The master branch should always track Nightly. When a version merges into beta, a new branch is created for this specific Firefox version. If any code is broken on this branch, it is possible to cherry-pick the necessary commits without pulling other broken code in.

If you wish to contribute to this repository, please read `CONTRIBUTING.md`.

## How to use
1. Find your profile folder in Firefox: write in address field "about:support" > Profile Folder > Open Folder.
2. Create folder chrome and subfolders config, css, image.
3. Create two files in the chrome folder: userChrome.css, userContent.css.
4. Open userChrome.css in a text editor and paste in the relevant code block as is on the tweak page you are interested in (example  UserChrome-Tweaks/toolbars/show-bookmarks-only-on-newtab.css).
5. Restart Firefox.

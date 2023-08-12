# How to change default view as lists in MAC OS finder
1. Open finder;
2. Go to the `My Computer`;
3. Right click `Macintosh HD`;
4. Click `Show View Options`;
5. Check the two boxes: `Always open in list view` and `Browse in list view`;
6. Clikc `Use as Defaults`;
7. Close the finder;
8. Open terminal;
9. Run `sudo find / -name .DS_Store -delete; killall Finder`;

# Accelerate Mouse Speed (when fastest speed in System Preference is still too slow)
```shell
# check the current scaling factor
defaults read -g com.apple.mouse.scaling

# Update the scaling factor
defaults write -g com.apple.mouse.scaling <factor>
```

# Pinyin Input
## Google Docs: MacOS Pinyin Candidate Window Does Not Follow the Cursor
1. Open "Accessibility" setting.
2. Check "Turn on screen magnifier support".
3. [Reference](https://github.com/rime/squirrel/issues/345)

# Add (Noto) Fonts to MacOS for Applications like Keynote to Use
1. Download the fonts
    - [Noto Serif Simplified Chinese](https://fonts.google.com/noto/specimen/Noto+Serif+SC)
    - [Noto Serif Traditional Chinese](https://fonts.google.com/noto/specimen/Noto+Serif+TC)
    - [Noto Sans Simplified Chinese](https://fonts.google.com/noto/specimen/Noto+Sans+SC)
    - [Noto Sans Traditional Chinese](https://fonts.google.com/noto/specimen/Noto+Sans+TC)
2. Double click the .otf files to install them.
3. Check the installed fonts in the Font Book app.
4. Now it can be used in applications like Keynote

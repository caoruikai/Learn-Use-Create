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

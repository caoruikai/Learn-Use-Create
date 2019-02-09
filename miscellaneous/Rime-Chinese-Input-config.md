# Minimum Configuration for using Rime Chinese Input on different OS

I peronally don't like to change a lot of useless configs, the only annoying default setting of Rime is the `Shift` key switchs between Chinese and English. My preference is to use the English input built in OS as default input method. Whenever I need to input Chinese, toggle to Rime using the OS hotkeys.

1. Add a patch yaml config file `default.custom.yaml` to correct path:

  - For Linux (Ubuntu 18.04, ibus-rime):  `~/.config/ibus/rime`
  
  - For MacOS (El Captain, 鼠须管): `"/Library/Input Methods/Squirrel.app/Contents/SharedSupport/"`
  
  - For Windows 10 (小狼毫）:
  
2. Write the following into the yaml file to stop using `Shift` to toggle between Chinese and English:

```yaml
patch:
  ascii_composer:
    good_old_caps_lock: true
    switch_key:
      Shift_L: noop
      Shift_R: noop
      Control_L: noop
      Control_R: noop
      Caps_Lock: clear
      Eisu_toggle: clear
```

3. Deploy Rime.

4. When typing for the first time using Rime, press `Control+\``. Choose`朙月拼音-简化字`.

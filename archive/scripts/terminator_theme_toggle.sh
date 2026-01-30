#!/bin/bash
LIGHT_THEME=solarized-light
DARK_THEME=solarized-dark
PROFILE="$(grep "profile = " ~/.config/terminator/config)"
if [[ $PROFILE == *$DARK_THEME ]]; then
  sed -i -e "s/\(profile = \).*/\1$LIGHT_THEME/" ~/.config/terminator/config
else 
  sed -i -e "s/\(profile = \).*/\1$DARK_THEME/" ~/.config/terminator/config
fi
PROFILE="$(grep "profile = " ~/.config/terminator/config)"
echo $PROFILE

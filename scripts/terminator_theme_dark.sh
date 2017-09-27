#!/bin/bash
LIGHT_THEME=solarized-light
DARK_THEME=solarized-dark
sed -i -e "s/\(profile = \).*/\1$DARK_THEME/" ~/.config/terminator/config
PROFILE="$(grep "profile = " ~/.config/terminator/config)"
echo $PROFILE

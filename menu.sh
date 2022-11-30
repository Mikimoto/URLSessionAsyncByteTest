#!/bin/bash

##
# Color  Variables
##

green='\e[32m'
blue='\e[34m'
red='\e[0;41;30m'
std='\e[0;0;39m'
clear='\e[0m'

##
# Color Functions
##

ColorGreen(){
	echo -ne $green$1$clear
}
ColorBlue(){
	echo -ne $blue$1$clear
}

# Renders a text based list of options that can be selected by the
# user using up, down and enter keys and returns the chosen option.
#
#   Arguments   : list of options, maximum of 256
#                 "opt1" "opt2" ...
#   Return value: selected index (0 for opt1, 1 for opt2 ...)
function select_option {

    # little helpers for terminal print control and key input
    ESC=$( printf "\033")
    cursor_blink_on()  { printf "$ESC[?25h"; }
    cursor_blink_off() { printf "$ESC[?25l"; }
    cursor_to()        { printf "$ESC[$1;${2:-1}H"; }
    print_option()     { printf "   $1 "; }
    print_selected()   { printf "> $green$ESC[7m $1 $ESC[27m$clear"; }
    get_cursor_row()   { IFS=';' read -sdR -p $'\E[6n' ROW COL; echo ${ROW#*[}; }
    key_input()        { read -s -n3 key 2>/dev/null >&2
                         if [[ $key = $ESC[A ]]; then echo up;    fi
                         if [[ $key = $ESC[B ]]; then echo down;  fi
                         if [[ $key = ""     ]]; then echo enter; fi; }

    # initially print empty new lines (scroll down if at bottom of screen)
    for opt; do printf "\n"; done

    # determine current screen position for overwriting the options
    local lastrow=`get_cursor_row`
    local startrow=$(($lastrow - $#))

    # ensure cursor and input echoing back on upon a ctrl+c during read -s
    trap "cursor_blink_on; stty echo; printf '\n'; exit" 2
    cursor_blink_off

    local selected=0
    while true; do
        # print options by overwriting the last lines
        local idx=0
        for opt; do
            cursor_to $(($startrow + $idx))
            if [ $idx -eq $selected ]; then
                print_selected "$opt"
            else
                print_option "$opt"
            fi
            ((idx++))
        done

        # user key control
        case `key_input` in
            enter) break;;
            up)    ((selected--));
                   if [ $selected -lt 0 ]; then selected=$(($# - 1)); fi;;
            down)  ((selected++));
                   if [ $selected -ge $# ]; then selected=0; fi;;
        esac
    done

    # cursor position back to normal
    cursor_to $lastrow
    printf "\n"
    cursor_blink_on

    return $selected
}

function select_opt {
    select_option "$@" 1>&2
    local result=$?
    echo $result
    return $result
}

#----------------------------------------------------------------
echo "                                                                                                        "
echo "                                                                                                        "
echo "                         _/_/_/  _/      _/                                                             "
echo "                      _/        _/_/  _/_/    _/_/    _/_/_/      _/_/    _/    _/                      "
echo "                     _/        _/  _/  _/  _/    _/  _/    _/  _/_/_/_/  _/    _/                       "
echo "                    _/        _/      _/  _/    _/  _/    _/  _/        _/    _/                        "
echo "                     _/_/_/  _/      _/    _/_/    _/    _/    _/_/_/    _/_/_/                         "
echo "                                                                            _/                          "
echo "                                                                       _/_/                             "
echo "                                                                                                        "
echo "                                                                                                        "                                                                                                    
#----------------------------------------------------------------                                                                                                        

echo "Select one option using up/down keys and enter to confirm:"
echo

options=("單筆相同" "單筆不相同" "多筆相同" "多筆不相同" "SSE/單筆相同" "SSE/單筆不相同" "SSE/多筆相同" "SSE/多筆不相同" "${array[@]}") # join arrays to add some variable array
case `select_opt "${options[@]}"` in
    0) curl -N http://127.0.0.1:8000/oneSameQuote;;
    1) curl -N http://127.0.0.1:8000/oneDifferentQuote;;
    2) curl -N http://127.0.0.1:8000/manySameQuote;;
    3) curl -N http://127.0.0.1:8000/manyDifferentQuote;;
    4) curl -N http://127.0.0.1:8000/stream/oneSameQuote;;
    5) curl -N http://127.0.0.1:8000/stream/oneDifferentQuote;;
    6) curl -N http://127.0.0.1:8000/stream/manySameQuote;;
    7) curl -N http://127.0.0.1:8000/stream/manyDifferentQuote;;
    *) echo "selected ${options[$?]}";;
esac
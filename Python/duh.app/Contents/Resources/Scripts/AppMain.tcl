wm title . "TIMER"
wm geometry . +20+0
cd [file dirname [info script]]
bind . <Control-c> {console show}
#console show
menu .mbar
. config -menu .mbar
source timer.tcl


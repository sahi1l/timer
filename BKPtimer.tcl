pack [entry .time -width 5 -font "Times 48" -textvariable thetime -justify center] -padx 20 -pady 10 -side top
pack [label .instructions -text "Press return to start timer.\nClick time to pause or change." -font "Times-Italic 12"] -side top
puts [wm geometry .]
wm geometry . +100+100
set thetime "15:00"
update
proc topretty {seconds} {
    return "[expr int($seconds/60)]:[format %02d [expr $seconds%60]]"
}
proc frompretty {thetime} {
    set tt [regsub "\[^0-9 \]" [split $thetime ":"] ""]
    set tt [switch [llength $tt] {
        0 {set H 0; set M 0}
        1 {set H 0; set M $tt}
        2 {set H [lindex $tt 0]; set M [lindex $tt 1]}
    }]
    puts $H,$M 
    
    
    set result [expr $H*60+$M]
    return $result
}
proc startclock {} {
    global begin countfrom thetime stoptime
    focus .
    set begin [clock seconds]
    set countfrom [frompretty $thetime]
    set stoptime 0
    run
}
proc run {} {
    global begin countfrom thetime stoptime
    if {$stoptime} {return}
    set now [clock seconds]
    set show [expr $countfrom-($now-$begin)]
    if {$show<=0} {
        set thetime "0:00";
        set stoptime 0;
        if [catch {exec afplay Bell.m4a &}] {#TO FIX: Make this general for all OS, afplay is just for Mac
            bell -nice
            after 100 {bell -nice}
            after 200 {bell -nice}
        }
        return
    }
    set thetime [topretty $show]
    after 1000 {run}
}

bind .time <FocusIn> {set stoptime 1;.time selection range 0 end}
bind .time <Key-Return> {startclock}

focus .time

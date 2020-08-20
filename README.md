# CLOAK: PV-aware Wear Leveling and Active Self-protection Mechanisms Against Flip Attacks on Non-Volatile Memories


&#160; &#160; &#160; &#160; CLOAK is a detection and defense mechanism to neutralize Flip Attacks. CLOAK leverages a novel wear leveling algorithm called CLIMBER to dynamically calibrate address mappings so that intensive writes to weak cells are redirected to strong cells.  CLIMBER also conceals weak NVM cells from attackers by randomly mapping cold addresses to weak NVM area. Moreover, CLOAK uses a new metric--hotness deviation to characterize violent fluctuations of write intensity on a memory address in two adjacent intervals, and thus can identify Flip Attacks efficiently. CLOAK then leverages an active self-protection scheme to defend Flip Attacks.

CLOAK Dependencies, Running, and Result
------------
**1.External Dependencies**  
&#160; &#160; &#160; &#160; Before running CLOAK codes, it's essential that you have already install dependencies listing below.
* numpy
* python(>=2.7)
* Zsim-NVMain (We use Zsim to collect memory access trace. You can also use other simulators to collect trace) [axle-zsim-nvmain](https://github.com/AXLEproject/axle-zsim-nvmain)

**2.Running**

* First, make sure the trace is in the ./ directory.
* Run CLOAK codes by:
```javascript
[root @node1 CLOAK]# python typeX_***_climber.py arg1 arg2
```
* X = 0 is non-attack; X = 1 is Inconsistent Write Attack; X = 2 is Hot-cold Page Swapping Attack.
* Arg1 and arg2 are used to enable our climber and WPRM schemes.

**3.Result**  
&#160; &#160; &#160; &#160; The hotness deviation result and endurance result are recorded by defenselayer_*_climber.py and \*mm_climber.py in \*.dat files.



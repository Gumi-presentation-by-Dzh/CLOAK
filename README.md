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

* First, make sure the trace is in the same path.
* run CLOAK codes by: python typeX_YYY_climber.py arg1 arg2.
* X means attack types : non-attack, Inconsistent Write Attack, and Hot-cold Page Swapping Attack.
* YYY means the baseline system : HC-to-SW, BWL, and TWL.
* arg1 and arg2 are used to enable our climber and WPRM schemes.

**3.Result**  
&#160; &#160; &#160; &#160; The hotness deviation result and endurance result are recorded by defenselayer_YYY_climber.py and YYYmm_climber.py in \*.dat files.



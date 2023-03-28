# TM2020 Daily Report

This is a project regarding Nadeo's TrackMania 2020 game. It provides, on demand by terminal commands, a daily report of Personal Best times achieved on that day.

Visit the [wiki page](https://github.com/cinephos/TM2020-Daily-Report/wiki) to find out the required libraries in c# and python. Read instructions how to use it.

**CHECKPOINT 1** C# code which reads the headers of all .replay.gbx files stored in Autosaves directory in order to extract map uid and PB time. Data are stored to a local .txt file. Two methods suuplied: a) Autosaves dir is available locally, and b) via [SMBLibrary](https://github.com/TalAloni/SMBLibrary), when Autosaves dir is located on a different computer.

_Proud to say that this code is a showcase implementation of the_ ***SMBLibrary.***

**CHECKPOINT 2** Python code which creates a local db in text format, which contains info of the played maps: name, name stripped of manialib format, author and medal times.

**CHECKPOINT 3** Python Create / maintain a local file with all new PBs achieved.

_The program goes through the above checkpoints as long as there is a new file created by the first checkpoint._

**FINISH LINE** The program displayes data of all maps having a PB achieved within the last 24 hours. Additionally, the user may request info (map medal times and PBs) of all maps containing an input string in their name. _(Name stripped of manialib format)_

The output of the program looks like this:

```
Name:  Winter 2023 - 21
 
            Bronze medal:  1:26.000
2023-03-04 09:40:07   PB:  1:11.984
2023-03-08 19:53:34   PB:  1:11.155
2023-03-20 19:36:53   PB:  1:10.875
2023-03-23 19:19:30   PB:  1:10.387
            Silver medal:  1:09.000
2023-03-26 23:13:28   PB:  1:08.832
              Gold medal:  1:01.000
            Author medal:    57.140
-----------------------------------
 
Name:  Winter 2023 - 22
 
            Bronze medal:  1:33.000
2023-03-04 09:42:00   PB:  1:21.194
2023-03-23 19:28:12   PB:  1:20.474
            Silver medal:  1:14.000
              Gold medal:  1:06.000
            Author medal:  1:01.423
-----------------------------------
```

_I express my deep appreciation to the members of the Openplanet community without whom, I would have not reached that far in my journey._

_Thank you ladies and gentlemen!_


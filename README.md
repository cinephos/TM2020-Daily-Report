# TM2020 Daily Report

This is a project regarding Nadeo's TrackMania 2020 game. It provides, on demand by terminal commands, a daily report of Personal Best times achieved on that day.

**WORKS IN PROGRESS**

The project has various checkpoints to be met. As soon as each check point is cleared, the relevant code will be uploaded here. Visit the [wiki page](https://github.com/cinephos/TM2020-Daily-Report/wiki) to find out how to use it.

**CHECKPOINT 1** Create c# code to read the headers of all .replay.gbx files stored in Autosaves directory in order to extract map uid and PB time. Then, store these values to a local .txt file. Two methods suuplied: a) Autosaves dir is available locally, and b) via [SMBLibrary](https://github.com/TalAloni/SMBLibrary), when Autosaves dir is located on a different computer.

**CHECKPOINT 2** Create a local db in text format, which contains info of the played maps: name, name stripped of manialib format, author and medal times (almost completed)

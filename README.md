# Introduction
The aim of this project is to provide an automated method to reliably and accurately produce highlights for sports broadcasting. The current method employed consists of filtering for loud volume spikes, theoretically corresponding to a 'key' moment in the match. Then, using ML speech recognition models, the audio is scanned for key words (e.g. goal, shot, foul).

# Problem
Sport highlights are still frequently manually edited by teams and leagues alike, especially among lower budget organisations. The potential for increasing the speed and efficiency of this process is something that can be exploited further than is currently being .

# Solution
Through the development of a software application that can process a full event video + audio file and output a ready-made highlight video. The application in its current state utilises a function to isolate loud points within the audio file and form clips starting 4 seconds before and after these points.  

# How to run
1. download all files within the 'code' folder
2. make sure all files are in the same location
3. run only the 'main' python file


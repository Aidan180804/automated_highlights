# Introduction
-The aim of this project is to provide an automated method to reliably and accurately produce highlights for sports broadcasting. 

-There are currently two functions used concurrently to select clips: 
  1. loud section detection
  2. key word recognition using ML speech recognition


# Problem
Sport highlights are still frequently manually edited by teams and leagues alike, especially among lower budget organisations. Increasing the speed and efficiency of this process is something that was identified as a potential software development project, even potentially leading to an entreprenuerial opportunity moving forward. 

# Technical approach
Through the development of a software application that can process a full event video + audio file and output a ready-made highlight video. The application in its current state utilises a function to isolate loud points within the audio file and form clips starting 4 seconds before and after these points.  

# Future enhancements

# File breakdown
- code folder: contains all python files used within the production of the highlights
- code_yt_app: contains the python file for the youtube video download application, primarily used to test the main application


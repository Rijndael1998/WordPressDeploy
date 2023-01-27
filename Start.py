#!/bin/python3
import Settings

for website in Settings.websites:
    website.startDocker()

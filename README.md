# Client-Server-Communication
This project implements a real-time client-server communication system to monitor and display system performance metrics from 2 separate clients. Client collects CPU , GPU usage, and memory utilization sending them to a centralized server over a socket connection. Server processes data from clients, dynamically updating a website for visualization.

## Features

- Real-time data transmission from two clients
- CPU, GPU, and memory usage monitoring using `psutil` and PowerShell
- HTML dashboard that updates every 10 seconds
- Visual alerts (highlighting) for threshold violations
- Interactive interface for setting client-specific thresholds

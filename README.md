# Time Tracker v20241121 Beta

## Overview

Time Tracker is a comprehensive desktop application designed to help you manage your time, track tasks, and maintain productivity. With multiple features including clock-in/out functionality, task tracking, to-do lists, and a scratch pad, this app provides a robust solution for personal and professional time management.

## Features

### 1. Clock In/Out Tab
- Track your total work time
- Clock in and out with a single button
- View daily time summaries
- Maintain a detailed clock-in/out history

### 2. Task List Tab
- Create tasks with estimated hours
- Add multiple tasks
- Track progress for each task
- Monitor total estimated and spent hours

### 3. Track Tasks Tab
- Start and stop individual tasks
- View active task and total tracked time
- Manage multiple tasks simultaneously
- Reset or delete tasks as needed

### 4. To-Do List Tab
- Add and remove to-do items
- Persistent storage of to-do items
- Simple, straightforward interface

### 5. Scratch Pad Tab
- Take notes and save them automatically
- Plain text editing
- Dark-themed interface for reduced eye strain

## Getting Started

### Installation
1. Ensure you have Python and PyQt6 installed
2. Clone the repository
3. Install required dependencies:
   ```
   pip install PyQt6
   ```

### Running the Application
- Execute the `main.py` script
- The application will launch with the Clock In/Out tab active

## Usage Guide

### Clock In/Out
1. Click "Clock In" to start tracking work time
2. Click "Clock Out" to stop tracking
3. View your daily time summaries in the history section

### Managing Tasks
1. In the Task List tab, enter a task name and estimated hours
2. Click "Add Task" to create the task
3. Use start/stop, reset, and delete buttons to manage tasks
4. Track progress via the progress bar and task list

### To-Do List
1. Enter a task in the input field
2. Click "Add Item" or press Enter
3. Remove items by selecting and clicking "Remove Selected Item"

### Scratch Pad
- Type your notes directly
- Content is auto-saved every minute

## System Tray Integration
- Minimize the app to system tray
- Right-click the tray icon to restore or exit the application

## Data Persistence
- Tasks, to-do items, and scratch pad content are automatically saved
- Clock history is maintained between sessions

## Keyboard Shortcuts
- Standard text editing shortcuts work in the scratch pad
- Tab key navigates between application tabs

## Troubleshooting
- Ensure you have the latest version of Python and PyQt6
- Check that `clock.png` icon is in the same directory as the script
- Create a `data` directory in the script's location for saving files

## Version
Current Version: v20241121 Beta

## License
GPL v2.0

## Support
For issues or feature requests, please contact brian@wedovids.com


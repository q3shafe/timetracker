# main.py
import sys
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (QApplication, QWidgetAction, QMainWindow, QTabWidget, QWidget, QSystemTrayIcon, QMenu,
                           QVBoxLayout, QPushButton, QLabel, QLineEdit,
                           QProgressBar, QListWidget, QHBoxLayout, QMessageBox,
                           QDoubleSpinBox, QFrame, QScrollArea)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QIcon

class Task:
    def __init__(self, name, expected_hours):
        self.name = name
        self.expected_hours = expected_hours
        self.elapsed_time = timedelta()
        self.timer = None
        self.is_running = False

class TaskWidget(QFrame):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        


        # Task information
        info_layout = QVBoxLayout()
        
        # Task name
        self.name_label = QLabel(self.task.name)
        self.name_label.setStyleSheet("font-weight: bold;")
        
        # Time information split into multiple labels for clarity
        time_layout = QVBoxLayout()
        self.elapsed_label = QLabel(self.get_elapsed_text())
        self.expected_label = QLabel(self.get_expected_text())
        self.percentage_label = QLabel(self.get_percentage_text())
        
        time_layout.addWidget(self.elapsed_label)
        time_layout.addWidget(self.expected_label)
        time_layout.addWidget(self.percentage_label)
        
        info_layout.addWidget(self.name_label)
        info_layout.addLayout(time_layout)

        # Controls
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.setFixedWidth(60)
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedWidth(60)
        self.delete_button = QPushButton("Delete")
        self.delete_button.setFixedWidth(60)

        # Status indicator
        self.status_label = QLabel("Stopped")
        self.status_label.setStyleSheet("color: gray;")
        
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(self.status_label)
        layout.addWidget(self.start_stop_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.delete_button)

    def get_elapsed_text(self):
        hours = self.task.elapsed_time.total_seconds() / 3600
        return f"Time spent: {hours:.2f} hours"

    def get_expected_text(self):
        return f"Expected: {self.task.expected_hours:.2f} hours"

    def get_percentage_text(self):
        if self.task.expected_hours > 0:
            percentage = (self.task.elapsed_time.total_seconds() / 3600) / self.task.expected_hours * 100
            return f"Progress: {percentage:.1f}%"
        return "Progress: 0%"

    def update_display(self):
        self.elapsed_label.setText(self.get_elapsed_text())
        self.expected_label.setText(self.get_expected_text())
        self.percentage_label.setText(self.get_percentage_text())
        self.start_stop_button.setText("Stop" if self.task.is_running else "Start")
        self.status_label.setText("Running" if self.task.is_running else "Stopped")
        self.status_label.setStyleSheet("color: green;" if self.task.is_running else "color: gray;")

class TimeTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Time Tracker")
        self.setGeometry(100, 100, 800, 600)
        

        # Initialize state
        self.tasks = []
        self.task_widgets = []
        self.clock_in_time = None
        self.total_work_time = timedelta()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_times)
        self.timer.start(1000)  # Update every second
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create tabs
        self.clock_tab = self.create_clock_tab()
        self.task_list_tab = self.create_task_list_tab()
        self.track_tasks_tab = self.create_track_tasks_tab()
        
        # Add tabs to widget
        self.tabs.addTab(self.clock_tab, "Clock In/Out")
        self.tabs.addTab(self.task_list_tab, "Task List")
        self.tabs.addTab(self.track_tasks_tab, "Track Tasks")
        
        # Disable tabs initially
        self.task_list_tab.setEnabled(False)
        self.track_tasks_tab.setEnabled(False)
        #self.setWindowIcon(self.app_icon)
        #self.setupSystemTray()

    
       

    def create_clock_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.clock_button = QPushButton("Clock In")
        self.clock_button.clicked.connect(self.toggle_clock)
        
        self.clock_status = QLabel("Not clocked in")
        self.total_time_label = QLabel("Total clocked time: 0:00:00")
        
        layout.addWidget(self.clock_button)
        layout.addWidget(self.clock_status)
        layout.addWidget(self.total_time_label)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab

    def create_task_list_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Task input
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Task name")
        self.hours_input = QDoubleSpinBox()
        self.hours_input.setRange(0.25, 24)
        self.hours_input.setSingleStep(0.25)
        self.hours_input.setValue(1)
        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.hours_input)
        input_layout.addWidget(add_button)
        
        # Task list
        self.task_list = QListWidget()
        self.task_list.currentItemChanged.connect(self.select_task)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(800)  # 8 hours in tenths
        
        layout.addLayout(input_layout)
        layout.addWidget(self.task_list)
        layout.addWidget(self.progress_bar)
        
        tab.setLayout(layout)
        return tab

    def create_track_tasks_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Summary at the top
        self.summary_frame = QFrame()
        self.summary_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        summary_layout = QVBoxLayout()
        
        self.total_tracked_time = QLabel("Total tracked time: 0:00:00")
        self.active_task_label = QLabel("Current active task: None")
        
        summary_layout.addWidget(self.total_tracked_time)
        summary_layout.addWidget(self.active_task_label)
        self.summary_frame.setLayout(summary_layout)
        
        # Container for task widgets
        self.task_container = QWidget()
        self.task_container_layout = QVBoxLayout()
        self.task_container.setLayout(self.task_container_layout)
        
        # Scroll area for tasks
        scroll = QScrollArea()
        scroll.setWidget(self.task_container)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(self.summary_frame)
        layout.addWidget(scroll)
        
        tab.setLayout(layout)
        return tab

    def toggle_clock(self):
        if not self.clock_in_time:  # Clock in
            self.clock_in_time = datetime.now()
            self.clock_button.setText("Clock Out")
            self.clock_status.setText("Clocked in")
            self.task_list_tab.setEnabled(True)
            self.track_tasks_tab.setEnabled(True)
        else:  # Clock out
            self.clock_in_time = None
            self.clock_button.setText("Clock In")
            self.clock_status.setText("Not clocked in")
            self.task_list_tab.setEnabled(False)
            self.track_tasks_tab.setEnabled(False)
            # Stop all running tasks
            for task in self.tasks:
                if task.is_running:
                    self.stop_task(task)

    def add_task(self):
        name = self.task_input.text()
        hours = self.hours_input.value()
        
        if name:
            task = Task(name, hours)
            self.tasks.append(task)
            
            # Create and add task widget
            task_widget = TaskWidget(task)
            task_widget.start_stop_button.clicked.connect(lambda: self.toggle_task_timer(task))
            task_widget.reset_button.clicked.connect(lambda: self.reset_task(task))
            task_widget.delete_button.clicked.connect(lambda: self.delete_task(task))
            self.task_widgets.append(task_widget)
            self.task_container_layout.addWidget(task_widget)
            
            self.update_task_displays()
            self.task_input.clear()
            self.hours_input.setValue(1)

    def delete_task(self, task):
        # Remove the task from the list of tasks
        self.tasks.remove(task)
        
        # Remove the corresponding task widget from the layout
        for i, widget in enumerate(self.task_widgets):
            if widget.task == task:
                self.task_container_layout.removeWidget(widget)
                self.task_widgets.pop(i)
                break
        
        # Update the task list and other displays
        self.update_task_displays()

    def update_task_displays(self):
        # Update task list
        self.task_list.clear()
        
        total_expected_hours = 0
        total_elapsed_time = timedelta()
        active_task_name = "None"
        
        for task in self.tasks:
            # Update task list display
            hours_spent = task.elapsed_time.total_seconds() / 3600
            self.task_list.addItem(
                f"{task.name} - Expected: {task.expected_hours:.2f}hrs, Spent: {hours_spent:.2f}hrs"
            )
            
            total_expected_hours += task.expected_hours
            total_elapsed_time += task.elapsed_time
            
            if task.is_running:
                active_task_name = task.name
        
        # Update progress bar
        progress = int(total_expected_hours * 100)
        self.progress_bar.setValue(progress)
        if total_expected_hours > 8:
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        else:
            self.progress_bar.setStyleSheet("")
        
        # Update task widgets and summary
        for widget in self.task_widgets:
            widget.update_display()
        
        total_hours = total_elapsed_time.total_seconds() / 3600
        self.total_tracked_time.setText(f"Total tracked time: {total_hours:.2f} hours")
        self.active_task_label.setText(f"Current active task: {active_task_name}")

    def update_times(self):
        if self.clock_in_time:
            elapsed = datetime.now() - self.clock_in_time
            self.total_time_label.setText(f"Total clocked time: {str(elapsed).split('.')[0]}")
            
            # Update running tasks
            for task in self.tasks:
                if task.is_running:
                    task.elapsed_time += timedelta(seconds=1)
            
            self.update_task_displays()

    def toggle_task_timer(self, task):
        if not task.is_running:
            # Stop any other running tasks
            for other_task in self.tasks:
                if other_task != task and other_task.is_running:
                    self.stop_task(other_task)
            # Start this task
            task.is_running = True
        else:
            self.stop_task(task)
        
        self.update_task_displays()

    def stop_task(self, task):
        task.is_running = False
        self.update_task_displays()

    def reset_task(self, task):
        if task.is_running:
            self.stop_task(task)
        task.elapsed_time = timedelta()
        self.update_task_displays()
    
    def select_task(self, current, previous):
        if current:
            # Highlight the selected task in the task list
            self.task_list.setCurrentItem(current)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimeTracker()
    window.show()
    sys.exit(app.exec())
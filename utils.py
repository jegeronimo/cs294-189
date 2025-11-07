"""
Email Viewer Widget Utility

This module provides a widget for viewing ham and spam emails from the dataset.
"""

import ipywidgets as widgets
from IPython.display import display
import random
from pathlib import Path


class EmailViewer:
    """Interactive widget for viewing ham and spam emails with navigation."""
    
    def __init__(self, ham_files, spam_files):
        """
        Initialize the email viewer widget.
        
        Parameters:
        -----------
        ham_files : list
            Sorted list of Path objects for ham email files
        spam_files : list
            Sorted list of Path objects for spam email files
        """
        self.ham_files = ham_files
        self.spam_files = spam_files
        self.current_mode = 'ham'
        self.current_index = None
        
        # Create widget components
        self.output = widgets.Output()
        self.info_label = widgets.HTML(
            value="<b>Mode: <span style='color:green'>HAM</span> | Click the button to load a random email</b>"
        )
        
        # Mode toggle button
        self.mode_button = widgets.Button(
            description='Switch to SPAM',
            button_style='info',
            layout=widgets.Layout(width='150px', height='40px')
        )
        
        # Button to load random email
        self.load_button = widgets.Button(
            description='Load Random Email',
            button_style='primary',
            layout=widgets.Layout(width='150px', height='40px')
        )
        
        # Navigation buttons
        self.prev_button = widgets.Button(
            description='◀ Previous',
            button_style='',
            layout=widgets.Layout(width='120px', height='40px'),
            disabled=True
        )
        
        self.next_button = widgets.Button(
            description='Next ▶',
            button_style='',
            layout=widgets.Layout(width='120px', height='40px'),
            disabled=True
        )
        
        # Connect buttons to functions
        self.mode_button.on_click(self._toggle_mode)
        self.load_button.on_click(self._load_random_email)
        self.prev_button.on_click(self._load_previous_email)
        self.next_button.on_click(self._load_next_email)
        
        # Create the widget layout
        self.widget = widgets.VBox([
            self.info_label,
            widgets.HBox([self.mode_button, self.load_button]),
            widgets.HBox([self.prev_button, self.next_button]),
            self.output
        ])
    
    def _get_current_file_list(self):
        """Get the current file list based on mode."""
        return self.ham_files if self.current_mode == 'ham' else self.spam_files
    
    def _load_email_by_index(self, index):
        """Load and display an email by its index in the sorted list."""
        file_list = self._get_current_file_list()
        
        if index < 0 or index >= len(file_list):
            return
        
        self.current_index = index
        file_path = file_list[index]
        email_type = self.current_mode
        type_color = 'green' if email_type == 'ham' else 'red'
        
        with self.output:
            self.output.clear_output(wait=True)
            
            # Read the email content
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Update info label with index info
                file_name = file_path.name
                total = len(file_list)
                self.info_label.value = (
                    f"<b>Mode: <span style='color:{type_color}'>{email_type.upper()}</span> | "
                    f"Email {index + 1}/{total} | <code>{file_name}</code></b>"
                )
                
                # Update navigation button states
                self.prev_button.disabled = (index == 0)
                self.next_button.disabled = (index == len(file_list) - 1)
                
                # Display the email
                print(f"Email Type: {email_type.upper()}")
                print(f"File: {file_name} (Index: {index + 1}/{total})")
                print(f"{'='*60}")
                print(content)
                print(f"{'='*60}")
                
            except Exception as e:
                print(f"Error reading file: {e}")
    
    def _toggle_mode(self, b):
        """Toggle between ham and spam mode."""
        if self.current_mode == 'ham':
            self.current_mode = 'spam'
            self.mode_button.description = 'Switch to HAM'
            self.mode_button.button_style = 'warning'
            self.info_label.value = (
                "<b>Mode: <span style='color:red'>SPAM</span> | Click the button to load a random email</b>"
            )
        else:
            self.current_mode = 'ham'
            self.mode_button.description = 'Switch to SPAM'
            self.mode_button.button_style = 'info'
            self.info_label.value = (
                "<b>Mode: <span style='color:green'>HAM</span> | Click the button to load a random email</b>"
            )
        
        # Reset navigation when switching modes
        self.current_index = None
        self.prev_button.disabled = True
        self.next_button.disabled = True
    
    def _load_random_email(self, b):
        """Load and display a random email based on current mode."""
        file_list = self._get_current_file_list()
        random_index = random.randint(0, len(file_list) - 1)
        self._load_email_by_index(random_index)
    
    def _load_previous_email(self, b):
        """Load the previous email in the sequence."""
        if self.current_index is not None and self.current_index > 0:
            self._load_email_by_index(self.current_index - 1)
    
    def _load_next_email(self, b):
        """Load the next email in the sequence."""
        file_list = self._get_current_file_list()
        if self.current_index is not None and self.current_index < len(file_list) - 1:
            self._load_email_by_index(self.current_index + 1)
    
    def display(self):
        """Display the widget."""
        return self.widget


def load_email_files(ham_dir='data/ham', spam_dir='data/spam'):
    """
    Load and sort email files from the specified directories.
    
    Parameters:
    -----------
    ham_dir : str or Path
        Path to the ham email directory
    spam_dir : str or Path
        Path to the spam email directory
    
    Returns:
    --------
    tuple : (ham_files, spam_files)
        Sorted lists of Path objects for ham and spam files
    """
    ham_dir = Path(ham_dir)
    spam_dir = Path(spam_dir)
    
    # Get all ham and spam files recursively
    ham_files_raw = list(ham_dir.rglob('*.txt'))
    spam_files_raw = list(spam_dir.rglob('*.txt'))
    
    # Sort files numerically by filename (extract number from filename)
    def sort_key(path):
        try:
            # Extract number from filename (e.g., "123.txt" -> 123)
            return int(path.stem)
        except ValueError:
            # If filename is not a number, use string comparison
            return float('inf')
    
    ham_files = sorted(ham_files_raw, key=sort_key)
    spam_files = sorted(spam_files_raw, key=sort_key)
    
    return ham_files, spam_files


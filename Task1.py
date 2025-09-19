import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Data file
        self.filename = "todo_data.json"
        self.tasks = self.load_tasks()
        
        self.setup_ui()
        self.refresh_list()
    
    def load_tasks(self):
        """Load tasks from JSON file if it exists"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=4)
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="To-Do List", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Input section
        ttk.Label(main_frame, text="New Task:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.task_entry = ttk.Entry(main_frame, width=40)
        self.task_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 5), padx=(5, 5))
        self.task_entry.bind('<Return>', self.add_task_event)
        
        add_button = ttk.Button(main_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=1, column=2, pady=(0, 5))
        
        # Task list
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 10))
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Create treeview with scrollbar
        self.tree = ttk.Treeview(list_frame, columns=('Status', 'Created', 'Completed'), show='headings', height=12)
        
        # Define headings
        self.tree.heading('#0', text='ID')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Created', text='Created')
        self.tree.heading('Completed', text='Completed')
        
        # Define columns
        self.tree.column('#0', width=40, stretch=False)
        self.tree.column('Status', width=80, stretch=False)
        self.tree.column('Created', width=120, stretch=False)
        self.tree.column('Completed', width=120, stretch=False)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        complete_button = ttk.Button(button_frame, text="Mark Completed", command=self.mark_completed)
        complete_button.grid(row=0, column=0, padx=(0, 5))
        
        delete_button = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        delete_button.grid(row=0, column=1, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear All", command=self.clear_all)
        clear_button.grid(row=0, column=2, padx=5)
        
        # Filter frame
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Label(filter_frame, text="Filter:").grid(row=0, column=0, padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["All", "Pending", "Completed"], state="readonly", width=10)
        filter_combo.grid(row=0, column=1, padx=(0, 10))
        filter_combo.bind('<<ComboboxSelected>>', self.filter_tasks)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def add_task(self):
        """Add a new task to the list"""
        description = self.task_entry.get().strip()
        if not description:
            messagebox.showwarning("Input Error", "Task description cannot be empty!")
            return
        
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'status': 'Pending',
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'completed_at': None
        }
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_list()
        self.task_entry.delete(0, tk.END)
        self.status_var.set(f"Task added successfully (ID: {task['id']})")
    
    def add_task_event(self, event):
        """Handle Enter key press in task entry"""
        self.add_task()
    
    def refresh_list(self):
        """Refresh the task list display"""
        # Clear current treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add tasks to treeview
        for task in self.tasks:
            status_icon = "✓" if task['status'] == 'Completed' else "◯"
            completed = task['completed_at'] if task['completed_at'] else "-"
            
            self.tree.insert('', 'end', iid=task['id'], 
                            values=(status_icon, task['created_at'], completed), 
                            text=task['description'])
        
        # Update status bar
        pending = sum(1 for t in self.tasks if t['status'] == 'Pending')
        completed = sum(1 for t in self.tasks if t['status'] == 'Completed')
        self.status_var.set(f"Total: {len(self.tasks)} tasks ({pending} pending, {completed} completed)")
    
    def mark_completed(self):
        """Mark selected task as completed"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed!")
            return
        
        task_id = int(selected[0])
        for task in self.tasks:
            if task['id'] == task_id:
                if task['status'] == 'Pending':
                    task['status'] = 'Completed'
                    task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    self.save_tasks()
                    self.refresh_list()
                    self.status_var.set(f"Task {task_id} marked as completed!")
                else:
                    messagebox.showinfo("Info", f"Task {task_id} is already completed!")
                return
    
    def delete_task(self):
        """Delete selected task"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to delete!")
            return
        
        task_id = int(selected[0])
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                self.save_tasks()
                self.refresh_list()
                self.status_var.set(f"Task {task_id} deleted successfully!")
                return
    
    def clear_all(self):
        """Clear all tasks"""
        if not self.tasks:
            messagebox.showinfo("Info", "The to-do list is already empty!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.tasks = []
            self.save_tasks()
            self.refresh_list()
            self.status_var.set("All tasks have been cleared!")
    
    def filter_tasks(self, event=None):
        """Filter tasks based on selection"""
        filter_value = self.filter_var.get()
        
        # Clear current treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add filtered tasks to treeview
        for task in self.tasks:
            if filter_value == "All" or task['status'] == filter_value:
                status_icon = "✓" if task['status'] == 'Completed' else "◯"
                completed = task['completed_at'] if task['completed_at'] else "-"
                
                self.tree.insert('', 'end', iid=task['id'], 
                                values=(status_icon, task['created_at'], completed), 
                                text=task['description'])

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
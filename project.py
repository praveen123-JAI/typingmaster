import time
import random
import tkinter as tk
from tkinter import messagebox

# Sample text options with special characters
sample_texts = [
    """The quick brown fox jumps over the lazy dog! This sentence is often used to test typing skills and contains every letter of the English alphabet. Typing quickly and accurately is an essential skill in the modern world, whether you are a student, a programmer, or a writer. Developing typing speed requires regular practice and a focus on proper technique. Remember to maintain a straight posture, position your hands correctly on the keyboard, and avoid looking at your fingers while typing. Speed and accuracy will improve over time, leading to greater productivity and efficiency. The goal of any typing test is not only to improve your words-per-minute score but also to ensure that you type with minimal errors. By participating in typing tests, you can track your progress and identify areas for improvement. Take the time to practice consistently and challenge yourself to beat your previous records.""",
    """Python is an amazing programming language known for its simplicity and versatility. It is widely used in various fields, including web development, data science, artificial intelligence, and more. Learning Python opens up many opportunities for both beginners and experienced programmers. The key to mastering Python is to practice consistently and build projects that solve real-world problems. Understanding Python's syntax is straightforward, and the language encourages readability and clarity. Libraries like NumPy, Pandas, and TensorFlow expand Python's capabilities, making it a powerful tool for modern applications. Whether you want to analyze data, create machine learning models, or develop web applications, Python is an excellent choice. The journey to learning Python is exciting and filled with endless possibilities. Start your Python journey today and unlock the potential of this incredible language.""",
    """Typing speed tests are an excellent way to improve your efficiency and accuracy while using a keyboard. These tests provide a fun and engaging way to challenge yourself and monitor your progress. To get the most out of a typing speed test, it's important to stay focused and relaxed. Avoid unnecessary stress, as it can lead to mistakes and reduce your overall performance. Typing tests typically measure your words per minute (WPM) and accuracy percentage. WPM reflects the speed of your typing, while accuracy indicates how many errors you make while typing. Improving both metrics requires consistent practice and attention to detail. Start by practicing with shorter texts and gradually increase the complexity and length of the passages you type. Over time, you will notice significant improvements in your speed and accuracy, making you more efficient and productive in your daily tasks! @$%#^&*()""",
]

# Timer variables
time_remaining = 60
timer_running = False
start_time = None
current_text = None

# Function to update the timer
def update_timer():
    global time_remaining, timer_running
    if time_remaining > 0:
        time_remaining_label.config(text=f"Time Remaining: {time_remaining}s", font=("Helvetica", 16, "bold"))
        time_remaining -= 1
        root.after(1000, update_timer)
    else:
        timer_running = False
        end_test()

# Function to start the test
def start_test():
    global start_time, current_text, time_remaining, timer_running
    if timer_running:
        return

    # Reset variables and UI
    start_time = time.time()
    time_remaining = 60
    timer_running = True
    current_text = random.choice(sample_texts)  # Randomly select a paragraph from the list
    
    # Update the color-coded text in the typing_output widget
    typing_output.delete(1.0, tk.END)  # Clear the output text widget
    typing_output.insert(tk.END, current_text, 'untouched')

    result_label.config(text="")
    typing_entry.delete(0, tk.END)
    typing_entry.focus()

    # Start the timer
    update_timer()

# Function to check the user's input and give color-coded feedback
def check_input(event):
    global current_text
    typed_text = typing_entry.get().strip()
    current_visible_text = current_text[:len(typed_text)]  # Only compare the part typed so far

    # Clear the text widget before inserting new content
    typing_output.delete(1.0, tk.END)
    
    # Highlight typed characters as correct (green) or incorrect (red)
    for i in range(len(typed_text)):
        if typed_text[i] == current_visible_text[i]:
            typing_output.insert(tk.END, typed_text[i], 'correct')
        else:
            typing_output.insert(tk.END, typed_text[i], 'incorrect')
    
    # Insert remaining untyped text as plain
    if len(typed_text) < len(current_text):
        typing_output.insert(tk.END, current_text[len(typed_text):], 'untouched')

    # Check if the entire text has been typed correctly
    if typed_text == current_text:
        end_test()

# Function to end the test automatically
def end_test():
    global timer_running
    typed_text = typing_entry.get()

    # If the timer has not been started
    if not current_text:
        messagebox.showerror("Error", "Click 'Start Test' before typing!")
        return

    # Calculate words per minute (WPM) and accuracy
    time_taken = time.time() - start_time
    if time_taken == 0:  # Avoid division by zero
        time_taken = 1
    
    words = len(typed_text.split())
    wpm = words / (time_taken / 60)  # Calculate WPM
    accuracy = 100 * sum(1 for i in range(min(len(typed_text), len(current_text))) if typed_text[i] == current_text[i]) / len(current_text)
    
    # Display results in the result label
    result_label.config(text=f"Time: {int(time_taken)}s | WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")

    # Stop the timer
    timer_running = False
    typing_output.delete(1.0, tk.END)  # Clear the typing area after time ends

# Function to end the test manually
def manual_end_test():
    global timer_running
    if not timer_running:
        messagebox.showerror("Error", "The test is not currently running. Click 'Start Test' to begin.")
        return

    # Calculate time taken so far
    time_taken = time.time() - start_time
    if time_taken == 0:  # Avoid division by zero
        time_taken = 1
    
    typed_text = typing_entry.get()
    words = len(typed_text.split())
    wpm = words / (time_taken / 60)  # Calculate WPM
    accuracy = 100 * sum(1 for i in range(min(len(typed_text), len(current_text))) if typed_text[i] == current_text[i]) / len(current_text)

    # Update results label
    result_label.config(text=f"Time: {int(time_taken)}s | WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")

    # Stop the test
    timer_running = False
    time_remaining_label.config(text="Time Remaining: 0s")
    typing_output.delete(1.0, tk.END)  # Clear the typing area after ending the test

# Set up the main window
root = tk.Tk()
root.title("Typing Speed Test")

# Set up the UI elements
root.config(bg="#f0f0f0")  # Light gray background color

time_remaining_label = tk.Label(root, text="Time Remaining: 60s", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
time_remaining_label.pack(pady=10)

typing_output = tk.Text(root, height=10, width=50, wrap=tk.WORD, font=("Helvetica", 14))
typing_output.tag_configure('correct', foreground='green')
typing_output.tag_configure('incorrect', foreground='red')
typing_output.tag_configure('untouched', foreground='black')
typing_output.pack(pady=10)

typing_entry = tk.Entry(root, font=("Helvetica", 14), width=50)
typing_entry.pack(pady=10)
typing_entry.bind('<KeyRelease>', check_input)

start_button = tk.Button(root, text="Start Test", font=("Helvetica", 14), command=start_test, bg="#4CAF50", fg="white")
start_button.pack(pady=10)

end_button = tk.Button(root, text="End Test", font=("Helvetica", 14), command=manual_end_test, bg="#FF5722", fg="white")
end_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f0f0f0")
result_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
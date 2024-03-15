import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO # using this as inspiration https://stackoverflow.com/questions/42800250/difference-between-open-and-io-bytesio-in-binary-streams
from tkinter import scrolledtext
import random

GIPHY_API_KEY = "2D2P3xA2sMtukT8PPqzKiUNqVzoPa92h" #TODO create your own API Key under https://support.giphy.com/hc/en-us/articles/360020283431-Request-A-GIPHY-API-Key
GIPHY_API_ENDPOINT = "https://api.giphy.com/v1/gifs/random"
GIPHY_SEARCH_ENDPOINT = "https://api.giphy.com/v1/gifs/search"


def create_page(notebook, title, endpoint, tag=None):
    """
    creating a new page in the notebook. Includes: text input field for user, send button
    :param:
    - notebook:(ttk.Notebook): The parent notebook where the new page will be added.
    - title (str): The title of the new page.
    - endpoint (str): API to fetch GIfs
    - tag (str, optional): linking it to the user input for more fitting results.
    The send button is associated with the process_input function for user input to be processed.
    Includes: ScrolledText widget for displaying messages, entry widget for user input,
    button widget for sending the input
    """
    frame = ttk.Frame(notebook, style="Blue.TFrame")  # Change style to "Blue.TFrame"
    notebook.add(frame, text=title)

    message_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=20, bg="#ADD8E6", fg="black", insertbackground="black")  # Change background color to light blue
    message_text.pack(pady=10, padx=10, side=tk.TOP, expand=True, fill=tk.BOTH)

    input_frame = tk.Frame(frame, bg="#ADD8E6")  # Change background color to light blue
    input_frame.pack(pady=10, padx=10, side=tk.TOP, fill=tk.X)

    input_field = tk.Entry(input_frame, bg="#ADD8E6", fg="black")  # Change background color to light blue
    input_field.pack(side=tk.LEFT, expand=True, fill=tk.X)

    send_button = tk.Button(input_frame, text="Send", bg="#00008B", fg="white",  # Change button background to dark blue
                            command=lambda text=message_text, field=input_field, ep=endpoint: process_input(text, field, ep))
    send_button.pack(side=tk.RIGHT)


def display_message(message_text, user_message, gif_url):
    """
    displays a chat message with the last user input, optionally the GIF URL, updates the GUI
    :param message_text: tkinter Text widget used for the chat window
    :param user_message: User input after pressing 'send', displayed in the chat window
    :param gif_url: URL of the GIF that is displayed in response to the user_message
    :return: NOne

    Creating a Frame to organuize and display the messages and GIFs
    Short delay before displaying the GIF
    Chat window is then updated to display both
    """
    message_widget = tk.Frame(message_text)
    message_widget.pack(pady=5, padx=10, side=tk.TOP, fill=tk.X)

    user_label = tk.Label(message_widget, text=user_message, bg="#DCF8C6", padx=10, pady=5, anchor="e")
    user_label.pack(side=tk.TOP, fill=tk.X)

    gif_label = tk.Label(message_widget, text="GIF will be displayed here", padx=10, pady=5, anchor="w")
    gif_label.pack(side=tk.TOP, fill=tk.X)

    # Display user message first, 100 seems good, play around with it
    user_label.after(100, lambda: display_gif_label(gif_label, gif_url))

    message_text.window_create(tk.END, window=message_widget)
    message_text.yview(tk.END)



def process_input(message_text, input_field, endpoint):
    """
    Uses/ processes user input to retrieve a GIF from the API endpoint
    Displays both in a chat window

    :param message_text: same as above.
    :param input_field: Using the tkinter entry widget here.
    :param endpoint (str): GIPHY API.
    :return: None

    Retrieves the user input from the input field
    gif_url to retrieve a GIF URL with 2 args
    display_message to display input and response in the chat window
    clearing the input field for a new message
    """
    user_input = input_field.get()
    gif_url = get_gif(endpoint, user_input)
    display_message(message_text, user_input, gif_url)
    input_field.delete(0, tk.END)

#the following function was written using ChatGPT. I didn't know how to implement the API properly
# It took forever and a lot of troubleshooting even with ChatGPT's help
def get_gif(endpoint, user_input=None):
    """Fetching a random GIF from the endpoint of each page
    Parameters:
    - endpoint (str): URL to fetch GIFs.
    - user_input (str, optional): User input. Default is None.

    Returns:
    str or None: The fetched GIF if successful. None if no GIFs were found.

    This sends a request to the GIPHY API using the endpoint.
    For the random GIF endpoint, it fetches a random GIF.
    For the specific URLs, it fetches GIFs from those URLs.
    If GIFs are found in the API response, the function returns the URL of a randomly selected GIF.
    If it doesn't find any GIFs, it prints an error message and returns None.
    """
    try:
        if endpoint == "https://api.giphy.com/v1/gifs/random":
            params = {"api_key": GIPHY_API_KEY}
        else:
            params = {}
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        if endpoint == "https://api.giphy.com/v1/gifs/random":
            gif_url = data.get("data", {}).get("images", {}).get("original", {}).get("url")
        else:
            if "data" in data and isinstance(data["data"], list) and data["data"]:
                gif_data = random.choice(data["data"])
                gif_url = gif_data.get("images", {}).get("original", {}).get("url")
            else:
                print(f"No GIFs found for the given query. Endpoint: {endpoint}")
                return None

        if gif_url:
            return gif_url
        else:
            print("No GIF URL found in the response.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GIF: {e}")

    return None

def display_gif_label(gif_label, gif_url):
    """
    Using tkinter widget label to display the GIF
    :param gif_label: label widget for displaying the GIF
    :param gif_url: URL of the GIF to display
    :return:none

    Fetching the GIF from the URL, then converting it to a format compatible with tkinter
    Updates Label widget to display GIF initiating subsequently new frames
    error message in case of mishaps
    """
    if gif_url:
        try:
            response = requests.get(gif_url)
            response.raise_for_status()
            gif_data = BytesIO(response.content)

            #using Image from PIL to create an object
            gif_image = Image.open(gif_data)
            gif_photo = ImageTk.PhotoImage(gif_image)

            gif_label.config(text="", image=gif_photo, compound="left")
            gif_label.image = gif_photo

            display_next_frame(gif_image, 1, gif_label) #to finallyyy make it animated

        except requests.exceptions.RequestException as e:
            print(f"Error fetching GIF: {e}")
            gif_label.config(text="Error fetching GIF", image=None)

# used geeksforgeeks.org for inspiration. Used Image.seek() and .after() method
def display_next_frame(gif_image, current_frame, gif_label):
    """
    displaing the next frame of the GIF on tkinter Label widget
    :param gif_image:
    :param current_frame:
    :param gif_label:
    :return:

    Retrieving and displaing the next frame of the GIF, with 100 milliseconds delay
    After reaching the end of the GIF, looping from the first frame after 100ms
    """
    try:
        gif_image.seek(current_frame)
        frame = gif_image.copy()
        new_gif_photo = ImageTk.PhotoImage(frame)

        gif_label.config(image=new_gif_photo, compound="left")
        gif_label.image = new_gif_photo

        gif_label.after(100, lambda: display_next_frame(gif_image, current_frame + 1, gif_label))

    except EOFError:
        gif_label.after(100, lambda: display_next_frame(gif_image, 1, gif_label))


def main():
    """
    Launching the application, creating a tkinter GUI with different tabs for the categories
    :return: none

    Initializes the root window titled "GUPHY" and creating notebook with tabs
    First tab: random GIFs from the API Endpoint
    App runs until user closes the window
    """
    root = tk.Tk()
    root.title("GUPHY")

    notebook = ttk.Notebook(root)

    create_page(notebook, "Random", GIPHY_API_ENDPOINT)
    create_page(notebook, "Funny", "https://api.giphy.com/v1/gifs/search?q=funny&api_key=" + GIPHY_API_KEY)
    create_page(notebook, "Serious", "https://api.giphy.com/v1/gifs/search?q=serious&api_key=" + GIPHY_API_KEY)
    create_page(notebook, "Angry", "https://api.giphy.com/v1/gifs/search?q=angry&api_key=" + GIPHY_API_KEY)

    notebook.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    """
    Script's entry point
    Calling main function to launch the app
    """
    main()

    #happy texting!! :)







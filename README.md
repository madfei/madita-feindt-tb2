# madita-feindt-tb2
Repository for my Tech Basics II assessment at Leuphana University
# GUPHY Chat Application

The GUPHY Chat Application is a simple GUI chat application that allows users to interact with the GIPHY API to fetch and display random GIFs. You can interact with 4 different settings, depending on what you want the answer to look like. Next to the first page with random results,  you have the possibility to receive GIF responses with specific emotions (angry, funny, and serious). The application uses the Tkinter library for creating the graphical interface and the PIL library for handling images. 

# Visuals
Screen recording of the GUPHY in the repo (GUPHY at work.mp4)

## Requirements

- Tkinter: Library in GUI for creating a graphical interface.
- PIL (Pillow): Library for opening, manipulating, and saving image files.
- Requests: Library for making HTTP requests.


## Getting Started

To run the GUPHY Chat Application, make sure you have Python installed. Additionally, please use the package installer to install the required libraries by running the following command:

```bash
pip install pillow 
pip install requests
pip install tk # usually pre-installed, only necessary if your python distribution does not have it
```

Once the dependencies are installed, you can execute the script. I recommend opening the script in a virtual environment. In your terminal, navigate to the folder you saved the script in and type in the following:

```bash
.\venv\Scripts\Activate
python app.py
```

## How to Use

1.	Run the script to launch the application
2.	Navigate through the different tabs by clicking on them to explore either random or category-specific GIFs. 
3.	Type your message to the input field and press “Send” or use the Enter button on your keyboard to submit your input
4.	See your message alongside the GIF the bot answers you with. 
5.	Repeat as wanted😊

## Note

The application currently utilizes my GIPHY API Key for fetching GIFs. Make sure it’s up to date. If it isn’t, you can replace the `GIPHY_API_KEY` variable in the script with your own API key.
Please also let me know if you need support or if anything does not run as expected at madita-feindt@gmx.de.

## Author

This application was created by Madita Feindt.

## Acknowledgments

- For reading and helping with my script: Luis Beaucamp.
- For being patient and being patient test users: Louisa, Lilia, Ruben, Basti ;)
- GIPHY for providing the API.
- ChatGPT for writing a snippet where I was stuck (Marked in the script)

Feel free to explore, customize, and chat!:)

# The Divya Vaani

## Project Overview

**The Divya Vaani** is a project designed to assist deaf and disabled individuals by providing an integrated communication platform. The system incorporates Firebase for managing user data, Azure Cognitive Services for text translation and speech synthesis, and a Flask server to serve video feeds. Additionally, the project provides a user-friendly interface for displaying video feeds in a GUI window on a web browser.

## Components

1. **Firebase Integration**: 
   - Used for storing and retrieving user data.
   - Manages user authentication and data storage with Firestore.

2. **Azure Cognitive Services**:
   - Provides text translation to facilitate communication across different languages.
   - Converts translated text to speech to support users with hearing impairments.

3. **Flask Server**:
   - Handles user requests and serves video feeds.
   - Supports multithreading to manage multiple user sessions concurrently.

4. **GUI Window for Video Feed**:
   - Displays video feeds in a web browser interface.
   - Enhances user interaction by providing a visual communication channel.

## Project Structure

Kamunikator/ │ ├── master.py # Main script that integrates all components. ├── translator.py # Script containing functions for text translation using Azure Cognitive Services. ├── server.py # Flask server script for handling video feeds and user requests.


## Detailed Plan

1. **Firebase Integration**:
   - Initialize Firebase with project-specific credentials.
   - Implement functionality to retrieve and update user data from Firestore.

2. **Azure Cognitive Services**:
   - Set up Azure Speech SDK to enable text-to-speech conversion.
   - Configure Azure Translation Client to translate text into multiple languages.

3. **Flask Server**:
   - Develop routes for managing server operations, such as starting and stopping.
   - Create an endpoint for serving video feeds to users.
   - Ensure server capabilities include support for multithreading to handle multiple users.

4. **GUI Window for Video Feed**:
   - Implement a user interface to display video feeds in a web browser.
   - Integrate with the Flask server to receive and show real-time video content.


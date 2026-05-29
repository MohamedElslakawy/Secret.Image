#the explainging of the Project.
# EncryptionManager Module by Mohamed Elslakawy

## Overview
This module is responsible for **encrypting and decrypting text messages** using the `cryptography` library in Python.
It provides a simple interface to:
- Generate a secure encryption key.
- Encrypt plaintext messages into ciphertext.
- Decrypt ciphertext back into plaintext.

## Installation
Before running the project, make sure to install the required libraries:

```bash
pip install cryptography
-----------------------------------------------------------------
---

# Work Completed

The original project structure and `EncryptionManager` class were kept as they were.

The work completed in this version focused on finishing the remaining parts of the project and connecting all components together.

## 1- StegoManager

The `StegoManager` class was completed.

It is responsible for hiding the encrypted message inside an image and extracting it later.

The class uses LSB steganography, where the secret message is converted into binary and hidden inside the least significant bits of the image pixels.

Main work completed:

* Open the selected image.
* Convert the encrypted message into binary.
* Hide the binary message inside the image pixels.
* Add an end marker to know where the hidden message stops.
* Save a new image that contains the hidden message.
* Extract the hidden message from the image.
* Convert the extracted binary data back into text.
* Show an error if no hidden message is found.

Libraries used:

```text
Pillow
numpy
```

---

## 2- Interface

The `Interface` class was completed.

It is responsible for the graphical user interface and for connecting the user actions with the encryption and steganography classes.

Main work completed:

* Create the main GUI window.
* Add an Upload Image button.
* Add a text box for writing the secret message.
* Add an encryption key field.
* Add a Hide Message button.
* Add an Extract Message button.
* Add a Clear button.
* Add a result area to display encrypted and decrypted messages.
* Show success messages when hiding or extracting works.
* Show error messages when the user does not select an image, does not enter a message, or uses a wrong key.

Library used:

```text
Tkinter
```

---

## 3- Main Integration

The `main.py` file was completed.

It is responsible for running the application and connecting the GUI with the rest of the project.

Main work completed:

* Import the `Interface` class.
* Create an object from the `Interface` class.
* Run the GUI application.

---

## 4- Requirements

The `requirements.txt` file was updated with the libraries needed to run the project.

Libraries included:

```text
cryptography
Pillow
numpy
```

Tkinter is also used for the GUI, but it is built into Python, so it does not need to be installed using pip.

---

## Final Workflow

The final project workflow is:

```text
User uploads an image
        ↓
User writes a secret message
        ↓
EncryptionManager encrypts the message
        ↓
StegoManager hides the encrypted message inside the image
        ↓
New image is saved
```

For extraction:

```text
User uploads the image with the hidden message
        ↓
StegoManager extracts the encrypted message
        ↓
EncryptionManager decrypts the message
        ↓
Original secret message appears in the GUI
```

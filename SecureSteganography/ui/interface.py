# Version 1.0
# GUI for User Interaction.

# Import tkinter for creating the graphical user interface.
import tkinter as tk

# Import filedialog to allow the user to select/save files.
# Import messagebox to show success and error messages.
from tkinter import filedialog, messagebox

# Import Path to work with file names and paths.
from pathlib import Path

# Import the EncryptionManager class.
# This class encrypts and decrypts the message.
from core.encryption_manager import EncryptionManager

# Import the StegoManager class.
# This class hides and extracts the encrypted message inside/from an image.
from core.stego_manager import StegoManager


class Interface:
    """
    This class is responsible for creating the graphical user interface (GUI)
    and connecting the user actions with EncryptionManager and StegoManager.
    """

    def __init__(self):
        """
        Constructor method.
        It creates the window and initializes the needed objects.
        """

        # Create the main application window.
        self.window = tk.Tk()

        # Set the title of the window.
        self.window.title("Secure Steganography")

        # Set the window size.
        self.window.geometry("780x620")

        # Prevent resizing the window.
        self.window.resizable(False, False)

        # This variable stores the path of the image selected by the user.
        self.selected_image_path = None

        # Create object from EncryptionManager to encrypt/decrypt messages.
        self.encryption_manager = EncryptionManager()

        # Create object from StegoManager to hide/extract messages.
        self.stego_manager = StegoManager()

        # Build all GUI components.
        self._build_interface()

    def _build_interface(self):
        """
        Create and organize all GUI components:
        labels, buttons, text boxes, and result area.
        """

        # Main title label.
        title_label = tk.Label(
            self.window,
            text="Secure Steganography System",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=15)

        # Short description label.
        description_label = tk.Label(
            self.window,
            text="Encrypt a secret message, hide it inside an image, then extract and decrypt it later.",
            font=("Arial", 11)
        )
        description_label.pack(pady=5)

        # Frame for image upload section.
        image_frame = tk.Frame(self.window)
        image_frame.pack(pady=10)

        # Button used to upload/select an image.
        upload_button = tk.Button(
            image_frame,
            text="Upload Image",
            width=20,
            command=self.upload_image
        )
        upload_button.grid(row=0, column=0, padx=10)

        # Label used to show selected image path.
        self.image_label = tk.Label(
            image_frame,
            text="No image selected",
            width=55,
            anchor="w"
        )
        self.image_label.grid(row=0, column=1, padx=10)

        # Label for the secret message input area.
        message_label = tk.Label(
            self.window,
            text="Secret Message:",
            font=("Arial", 12, "bold")
        )
        message_label.pack(anchor="w", padx=40, pady=(15, 5))

        # Text box where the user writes the secret message.
        self.message_text = tk.Text(self.window, height=6, width=85)
        self.message_text.pack(padx=40)

        # Label for the encryption key field.
        key_label = tk.Label(
            self.window,
            text="Encryption Key (copy this key to decrypt later):",
            font=("Arial", 12, "bold")
        )
        key_label.pack(anchor="w", padx=40, pady=(15, 5))

        # Entry field that displays the encryption key.
        self.key_entry = tk.Entry(self.window, width=95)
        self.key_entry.pack(padx=40)

        # Insert the generated key into the key field.
        self.key_entry.insert(0, self.encryption_manager.get_key().decode('utf-8'))

        # Frame for action buttons.
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)

        # Button to encrypt and hide the message inside the image.
        hide_button = tk.Button(
            button_frame,
            text="Hide Message",
            width=20,
            command=self.hide_message
        )
        hide_button.grid(row=0, column=0, padx=10)

        # Button to extract and decrypt the hidden message.
        extract_button = tk.Button(
            button_frame,
            text="Extract Message",
            width=20,
            command=self.extract_message
        )
        extract_button.grid(row=0, column=1, padx=10)

        # Button to clear the input and result areas.
        clear_button = tk.Button(
            button_frame,
            text="Clear",
            width=20,
            command=self.clear_fields
        )
        clear_button.grid(row=0, column=2, padx=10)

        # Label for the output/result area.
        result_label = tk.Label(
            self.window,
            text="Result:",
            font=("Arial", 12, "bold")
        )
        result_label.pack(anchor="w", padx=40, pady=(5, 5))

        # Text box used to show encrypted and decrypted results.
        self.result_text = tk.Text(self.window, height=10, width=85)
        self.result_text.pack(padx=40)

    def upload_image(self):
        """
        Allow the user to choose an image from the computer.
        """

        # Open file dialog to select image.
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.bmp"),
                ("PNG Files", "*.png"),
                ("All Files", "*.*")
            ]
        )

        # If the user selected a file, store its path and show it in the label.
        if file_path:
            self.selected_image_path = file_path
            self.image_label.config(text=file_path)

    def hide_message(self):
        """
        Encrypt the message and hide it inside the selected image.
        """

        try:
            # Make sure the user selected an image.
            if not self.selected_image_path:
                messagebox.showerror("Error", "Please upload an image first.")
                return

            # Get the message from the text box.
            plain_message = self.message_text.get("1.0", tk.END).strip()

            # Make sure the user entered a message.
            if not plain_message:
                messagebox.showerror("Error", "Please enter a secret message first.")
                return

            # Encrypt the plain message using EncryptionManager.
            # The result from Fernet is bytes, so we convert it to string using decode.
            encrypted_message = self.encryption_manager.encrypt_text(plain_message).decode('utf-8')

            # Get original image path to suggest a default output file name.
            original_path = Path(self.selected_image_path)

            # Ask the user where to save the new image.
            output_path = filedialog.asksaveasfilename(
                title="Save Image With Hidden Message",
                defaultextension=".png",
                initialfile=f"{original_path.stem}_secret.png",
                filetypes=[("PNG Files", "*.png")]
            )

            # If the user cancels saving, stop the function.
            if not output_path:
                return

            # Hide the encrypted message inside the selected image.
            self.stego_manager.hide_message(
                self.selected_image_path,
                encrypted_message,
                output_path
            )

            # Show success result in the result box.
            self._show_result(
                "Message hidden successfully.\n\n"
                f"Saved image: {output_path}\n\n"
                f"Encrypted message:\n{encrypted_message}\n\n"
                "Important: Keep the encryption key shown above. It is needed for decryption."
            )

            # Show success popup.
            messagebox.showinfo("Success", "Message encrypted and hidden successfully.")

        except Exception as error:
            # Show any error that happens during the process.
            messagebox.showerror("Error", str(error))

    def extract_message(self):
        """
        Extract the encrypted message from the selected image and decrypt it.
        """

        try:
            # Make sure the user selected an image.
            if not self.selected_image_path:
                messagebox.showerror("Error", "Please upload an image first.")
                return

            # Get the encryption key from the key field.
            key = self.key_entry.get().strip()

            # Make sure the key exists.
            if not key:
                messagebox.showerror("Error", "Please enter the encryption key.")
                return

            # Extract the encrypted message from the selected image.
            encrypted_message = self.stego_manager.extract_message(self.selected_image_path)

            # Create a new EncryptionManager using the entered key.
            decrypt_manager = EncryptionManager(key.encode('utf-8'))

            # Decrypt the extracted encrypted message.
            decrypted_message = decrypt_manager.decrypt_text(encrypted_message.encode('utf-8'))

            # Show encrypted and decrypted messages in the result box.
            self._show_result(
                "Message extracted successfully.\n\n"
                f"Encrypted message:\n{encrypted_message}\n\n"
                f"Decrypted message:\n{decrypted_message}"
            )

            # Show success popup.
            messagebox.showinfo("Success", "Message extracted and decrypted successfully.")

        except Exception as error:
            # Show any error that happens during extraction or decryption.
            messagebox.showerror("Error", str(error))

    def clear_fields(self):
        """
        Clear the message input and result output areas.
        """

        # Clear secret message text box.
        self.message_text.delete("1.0", tk.END)

        # Clear result text box.
        self.result_text.delete("1.0", tk.END)

    def _show_result(self, text: str):
        """
        Display text inside the result text area.
        """

        # Clear old result.
        self.result_text.delete("1.0", tk.END)

        # Insert new result.
        self.result_text.insert(tk.END, text)

    def run(self):
        """
        Start the GUI application.
        """

        # Run the Tkinter event loop.
        self.window.mainloop()

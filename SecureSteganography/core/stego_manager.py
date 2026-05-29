# Version 1.0
# This class is responsible for hiding data inside the image using LSB steganography.

# Import Image from Pillow to open, edit, and save images.
from PIL import Image

# Import numpy to convert the image pixels into arrays.
import numpy as np


class StegoManager:
    """
    This class is responsible for hiding encrypted text inside an image
    and extracting the hidden text again using LSB steganography.
    """

    # This marker is added at the end of the hidden message.
    # It helps the program know where the hidden message ends during extraction.
    END_MARKER = "###END_OF_SECRET_MESSAGE###"

    def _text_to_binary(self, text: str) -> str:
        """
        Convert text into binary.
        Example: A becomes 01000001
        """
        return ''.join(format(ord(character), '08b') for character in text)

    def _binary_to_text(self, binary_data: str) -> str:
        """
        Convert binary data back into normal text.
        """
        characters = []

        # Read every 8 bits as one character.
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i + 8]

            # Make sure the byte contains exactly 8 bits.
            if len(byte) == 8:
                characters.append(chr(int(byte, 2)))

        return ''.join(characters)

    def hide_message(self, image_path: str, secret_message: str, output_path: str) -> str:
        """
        Hide a secret message inside an image and save the new image.

        image_path: path of the original image selected by the user.
        secret_message: encrypted message that will be hidden inside the image.
        output_path: path where the new image will be saved.
        """

        # Check if the user selected an image.
        if not image_path:
            raise ValueError("No image was selected.")

        # Check if the user entered a message.
        if not secret_message:
            raise ValueError("No message was entered.")

        # Open the image and convert it to RGB format.
        image = Image.open(image_path).convert("RGB")

        # Convert the image into a numpy array so we can edit pixel values.
        image_array = np.array(image)

        # Add the end marker to the message so extraction knows when to stop.
        message_with_marker = secret_message + self.END_MARKER

        # Convert the message into binary bits.
        binary_message = self._text_to_binary(message_with_marker)

        # Count how many pixel values are available for hiding bits.
        available_bits = image_array.size

        # Check if the image has enough space to store the message.
        if len(binary_message) > available_bits:
            raise ValueError("The message is too large to hide inside this image.")

        # Flatten the image array to make it easier to edit pixel values one by one.
        flat_pixels = image_array.flatten()

        # Hide each bit of the message inside the least significant bit of a pixel value.
        for index, bit in enumerate(binary_message):
            # 254 in binary ends with 0, so this clears the last bit.
            # Then OR with int(bit) puts the message bit in the last bit.
            flat_pixels[index] = (flat_pixels[index] & 254) | int(bit)

        # Reshape the flattened pixels back to the original image shape.
        encoded_array = flat_pixels.reshape(image_array.shape).astype('uint8')

        # Convert the numpy array back into an image.
        encoded_image = Image.fromarray(encoded_array)

        # Save the image that contains the hidden message.
        encoded_image.save(output_path)

        # Return the path of the saved image.
        return output_path

    def extract_message(self, image_path: str) -> str:
        """
        Extract the hidden message from an image.
        """

        # Check if the user selected an image.
        if not image_path:
            raise ValueError("No image was selected.")

        # Open the selected image and convert it to RGB.
        image = Image.open(image_path).convert("RGB")

        # Convert image pixels into a numpy array.
        image_array = np.array(image)

        # Flatten the image array to read pixel values one by one.
        flat_pixels = image_array.flatten()

        # This variable stores the extracted bits.
        binary_data = ""

        # This variable stores the extracted text while reading the image.
        extracted_text = ""

        # Read the least significant bit from each pixel value.
        for value in flat_pixels:
            binary_data += str(value & 1)

            # Convert binary to text after every 8 bits.
            if len(binary_data) % 8 == 0:
                extracted_text = self._binary_to_text(binary_data)

                # Stop when the end marker is found.
                if self.END_MARKER in extracted_text:
                    return extracted_text.split(self.END_MARKER)[0]

        # If the end marker was not found, then there is no hidden message.
        raise ValueError("No hidden message was found in this image.")

from flask import Flask, request, jsonify
from PIL import Image
import os

app = Flask(__name__)

# Encryption and Decryption Functions
def encrypt_message(message, shift=3):
    return ''.join(chr((ord(char) - 32 + shift) % 95 + 32) for char in message)

def decrypt_message(encrypted_message, shift=3):
    return ''.join(chr((ord(char) - 32 - shift) % 95 + 32) for char in encrypted_message)

# Encoding Function
def encode_image(image_path, message):
    encrypted_message = encrypt_message(message)
    img = Image.open(image_path)

    binary_message = ''.join(format(ord(char), '08b') for char in encrypted_message) + '11111111'

    if len(binary_message) > img.width * img.height * 3:
        raise ValueError("Message is too large for the image")

    data_index = 0
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1
            img.putpixel((x, y), tuple(pixel))

    encoded_path = 'encoded_image.png'
    img.save(encoded_path)
    return encoded_path

# Decoding Function
def decode_image(image_path):
    try:
        img = Image.open(image_path)
    except Exception as e:
        raise ValueError(f"Error opening image: {e}")

    binary_message = ''
    for y in range(img.height):
        for x in range(img.width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    if '11111111' not in binary_message:
        raise ValueError("No hidden data found in the image")

    binary_message = binary_message.split('11111111')[0]

    try:
        message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    except ValueError:
        raise ValueError("Error decoding binary message.")

    return decrypt_message(message)

# Flask Routes
@app.route('/encode', methods=['POST'])
def encode():
    image = request.files['image']
    message = request.form.get('message')

    if not image or not message:
        return jsonify({'error': 'Image and message are required!'}), 400

    image_path = 'input_image.png'
    image.save(image_path)

    try:
        encoded_path = encode_image(image_path, message)
        return jsonify({'message': 'Encoding successful!', 'encoded_image': encoded_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decode', methods=['POST'])
def decode():
    image = request.files['image']
    
    if not image:
        return jsonify({'error': 'Image file is required!'}), 400

    image_path = 'encoded_image.png'
    image.save(image_path)

    try:
        decoded_message = decode_image(image_path)
        return jsonify({'message': decoded_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

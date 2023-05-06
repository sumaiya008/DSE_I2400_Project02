from flask import Flask, render_template

app = Flask(__name__)


data = [('iphone 14 pro', 'duckduckgo', 'https://www.apple.com/iphone-14-pro/', 'iPhone 14 Pro and iPhone 14 Pro Max - Apple', None, 'iPhone 14 Pro can detect a severe car crash, then call 911 and notify your emergency contacts. 6 Hardware sensors and advanced motion algorithms identify signs of a crash — including sudden changes in speed, direction, and cabin pressure. Over 1 million hours of real‑world driving and crash data helps iPhone recognize accidents'), ('iphone 14 pro', 'duckduckgo', 'https://www.apple.com/iphone-14-pro/specs/', 'iPhone 14 Pro and 14 Pro Max - Technical Specifications - Apple', None, 'The iPhone 14 Pro display has rounded corners that follow a beautiful curved design, and these corners are within a standard rectangle. When measured as a standard rectangular shape, the screen is 6.12 inches diagonally (actual viewable area is less). Super Retina XDR display 6.7‑inch (diagonal) all‑screen OLED display')]


@app.route('/')
def index():

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
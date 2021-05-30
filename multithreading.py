from PIL import Image


def validate_picture():
            try: 
                image = Image.open("./piano_package/Notes_piano/27_Note-Bass-B2.png")
            except:
                print("Error")

validate_picture()
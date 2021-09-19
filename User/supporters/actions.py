from PIL import Image

def save_profile(path):
    img =Image.open(path)
    if(img.height >300 or img.width >300):
        height =img.height
        width =img.width
        while(height >300):
            height =height//2
        while(width >300):
            width =width//2
        output_size =(width , height)
        img.resize(output_size)
        img.save(path)



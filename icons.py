import pygame

#creating list of images to be used as icons

icon_images = [ 'images/bg1.png', 'images/bg2.jpeg', 'images/bg3.jpg', 'images/bg4.jpg' ]

# creating a dictionary to store pygame image object
icon_dict = {}
for i,img in enumerate(icon_images):
    #value of this key is a list, more items will be appended in other modules
    icon_dict['icon'+str(i+1)] = [pygame.image.load(img)]

backgrounds = list(icon_dict.keys())[0:4]
#food_icons = list(icon_dict.keys())[4:]
print(icon_dict['icon1'][0])
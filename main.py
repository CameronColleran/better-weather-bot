from time import sleep
from utils import *
def main():
    for mention in get_mentions():
        respond_to_mention(mention)       
while True:
    main()
    sleep(15) # make replies every 15 seconds
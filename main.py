from utils import *
def main():
    for mention in get_mentions():
        respond_to_mention(mention)
main()
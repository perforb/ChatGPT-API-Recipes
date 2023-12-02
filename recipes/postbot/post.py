from generator import make_content
from tweeter import post

if __name__ == '__main__':
    content = make_content()
    post(content)

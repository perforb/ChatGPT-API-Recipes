from recipes.chatbot.generator import make_content
from recipes.chatbot.tweeter import post

if __name__ == '__main__':
    content = make_content()
    post(content)

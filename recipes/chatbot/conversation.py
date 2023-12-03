from search import answer_question

if __name__ == '__main__':
    print("Input your question.")
    conversation_history = []
    while True:
        user_input = input()
        if user_input == "exit":
            break
        conversation_history.append(
            {"role": "system",
             "content": "あなたは世界的に有名なホテルマンです。誠実かつ簡潔な表現を使って回答してください。"},
        )
        conversation_history.append(
            {"role": "user", "content": user_input}
        )
        answer = answer_question(user_input, conversation_history)
        print("ChatGPT:", answer)
        conversation_history.append({"role": "assistant", "content": answer})

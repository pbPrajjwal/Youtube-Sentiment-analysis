from services.sentiment_service import predict_sentiment

while True:
    comment = input("Comment: ")

    if comment == "exit":
        break

    print(predict_sentiment(comment))
from flask import Flask, render_template, request, url_for 
from textblob import TextBlob

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET']) # default route
def prediction():

	if request.method == 'POST':
		requested_sentence = request.form['sentence']
		blob = TextBlob(requested_sentence)
		overall_result = 0
		word_sentiment_code = []
		for sentence in blob.sentences:
			overall_result += sentence.sentiment.polarity
			for word in sentence.words:
				word_sentiment = {}
				word_blob = TextBlob(word)
				word_result = word_blob.sentiment.polarity
				word_sentiment['word'] = word
				word_sentiment['score'] = word_result
				
				if word_result < 0.0:
					word_sentiment['color_code'] = "#f54278"
				elif word_result > 0.0:
					word_sentiment['color_code'] = "#42f554"
				else:
					word_sentiment['color_code'] = "#42bcf5"
				word_sentiment_code.append(word_sentiment)

        

		if overall_result < 0.0:
			sentiment_label = 'NEGATIVE'
		elif overall_result > 0.0:
			sentiment_label = 'POSITIVE'
		else:
			sentiment_label = 'NEUTRAL'
		
		return render_template('index.html', sentence=requested_sentence, sentiment_label=sentiment_label, sentiment_score=overall_result, word_sentiment=word_sentiment_code)
	else:
		result = "method invalid passed"
		return render_template('index.html', result = result)


if __name__ == '__main__':
	app.debug = True
	app.run()
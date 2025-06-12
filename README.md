# Emphatic Emotional Mental Health Chatbot

An advanced AI-powered mental health chatbot that provides empathetic and supportive responses using state-of-the-art NLP techniques. The chatbot is designed to understand user emotions, provide appropriate responses, and maintain meaningful conversations.

## Features

- 🤖 **Advanced NLP Models**: Utilizes DistilBERT, BART-large-mnli, and FLAN-T5-large for sophisticated text understanding and generation
- 😊 **Emotion Detection**: Identifies 25 different emotions in user input
- 📊 **Sentiment Analysis**: Analyzes the sentiment of user messages
- 💬 **Contextual Responses**: Provides different types of responses based on the nature of the input:
  - Empathetic responses for emotional content
  - Knowledgeable answers for questions
  - Engaging conversation for general chat
- 🎤 **Voice Input Support**: Accepts both text and voice input
- 🌐 **Web Interface**: Clean and responsive web interface built with Flask and Bootstrap

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- HuggingFace API token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/mental-health-chatbot.git
cd mental-health-chatbot
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
Create a `.env` file in the root directory and add your HuggingFace API token:
```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Start chatting with the bot!

## Project Structure

```
mental-health-chatbot/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Project dependencies
├── models/
│   └── model_loader.py   # AI model loading and processing
├── static/
│   ├── css/
│   │   └── styles.css    # Custom styles
│   └── js/
│       └── scripts.js    # Frontend functionality
└── templates/
    └── index.html        # Main chat interface
```

## Technologies Used

- **Backend**:
  - Flask (Python web framework)
  - Transformers (HuggingFace)
  - LangChain
  - PyTorch

- **Frontend**:
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap
  - jQuery

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- HuggingFace for providing the pre-trained models
- The open-source community for their valuable contributions
- All contributors who have helped improve this project

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/mental-health-chatbot](https://github.com/yourusername/mental-health-chatbot) 
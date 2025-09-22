# 🎬 Movie Recommender System

A machine learning-based movie recommendation system that suggests movies to users based on their preferences using cosine similarity algorithms.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Model Development](#model-development)
- [Deployment](#deployment)
  

## 🎯 Overview

This project implements a content-based movie recommendation system that analyzes movie features and calculates similarity scores between movies to provide personalized recommendations. The system uses cosine similarity to find movies similar to a user's searched movie and suggests relevant titles.

## ✨ Features

- **Intelligent Recommendations**: Uses cosine similarity algorithm for accurate movie suggestions
- **User-Friendly Interface**: Intuitive frontend developed with PyCharm IDE
- **Large Dataset**: Trained on 5000+ movies from Kaggle
- **Real-time Search**: Instant movie recommendations based on user input
- **Data Processing**: Comprehensive data cleaning and preprocessing pipeline
- **Scalable Architecture**: Modular design for easy maintenance and updates

## 🛠️ Technologies Used

### Backend & Machine Learning
- **Python 3.8+**: Core programming language
- **scikit-learn**: Machine learning library for cosine similarity
- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **pickle**: Model serialization
- **ast**: Abstract syntax tree processing

### Development Environment
- **Jupyter Notebook**: Model development and experimentation
- **PyCharm IDE**: Frontend development and project management

### Additional Libraries
- **matplotlib/seaborn**: Data visualization (optional)
- **streamlit/flask**: Web framework (if applicable)

## 📊 Dataset

- **Source**: Kaggle Movies Dataset
- **Size**: 5,000 movies
- **Features**: Movie titles, genres, cast, crew, overview, ratings, etc.
- **Format**: CSV file with comprehensive movie information

## 🚀 Installation

### Prerequisites
```bash
Python 3.8 or higher
pip package manager
```

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/movie-recommender-system.git
cd movie-recommender-system
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv movie_env

# Activate virtual environment
# On Windows:
movie_env\Scripts\activate
# On macOS/Linux:
source movie_env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Dataset
1. Download the movie dataset from Kaggle
2. Place the CSV file in the `data/` directory
3. Update the file path in the configuration if necessary

## 💻 Usage

### Running the Jupyter Notebook (Model Development)
```bash
jupyter notebook
# Open 'movie_recommender_model.ipynb'
```

### Running the Application
```bash
# If using Streamlit
streamlit run app.py

# If using Flask
python app.py
```

### Basic Usage Example
```python
from movie_recommender import MovieRecommender

# Initialize the recommender
recommender = MovieRecommender()

# Load the trained model
recommender.load_model('models/movie_similarity_model.pkl')

# Get recommendations
recommendations = recommender.recommend_movies('The Dark Knight', num_recommendations=5)
print(recommendations)
```

## 📁 Project Structure

```
movie-recommender-system/
│
├── data/
│   ├── raw/
│   │   └── movies_dataset.csv
│   └── processed/
│       └── cleaned_movies.csv
│
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── data_preprocessing.ipynb
│   └── model_development.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── feature_extraction.py
│   ├── model.py
│   └── recommender.py
│
├── models/
│   ├── similarity_matrix.pkl
│   └── movie_features.pkl
│
├── frontend/
│   ├── app.py
│   ├── templates/
│   └── static/
│
├── tests/
│   ├── test_model.py
│   └── test_recommender.py
│
├── requirements.txt
├── setup.py
├── README.md
└── .gitignore
```

## 🧠 Model Development

### Data Preprocessing Steps
1. **Data Cleaning**: Remove duplicates, handle missing values
2. **Feature Engineering**: Extract relevant features (genres, cast, keywords)
3. **Text Processing**: Tokenization, stemming, stop word removal
4. **Vectorization**: Convert text data to numerical vectors

### Model Training Process
1. **Feature Extraction**: Create feature vectors for each movie
2. **Similarity Calculation**: Compute cosine similarity matrix
3. **Model Serialization**: Save trained model using pickle
4. **Validation**: Test model performance and accuracy

### Algorithm: Cosine Similarity
```python
from sklearn.metrics.pairwise import cosine_similarity

# Calculate similarity matrix
similarity_matrix = cosine_similarity(movie_features)
```

## 🌐 Deployment

### Local Deployment

#### Option 1: Streamlit (Recommended for beginners)
```bash
# Install Streamlit
pip install streamlit

# Run the application
streamlit run app.py
```

#### Option 2: Flask
```bash
# Install Flask
pip install flask

# Run the application
python app.py
```

### Cloud Deployment

#### Heroku Deployment
1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `runtime.txt`:
```
python-3.9.16
```

3. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

#### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy automatically

#### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

```bash
# Build and run Docker container
docker build -t movie-recommender .
docker run -p 8501:8501 movie-recommender
```

### Production Considerations
- **Caching**: Implement Redis for faster recommendations
- **Database**: Use PostgreSQL/MongoDB for movie data storage
- **API**: Create REST API endpoints for recommendations
- **Monitoring**: Add logging and error tracking
- **Security**: Implement input validation and rate limiting

## 🔧 Configuration

Create a `config.py` file:
```python
# Configuration settings
DATA_PATH = 'data/movies_dataset.csv'
MODEL_PATH = 'models/similarity_matrix.pkl'
NUM_RECOMMENDATIONS = 10
SIMILARITY_THRESHOLD = 0.1
```

## 📈 Performance Optimization

1. **Preprocessing**: Cache processed data
2. **Model Loading**: Load model once at startup
3. **Vectorization**: Use sparse matrices for memory efficiency
4. **Indexing**: Implement efficient search algorithms

## 🧪 Testing

Run tests using:
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_model.py -v
```



## 🙏 Acknowledgments

- Kaggle for providing the movie dataset
- scikit-learn community for excellent documentation
- PyCharm team for the powerful IDE



**⭐ Star this repository if you found it helpful!**

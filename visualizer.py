import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

class Visualizer:
    @staticmethod
    def create_wordcloud(text: str):
        if text:
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
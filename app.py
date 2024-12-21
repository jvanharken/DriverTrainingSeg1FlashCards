import streamlit as st
import random
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Flashcard:
    question: str
    answer: str
    category: str

class FlashcardApp:
    def __init__(self):
        self.flashcards: List[Flashcard] = []
        self.categories: set = set()
        self.load_flashcards()

    def load_flashcards(self):
        # Basic Vehicle Operations
        self.add_card(
            "How should the inside rear-view mirror be adjusted?",
            "To show the center of the road behind the vehicle",
            "Basic Vehicle Operations"
        )
        self.add_card(
            "What is the BEST way to see clearly in the direction your car is moving while backing?",
            "Turn your head and shoulders and look backward",
            "Basic Vehicle Operations"
        )
        self.add_card(
            "Before starting the engine, what should you check?",
            "Check all information gauges",
            "Basic Vehicle Operations"
        )
        
        # Road Safety
        self.add_card(
            "As the speed of a vehicle doubles, its destructive power in a crash:",
            "Increases by four times",
            "Road Safety"
        )
        self.add_card(
            "On slippery roads, you should stay at least how many seconds of travel time behind the vehicle ahead?",
            "4 seconds",
            "Road Safety"
        )
        self.add_card(
            "When passing a vehicle on a two-lane road, you should return to the right side when:",
            "You can see both headlights of the passed vehicle in your rear-view mirror",
            "Road Safety"
        )

        # Weather & Road Conditions
        self.add_card(
            "When driving in fog, you should:",
            "Drive slow enough to stop within the distance you can see",
            "Weather & Road Conditions"
        )
        self.add_card(
            "One danger of driving in fog is:",
            "Reduced traction",
            "Weather & Road Conditions"
        )
        self.add_card(
            "If you want to stop or slow down gradually when driving on ice, you should:",
            "Use light and steady pressure on the brakes",
            "Weather & Road Conditions"
        )

        # Traffic Rules
        self.add_card(
            "Michigan law requires headlights be used when there is not enough light to see people and vehicles clearly at:",
            "1,000 feet",
            "Traffic Rules"
        )
        self.add_card(
            "When the traffic signal light changes from green to yellow, you should:",
            "Stop before entering the intersection if you can do so safely",
            "Traffic Rules"
        )
        self.add_card(
            "If a police officer waves you on at an intersection when the traffic light is red, you should:",
            "Follow the directions of the officer",
            "Traffic Rules"
        )

        # Emergency Situations
        self.add_card(
            "If your vehicle's brakes fail completely, you may be able to stop safely by:",
            "Slowly applying the parking brake",
            "Emergency Situations"
        )
        self.add_card(
            "If your vehicle is skidding, you should:",
            "Turn the wheels in the direction you want to go",
            "Emergency Situations"
        )
        self.add_card(
            "When an emergency vehicle with siren sounding and lights flashing is approaching, you should:",
            "Move to the side of the road or shoulder and stop",
            "Emergency Situations"
        )

        # Special Topics
        self.add_card(
            "Having just one or two drinks before driving:",
            "Affects your reaction time and judgment",
            "Special Topics"
        )
        self.add_card(
            "Which organ of the body is affected FIRST by alcohol?",
            "Brain",
            "Special Topics"
        )
        self.add_card(
            "Michigan's safety belt use law requires front seat occupants to wear a safety belt:",
            "At all times",
            "Special Topics"
        )

    def add_card(self, question: str, answer: str, category: str):
        self.flashcards.append(Flashcard(question, answer, category))
        self.categories.add(category)

    def get_cards_by_category(self, category: str) -> List[Flashcard]:
        return [card for card in self.flashcards if card.category == category]

def main():
    st.set_page_config(page_title="Michigan Driver's Training Flashcards", layout="wide")
    
    # Custom CSS
    st.markdown("""
        <style>
        .big-font {
            font-size:20px !important;
            font-weight: bold;
        }
        .card {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f2f6;
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Michigan Driver's Training Flashcards")

    # Initialize the app state if not already done
    if 'app' not in st.session_state:
        st.session_state.app = FlashcardApp()
        st.session_state.current_cards = []
        st.session_state.current_index = 0
        st.session_state.show_answer = False

    # Sidebar for mode selection
    study_mode = st.sidebar.radio(
        "Select Study Mode",
        ["Study by Category", "Random Cards from All Categories"]
    )

    if study_mode == "Study by Category":
        category = st.sidebar.selectbox(
            "Select Category",
            sorted(st.session_state.app.categories)
        )
        if st.sidebar.button("Start/Reset Category"):
            st.session_state.current_cards = st.session_state.app.get_cards_by_category(category)
            random.shuffle(st.session_state.current_cards)
            st.session_state.current_index = 0
            st.session_state.show_answer = False
    else:
        if st.sidebar.button("Start/Reset Random Study"):
            st.session_state.current_cards = st.session_state.app.flashcards.copy()
            random.shuffle(st.session_state.current_cards)
            st.session_state.current_index = 0
            st.session_state.show_answer = False

    # Main content area
    if st.session_state.current_cards:
        current_card = st.session_state.current_cards[st.session_state.current_index]
        
        # Display progress
        progress = (st.session_state.current_index + 1) / len(st.session_state.current_cards)
        st.progress(progress)
        st.write(f"Card {st.session_state.current_index + 1} of {len(st.session_state.current_cards)}")
        
        # Display category
        st.markdown(f"**Category:** {current_card.category}")
        
        # Display question
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<p class='big-font'>Question:</p>", unsafe_allow_html=True)
        st.write(current_card.question)
        st.markdown("</div>", unsafe_allow_html=True)

        # Show/Hide answer button
        if st.button("Show/Hide Answer"):
            st.session_state.show_answer = not st.session_state.show_answer

        # Display answer if button was clicked
        if st.session_state.show_answer:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<p class='big-font'>Answer:</p>", unsafe_allow_html=True)
            st.write(current_card.answer)
            st.markdown("</div>", unsafe_allow_html=True)

        # Navigation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Previous Card") and st.session_state.current_index > 0:
                st.session_state.current_index -= 1
                st.session_state.show_answer = False
                st.experimental_rerun()

        with col2:
            if st.button("Next Card") and st.session_state.current_index < len(st.session_state.current_cards) - 1:
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.experimental_rerun()

    else:
        st.info("Please select a study mode and click the Start button in the sidebar to begin studying.")

if __name__ == "__main__":
    main()

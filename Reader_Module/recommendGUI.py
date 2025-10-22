from customtkinter import *
import threading
from openai import OpenAI
from Reader_Module.recommendFunctionality import get_recommendation_data

class RecommendGUI:
    def __init__(self, u_Id):
        self.u_Id = u_Id

        # ---------------- Popup window ----------------
        self.popup = CTkToplevel()
        self.popup.title("Recommended Books")
        self.popup.geometry("600x400")
        self.popup.resizable(False, False)

        # Bring to foreground
        self.popup.grab_set()
        self.popup.focus_force()

        # Title
        CTkLabel(
            self.popup,
            text="📚 Recommended for You",
            font=("Arial", 18, "bold"),
            justify="center",
            wraplength=550
        ).pack(pady=(15, 10), padx=10)

        # Scrollable frame
        self.scrollable_frame = CTkScrollableFrame(self.popup, corner_radius=10)
        self.scrollable_frame.pack(padx=15, pady=10, fill="both", expand=True)

        # Label to show recommendations
        self.recommendations_label = CTkLabel(
            self.scrollable_frame,
            text="Loading recommendations, please wait...",
            font=("Arial", 14),
            wraplength=520,
            justify="left"
        )
        self.recommendations_label.pack(padx=10, pady=10, anchor="nw")

        # Close button
        CTkButton(self.popup, text="Close", width=100, command=self.popup.destroy).pack(pady=(5, 10))

        # Fetch recommendations in a separate thread
        threading.Thread(target=self.fetch_recommendations, daemon=True).start()

    def fetch_recommendations(self):
        try:
            api_key = "Your API key"
            client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

            available_books, borrowed_books = get_recommendation_data(self.u_Id)
            available_titles = [f"{b['title']} by {b['author']}" for b in available_books]

            prompt = (
                "You are an AI recommending books.\n"
                f"The user has previously borrowed the following book IDs: {borrowed_books}\n"
                f"The following books are currently available: {available_titles}\n"
                "Recommend 3 books to the user in normal paragraphs based on their previous history, "
                "but only from the available books. Give a short reason for each recommendation."
            )

            response = client.responses.create(input=prompt, model="openai/gpt-oss-20b")
            recommendations = response.output_text.strip() if hasattr(response, "output_text") else "No recommendations found."

        except Exception as e:
            recommendations = f"⚠️ Error fetching recommendations:\n{e}"

        # Update label in main thread
        self.recommendations_label.after(0, lambda: self.recommendations_label.configure(text=recommendations))

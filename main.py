import math
import sympy as sp
import numpy as np
import tkinter as tk
import smtplib
import webbrowser
import os
from kivy.uix.image import Image
from tkinter import simpledialog, messagebox
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function to solve linear equations
def solve_linear_equation(equation):
    symbols = set(ch for ch in equation if ch.isalpha())  # Get all alphabets from the equation
    symbols = [sp.symbols(symbol) for symbol in symbols]  # Create symbols dynamically
    lhs, rhs = equation.split('=')
    for symbol in symbols:
        lhs = lhs.replace(symbol.name, f'*{symbol.name}')  # Replace each symbol in lhs with '*symbol'
    lhs = sp.sympify(lhs)
    rhs = sp.sympify(rhs)
    solution = sp.solve(lhs - rhs, symbols)
    return solution


# Function to solve quadratic equations
def solve_quadratic_equation(a, b, c):
    x = sp.symbols('x')
    solutions = sp.solve(a * x ** 2 + b * x + c, x)
    return solutions


# Function to solve polynomial equations
def solve_polynomial_equation(coefficients):
    x = sp.symbols('x')
    polynomial = sum(coef * x ** i for i, coef in enumerate(reversed(coefficients)))
    roots = sp.solve(polynomial, x)
    return roots


# Function to solve cubic equations
def solve_cubic_equation(a, b, c, d):
    x = sp.symbols('x')
    cubic_eq = a * x ** 3 + b * x ** 2 + c * x + d
    roots = sp.solve(cubic_eq, x)
    return roots


# Function to differentiate expressions
def differentiate(expression):
    x = sp.symbols('x')
    expr = sp.sympify(expression)
    derivative = sp.diff(expr, x)
    return derivative


# Function to integrate expressions
def integrate(expression):
    x = sp.symbols('x')
    expr = sp.sympify(expression)
    integral = sp.integrate(expr, x)
    return integral


# Function to invert a matrix
def matrix_inversion(matrix):
    try:
        inv_matrix = np.linalg.inv(matrix)
        return inv_matrix
    except np.linalg.LinAlgError:
        return None


# Function to calculate determinant of a matrix
def matrix_determinant(matrix):
    try:
        det = np.linalg.det(matrix)
        return det
    except np.linalg.LinAlgError:
        return None


from kivy.uix.button import Button

class DestiSolverApp(App):
    def build(self):
        layout = GridLayout(cols=2, padding=10)

        # Add welcome message
        welcome_message = "Welcome to DestiSolver AI! Get ready to explore the world of mathematics"
        self.welcome_label = Label(text=welcome_message, font_size=20)
        layout.add_widget(self.welcome_label)

        # Add logo image
        try:
            logo_path = "C:/Users/ENGR. DESTINY/Downloads/icon/icon_bg.ico"  # Replace with the actual path to your logo image
            self.logo_image = Image(source=logo_path, size_hint=(1, None), width=500, height=400)
            layout.add_widget(self.logo_image)
        except FileNotFoundError:
            self.logo_label = Label(text="Logo not found")
            layout.add_widget(self.logo_label)

        self.label = Label(text="Select an option and explore by asking the ai some questions ")
        layout.add_widget(self.label)

        options = [
            "Select Your Problem",
            "Simple Calculator Add, Sub, Divide, Multiply",
            "Solve linear equation",
            "Solve quadratic equation",
            "Solve polynomial equation",
            "Solve cubic equation",
            "Differentiate expression",
            "Integrate expression",
            "Exponential functions",
            "Trigonometric functions",
            "Matrix Inversion",
            "Matrix Determinant",
            "None Of The Above"
        ]
        self.option_menu = DropDown()
        for option in options:
            btn = Button(text=option, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.option_selected(btn.text))
            self.option_menu.add_widget(btn)

        self.option_button = Button(text='Select Your Problem', size_hint=(None, None), width=200, height=40)
        self.option_button.bind(on_release=self.option_menu.open)
        layout.add_widget(self.option_button)

        self.suggest_button = Button(text="Suggest Questions", size_hint=(None, None), width=200, height=40)
        self.suggest_button.bind(on_release=self.suggest_questions)
        layout.add_widget(self.suggest_button)

        self.run_button = Button(text="Run", size_hint=(None, None), width=200, height=40)
        self.run_button.bind(on_release=self.run_option)
        layout.add_widget(self.run_button)

        self.suggest_improvement_button = Button(text="Suggest Improvement", size_hint=(None, None), width=200,
                                                 height=40)
        self.suggest_improvement_button.bind(on_release=self.suggest_improvement)
        layout.add_widget(self.suggest_improvement_button)

        self.about_button = Button(text="About", size_hint=(None, None), width=200, height=40)
        self.about_button.bind(on_release=self.display_about)
        layout.add_widget(self.about_button)

        self.instruction_button = Button(text="Instructions", size_hint=(None, None), width=200, height=40)
        self.instruction_button.bind(on_release=self.display_instructions)
        layout.add_widget(self.instruction_button)

        self.guide_button = Button(text="Guide", size_hint=(None, None), width=200, height=40)
        self.guide_button.bind(on_release=self.display_guide)
        layout.add_widget(self.guide_button)

        self.call_button = Button(text="Call Us", size_hint=(None, None), width=200, height=40)
        self.call_button.bind(on_release=self.call_phone)
        layout.add_widget(self.call_button)

        self.email_button = Button(text="Email Us", size_hint=(None, None), width=200, height=40)
        self.email_button.bind(on_release=self.email_us)
        layout.add_widget(self.email_button)

        self.site_selection_button = Button(text="Search Math Problems on Google", size_hint=(None, None), width=280, height=40)
        self.site_selection_button.bind(on_release=self.select_site)
        layout.add_widget(self.site_selection_button)

        self.notes_button = Button(text="Take Notes", size_hint=(None, None), width=200, height=40)
        self.notes_button.bind(on_release=self.take_notes)
        layout.add_widget(self.notes_button)

        qa_chart_button = Button(text="Questions & Answers Chart", size_hint=(None, None), width=250, height=40)
        qa_chart_button.bind(on_release=self.display_qa_chart)
        layout.add_widget(qa_chart_button)

        self.social_media_button = Button(text="Follow us on Social Media", size_hint=(None, None), width=220, height=40)
        self.social_media_button.bind(on_release=self.redirect_to_social_media)
        layout.add_widget(self.social_media_button)

        self.update_button = Button(text="App Update", size_hint=(None, None), width=200, height=40)
        self.update_button.bind(on_release=self.check_for_update)
        layout.add_widget(self.update_button)

        self.support_button = Button(text="Support Development", size_hint=(None, None), width=200, height=40)
        self.support_button.bind(on_release=self.display_support_details)
        layout.add_widget(self.support_button)

        self.exit_button = Button(text="Exit", size_hint=(None, None), width=200, height=40)
        self.exit_button.bind(on_release=self.exit_app)
        layout.add_widget(self.exit_button)

        self.current_option = None

        return layout

        # Add button to view saved notes
        view_notes_button = Button(text="View Saved Notes", size_hint=(None, None), width=200, height=40)
        view_notes_button.bind(on_release=self.view_saved_notes)
        layout.add_widget(view_notes_button)

        return layout

    def select_site(self, instance):
        sites = ["Google", "Bing", "Yahoo", "DuckDuckGo", "Ask", "Yandex"]  # Add more sites if needed
        popup_content = GridLayout(cols=1, spacing=10, padding=10)

        for site in sites:
            btn = Button(text=site, size_hint=(None, None), width=200, height=40)
            btn.bind(on_release=lambda btn, site=site: self.search_math_on_site(site))
            popup_content.add_widget(btn)

        back_button = Button(text="Back To Main Menu", size_hint=(None, None), width=200, height=40)
        back_button.bind(on_release=lambda instance: popup.dismiss())
        popup_content.add_widget(back_button)

        popup = Popup(title="Select Search Engine", content=popup_content, size_hint=(None, None), size=(300, 420))
        popup.open()


    def search_math_on_site(self, site):
        query = "site:StudyXmathAi.com"  # Modify this to target specific sites or queries
        if site.lower() == "google":
            url = f"https://www.google.com/search?q={query}"
        elif site.lower() == "bing":
            url = f"https://www.bing.com/search?q={query}"
        elif site.lower() == "yahoo":
            url = f"https://search.yahoo.com/search?p={query}"
        elif site.lower() == "duckduckgo":
            url = f"https://duckduckgo.com/?q={query}"
        elif site.lower() == "ask":
            url = f"https://www.ask.com/web?q={query}"
        elif site.lower() == "yandex":
            url = f"https://yandex.com/search/?text={query}"
        else:
            return  # Handle unsupported site
        webbrowser.open("https://www.bing.com/ck/a?!&&p=760ba9b7eda3d509JmltdHM9MTcxNzU0NTYwMCZpZ3VpZD0zZWY0MGE1Ni03MDg0LTY4MmYtM2QzNC0xZTI3NzE0ZjY5MWQmaW5zaWQ9NTIwOA&ptn=3&ver=2&hsh=3&fclid=3ef40a56-7084-682f-3d34-1e27714f691d&psq=site+for+solving+math+problems+ai&u=a1aHR0cHM6Ly9zdHVkeXguYWkvbWF0aC1zb2x2ZXI&ntb=1")


    def display_instructions(self, instance):
        instructions_text = (
            "Instructions:\n\n"
            "1. Select your problem from the dropdown menu.\n"
            "2. Read the problem carefully and input the required information.\n"
            "3. Click on 'Suggest Questions' to get example questions related to the selected problem.\n"
            "4. Click on 'Run' to solve the problem.\n"
            "5. You can also click on 'About' to know more about DestiSolver AI.\n"
            "6. To exit the application, click on 'Exit'.\n\n"
            "Additional Features:\n\n"
            "- Click on 'Instructions' to view these instructions again.\n"
            "- Click on 'Follow us on Social Media' to connect with us on various platforms."
        )
        popup = Popup(title='Instructions', content=Label(text=instructions_text), size_hint=(None, None),
                      size=(400, 400))
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), width=200, height=40)
        back_button.bind(on_release=popup.dismiss)
        popup.content.add_widget(back_button)
        popup.open()

    def check_for_update(self, instance):
        # Code to check for app update goes here
        webbrowser.open("https://your-update-url.com")

    def suggest_improvement(self, instance):
        # Pre-defined suggested improvements
        predefined_improvements = (
            "Solver Interface: Enhance the user interface of the solver to make it more intuitive and user-friendly.\n",
            "Feature Request: Include additional features such as [describe feature] to expand the functionality of the solver.\n",
            "Performance Optimization: Optimize the solver algorithms for faster computation and response times.\n",
            "Bug Fixes: Address any known bugs or issues to ensure a smoother user experience.\n",
            "Documentation Update: Improve the documentation to provide clearer instructions and examples for users.\n"
        )

        # Convert predefined improvements to a single string
        predefined_improvements_str = "\n".join(predefined_improvements)

        # Email body including predefined improvements
        email_body = predefined_improvements_str

        # Open the URL that redirects the user to Gmail's compose email page
        webbrowser.open(
            "https://mail.google.com/mail/?view=cm&fs=1&to=destisolverai@gmail.com&su=Suggestion%20for%20Improvement&body=" + email_body)

    def display_guide(self, instance):
        guide_text = (
            "Guide:\n\n"
            "This guide will help you understand how to use the DestiSolver AI application.\n\n"
            "1. Overview of Features:\n"
            "   - Simple Calculator: Perform basic arithmetic operations.\n"
            "   - Equation Solvers: Solve linear, quadratic, polynomial, and cubic equations.\n"
            "   - Differentiation and Integration: Find derivatives and integrals of expressions.\n"
            "   - Function Analysis: Work with exponential and trigonometric functions.\n"
            "   - Matrix Operations: Inverse matrices and find determinants.\n"
            "2. How to Use:\n"
            "   - Select an option from the dropdown menu.\n"
            "   - Follow on-screen prompts to input data.\n"
            "   - Click 'Run' to execute the selected option.\n"
            "   - View results and suggested questions for further learning.\n"
            "3. Additional Tips:\n"
            "   - Ensure your inputs are correct for accurate results.\n"
            "   - Use the 'Suggest Questions' button to explore related topics.\n"
            "   - Check the 'About' section to learn more about the app.\n"
            "   - Follow us on social media for updates and support."
        )
        popup_content = GridLayout(cols=1, padding=10)
        popup_content.add_widget(Label(text=guide_text))

        back_button = Button(text="Back to Main Menu", size_hint=(None, None), width=200, height=40)
        back_button.bind(on_release=lambda x: popup.dismiss())
        popup_content.add_widget(back_button)

        popup = Popup(title='Guide', content=popup_content, size_hint=(None, None), size=(600, 600))
        popup.open()

    def call_phone(self, instance):
        phone_number = "tel:+234 9068754630"  # Replace with your phone number
        webbrowser.open(phone_number)

    def email_us(self, instance):
        email_services = [
            ("Gmail", "https://mail.google.com/mail/u/0/?view=cm&fs=1&to=destisolverai@gmail.com&su=Support%20Request"),
            ("Yahoo Mail", "https://compose.mail.yahoo.com?to=destisolverai@gmail.com&subject=Support%20Request"),
            ("Outlook", "https://outlook.live.com/owa/?path=/mail/action/compose&to=destisolverai@gmail.com&subject=Support%20Request"),
            ("Other", "https://www.example.com")  # Change the URL to your desired fallback website
        ]

        popup_content = GridLayout(cols=1, spacing=10, padding=10)

        for service, url in email_services:
            btn = Button(text=service, size_hint=(None, None), width=200, height=40)
            btn.bind(on_release=lambda btn, url=url: self.open_email_service(url))
            popup_content.add_widget(btn)

        back_button = Button(text="Back to Main Menu", size_hint=(None, None), width=200, height=40)
        back_button.bind(on_release=lambda instance: popup.dismiss())
        popup_content.add_widget(back_button)

        popup = Popup(title="Select Email Service", content=popup_content, size_hint=(None, None), size=(300, 340))
        popup.open()

    def open_email_service(self, url):
        webbrowser.open(url, new=2)

    def display_support_details(self, instance):
        support_details = (
            "Thank you for considering supporting DestiSolver AI!\n\n"
            "You can support us via the following methods:\n\n"
            "1. Dollar Account:\n"
            "   Account name: DESTINY AKHERE\n"
            "   Bank: Wells Fargo\n"
            "   Account number: 40630261076553345\n"
            "   Routing number: 121000248\n"
            "   Swift Code: WFBIUS6S\n"
            "   Account Type: BUSINESS CHECKING\n"
            "   Address: 9450 Southwest Gemini Drive, Beaverton, OR, 97008, USA\n\n"
            "2. Palmpay: 9068754630\n"
            "\n"
            "3. Opay: 9068754630\n"
            "\n"
            "4. Bank Transfer: Acct Name: Destiny Akhere, Acct No: 2408195540\n"
            "   Bank Name: Zenith Bank Plc\n\n"
            "5. Other: Contact us for alternative methods - 09068754630 or 07050562437\n"
            "   or Email @destisolverai\n"
            "       \n"
            "Also you can support us by following our Social Media Platform @destisolverai\n"
        )

        popup_content = GridLayout(cols=1, spacing=10, padding=10)
        popup_content.add_widget(Button(text=support_details, size_hint=(None, None), size=(700, 650)))

        # Add back button
        back_button = Button(text="Back", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=self.dismiss_popup)
        popup_content.add_widget(back_button)

        popup = Popup(title="Support Development", content=popup_content, size_hint=(None, None), size=(800, 800))
        popup.open()

    def contact_support(self, instance):
        webbrowser.open("mailto:support@destisolverai.com?subject=Support%20Request")

    def dismiss_popup(self, instance):
        # Dismiss the popup
        for widget in instance.parent.children:
            if isinstance(widget, Popup):
                widget.dismiss()

    def take_notes(self, instance):
        popup_content = GridLayout(cols=1, padding=10)

        self.notes_input = TextInput(text="", multiline=True, size_hint=(None, None), width=350, height=300)
        popup_content.add_widget(self.notes_input)

        save_button = Button(text="Save", size_hint=(None, None), width=200, height=40)
        save_button.bind(on_release=self.save_notes)
        popup_content.add_widget(save_button)

        view_notes_button = Button(text="View Saved Notes", size_hint=(None, None), width=200, height=40)
        view_notes_button.bind(on_release=self.view_saved_notes)
        popup_content.add_widget(view_notes_button)

        back_button = Button(text="Back to Main Menu", size_hint=(None, None), width=200, height=40)
        back_button.bind(on_release=lambda x: popup.dismiss())
        popup_content.add_widget(back_button)

        self.notes_popup = Popup(title='Notes', content=popup_content, size_hint=(None, None), size=(400, 400))
        self.notes_popup.open()

    def save_notes(self, instance):
        notes = self.notes_input.text
        save_dir = os.path.join(os.path.dirname(__file__), "saved_notes")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, "notes.txt")
        with open(save_path, "w") as notes_file:
            notes_file.write(notes)
        self.notes_popup.dismiss()  # Dismiss the notes popup
        self.view_saved_notes()

    def view_saved_notes(self):
        save_dir = os.path.join(os.path.dirname(__file__), "saved_notes")
        notes_path = os.path.join(save_dir, "notes.txt")
        try:
            with open(notes_path, "r") as notes_file:
                notes_content = notes_file.read()
                view_notes_popup = Popup(title='View Saved Notes', content=Label(),  # Remove multiline=True
                                         size_hint=(None, None), size=(400, 400))
                view_notes_popup.content.text = notes_content  # Set the text and multiline property
                view_notes_popup.content.multiline = True

                # Add a button to close the popup
                back_button = Button(text="Back", size_hint=(None, None), size=(100, 50))
                back_button.bind(on_release=view_notes_popup.dismiss)
                view_notes_popup.content.add_widget(back_button)

                view_notes_popup.open()
        except FileNotFoundError:
            error_popup = Popup(title='Error', content=Label(text='No notes found!'), size_hint=(None, None),
                                size=(300, 200))
            error_popup.open()

    def display_qa_chart(self, instance):
        qa_chart_text = (
            "Questions & Answers Chart:\n\n"
        "Q: What is 2 + 2?\n"
        "A: 2 + 2 is 4.\n\n"
        "Q: What is the capital of France?\n"
        "A: The capital of France is Paris.\n\n"
        "Q: What is the square root of 16?\n"
        "A: The square root of 16 is 4.\n\n"
        "Q: Who wrote 'Romeo and Juliet'?\n"
        "A: 'Romeo and Juliet' was written by William Shakespeare.\n\n"
        "Q: What is the chemical symbol for water?\n"
        "A: The chemical symbol for water is H2O.\n\n"
        "Q: Who discovered penicillin?\n"
        "A: Penicillin was discovered by Alexander Fleming."
    )

        popup_content = GridLayout(cols=1, padding=10)

        qa_label = Label(text=qa_chart_text)
        popup_content.add_widget(qa_label)

        # Add button to redirect to external QA site (Stack Overflow)
        stackoverflow_button = Button(text="More Q&A (Stack Overflow)", size_hint=(None, None), size=(250, 40))
        stackoverflow_button.bind(on_release=self.redirect_to_stackoverflow)
        popup_content.add_widget(stackoverflow_button)

        # Add button to redirect to external QA site (Quora)
        quora_button = Button(text="More Q&A (Quora)", size_hint=(None, None), size=(200, 40))
        quora_button.bind(on_release=self.redirect_to_quora)
        popup_content.add_widget(quora_button)

        # Add button to redirect to instructions
        instructions_button = Button(text="Instructions", size_hint=(None, None), size=(200, 40))
        instructions_button.bind(on_release=self.display_instructions)
        popup_content.add_widget(instructions_button)

        back_button = Button(text="Back to Main Menu", size_hint=(None, None), width=200, height=40)
        back_button.bind(on_release=lambda x: popup.dismiss())
        popup_content.add_widget(back_button)

        popup = Popup(title='Questions & Answers Chart', content=popup_content, size_hint=(None, None), size=(600, 700))
        popup.open()

    def redirect_to_stackoverflow(self, instance):
        # Redirect user to Stack Overflow's homepage
        import webbrowser
        webbrowser.open("https://stackoverflow.com/")

    def redirect_to_quora(self, instance):
        # Redirect user to Quora's homepage
        import webbrowser
        webbrowser.open("https://www.quora.com/")

    def display_instructions(self, instance):
        instructions_text = (
            "To access the websites:\n\n"
            "1. Click on the respective 'More Q&A' button.\n\n"
            "2. You will be directed to the homepage of the selected\n"
            " website, where you can browse questions and answers\n"
            "on various topics.\n\n"
            "3. If you wish to interact with the community by asking\n"
            "questions or providing answers, you may need\n"
            "to sign up or log in to your account on the respective website.\n\n"
            "4. If you don't have an account, you can typically create one\n"
            "by clicking on the 'Sign Up' link\n"
            "on the website's homepage and following the instructions.\n"
            "\n"
            "Thank you for Choosing DESTISOLVERAI\n"
            "Your All Problem Solving Ai feel free to tell us what to add for\n"
            "effective use by users One Love From Us @Nigeria\n"
        )

        popup_content = GridLayout(cols=1, padding=10)

        instructions_label = Label(text=instructions_text)
        popup_content.add_widget(instructions_label)

        back_button = Button(text="Back", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda x: popup.dismiss())
        popup_content.add_widget(back_button)

        popup = Popup(title='Instructions', content=popup_content, size_hint=(None, None), size=(600, 600))
        popup.open()

    # Add the redirect_to_social_media method
    def redirect_to_social_media(self, instance):
        # Create a layout for the popup
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Create buttons for each social media link
        facebook_button = Button(text='Facebook', size_hint_y=None, height=30)
        facebook_button.bind(
            on_release=lambda btn: webbrowser.open_new_tab('https://www.facebook.com/profile.php?id=61560834925041'))
        layout.add_widget(facebook_button)

        twitter_button = Button(text='Twitter', size_hint_y=None, height=30)
        twitter_button.bind(on_release=lambda btn: webbrowser.open_new_tab('https://x.com/DestiSolver_Ai'))
        layout.add_widget(twitter_button)

        instagram_button = Button(text='Instagram', size_hint_y=None, height=30)
        instagram_button.bind(
            on_release=lambda btn: webbrowser.open_new_tab('https://www.instagram.com/destisolver_ai/#'))
        layout.add_widget(instagram_button)

        threads_button = Button(text='Threads', size_hint_y=None, height=30)
        threads_button.bind(on_release=lambda btn: webbrowser.open_new_tab('https://www.threads.net/@destisolver_ai'))
        layout.add_widget(threads_button)

        # Create a cancel button to close the popup
        cancel_button = Button(text='Cancel', size_hint_y=None, height=30)
        cancel_button.bind(on_release=lambda btn: popup.dismiss())
        layout.add_widget(cancel_button)

        # Create the popup
        popup = Popup(title='Follow Us on Social Media',
                      content=layout,
                      size_hint=(None, None), size=(400, 300))

        # Open the popup
        popup.open()

    def option_selected(self, text):
        self.option_button.text = text
        self.option_menu.dismiss()
        self.current_option = text

    def suggest_questions(self, instance):
        selected_option = self.option_button.text
        suggestions = {
            "Simple Calculator Add, Sub, Divide, Multiply": ["2 + 3", "4 * 5", "6 / 2", "7 - 4"],
            "Solve linear equation": ["2x + 3 = 0", "5x - 10 = 0"],
            "Solve quadratic equation": ["1x^2 - 3x + 2", "2x^2 + 4x + 2"],
            "Solve polynomial equation": ["3x^3 - 2x^2 + x - 5", "x^4 - 16"],
            "Solve cubic equation": ["x^3 + 2x^2 + 3x + 4", "x^3 - 6x^2 + 11x - 6"],
            "Differentiate expression": ["x^2 + 2x + 1", "sin(x) * cos(x)"],
            "Integrate expression": ["x^2", "1 / x"],
            "Exponential functions": ["e^x", "2^x"],
            "Trigonometric functions": ["sin(x)", "cos(x)", "tan(x)"],
            "Matrix Inversion": ["[[1, 2], [3, 4]]"],
            "Matrix Determinant": ["[[1, 2], [3, 4]]"]
        }
        suggestion_text = '\n'.join(suggestions.get(selected_option, ["No suggestions available."]))
        popup = Popup(title='Suggestions',
                      content=Label(text=f"Suggestions for {selected_option}:\n\n{suggestion_text}"),
                      size_hint=(None, None), size=(400, 400))
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), width=200, height=40)
        back_button.bind(on_release=popup.dismiss)
        popup.content.add_widget(back_button)
        popup.open()
        popup.open()

    def run_option(self, instance):
        if self.current_option:
            self.show_instructions()

        popup = Popup(title='Instructions',
                      content=Label(text=instructions),
                      size_hint=(None, None), size=(400, 400))

        # Add next button to enter the solver
        next_button = Button(text="Next", size_hint=(None, None), size=(200, 40))
        next_button.bind(on_release=self.enter_solver)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(popup.content)
        layout.add_widget(next_button)

        popup.content = layout
        popup.open()

    def enter_solver(self, instance):
        self.process_option()

    def run_option(self, instance):
        self.process_option()

    def process_option(self):
        if self.current_option:
            if self.current_option == "Simple Calculator Add, Sub, Divide, Multiply":
                self.calculate()
            elif self.current_option == "Solve linear equation":
                self.solve_linear()
            elif self.current_option == "Solve quadratic equation":
                self.solve_quadratic()
            elif self.current_option == "Solve polynomial equation":
                self.solve_polynomial()
            elif self.current_option == "Solve cubic equation":
                self.solve_cubic()
            elif self.current_option == "Differentiate expression":
                self.differentiate_expression()
            elif self.current_option == "Integrate expression":
                self.integrate_expression()
            elif self.current_option == "Exponential functions":
                self.exponential_functions()
            elif self.current_option == "Trigonometric functions":
                self.trigonometric_functions()
            elif self.current_option == "Matrix Inversion":
                self.matrix_inversion()
            elif self.current_option == "Matrix Determinant":
                self.matrix_determinant()
            elif self.current_option == "None Of The Above":
                self.general_answer()

    def calculate(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter values to calculate (Add: +, Subtract: -, Multiply: *, Divide: /):"))
        expression_input = TextInput()
        content.add_widget(expression_input)

        popup = Popup(title='Calculate', content=content, size_hint=(None, None), size=(600, 400), auto_dismiss=False)

        def on_calculate(instance):
            expression = expression_input.text
            if expression:
                try:
                    result = eval(expression, {'__builtins__': None},
                                  {'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                                   'exp': math.exp,
                                   'log': math.log, 'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh})
                    result_label.text = f"The Answer Is =: {result}"
                except Exception as e:
                    result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        calculate_button = Button(text="Calculate")
        calculate_button.bind(on_release=on_calculate)
        content.add_widget(result_label)
        content.add_widget(calculate_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def solve_linear(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter linear equation (e.g., 2x + 3 = 0):"))
        equation_input = TextInput()
        content.add_widget(equation_input)

        popup = Popup(title='Solve Linear Equation', content=content, size_hint=(None, None), size=(600, 400),
                      auto_dismiss=False)

        def on_solve(instance):
            equation = equation_input.text
            if equation:
                try:
                    solution = solve_linear_equation(equation)
                    result_label.text = f"The solution is: {solution}"
                except Exception as e:
                    result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        solve_button = Button(text="Solve")
        solve_button.bind(on_release=on_solve)
        content.add_widget(result_label)
        content.add_widget(solve_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def solve_quadratic(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter coefficients a, b, c for ax^2 + bx + c = 0:"))
        a_input = TextInput(hint_text="a")
        b_input = TextInput(hint_text="b")
        c_input = TextInput(hint_text="c")
        content.add_widget(a_input)
        content.add_widget(b_input)
        content.add_widget(c_input)

        popup = Popup(title='Solve Quadratic Equation', content=content, size_hint=(None, None), size=(600, 400),
                      auto_dismiss=False)

        def on_solve(instance):
            try:
                a = float(a_input.text)
                b = float(b_input.text)
                c = float(c_input.text)
                solutions = solve_quadratic_equation(a, b, c)
                result_label.text = f"The solutions are: {solutions}"
            except Exception as e:
                result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        solve_button = Button(text="Solve")
        solve_button.bind(on_release=on_solve)
        content.add_widget(result_label)
        content.add_widget(solve_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def solve_polynomial(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(
            text="Enter polynomial coefficients as comma-separated values (e.g., 1, -3, 2 for x^2 - 3x + 2):"))
        coefficients_input = TextInput()
        content.add_widget(coefficients_input)

        popup = Popup(title='Solve Polynomial Equation', content=content, size_hint=(None, None), size=(600, 400),
                      auto_dismiss=False)

        def on_solve(instance):
            coefficients = coefficients_input.text.split(',')
            coefficients = [float(coef) for coef in coefficients]
            if coefficients:
                try:
                    solutions = solve_polynomial_equation(coefficients)
                    result_label.text = f"The solutions are: {solutions}"
                except Exception as e:
                    result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        solve_button = Button(text="Solve")
        solve_button.bind(on_release=on_solve)
        content.add_widget(result_label)
        content.add_widget(solve_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def solve_cubic(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter coefficients a, b, c, d for ax^3 + bx^2 + cx + d = 0:"))
        a_input = TextInput(hint_text="a")
        b_input = TextInput(hint_text="b")
        c_input = TextInput(hint_text="c")
        d_input = TextInput(hint_text="d")
        content.add_widget(a_input)
        content.add_widget(b_input)
        content.add_widget(c_input)
        content.add_widget(d_input)

        popup = Popup(title='Solve Cubic Equation', content=content, size_hint=(None, None), size=(600, 400),
                      auto_dismiss=False)

        def on_solve(instance):
            try:
                a = float(a_input.text)
                b = float(b_input.text)
                c = float(c_input.text)
                d = float(d_input.text)
                solutions = solve_cubic_equation(a, b, c, d)
                result_label.text = f"The solutions are: {solutions}"
            except Exception as e:
                result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        solve_button = Button(text="Solve")
        solve_button.bind(on_release=on_solve)
        content.add_widget(result_label)
        content.add_widget(solve_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def differentiate_expression(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter the expression to differentiate (e.g., x^2 + 2x + 1):"))
        expression_input = TextInput()
        content.add_widget(expression_input)

        popup = Popup(title='Differentiate Expression', content=content, size_hint=(None, None), size=(600, 400),
                      auto_dismiss=False)

        def on_differentiate(instance):
            expression = expression_input.text
            if expression:
                try:
                    result = differentiate(expression)
                    result_label.text = f"The derivative is: {result}"
                except Exception as e:
                    result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        differentiate_button = Button(text="Differentiate")
        differentiate_button.bind(on_release=on_differentiate)
        content.add_widget(result_label)
        content.add_widget(differentiate_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def integrate_expression(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter the expression to integrate (e.g., x^2):"))
        expression_input = TextInput()
        content.add_widget(expression_input)

        popup = Popup(title='Integrate Expression', content=content, size_hint=(None, None), size=(600, 400),
                      auto_dismiss=False)

        def on_integrate(instance):
            expression = expression_input.text
            if expression:
                try:
                    result = integrate(expression)
                    result_label.text = f"The integral is: {result}"
                except Exception as e:
                    result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        integrate_button = Button(text="Integrate")
        integrate_button.bind(on_release=on_integrate)
        content.add_widget(result_label)
        content.add_widget(integrate_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def exponential_functions(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter the base and exponent (e.g., 2^3):"))
        expression_input = TextInput()
        content.add_widget(expression_input)

        popup = Popup(title='Exponential Functions', content=content, size_hint=(None, None), size=(600, 400),
                      auto_dismiss=False)

        def on_calculate(instance):
            expression = expression_input.text
            if expression:
                try:
                    base, exponent = expression.split('^')
                    base = float(base)
                    exponent = float(exponent)
                    result = base ** exponent
                    result_label.text = f"The result is: {result}"
                except Exception as e:
                    result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        calculate_button = Button(text="Calculate")
        calculate_button.bind(on_release=on_calculate)
        content.add_widget(result_label)
        content.add_widget(calculate_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def trigonometric_functions(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter the trigonometric function (e.g., sin(30), cos(45), tan(60), Note: After The Answer Is Giving Approximate It If Needed):"))
        expression_input = TextInput()
        content.add_widget(expression_input)

        popup = Popup(title='Trigonometric Functions', content=content, size_hint=(None, None), size=(1000, 400),
                      auto_dismiss=False)

        def on_calculate(instance):
            expression = expression_input.text
            if expression:
                try:
                    result = eval(expression, {'__builtins__': None},
                                  {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'radians': math.radians})
                    result_label.text = f"The result is: {result}"
                except Exception as e:
                    result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        calculate_button = Button(text="Calculate")
        calculate_button.bind(on_release=on_calculate)
        content.add_widget(result_label)
        content.add_widget(calculate_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def matrix_inversion(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter the matrix as comma-separated rows (e.g., [[1, 2], [3, 4]]):"))
        matrix_input = TextInput()
        content.add_widget(matrix_input)

        popup = Popup(title='Matrix Inversion', content=content, size_hint=(None, None), size=(600, 400),
                      auto_dismiss=False)

        def on_invert(instance):
            matrix_str = matrix_input.text
            if matrix_str:
                try:
                    matrix = eval(matrix_str)
                    result = matrix_inversion(matrix)
                    result_label.text = f"The inverted matrix is: {result}"
                except Exception as e:
                    result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        invert_button = Button(text="Invert")
        invert_button.bind(on_release=on_invert)
        content.add_widget(result_label)
        content.add_widget(invert_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def matrix_determinant(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Enter the matrix as comma-separated rows (e.g., [[1, 2], [3, 4]]):"))
        matrix_input = TextInput()
        content.add_widget(matrix_input)

        popup = Popup(title='Matrix Determinant', content=content, size_hint=(None, None), size=(600, 400),
                      auto_dismiss=False)

        def on_calculate(instance):
            matrix_str = matrix_input.text
            if matrix_str:
                try:
                    matrix = eval(matrix_str)
                    result = matrix_determinant(matrix)
                    result_label.text = f"The determinant is: {result}"
                except Exception as e:
                    result_label.text = f"Error: {str(e)}"

        result_label = Label(text="")
        calculate_button = Button(text="Calculate")
        calculate_button.bind(on_release=on_calculate)
        content.add_widget(result_label)
        content.add_widget(calculate_button)

        # Add back button
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: popup.dismiss())
        content.add_widget(back_button)

        popup.open()

    def display_about(self, instance):
        about_info = (
            "DestiSolver AI\n\n"
            "A smart math problem-solving application.\n\n"
            "Created by Engineer Destiny Akhere and Engineer Success Mackson as a student-developed innovation for Mudiame University Irrua.\n\n"
            "Contact Information:\n"
            "Email: Destisolverai@gmail.com\n"
            "Phone Numbers: 09068754630, 0808 740 5076\n\n"
            "Follow us on Social Media:\n"
            "Facebook: @Destisolverai\n"
            "Twitter: @Destisolverai\n"
            "Instagram: @Destisolverai\n"
            "LinkedIn: @Destisolverai\n\n"
            "Copyright ©️ 2024")
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=about_info))

        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 40))
        back_button.bind(on_release=lambda btn: self.dismiss_popup())
        content.add_widget(back_button)

        popup = Popup(title='About DestiSolver AI', content=content, size_hint=(None, None), size=(400, 400))
        self._popup = popup  # Store the reference to the popup to access it later
        popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def exit_app(self, instance):
        App.get_running_app().stop()

    def general_answer(self):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text="Describe your problem:"))
        problem_input = TextInput()
        content.add_widget(problem_input)

        popup = Popup(title='Describe Your Problem', content=content, size_hint=(None, None), size=(400, 200),
                      auto_dismiss=False)

        def on_submit(instance):
            problem_description = problem_input.text
            if not problem_description:
                return
            self.send_feedback(problem_description)
            # Update or remove messagebox based on your implementation
            messagebox.showinfo("Problem Description", f"Problem: {problem_description}\nFeedback submitted.")

        submit_button = Button(text="Submit")
        submit_button.bind(on_release=on_submit)
        content.add_widget(submit_button)

        popup.open()

    import smtplib
    from email.message import EmailMessage

    class DestiSolverApp(App):
        def build(self):
            return MyGrid()

        def send_feedback(self, feedback):
            msg = EmailMessage()
            msg.set_content(feedback)

            msg['Subject'] = 'Feedback from DestiSolver AI User'
            msg['From'] = 'destinyakhere98@gmail.com'  # Replace with your email address
            msg['To'] = 'Destisolverai@gmail.com'

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login('destinyakhere98@gmail.com',
                             'DestinyDestiny123456789@#')  # Replace with your email login credentials
                server.send_message(msg)
                server.quit()
                return True
            except Exception as e:
                print("Error sending feedback email:", e)
                return False

if __name__ == "__main__":
    app = DestiSolverApp()
    app.run()
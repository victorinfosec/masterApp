import customtkinter as ctk
from tkinter import PhotoImage, StringVar
from pathlib import Path
from PIL import Image, ImageTk
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore
from script.generateFacture import generate_invoice
import tkintermapview
#pip install PyMuPDF
from script.CtkPDFViewer import *

class Client:
    def __init__(self, nom, prenom, adresse, email, numero, entreprise):
        self.nom = nom
        self.prenom = prenom
        self.adresse = adresse
        self.email = email
        self.numero = numero
        self.entreprise = entreprise

    def __repr__(self):
        return f"Client({self.nom}, {self.prenom}, {self.adresse}, {self.email}, {self.numero}, {self.entreprise})"


class MainGUI:
    def __init__(self, root):
        # Initialize Firebase
        self.cred = credentials.Certificate("tkinter-42267.json")
        #firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        
        self.root = root
        self.root.geometry("700x460")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg="#FFFFFF")
        self.root.title("Cyber Garde Admin Panel")
        self.root.iconbitmap("images/earth.ico")

        self.todo_list = []
        self.clients = []
        self.exit_image = Image.open("images/exit.ico")
        self.exit_image = self.exit_image.resize((30, 30), Image.LANCZOS)  # Resize the image using LANCZOS filter
        self.exit_image_tk = ImageTk.PhotoImage(self.exit_image)  # Convert to PhotoImage
        
        self.entreprise_image = Image.open("images/entreprise.jpg")
        self.entreprise_image_tk = ImageTk.PhotoImage(self.entreprise_image)
        self.create_widgets()

    def create_widgets(self):
        # Frame to hold the content
        self.frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="#FFFFFF")
        self.frame.pack(fill="both", expand=True)
        
        self.explication_label = ctk.CTkLabel(self.frame, text="Bienvenue sur votre application d'administration", font=("Arial", 16, "bold"), text_color="black")
        self.explication_label.pack(pady=20)
        self.explication_label.place(x=200, y=10)
        
        self.home_label = ctk.CTkLabel(self.frame, text="Cette application va vous permettre de gérer simplement \nvos votre entreprise",font=("Arial", 13), text_color="black")
        self.home_label.pack(pady=20)
        self.home_label.place(x=220, y=50)
        # Image
        self.home_image = Image.open("images/iconPDF.png")
        self.home_image = ImageTk.PhotoImage(self.home_image)
        
        # Frame menu
        self.frame2 = ctk.CTkFrame(master=self.frame, width=200, height=200, corner_radius=0, fg_color="#265461")
        self.frame2.pack(side="left", fill="both", expand=True)
        self.frame2.place(x=0, y=0)
        self.frame2.place_configure(height="700px", width="150px")
        
        # Frame menu 1
        self.frame3 = ctk.CTkFrame(master=self.frame, width=50, height=50, corner_radius=0, fg_color="#FFFFFF")
       
        self.frame4App = ctk.CTkFrame(master=self.frame, width=50, height=50, corner_radius=0, fg_color="#FFFFFF")
        
        # Welcome text
        self.welcome_label = ctk.CTkLabel(self.frame, text="Bienvenue", font=("Arial", 24, "bold"), bg_color="#265461", text_color="#FFFFFF")
        self.welcome_label.pack(pady=20)
        self.welcome_label.place(x=15, y=5)
        
        # Frame 3 component
        self.start_button = ctk.CTkButton(self.frame3, text="Sauvegarder", command=self.sauvegarder_action, font=("Arial", 16, "bold"), width=130, height=30, hover_color="green")
        self.start_button.pack(pady=20)
        self.start_button.place(x=370, y=400)  
        
        self.label_texte = ctk.CTkLabel(self.frame3, text="Paramètres", text_color="black", font=("Arial", 24, "bold"))
        self.label_texte.pack(pady=20)
        self.label_texte.place(x=200, y=10)
        
        self.label_texte_api = ctk.CTkLabel(self.frame3, text="API Key ChatGPT :", text_color="black", font=("Arial", 14))
        self.label_texte_api.pack(pady=20)
        self.label_texte_api.place(x=150, y=70)
        self.entry_api_key = ctk.CTkEntry(self.frame3, placeholder_text="api key", width=130, height=30)
        self.entry_api_key.pack(pady=20)
        self.entry_api_key.place(x=280, y=70)
        
        
        self.button_carre1 = ctk.CTkButton(self.frame4App, text="Génerer \nfacture", command=self.generer_facture_action, font=("Arial", 16, "bold"), width=130, height=30, hover_color="white", corner_radius=15, fg_color="#BBE9FF", text_color="black")
        self.button_carre1.pack(pady=20)
        self.button_carre1.place(x=30, y=30)
        self.button_carre1.place_configure(height="130px", width="130px")
        
        self.button_carre2 = ctk.CTkButton(self.frame4App, text="Gérer \nclients", command=self.gerer_clients_action, font=("Arial", 16, "bold"), width=130, height=30, hover_color="white", corner_radius=15, fg_color="#BBE9FF", text_color="black")
        self.button_carre2.pack(pady=20)
        self.button_carre2.place(x=190, y=30)
        self.button_carre2.place_configure(height="130px", width="130px")
        
        self.button_carre3 = ctk.CTkButton(self.frame4App, text="Todo \nlist", command=self.todo_list_action, font=("Arial", 16, "bold"), width=130, height=30, hover_color="white", corner_radius=15, fg_color="#BBE9FF", text_color="black")
        self.button_carre3.pack(pady=20)
        self.button_carre3.place(x=350, y=30)
        self.button_carre3.place_configure(height="130px", width="130px")
        
        self.button_carre4 = ctk.CTkButton(self.frame4App, text="Localisation \nchantier", command=self.localisation_chantier_action, font=("Arial", 16, "bold"), width=130, height=30, hover_color="white", corner_radius=15, fg_color="#BBE9FF", text_color="black")
        self.button_carre4.pack(pady=20)
        self.button_carre4.place(x=30, y=190)
        self.button_carre4.place_configure(height="130px", width="130px")
        
        # Frame for to-do list
        self.todo_frame = ctk.CTkFrame(master=self.frame, width=50, height=50, corner_radius=0, fg_color="#FFFFFF")
        
        # Frame for chantier
        self.chantier_frame = ctk.CTkFrame(master=self.frame, width=50, height=50, corner_radius=0, fg_color="#FFFFFF")
        
        # Menu button
        self.home_button = ctk.CTkButton(self.frame2, text="Accueil", command=self.home_menu_action, font=("Arial", 16, "bold"),  width=130, height=30)
        self.home_button.pack(pady=20)
        self.home_button.place(x=15, y=140)
        
        self.menu2_button = ctk.CTkButton(self.frame2, text="App", command=self.app_menu_action, font=("Arial", 16, "bold"),  width=130, height=30)
        self.menu2_button.pack(pady=20)
        self.menu2_button.place(x=15, y=190)
        
        self.menu3_button = ctk.CTkButton(self.frame2, text="Paramètres", command=self.parametres_action, font=("Arial", 16, "bold"),  width=130, height=30)
        self.menu3_button.pack(pady=20)
        self.menu3_button.place(x=15, y=240)
        
        # Logout button
        self.logout_button = ctk.CTkButton(self.frame2, text="Logout", command=self.logout_action, font=("Arial", 16, "bold"), width=130, height=30, hover_color="red")
        self.logout_button.pack(pady=20)
        self.logout_button.place(x=15, y=420)


    def app_menu_action(self):
        if self.frame3.winfo_exists():
            self.frame3.place_forget()
            self.frame3.pack_forget()
        
        self.frame4App.pack(fill="both", expand=True)
        self.frame4App.place(x=160, y=0)
        self.frame4App.place_configure(height="460px", width="700px")
        
            #self.frame3.destroy()
    def home_menu_action(self):
        if self.frame3.winfo_exists():
            self.frame3.place_forget()
            self.frame3.pack_forget()
            #self.frame3.destroy()
        if self.frame4App.winfo_exists():
            self.frame4App.place_forget()
            self.frame4App.pack_forget()
        
    def parametres_action(self):
        if self.frame4App.winfo_exists():
            self.frame4App.place_forget()
            self.frame4App.pack_forget()
            
        self.frame3.pack(fill="both", expand=True)
        self.frame3.place(x=160, y=0)
        self.frame3.place_configure(height="460px", width="700px")
        
        
    def sauvegarder_action(self):
        api_key = self.entry_api_key.get()
        self.api_key_value = api_key
         # Send the API key to Firebase
        doc_ref = self.db.collection('api_keys').document('api_keys')
        doc_ref.set({'api_key': api_key})
        
    def logout_action(self):
        self.root.destroy()
        
    def generer_facture_action(self):
        if self.frame3.winfo_exists():
            self.frame3.place_forget()
            self.frame3.pack_forget()
        if self.frame4App.winfo_exists():
            self.frame4App.place_forget()
            self.frame4App.pack_forget()
        self.facture_frame = ctk.CTkFrame(master=self.frame, width=50, height=50, corner_radius=0, fg_color="#FFFFFF")
        self.facture_frame.pack(fill="both", expand=True)
        self.facture_frame.place(x=160, y=0)
        self.facture_frame.place_configure(height="460px", width="700px")
        
        #Text 
        self.facture_label = ctk.CTkLabel(self.facture_frame, text="Génerer une facture", font=("Arial", 24, "bold"), text_color="black")
        self.facture_label.pack(pady=20)
        self.facture_label.place_configure(x=200, y=1)
        
       # Numéro de facture
        self.invoice_number = ctk.CTkLabel(self.facture_frame, text="Numéro de facture :", text_color="black", font=("Arial", 14))
        self.invoice_number.pack(pady=20)
        self.invoice_number.place(x=150, y=30)
        self.invoice_number_entry = ctk.CTkEntry(self.facture_frame, placeholder_text="12345", width=130, height=30, border_color="#FFFFFF")
        self.invoice_number_entry.pack(pady=20)
        self.invoice_number_entry.place(x=280, y=30)

        # Date de création
        self.created_date = ctk.CTkLabel(self.facture_frame, text="Date de création :", text_color="black", font=("Arial", 14))
        self.created_date.pack(pady=20)
        self.created_date.place(x=150, y=70)
        self.created_date_entry = ctk.CTkEntry(self.facture_frame, placeholder_text="01/01/2024", width=130, height=30, border_color="#FFFFFF")
        self.created_date_entry.pack(pady=20)
        self.created_date_entry.place(x=280, y=70)

        # Date d'échéance
        self.due_date = ctk.CTkLabel(self.facture_frame, text="Date d'échéance :", text_color="black", font=("Arial", 14))
        self.due_date.pack(pady=20)
        self.due_date.place(x=150, y=110)
        self.due_date_entry = ctk.CTkEntry(self.facture_frame, placeholder_text="01/02/2024", width=130, height=30, border_color="#FFFFFF")
        self.due_date_entry.pack(pady=20)
        self.due_date_entry.place(x=280, y=110)

        # Nom de l'entreprise
        self.company_name = ctk.CTkLabel(self.facture_frame, text="Entreprise :", text_color="black", font=("Arial", 14))
        self.company_name.pack(pady=20)
        self.company_name.place(x=150, y=150)
        self.company_name_entry = ctk.CTkEntry(self.facture_frame, placeholder_text="ABC Company", width=130, height=30, border_color="#FFFFFF")
        self.company_name_entry.pack(pady=20)
        self.company_name_entry.place(x=280, y=150)
        
        # Create ctkOptionMenu
        #  # Fetch options from Firestore
        # self.options = self.fetch_options_from_firestore()

        # # Create ctkOptionMenu
        # self.selected_option = StringVar() # Set default selection
        # self.option_menu = ctk.CTkOptionMenu(self.root, options=self.options, selected_option=self.selected_option, width=200, height=30)
        # self.option_menu.pack(pady=20)

        # Adresse de l'entreprise
        self.company_address = ctk.CTkLabel(self.facture_frame, text="Adresse :", text_color="black", font=("Arial", 14))
        self.company_address.pack(pady=20)
        self.company_address.place(x=150, y=190)
        self.company_address_entry = ctk.CTkEntry(self.facture_frame, placeholder_text="123 Main Street, City, Country", width=130, height=30, border_color="#FFFFFF")
        self.company_address_entry.pack(pady=20)
        self.company_address_entry.place(x=280, y=190)

        # Adresse mail de l'entreprise
        self.company_email = ctk.CTkLabel(self.facture_frame, text="Adresse mail :", text_color="black", font=("Arial", 14))
        self.company_email.pack(pady=20)
        self.company_email.place(x=150, y=230)
        self.company_email_entry = ctk.CTkEntry(self.facture_frame, placeholder_text="contact@abccompany.com", width=130, height=30, border_color="#FFFFFF")
        self.company_email_entry.pack(pady=20)
        self.company_email_entry.place(x=280, y=230)

        # Nom du client
        self.client_name = ctk.CTkLabel(self.facture_frame, text="Nom du client :", text_color="black", font=("Arial", 14))
        self.client_name.pack(pady=20)
        self.client_name.place(x=150, y=270)
        self.client_name_entry = ctk.CTkEntry(self.facture_frame, placeholder_text="John Doe", width=130, height=30, border_color="#FFFFFF")
        self.client_name_entry.pack(pady=20)
        self.client_name_entry.place(x=280, y=270)

        # Email du client
        self.client_email = ctk.CTkLabel(self.facture_frame, text="Email du client :", text_color="black", font=("Arial", 14))
        self.client_email.pack(pady=20)
        self.client_email.place(x=150, y=310)
        self.client_email_entry = ctk.CTkEntry(self.facture_frame, placeholder_text="john.doe@example.com", width=130, height=30, border_color="#FFFFFF")
        self.client_email_entry.pack(pady=20)
        self.client_email_entry.place(x=280, y=310)

        # Articles
        self.items_button = ctk.CTkButton(self.facture_frame, text="Ajouter un article", command=self.ajouter_article, font=("Arial", 16, "bold"), width=130, height=30, hover_color="green")
        self.items_button.pack(pady=20)
        self.items_button.place(x=150, y=350)

        #Creer facture boutton 
        self.generer_facture_button = ctk.CTkButton(self.facture_frame, text="Ma facture", command=self.creer_facture, font=("Arial", 16, "bold"), width=130, height=30, hover_color="green")
        self.generer_facture_button.pack(pady=20)
        self.generer_facture_button.place(x=300, y=395)
        #Close button frame 
        self.close_facture_button = ctk.CTkButton(self.facture_frame, image=self.exit_image_tk, command=self.close_facture_button, width=13, height=13, fg_color="#FFFFFF", hover_color="#FFFFFF", corner_radius=100)
        self.close_facture_button.pack(pady=20)
        self.close_facture_button.place(x=500, y=425)
        
    def fetch_options_from_firestore(self):
        client_dispo =  []
        clients_ref = self.db.collection('clients').stream()
        for client_doc in clients_ref:
            client_data = client_doc.to_dict()
            client = Client(client_data['nom'], client_data['prenom'], client_data['adresse'],
                            client_data['email'], client_data['numero'], client_data['entreprise'])
            client_dispo.append(client)
    
    def ajouter_article(self):
        # Crée une nouvelle fenêtre
        article_window = ctk.CTkToplevel(self.root)
        article_window.title("Ajouter un Article")
          # Mettre la fenêtre au-dessus de la fenêtre principale
        article_window.grab_set()
        article_window.focus_force()

        # Centrer la fenêtre sur l'écran
        article_window.geometry("+%d+%d" % (self.root.winfo_x() + 50, self.root.winfo_y() + 50))

        # Label et champ d'entrée pour le nom de l'article
        article_label = ctk.CTkLabel(article_window, text="Article :", text_color="black", font=("Arial", 14))
        article_label.pack(pady=10)
        article_entry = ctk.CTkEntry(article_window, placeholder_text="Nom de l'article", width=200, height=30, border_color="#FFFFFF")
        article_entry.pack(pady=10)
        
        # Label et champ d'entrée pour le prix de l'article
        prix_label = ctk.CTkLabel(article_window, text="Prix :", text_color="black", font=("Arial", 14))
        prix_label.pack(pady=10)
        prix_entry = ctk.CTkEntry(article_window, placeholder_text="Prix de l'article", width=200, height=30, border_color="#FFFFFF")
        prix_entry.pack(pady=10)
        
        # Liste pour stocker les articles
        self.articles = []

        # Fonction pour ajouter l'article à la liste
        def ajouter():
            article = article_entry.get()
            prix = prix_entry.get()
            self.articles.append((article, prix))
            article_window.destroy()
        
        # Bouton pour valider l'ajout de l'article
        ajouter_button = ctk.CTkButton(article_window, text="Ajouter", command=ajouter, font=("Arial", 14), width=100, height=30, hover_color="green")
        ajouter_button.pack(pady=20)
        
    def creer_facture(self):
        data = {            
            "invoice_number": self.invoice_number_entry.get(),
            "created_date": self.created_date_entry.get(),
            "due_date": self.due_date_entry.get(),
            "company_name": self.company_name_entry.get(),
            "company_address": self.company_address_entry.get(),
            "company_email": self.company_email_entry.get(),
            "client_name": self.client_name_entry.get(),
            "client_email": self.client_email_entry.get(),
        } 
        articles_data = []
        for article, prix in self.articles:
            articles_data.append((article, prix))
        
        # Ajouter les articles à la structure de données
        data["items"] = articles_data
        generate_invoice(data)
    def close_facture_button(self):
        
        self.facture_frame.place_forget()
        self.facture_frame.pack_forget()
        
        self.frame4App.pack(fill="both", expand=True)
        self.frame4App.place(x=160, y=0)
        self.frame4App.place_configure(height="460px", width="700px")
        
    def gerer_clients_action(self):
        # Hide other frames
        if self.frame3.winfo_exists():
            self.frame3.place_forget()
            self.frame3.pack_forget()
        if self.frame4App.winfo_exists():
            self.frame4App.place_forget()
            self.frame4App.pack_forget()
        
        # Show clients_frame
        self.clients_frame = ctk.CTkFrame(master=self.frame, width=50, height=50, corner_radius=0, fg_color="#FFFFFF")
        self.clients_frame.pack(fill="both", expand=True)
        self.clients_frame.place(x=160, y=0)
        self.clients_frame.place_configure(height="460px", width="700px")
        
        self.clients_label = ctk.CTkLabel(self.clients_frame, text="Gérer Clients", font=("Arial", 24, "bold"), text_color="black")
        self.clients_label.pack(pady=20)
        self.clients_label.place_configure(x=250, y=10)
        
        self.nom_label = ctk.CTkLabel(self.clients_frame, text="Nom :", text_color="black", font=("Arial", 14))
        self.nom_label.pack(pady=20)
        self.nom_label.place(x=150, y=70)
        self.nom_entry = ctk.CTkEntry(self.clients_frame, placeholder_text="Nom", width=130, height=30, border_color="#FFFFFF")
        self.nom_entry.pack(pady=20)
        self.nom_entry.place(x=280, y=70)
        
        self.prenom_label = ctk.CTkLabel(self.clients_frame, text="Prénom :", text_color="black", font=("Arial", 14))
        self.prenom_label.pack(pady=20)
        self.prenom_label.place(x=150, y=110)
        self.prenom_entry = ctk.CTkEntry(self.clients_frame, placeholder_text="Prénom", width=130, height=30, border_color="#FFFFFF")
        self.prenom_entry.pack(pady=20)
        self.prenom_entry.place(x=280, y=110)
        
        self.adresse_label = ctk.CTkLabel(self.clients_frame, text="Adresse :", text_color="black", font=("Arial", 14))
        self.adresse_label.pack(pady=20)
        self.adresse_label.place(x=150, y=150)
        self.adresse_entry = ctk.CTkEntry(self.clients_frame, placeholder_text="Adresse", width=130, height=30, border_color="#FFFFFF")
        self.adresse_entry.pack(pady=20)
        self.adresse_entry.place(x=280, y=150)
        
        self.email_label = ctk.CTkLabel(self.clients_frame, text="Email :", text_color="black", font=("Arial", 14))
        self.email_label.pack(pady=20)
        self.email_label.place(x=150, y=190)
        self.email_entry = ctk.CTkEntry(self.clients_frame, placeholder_text="Email", width=130, height=30, border_color="#FFFFFF")
        self.email_entry.pack(pady=20)
        self.email_entry.place(x=280, y=190)
        
        self.numero_label = ctk.CTkLabel(self.clients_frame, text="Numéro :", text_color="black", font=("Arial", 14))
        self.numero_label.pack(pady=20)
        self.numero_label.place(x=150, y=230)
        self.numero_entry = ctk.CTkEntry(self.clients_frame, placeholder_text="Numéro", width=130, height=30, border_color="#FFFFFF")
        self.numero_entry.pack(pady=20)
        self.numero_entry.place(x=280, y=230)
        
        self.entreprise_label = ctk.CTkLabel(self.clients_frame, text="Entreprise :", text_color="black", font=("Arial", 14))
        self.entreprise_label.pack(pady=20)
        self.entreprise_label.place(x=150, y=270)
        self.entreprise_entry = ctk.CTkEntry(self.clients_frame, placeholder_text="Entreprise", width=130, height=30, border_color="#FFFFFF")
        self.entreprise_entry.pack(pady=20)
        self.entreprise_entry.place(x=280, y=270)
        
        self.ajouter_client_button = ctk.CTkButton(self.clients_frame, text="Ajouter client", command=self.ajouter_client, font=("Arial", 16, "bold"), width=130, height=30, hover_color="green")
        self.ajouter_client_button.pack(pady=20)
        self.ajouter_client_button.place(x=320, y=310)
        
        # List frame
        self.clients_list_frame = ctk.CTkScrollableFrame(self.clients_frame, width=460, height=150, fg_color="#FFFFFF", 
                                                        scrollbar_fg_color="white",
                                                        scrollbar_button_hover_color = "blue")
        self.clients_list_frame.pack(pady=20)
        self.clients_list_frame.place(x=10, y=360)
        
        # Load existing clients
        self.load_clients()
    
        self.close_clients_button = ctk.CTkButton(self.clients_frame, image=self.exit_image_tk, command=self.close_clients_frame, width=13, height=13, fg_color="#FFFFFF", hover_color="#FFFFFF", corner_radius=100)
        self.close_clients_button.pack(pady=20)
        self.close_clients_button.place(x=500, y=425)
    def close_clients_frame(self):
        
        self.clients_frame.place_forget()
        self.clients_frame.pack_forget()
        
        self.clients_list_frame.place_forget()
        self.clients_list_frame.pack_forget()
        
        self.frame4App.pack(fill="both", expand=True)
        self.frame4App.place(x=160, y=0)
        self.frame4App.place_configure(height="460px", width="700px")
        
    
    def ajouter_client(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        adresse = self.adresse_entry.get()
        email = self.email_entry.get()
        numero = self.numero_entry.get()
        entreprise = self.entreprise_entry.get()
        
        if nom and prenom and adresse and email and numero and entreprise:
            new_client = Client(nom, prenom, adresse, email, numero, entreprise)
            self.clients.append(new_client)
            self.save_client_to_firestore(new_client)
            self.create_client_frame(new_client)
            self.clear_client_entries()
    
    def save_client_to_firestore(self, client):
        doc_ref = self.db.collection('clients').document()
        doc_ref.set({
            'nom': client.nom,
            'prenom': client.prenom,
            'adresse': client.adresse,
            'email': client.email,
            'numero': client.numero,
            'entreprise': client.entreprise
        })
    
    def load_clients(self):
        # Load clients from Firestore
        clients_ref = self.db.collection('clients').stream()
        for client_doc in clients_ref:
            client_data = client_doc.to_dict()
            client = Client(client_data['nom'], client_data['prenom'], client_data['adresse'],
                            client_data['email'], client_data['numero'], client_data['entreprise'])
            self.clients.append(client)
            self.create_client_frame(client)
    
    def create_client_frame(self, client):
        client_frame = ctk.CTkFrame(self.clients_list_frame, fg_color="#E0E0E0", height=70)
        client_frame.pack(fill="x", pady=2)
        
        client_info = f"{client.nom} {client.prenom} - {client.email} - {client.numero}"
        
        client_label = ctk.CTkLabel(client_frame, text=client_info, font=("Arial", 14), text_color="black", width=270)
        client_label.pack(side="left", padx=10)
        
        delete_button = ctk.CTkButton(client_frame, text="Supprimer", command=lambda frm=client_frame, c=client: self.delete_client(frm, c), font=("Arial", 12, "bold"), width=80, height=30)
        delete_button.pack(side="right", padx=5)
    
    def delete_client(self, client_frame, client):
        client_frame.destroy()
        self.clients = [c for c in self.clients if c != client]
        self.delete_client_from_firestore(client)
    
    def delete_client_from_firestore(self, client):
        # Delete client from Firestore
        clients_ref = self.db.collection('clients').where('nom', '==', client.nom).where('prenom', '==', client.prenom).stream()
        for client_doc in clients_ref:
            client_doc.reference.delete()
    
    def clear_client_entries(self):
        self.nom_entry.delete(0, 'end')
        self.prenom_entry.delete(0, 'end')
        self.adresse_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.numero_entry.delete(0, 'end')
        self.entreprise_entry.delete(0, 'end')
    
    def get_chantier_entry_value(self,event):
        adresse = self.chantier_entry.get()
        self.map_widget.set_address(adresse)
        
    def localisation_chantier_action(self):
         # Hide other frames
        if self.frame3.winfo_exists():
            self.frame3.place_forget()
            self.frame3.pack_forget()
        if self.frame4App.winfo_exists():
            self.frame4App.place_forget()
            self.frame4App.pack_forget()
        
        # Show chantier_frame
        self.chantier_frame.pack(fill="both", expand=True)
        self.chantier_frame.place(x=160, y=0)
        self.chantier_frame.place_configure(height="460px", width="700px")
        
        self.chantier_label = ctk.CTkLabel(self.chantier_frame, text="Vos chantiers en cours", font=("Arial", 24, "bold"), text_color="black")
        self.chantier_label.pack(pady=20)
        self.chantier_label.place_configure(x=170, y=10)
        
        self.chantier_entry = ctk.CTkEntry(self.chantier_frame, placeholder_text="Entrer une adresse", width=300, height=30)
        self.chantier_entry.pack(pady=20)
        self.chantier_entry.place(x=110, y=45)
        
        # Bind the Return key to a function to get the value of todo_entry
        self.chantier_entry.bind("<Return>", self.get_chantier_entry_value)
        
        # create map widget
        self.map_widget = tkintermapview.TkinterMapView(self.chantier_frame, width=600, height=450, corner_radius=15)
        self.map_widget.place(x=40, y=100)
        # set current widget position and zoom
        self.map_widget.set_position(45.750000, 4.850000)  # Lyon, France
        self.map_widget.set_zoom(13)
        def add_marker_event(coords):
            print("Add marker:", coords)
            new_marker = self.map_widget.set_marker(coords[0], coords[1], text="Chantier")
            

        self.map_widget.add_right_click_menu_command(label="Ajouter un chantier",
                                                command=add_marker_event,
                                                pass_coords=True)
        
         # Add a button to close the frame        
        self.close_todo_button = ctk.CTkButton(self.chantier_frame, image=self.exit_image_tk, command=self.close_chantier_frame, width=13, height=13, fg_color="#FFFFFF", hover_color="#FFFFFF", corner_radius=100)
        self.close_todo_button.pack(pady=20)
        self.close_todo_button.place(x=500, y=425)
    def todo_list_action(self):
        # Hide other frames
        if self.frame3.winfo_exists():
            self.frame3.place_forget()
            self.frame3.pack_forget()
        if self.frame4App.winfo_exists():
            self.frame4App.place_forget()
            self.frame4App.pack_forget()
        
        # Show todo_frame
        self.todo_frame.pack(fill="both", expand=True)
        self.todo_frame.place(x=160, y=0)
        self.todo_frame.place_configure(height="460px", width="700px")
        
        # Add a label and entry for the to-do list
        self.todo_label = ctk.CTkLabel(self.todo_frame, text="To-Do List", font=("Arial", 24, "bold"), text_color="black")
        self.todo_label.pack(pady=20)
        self.todo_label.place(x=170, y=10)
        
        self.todo_entry = ctk.CTkEntry(self.todo_frame, placeholder_text="Entrer une tâche", width=300, height=30)
        self.todo_entry.pack(pady=20)
        self.todo_entry.place(x=110, y=70)
        
        # Bind the Return key to a function to get the value of todo_entry
        self.todo_entry.bind("<Return>", self.get_todo_entry_value)
        
        # Create a frame to hold the list of tasks
        self.todo_list_frame = ctk.CTkFrame(self.todo_frame, width=600, height=300, fg_color="#FFFFFF")
        self.todo_list_frame.pack(pady=20)
        self.todo_list_frame.place(x=50, y=120)
        
        # Load existing tasks
        for item in self.todo_list:
            self.create_task_frame(item)
            
        # Add a button to close the frame
        # self.close_todo_button = ctk.CTkButton(self.todo_frame, text="Close", command=self.close_todo_frame, font=("Arial", 16, "bold"), width=90, height=30)
        # self.close_todo_button.pack(pady=20)
        # self.close_todo_button.place(x=400, y=400)
 

        # Create the button with the resized image
        self.close_todo_button = ctk.CTkButton(self.todo_frame, image=self.exit_image_tk, command=self.close_todo_frame, width=13, height=13, fg_color="#FFFFFF", hover_color="#FFFFFF", corner_radius=100)
        self.close_todo_button.pack(pady=20)
        self.close_todo_button.place(x=500, y=425)
        
    def get_todo_entry_value(self, event):
        task = self.todo_entry.get()
        if task:
            self.add_task(task)
            self.todo_entry.delete(0, 'end')
    
    def add_task(self, task):
        new_task = {"task": task, "done": False}
        self.todo_list.append(new_task)
        self.create_task_frame(new_task)
    
    def create_task_frame(self, item):
        task_frame = ctk.CTkFrame(self.todo_list_frame, fg_color="#E0E0E0", height=40)
        task_frame.pack(fill="x", pady=2)

        task_label = ctk.CTkLabel(task_frame, text=item["task"], font=("Arial", 14), text_color="gray" if item["done"] else "black", width=270)
        task_label.pack(side="left", padx=10)

        done_button = ctk.CTkButton(task_frame, text="Done", command=lambda lbl=task_label, t=item["task"]: self.mark_task_done(lbl, t), font=("Arial", 12, "bold"), width=50, height=30)
        done_button.pack(side="right", padx=5)

        delete_button = ctk.CTkButton(task_frame, text="Delete", command=lambda frm=task_frame, t=item["task"]: self.delete_task(frm, t), font=("Arial", 12, "bold"), width=50, height=30)
        delete_button.pack(side="right", padx=5)
    
    def mark_task_done(self, task_label, task):
        task_label.configure(text_color="gray")
        for item in self.todo_list:
            if item["task"] == task:
                item["done"] = True
                break
    
    def delete_task(self, task_frame, task):
        task_frame.destroy()
        self.todo_list = [item for item in self.todo_list if item["task"] != task]
    
    def close_todo_frame(self):
        self.todo_frame.place_forget()
        self.todo_frame.pack_forget()
        
        self.todo_list_frame.place_forget()
        self.todo_list_frame.pack_forget()
        
        self.frame4App.pack(fill="both", expand=True)
        self.frame4App.place(x=160, y=0)
        self.frame4App.place_configure(height="460px", width="700px")
        
    def close_chantier_frame(self):
        self.chantier_frame.place_forget()
        self.chantier_frame.pack_forget()
        
        self.frame4App.pack(fill="both", expand=True)
        self.frame4App.place(x=160, y=0)
        self.frame4App.place_configure(height="460px", width="700px")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainGUI(root)
    root.mainloop()

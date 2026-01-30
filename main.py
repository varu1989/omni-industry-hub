#
import flet as ft
import os
from google import genai
from dotenv import load_dotenv

# 1. Setup & Config
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def main(page: ft.Page):
    page.title = "Omni-Industry Intelligence Hub"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    
    # Track current industry
    current_industry = ft.Text("Retail", size=25, weight="bold", color="blue")

    # 2. Gemini Integration Function
    def get_gemini_analysis(industry, user_query):
        try:
            prompt = f"""
            You are a specialized AI expert in the {industry} industry. 
            Analyze the following request with data-driven insights:
            Request: {user_query}
            """
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Error connecting to Gemini: {str(e)}"

    # 3. UI Event Handlers
    chat_history = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True)
    user_input = ft.TextField(hint_text="Ask about industry trends...", expand=True, shift_enter=True)

    def send_message(e):
        if not user_input.value: return
        
        # User message
        chat_history.controls.append(ft.Text(f"You: {user_input.value}", color="white70"))
        page.update()
        
        # Get AI Response
        analysis = get_gemini_analysis(current_industry.value, user_input.value)
        
        # AI message
        chat_history.controls.append(
            ft.Container(
                content=ft.Markdown(analysis),
                padding=10,
                bgcolor=ft.colors.GREY_900,
                border_radius=10
            )
        )
        user_input.value = ""
        page.update()

    def change_industry(e):
        # Update UI based on sidebar click
        selected = e.control.label
        current_industry.value = selected
        chat_history.controls.append(ft.Divider())
        chat_history.controls.append(ft.Text(f"--- Switched to {selected} Analyst ---", italic=True, size=12))
        page.update()

    # 4. Sidebar UI
    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.icons.SHOPPING_CART, label="Retail"),
            ft.NavigationRailDestination(icon=ft.icons.HEALTH_AND_SAFETY, label="Healthcare"),
            ft.NavigationRailDestination(icon=ft.icons.INSURANCE, label="Insurance"),
            ft.NavigationRailDestination(icon=ft.icons.ACCOUNT_BALANCE, label="Banking"),
            ft.NavigationRailDestination(icon=ft.icons.ATTACH_MONEY, label="Finance"),
            ft.NavigationRailDestination(icon=ft.icons.SHOW_CHART, label="Stock Market"),
        ],
        on_change=change_industry,
    )

    # 5. Main Layout
    page.add(
        ft.Row(
            [
                sidebar,
                ft.VerticalDivider(width=1),
                ft.Column(
                    [
                        ft.Container(content=current_industry, padding=20),
                        ft.Container(content=chat_history, expand=True, padding=10),
                        ft.Row(
                            [user_input, ft.IconButton(ft.icons.SEND, on_click=send_message)],
                            padding=20
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=int(os.getenv("PORT", 8502)))
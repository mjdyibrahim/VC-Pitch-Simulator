from app.data_extractor import extract_text_from_pdf, call_llm_for_section, embed_text, store_startup_profile

class PitchDeckAgent:
    def __init__(self, file_path, startup_id):
        self.file_path = file_path
        self.startup_id = startup_id
        self.text = extract_text_from_pdf(file_path)
        self.sections = {
            "team": [
                "How many team members do you have?",
                "List the team members with the following details:",
                "What is the team member's name?",
                "What is the team member's title?",
                "How many hours per week is the team member available?",
                "Since when has the team member been involved?",
                "What percentage of equity does the team member hold?",
                "What percentage of salary does the team member receive?",
                "How many years of experience does the team member have?",
                "Does the team member have an undergraduate degree?",
                "Does the team member have a graduate degree?",
                "Does the team member have a master's degree?",
                "Does the team member have a PhD or higher degree?",
                "Has the team member been part of a startup team?",
                "Has the team member been the founder of a startup?",
                "Has the team member held a previous C-level position?",
                "Has the team member been part of a successful exit?",
                "Is the team member's role in Marketing?",
                "Is the team member's role in Sales?",
                "Is the team member's role in Product?",
                "Is the team member's role in Creative?",
                "Is the team member's role in Technical?",
                "Is the team member's role in Operation?",
                "What other role does the team member have?",
                "Can you provide an overview of the team’s qualifications and expertise?",
                "How would you assess the team’s experience and ability to execute the business plan?"
            ],
            "fundraising": [
                "What is the current stage of fundraising?",
                "What is the target amount of funding?",
                "What is the current amount of funding?",
                "What is the minimum amount of funding?",
                "What is the maximum amount of funding?"
            ],
            "market": [
                "What is the primary industry?",
                "What is the market size?",
                "What is the market share in 3 years?"
            ],
            "business_model": [
                "What is the primary industry?",
                "What is the market size?",
                "What is the market share in 3 years?"
            ],
            "product": [
                "What is the product?",
                "What is the product's unique selling proposition?",
                "What is the product's competitive advantage?"
            ],
            "traction": [
                "What is the traction?",
                "What is the traction's unique selling proposition?",
                "What is the traction's competitive advantage?"
            ]
        }

    def process_section(self, section_name):
        questions = self.sections[section_name]
        response = call_llm_for_section(self.text, questions, section_name)
        embedded_text = embed_text(response)
        store_startup_profile(self.startup_id, section_name, response, embedded_text)

    def process_all_sections(self):
        for section in self.sections:
            self.process_section(section)

# Example usage
if __name__ == "__main__":
    agent = PitchDeckAgent("path_to_pitchdeck.pdf", "startup_123")
    agent.process_all_sections()

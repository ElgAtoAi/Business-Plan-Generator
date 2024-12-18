# Import required libraries
import pandas as pd
import streamlit as st
from groq import Groq



# Streamlit app header
st.set_page_config(
    page_title="Business Plan Generator",
    page_icon="📊",
    layout="centered"  # Enhanced UI with wide layout
)

# Set up Groq API Key
api = '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'
client = Groq(api_key=api)


# Load the CSV file
data = pd.read_csv("business plans dataset(1).csv")

# Define a function to get sub-industries based on the main industry
def get_sub_industries(main_industry):
    """Get the list of sub-industries based on the selected main industry."""
    return data[data['Main Industry'] == main_industry]['Sub-Industry'].unique().tolist()


# Function to generate a fallback business plan using the Groq API
def generate_fallback_plan(main_industry, sub_industry):
    """Generate a fallback business plan using Groq's Llama3-8b-8192 model."""
    # Prepare the user message for the Groq API
    user_message = (
        "You are a business analyst AI trained to generate detailed business plans. "
        "The answer make the user get clear idea to start the business"
        "Make all the sub heading font size 16 and content 14"
        "Your response should always follow this structure:\n\n"
        "Generate a business plan for:"
        f"Main Industry: {main_industry}""\n"
        f"Sub-Industry: {sub_industry}"
        "Follow this structure:"
        "Business Name : generated crispy name for the business"
        "1. Business Idea:\n" 
        " generate points such as Concept, problem solved, value proposition(unique selling propostion).\n"
        "2. Executive Summary:\n" 
        "generate points such as Mission, vision, objectives.\n"
        "3. Market Analysis:\n"
        "generate points such as Trends, target market, competitors, market gap.\n"
        "4. Products and Services:\n" 
        "generate points such as Offerings, pricing, revenue model.\n"
        "5. Marketing Strategy:\n"
        "generate points such as Channels, customer acquisition, retention.\n"
        "6. Financial Plan:\n" 
        "generate points such as Startup costs, projections, funding needs.\n"
        "7. Operations:\n"
        "generate points such as Daily workflow, tools, technology.\n"
        "8. Risk Management:\n" 
        "generate points such as Key risks and mitigation strategies.\n"
        f"Focus on accuracy, feasibility, and industry-specific insights. Generate a detailed business plan "
        f"for the main industry: {main_industry} and sub-industry: {sub_industry}."
    )

    # Call the Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_message,
            }
        ],
        model="llama3-8b-8192",
    )
    
    # Extract and return the generated content
    return chat_completion.choices[0].message.content

# Streamlit App
def main():
    st.title("📊 Business Plan Generator")

    # Step 1: Select Main Industry
    industries = data['Main Industry'].unique().tolist() + ["Other"]
    main_industry = st.selectbox(
        "Select Main Industry",
        industries,
        help="Choose the main industry or select 'Other' to input a custom value."
    )

    # Handle "Other" option for Main Industry
    if main_industry == "Other":
        main_industry = st.text_input("Enter Main Industry", help="Provide a custom main industry.")

    if main_industry:
        # Step 2: Select Sub Industry
        if main_industry != "Other":
            sub_industries = get_sub_industries(main_industry) + ["Other"]
        else:
            sub_industries = ["Other"]

        sub_industry = st.selectbox(
            "Select Sub Industry",
            sub_industries,
            help="Choose the sub-industry or select 'Other' to input a custom value."
        )

        # Handle "Other" option for Sub Industry
        if sub_industry == "Other":
            sub_industry = st.text_input("Enter Sub Industry", help="Provide a custom sub-industry.")

        if sub_industry:
            # Step 3: Display Business Plan Details
            st.subheader("📝 Business Plan Details")
            st.info("Generating Business Plan...")
            fallback_plan = generate_fallback_plan(main_industry, sub_industry)
            st.write(fallback_plan)

# Run the app
if __name__ == "__main__":
    main()

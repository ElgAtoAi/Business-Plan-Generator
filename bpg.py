#Import required libraries
import pandas as pd
import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate

#Load the CSV file
data = pd.read_csv("C:\\Users\\Monasri M\\Downloads\\expanded_business_plans_final re.csv")

# Streamlit app header
st.set_page_config(
    page_title="Business Plan Generator",
    page_icon="📊",
    layout="wide"  # Enhanced UI with wide layout
)

# Define a function to get sub-industries based on the main industry
def get_sub_industries(main_industry):
    """Get the list of sub-industries based on the selected main industry."""
    return data[data['Main Industry'] == main_industry]['Sub-Industry'].unique().tolist()

# Define a function to get the business plan details based on user selections
def get_business_plan(main_industry, sub_industry):
    """Retrieve business plan details based on selected main and sub-industry."""
    filtered_data = data[(data['Main Industry'] == main_industry) & (data['Sub-Industry'] == sub_industry)]
    if not filtered_data.empty:
        return {
            "Business Goals": filtered_data['Business Goals'].values[0],
            "Challenges": filtered_data['Challenges'].values[0],
            "Target Audience": filtered_data['Target Audience'].values[0],
            "Revenue Streams": filtered_data['Revenue Streams'].values[0],
            "Profit Range":
        }
    return None

# LangChain Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a business analyst AI trained to generate detailed business plans. Your response should always follow this structure: "
               "1. **Business Goals**: (Summarize 2-3 key goals based on the input)\n"
               "2. **Challenges**: (List 2-3 potential challenges)\n"
               "3. **Target Audience**: (Describe the audience and their preferences)\n"
               "4. **Revenue Streams**: (Provide 2-3 revenue generation ideas)\n"
               "5. **Profit Range**: (Estimate based on industry averages).\n"
               "Focus on accuracy, feasibility, and industry-specific insights."),
    ("user", "Main Industry: {main_industry}, Sub Industry: {sub_industry}")
])

# Initialize LangChain Model
llm = Ollama(model="llama2")  # Replace with your preferred model
chain = LLMChain(llm=llm, prompt=prompt)

# Define fallback plan generation function
def generate_fallback_plan(main_industry, sub_industry):
    """Generate a fallback business plan using LangChain."""
    response = chain.invoke({"main_industry": main_industry, "sub_industry": sub_industry})
    return response["text"]

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
            business_plan = get_business_plan(main_industry, sub_industry)
            if business_plan:
                st.write(f"**Business Goals**: {business_plan['Business Goals']}")
                st.write(f"**Challenges**: {business_plan['Challenges']}")
                st.write(f"**Target Audience**: {business_plan['Target Audience']}")
                st.write(f"**Revenue Streams**: {business_plan['Revenue Streams']}")
            else:
                # Fallback Plan
                st.info("Generating Business Plan...")
                fallback_plan = generate_fallback_plan(main_industry, sub_industry)
                st.write(fallback_plan)

# Run the app
if __name__ == "__main__":
    main()

# Import required libraries
import pandas as pd
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from groq import Groq

# Set up Groq API Key
api = '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'
client = Groq(api_key=api)

# Load the CSV file
data = pd.read_csv("business plans dataset(1).csv")

# Streamlit app header
st.set_page_config(
    page_title="Business Plan Generator",
    page_icon="📊",
    layout="centered"  # Enhanced UI with wide layout
)

# Define a function to get sub-industries based on the main industry
def get_sub_industries(main_industry):
    """Get the list of sub-industries based on the selected main industry."""
    return data[data['Main Industry'] == main_industry]['Sub-Industry'].unique().tolist()

def get_business_plan(main_industry, sub_industry):
    """Retrieve business plan details based on selected main and sub-industry."""
    filtered_data = data[(data['Main Industry'] == main_industry) & (data['Sub-Industry'] == sub_industry)]
    if not filtered_data.empty:
        return {
            "Business Goals":filtered_data['Business Goals'].values[0],
            "Challenges": filtered_data['Challenges'].values[0],
            "Target Audience": filtered_data['Target Audience'].values[0],
            "Revenue Streams": filtered_data['Revenue Streams'].values[0],
            "Profit Range": filtered_data["Profit Range"].values[0],
        }
    return None


# Function to generate a fallback business plan using the Groq API
def generate_fallback_plan(main_industry, sub_industry):
    """Generate a fallback business plan using Groq's Llama3-8b-8192 model."""
    # Prepare the user message for the Groq API
    user_message = (
        "You are a business analyst AI trained to generate detailed business plans. "
        "Your response should always follow this structure:\n\n"
        "1. **Business Goals**: (Summarize 2-3 key goals based on the input)\n"
        "2. **Challenges**: (List 2-3 potential challenges)\n"
        "3. **Target Audience**: (Describe the audience and their preferences)\n"
        "4. **Revenue Streams**: (Provide 2-3 revenue generation ideas)\n"
        "5. **Profit Range**: (Estimate based on industry averages).\n\n"
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


# Function to create a PDF from the business plan
def create_pdf(content):
    """Generate a PDF document with the provided content."""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(50, 750, "Business Plan")
    y_position = 700

    # Add content to PDF
    for key, value in content.items():
        pdf.drawString(50, y_position, f"{key}: {value}")
        y_position -= 30

    pdf.save()
    buffer.seek(0)
    return buffer

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
                # Display plan from CSV
                st.write("### Business Goals")
                st.write(business_plan['Business Goals'])
                
                st.write("### Challenges")
                st.write(business_plan['Challenges'])
                
                st.write("### Target Audience")
                st.write(business_plan['Target Audience'])
                
                st.write("### Revenue Streams")
                st.write(business_plan['Revenue Streams'])
                
                st.write("### Profit Range")
                st.write(business_plan['Profit Range'])

                # Add PDF Download Button
                pdf_buffer = create_pdf(business_plan)
                st.download_button(
                    label="📄 Download Business Plan as PDF",
                    data=pdf_buffer,
                    file_name="business_plan.pdf",
                    mime="application/pdf"
                )
            else:
                # Generate Fallback Plan using Groq API
                st.info("Generating Business Plan...")
                fallback_plan = generate_fallback_plan(main_industry, sub_industry)
                st.write(fallback_plan)

                # Add PDF Download Button for Fallback Plan
                pdf_buffer = create_pdf({"Generated Plan": fallback_plan})
                st.download_button(
                    label="📄 Download Generated Business Plan as PDF",
                    data=pdf_buffer,
                    file_name="generated_business_plan.pdf",
                    mime="application/pdf"
                )

# Run the app
if __name__ == "__main__":
    main()

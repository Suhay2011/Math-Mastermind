import streamlit as st
from openai import OpenAI
import io

API_KEY=st.secrets["API_KEY"]

client=OpenAI(api_key=API_KEY,base_url="https://api.groq.com/openai/v1")

Model = "openai/gpt-oss-20b"
SYSTEM_PROMPT="""
you are a math mastermind
solve the problem step by step
Explain the reasoning clearly.
give the final answer.
verify the answer if possible."""
def solve_math(problem,level):
  prompt=f"""
  {SYSTEM_PROMPT}
  level:{level}
  Problem:{problem}
  """
  try:
    response = client.chat.completions.create(
        model=Model,
        messages=[
         {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=1024
    )

    return response.choices[0].message.content

  except Exception as e:
    return "Error: "+ str(e)

st.set_page_config(page_title="math mastermind")
st.title("math mastermind1")
st.write("Enter a math problem and get a step by step solution.")

if "history" not in st.session_state:
  st.session_state.history=[]
problem=st.text_area(
  "math problem",
  placeholder="example: solve X*X + 5X+6==0"
)

level=st.selectbox("level",["Basic","intermediate","advanced"])

if st.button("solve"):
  if not problem.strip():
    st.warning("please enter a problem.")
  else:
    with st.spinner("solving..."):
      try:
        answer= solve_math(problem,level)
        st.session_state.history.append({
          "problem":problem,
          "answer":answer
        })
        st.subheader("solution")
        st.write(answer)
      except Exception as e:
        st.error(f"error : {e}")

if st.button("clear history"):
  st.session_state.history=[]
  st.rerun()

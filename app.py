import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import base64, random
import pafy
import youtube_dl



from dotenv import load_dotenv

from Courses import ds_course, web_course, android_course, ios_course, uiux_course, resume_videos, interview_videos

# Combining all courses into one list for recommendations
all_courses = ds_course + web_course + android_course + ios_course + uiux_course

load_dotenv()     ##load env variables

###access API key
genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

### gemini pro response
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text


### text extraction
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    
    text = ""

    # for multiple page read
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())

    return text

### customized prompt template

#prompt template
input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in multipe lines string having the prettier structure
{{"JD Match":"%","\n\nMissing Keywords:[]","\n\nProfile Summary":"\n"}}
"""
##course recommendation
def course_recommender(course_list):
        st.subheader("**Courses & Certificates🎓 Recommendations**")
        c = 0
        rec_course = []
        no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4, key='slider_1')
        random.shuffle(course_list)
        for c_name, c_link in course_list:
            c += 1
            st.markdown(f"({c}) [{c_name}]({c_link})")
            rec_course.append(c_name)
            if c == no_of_reco:
                break
        return rec_course

def resume_recommender(resume_list):
        st.subheader("**Bonus Video for Resume Writing Tips💡**")
        r = 0
        rec_resvid = []
        no_of_reco = st.slider('Choose Number of Recommendations:', 1, 10, 3, key='slider_2')
        random.shuffle(resume_list)
        for r_name, r_link in resume_list:
            r += 1
            st.markdown(f"({r}) [{r_name}]({r_link})")
            rec_resvid.append(r_name)
            if r == no_of_reco:
                break
        return rec_resvid

def interview_recommender(interview_list):
        st.subheader("**Bonus Video for Interview👨‍💼 Tips💡**")
        itr = 0
        rec_itrvid = []
        no_of_reco = st.slider('Choose Number of Recommendations:', 1, 10, 3, key='slider_3')
        random.shuffle(interview_list)
        for itr_name, itr_link in interview_list:
            itr += 1
            st.markdown(f"({itr}) [{itr_name}]({itr_link})")
            rec_itrvid.append(itr_name)
            if itr == no_of_reco:
                break
        return rec_itrvid

# Function to fetch YouTube video title
def fetch_yt_video(link):
    video = pafy.new(link)
    return video.title


### streamlit app

st.set_page_config(
    page_title="Resume Screening System",
    
)
st.sidebar.markdown("# Choose activity : ")
activities = ["Resume Analysis", "Course Recommendations", "About"]
choice = st.sidebar.selectbox("Choose among the given options:", activities)

st.title("RESUME SCREENING SYSTEM")
st.subheader("Improve your Resume ATS !!!")


if choice == 'Resume Analysis':

    st.text('The integrated system helps candidates analyze, enhance, and match their resumes with targeted job roles, improving their chances of success in competitive job markets.')
    st.text(' ')
    st.text(' ')

    jd = st.text_area("Paste your Job Description")
    st.text(" ")
    st.text(" ")

    uploaded_file = st.file_uploader("Upload your Resume", type="pdf", help="Please upload a pdf file")
    st.text(" ")
    submit = st.button("Process")
    ## applying conditions for submit button
    if submit:
        if uploaded_file is not None:
            text = input_pdf_text(uploaded_file)
            response = get_gemini_response(input_prompt)
            st.subheader(response)

elif choice== 'Course Recommendations':

     # Show general course recommendations

    course_recommender(all_courses)

    # st.header("**Bonus Resources**")
    # st.video("https://www.youtube.com/watch?v=resume_tips_video")  # Replace with a real URL
    # st.video("https://www.youtube.com/watch?v=interview_tips_video")  # Replace with a real URL

    ## Resume writing video
    resume_recommender(resume_videos)
    # st.header("**Bonus Video for Resume Writing Tips💡**")
    # resume_vid = random.choice(resume_videos)
    # res_vid_title = fetch_yt_video(resume_vid)
    # st.subheader("✅ **" + res_vid_title + "**")
    # st.video(resume_vid)

    ## Interview Preparation Video
    interview_recommender(interview_videos)

    # st.header("**Bonus Video for Interview👨‍💼 Tips💡**")
    # interview_vid = random.choice(interview_videos)
    # int_vid_title = fetch_yt_video(interview_vid)
    # st.subheader("✅ **" + int_vid_title + "**")
    # st.video(interview_vid)

else : 
    st.text(" ")
    st.text(" ")
    st.text(" ")
    st.subheader("Group Members :")
    st.text(" ")
    st.text("Prajwal Tandekar\t\t BT21CSE103\n Ayush Meshram\t\t BT21CSE030\n Adarsh Raut\t\t BT21CSE041\n Vinit Tabhane\t\t BT21CSE039")
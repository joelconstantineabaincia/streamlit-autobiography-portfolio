import re
from pathlib import Path

import pandas as pd
import streamlit as st

# ----------------- CONSTANTS & DATA -----------------
NAME = "Joel Constantine Abaincia"
COURSE = "CS 365: Applied AI" 
SECTION = "BSCS - F1"
SCHOOL = "Cebu Institute of Technology - University (CIT-U), Cebu City"
PHOTO = Path(__file__).parent / "profile.jpg"
GITHUB = "https://github.com/joelconstantineabaincia"

SKILL_DEFAULT = 80  # lowest skill is 82, so 80 shows everything by default

skills_data = {
    "Domain": ["Languages", "Languages", "Languages", "Mobile & UI", "Mobile & UI",
               "AI & Controllers", "Web & Serving", "Databases & Storage"],
    "Skill": ["Kotlin", "C# / .NET", "Python", "Android SDK / MVP", "Material Design 3",
              "Mamdani Fuzzy Logic", "Streamlit", "Gson / Local Storage"],
    "Proficiency (%)": [92, 88, 85, 90, 86, 84, 82, 88],
    "Experience (Years)": [2.5, 2.0, 2.0, 2.5, 2.0, 1.5, 1.5, 2.0],
}
df_skills = pd.DataFrame(skills_data)

tech_details = {
    "Mobile Development": "Android Studio, Kotlin 1.9.0, ViewBinding, Material 3, AlarmManager, SharedPreferences, Gradle KTS",
    "Applied AI & Logic": "Mamdani Fuzzy Inference, Membership Functions, Defuzzification (Centroid), Clinical Rule Systems",
    "Desktop & Systems": "Visual Studio, C# 10+, .NET Framework 4.8, Windows Forms, DoubleBuffered Rendering",
    "Data & Scripting": "Python 3.10+, Pandas, JSON Serialization (Gson), Streamlit UI",
}

projects = [
    {
        "title": "SurgiCare: Intelligent Post-Op Recovery & Wound Monitoring Companion",
        "category": "Mobile Health",
        "role": "Lead Android Developer & Software Architect",
        "tools": ["Kotlin", "Android SDK (API 34)", "MVP Architecture", "AlarmManager", "Gson", "Material Design 3"],
        "description": "Engineered a native Android healthcare app for post-laparoscopic surgical recovery, featuring two-step wound photo documentation, an algorithmic symptom triage engine, and exact-alarm medication adherence reminders.",
        "outcome": "Implemented an offline-first architecture with 3-tier clinical triage rules (Green/Yellow/Red) and dynamic day-by-day healing timelines without external database dependencies.",
        "link": "https://github.com/joelconstantineabaincia/NursingApp",
    },
    {
        "title": "NutriNest: Personalized Nutrition & Smart Meal Planning Companion",
        "category": "Mobile Nutrition",
        "role": "Lead Mobile Developer & UI/UX Engineer",
        "tools": ["Kotlin", "Android SDK (API 34/36)", "MVP Architecture", "ViewBinding", "Material Design 3", "Gradle KTS"],
        "description": "Constructed an Android wellness app featuring a 3-step health onboarding flow, real-time daily calorie and macronutrient computation, an automated meal plan generator, and an interactive grocery checklist.",
        "outcome": "Built a clean MVP structure with type-safe ViewBinding, synced SeekBar caloric goal calculators, and animated micro-interactions for dynamic task completion.",
        "link": "https://github.com/joelconstantineabaincia/NutriNest",
    },
    {
        "title": "Fuzzy Logic Boss Fight: Mamdani AI Controller in 10x10 Arena",
        "category": "Applied AI / Intelligent Systems",
        "role": "AI & Gameplay Systems Engineer",
        "tools": ["C#", ".NET Framework 4.8", "Windows Forms", "Mamdani Fuzzy Logic", "Centroid Defuzzification"],
        "description": "Designed a real-time combat simulation featuring an AI boss controlled by a Mamdani-style fuzzy logic controller, evaluating Boss HP, Manhattan Distance, and Player Aggression to transition stances dynamically.",
        "outcome": "Implemented triangular fuzzification, min-max fuzzy rule composition, and live centroid defuzzification yielding smooth continuous stance transitions (0–100) and real-time membership graphs.",
        "link": "https://github.com/joelconstantineabaincia/VideoGameThemedFuzzy",
    },
]
CATEGORIES = ["All"] + list(dict.fromkeys(p["category"] for p in projects))


def md_escape(text: str) -> str:
    """Escape markdown characters so visitor input is shown as plain text."""
    return re.sub(r"([\\`*_{}\[\]()#+\-.!|<>~$])", r"\\\1", text)


def build_cv() -> str:
    """Build the downloadable profile from the same data shown on the page."""
    skill_lines = "\n".join(
        f"- {r['Skill']} ({r['Domain']}): {r['Proficiency (%)']}%, {r['Experience (Years)']} yrs"
        for _, r in df_skills.iterrows()
    )
    project_lines = "\n".join(
        f"{i}. {p['title']} [{p['category']}] - {p['role']}\n   Tools: {', '.join(p['tools'])}\n   {p['link']}"
        for i, p in enumerate(projects, 1)
    )
    return (
        f"{NAME.upper()}\n"
        f"BS Computer Science - {COURSE} (Section: {SECTION})\n"
        f"{SCHOOL}\n"
        f"GitHub: {GITHUB}\n\n"
        f"SKILLS:\n{skill_lines}\n\n"
        f"FEATURED PORTFOLIO PROJECTS:\n{project_lines}\n"
    )


def render_project(p: dict) -> None:
    c_p1, c_p2 = st.columns([3, 1])
    with c_p1:
        st.markdown(f"**Category:** `{p['category']}` | **Role:** *{p['role']}*")
        st.write(p["description"])
        st.markdown(f"**Key Outcome:** {p['outcome']}")
        st.markdown(f"**Tech Stack:** {', '.join(f'`{t}`' for t in p['tools'])}")
    with c_p2:
        st.markdown(f"[🔗 View Project Repository]({p['link']})")


def reset_filters() -> None:
    st.session_state["show_metrics"] = True
    st.session_state["focus_domain"] = "All"
    st.session_state["display_density"] = "Detailed View"
    st.session_state["skill_threshold"] = SKILL_DEFAULT


# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title=f"{NAME} | Portfolio & Autobiography",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state
if "guestbook_entries" not in st.session_state:
    st.session_state["guestbook_entries"] = []

# --- SIDEBAR ---
with st.sidebar:
    if PHOTO.exists():
        st.image(str(PHOTO), caption=f"{NAME} — Student Developer", width="stretch")
    else:
        st.info("📷 Photo placeholder — add profile.jpg next to app.py")

    st.markdown("### 🎓 Academic Profile")
    st.write(f"**Name:** {NAME}")
    st.write(f"**Course:** {COURSE}")
    st.write(f"**Section:** {SECTION}")
    st.write("**Specialization:** Software Engineering & Applied AI")

    st.markdown("---")
    st.markdown("### ⚙️ Interactive Controls")

    show_metrics = st.checkbox("Show Performance Metrics", value=True, key="show_metrics")

    focus_domain = st.selectbox(
        "Filter Projects by Category:",
        options=CATEGORIES,
        key="focus_domain",
    )

    display_density = st.radio(
        "Display Layout:",
        options=["Detailed View", "Compact View"],
        horizontal=True,
        key="display_density",
    )

    skill_threshold = st.slider(
        "Filter Skills by Proficiency (≥ %):",
        min_value=80,
        max_value=90,
        value=SKILL_DEFAULT,
        step=5,
        key="skill_threshold",
    )

    st.button("↺ Reset filters", on_click=reset_filters)

    st.markdown("---")
    st.download_button(
        label="📄 Download Resume Profile",
        data=build_cv(),
        file_name="Joel_Constantine_Abaincia_Profile.txt",
        mime="text/plain",
    )

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title(NAME)
    st.markdown(f"**{COURSE}** | **Section: {SECTION}** | 3rd Year BS Computer Science")
    st.markdown("*Software developer building native Android architectures, fuzzy decision systems, and human-centered applied AI tools.*")
with col_head2:
    st.info("💡 **Status:** Available for software development & AI applied research.")

# Metrics highlight
st.markdown("---")
if show_metrics:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Academic Year", "3rd Year", "In Progress", delta_color="off")
    m2.metric("Featured Repositories", f"{len(projects)} Projects", "Academic work", delta_color="off")
    m3.metric("Target Platforms", "Android & Windows", "Native Apps", delta_color="off")
    m4.metric("Architecture", "MVP Pattern", "Android projects", delta_color="off")
    st.markdown("---")

# --- MAIN NAVIGATION TABS ---
tab_bio, tab_skills, tab_projects, tab_contact = st.tabs([
    "📖 Autobiography",
    "📊 Skills & Analytics",
    "🚀 Portfolio Projects",
    "📬 Contact & Feedback",
])

# ----------------- TAB 1: AUTOBIOGRAPHY -----------------
with tab_bio:
    st.header("My Journey & Development Story")

    col_bio_left, col_bio_right = st.columns([2, 1])

    with col_bio_left:
        st.subheader("Background & Education")
        st.write(f"""
        I'm a 3rd-year BS Computer Science student at **{SCHOOL}**, Section **{SECTION}**,
        taking **{COURSE}**. I'm focusing on software engineering and applied AI.
        """)

        st.write(f"""I'm from Consolacion, Cebu but currently residing at Calamba, Cebu City. What got me into Computer Science was a mixture 
                  of things, namely my cousins were into Tech, with two of them being alumni of CIT-U Computer Science department. 
                  Another thing, that got me into this course was the career and at that time it was a lucrative career. 
                  Lastly, when I was debating between Computer Engineering, Computer Science and Accountacy, I just spinned the wheel
                  and it landed on Computer Science, so here I am.""")
        
        st.subheader("Architectural Discipline to Applied AI")
        st.write("""
        My software engineering journey is centered around building resilient, modular applications where user experience
        and algorithmic rigor meet. Whether architecting clean **Model-View-Presenter (MVP)** patterns in native Android using
        Kotlin, or crafting mathematical controllers in C# using **Mamdani Fuzzy Logic**, I focus on building systems that
        are predictable, responsive, and maintainable.

        In my coursework throughout Information Technology and Applied AI, I have placed particular emphasis on
        bringing intelligent behaviors directly to edge devices and desktop environments—ranging from clinical rule-based
        wound monitoring in healthcare to dynamic real-time game agents that reason under uncertainty.
        """)

        st.subheader("Academic & Technical Milestones")
        st.markdown("""
        * **2025 — Healthcare & Intelligent State Machines:** Developed algorithmic triage engines for clinical postoperative tracking (*SurgiCare*) and macro-planning nutrition apps (*NutriNest*).
        * **2026 — Applied AI & Computational Intelligence:** Designed Mamdani fuzzy logic decision engines with triangular fuzzification, dynamic rule clipping, and centroid defuzzification.
        """)

    with col_bio_right:
        st.subheader("Interests & Focus Areas")
        st.markdown("""
        * 📱 **Native Mobile Architecture:** Clean architecture, decoupled contracts, and offline-first persistence.
        * 🧠 **Fuzzy & Expert Systems:** Fuzzification, rule inferencing, and continuous state modeling.
        * 🎮 **Interactive Simulation:** Game AI agents, double-buffered graphics, and tile arenas.
        * 🛡️ **Software Craftsmanship:** Strict type safety, clean code principles, and reproducible testing.
        """)

        with st.expander("🌟 Engineering Philosophy"):
            st.write("""
            *"Clean architecture is not about writing more code; it is about creating strict boundaries so that critical business logic, whether a clinical triage rule or a fuzzy AI agent, can evolve independently of the UI."*
            """)

# ----------------- TAB 2: SKILLS & ANALYTICS -----------------
with tab_skills:
    st.header("Technical Competencies & Metrics")
    st.write(f"Displaying technical proficiencies filtered at **≥ {skill_threshold}%** competency level.")

    filtered_skills = df_skills[df_skills["Proficiency (%)"] >= skill_threshold]

    if filtered_skills.empty:
        st.warning(f"No skills at ≥ {skill_threshold}%. Lower the threshold in the sidebar.")
    else:
        col_chart, col_table = st.columns([3, 2])
        with col_chart:
            st.subheader("Proficiency Distribution")
            st.bar_chart(filtered_skills.set_index("Skill")[["Proficiency (%)"]])
        with col_table:
            st.subheader("Skill Matrix Table")
            st.dataframe(filtered_skills, width="stretch", hide_index=True)

    st.markdown("---")
    st.subheader("Technology Stack & Tooling Explorer")

    selected_areas = st.multiselect(
        "Select focus areas to view specific tools:",
        options=list(tech_details.keys()),
        default=["Mobile Development", "Applied AI & Logic"],
    )
    if not selected_areas:
        st.caption("Pick at least one focus area to see its tools.")
    for area in selected_areas:
        st.markdown(f"- **{area}:** {tech_details[area]}")

# ----------------- TAB 3: PORTFOLIO PROJECTS -----------------
with tab_projects:
    st.header("Featured Projects")
    st.caption("Demonstrating software architecture, mobile engineering, and applied computational intelligence.")

    visible_projects = [
        p for p in projects if focus_domain == "All" or p["category"] == focus_domain
    ]

    if not visible_projects:
        st.warning(f"No projects found under category '{focus_domain}'. Reset the category filter in the sidebar to view all.")
    else:
        for p in visible_projects:
            if display_density == "Compact View":
                with st.expander(f"{p['title']}  ·  {p['category']}"):
                    render_project(p)
            else:
                st.markdown(f"### {p['title']}")
                render_project(p)
                st.divider()

# ----------------- TAB 4: CONTACT & FEEDBACK -----------------
with tab_contact:
    st.header("Get in Touch")
    st.write("Have feedback on these projects, or want to connect? Leave a message below.")

    col_form, col_history = st.columns([3, 2])

    with col_form:
        with st.form("contact_form", clear_on_submit=True):
            st.subheader("Send Feedback / Inquiry")
            sender_name = st.text_input("Your Name *", placeholder="e.g., Prof. Garcia")
            sender_email = st.text_input("Your Email *", placeholder="e.g., garcia@university.edu")
            inquiry_type = st.selectbox(
                "Inquiry Type:",
                ["Project Feedback", "Collaboration Opportunity", "Academic Inquiry", "General Greeting"],
            )
            sender_message = st.text_area("Message *", height=120, max_chars=500,
                                          placeholder="Write your comments or message here...")

            submitted = st.form_submit_button("🚀 Submit Message")

            if submitted:
                name = sender_name.strip()
                email = sender_email.strip()
                message = sender_message.strip()
                email_ok = bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))
                if not (name and message):
                    st.error("Please provide both your name and message before submitting.")
                elif not email_ok:
                    st.error("Please enter a valid email address (e.g., name@school.edu).")
                else:
                    st.session_state["guestbook_entries"].append({
                        "name": name,
                        "email": email,
                        "type": inquiry_type,
                        "message": message,
                    })
                    st.success(f"Thank you, {md_escape(name)}! Your message has been received.")

    with col_history:
        st.subheader("Session Feedback Log")
        if not st.session_state["guestbook_entries"]:
            st.info("No messages submitted yet during this session. Test the form on the left!")
        else:
            for item in reversed(st.session_state["guestbook_entries"]):
                with st.chat_message("user"):
                    st.markdown(f"**{md_escape(item['name'])}** *({item['type']})*")
                    st.write(md_escape(item["message"]))

# --- FOOTER ---
st.markdown("---")
f_col1, f_col2, f_col3 = st.columns([2, 2, 1])
with f_col1:
    st.caption(f"Submitted for **{COURSE}** — Activity: Autobiography and Portfolio App")
with f_col2:
    st.caption(f"Student: **{NAME}** | Section: **{SECTION}**")
with f_col3:
    st.caption("Built with [Streamlit](https://streamlit.io)")
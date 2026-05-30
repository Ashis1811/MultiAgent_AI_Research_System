# import streamlit as st
# import re
# import time
# from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain, rag_chain
# from tools import extract_file_content, scrape_url
# from rag import create_vector_store, retrieve_relevant_context



# # ── Page config ──────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="ResearchMind · AI Research Agent",
#     page_icon="🔬",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ── Custom CSS ────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

# html, body, [class*="css"] {
#     font-family: 'DM Sans', sans-serif;
#     color: #e8e4dc;
# }
# .stApp {
#     background: #0a0a0f;
#     background-image:
#         radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
#         radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
# }
# #MainMenu, footer, header { visibility: hidden; }
# .block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

# .hero { text-align: center; padding: 3.5rem 0 2.5rem; position: relative; }
# .hero-eyebrow {
#     font-family: 'DM Mono', monospace; font-size: 0.7rem; font-weight: 500;
#     letter-spacing: 0.25em; text-transform: uppercase; color: #ff8c32;
#     margin-bottom: 1rem; opacity: 0.9;
# }
# .hero h1 {
#     font-family: 'Syne', sans-serif; font-size: clamp(2.8rem, 6vw, 5rem);
#     font-weight: 800; line-height: 1.0; letter-spacing: -0.03em;
#     color: #f0ebe0; margin: 0 0 1rem;
# }
# .hero h1 span { color: #ff8c32; }
# .hero-sub {
#     font-size: 1.05rem; font-weight: 300; color: #a09890;
#     max-width: 520px; margin: 0 auto; line-height: 1.65;
# }
# .divider {
#     height: 1px;
#     background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
#     margin: 2rem 0;
# }
# .input-card {
#     background: rgba(255,255,255,0.03); border: 1px solid rgba(255,140,50,0.15);
#     border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2rem;
#     backdrop-filter: blur(8px);
# }

# /* ── File uploader styling ── */
# .upload-zone {
#     border: 1px dashed rgba(255,140,50,0.3);
#     border-radius: 10px;
#     padding: 0.8rem 1rem;
#     margin: 0.8rem 0 1.2rem;
#     background: rgba(255,140,50,0.03);
#     transition: border-color 0.2s;
# }
# .upload-label {
#     font-family: 'DM Mono', monospace; font-size: 0.72rem;
#     letter-spacing: 0.15em; text-transform: uppercase;
#     color: #ff8c32; font-weight: 500; margin-bottom: 0.5rem;
#     display: block;
# }
# .file-badge {
#     display: inline-flex; align-items: center; gap: 0.4rem;
#     background: rgba(255,140,50,0.12); border: 1px solid rgba(255,140,50,0.25);
#     border-radius: 6px; padding: 0.3rem 0.7rem;
#     font-family: 'DM Mono', monospace; font-size: 0.72rem; color: #ff8c32;
#     margin-top: 0.4rem;
# }
# /* Override streamlit file uploader */
# [data-testid="stFileUploader"] {
#     background: transparent !important;
# }
# [data-testid="stFileUploader"] > div {
#     background: rgba(255,255,255,0.03) !important;
#     border: 1px dashed rgba(255,140,50,0.25) !important;
#     border-radius: 10px !important;
#     padding: 0.6rem 1rem !important;
# }
# [data-testid="stFileUploader"] label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.72rem !important;
#     letter-spacing: 0.15em !important;
#     text-transform: uppercase !important;
#     color: #ff8c32 !important;
#     font-weight: 500 !important;
# }
# [data-testid="stFileUploader"] button {
#     background: rgba(255,140,50,0.15) !important;
#     color: #ff8c32 !important;
#     border: 1px solid rgba(255,140,50,0.3) !important;
#     border-radius: 6px !important;
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.72rem !important;
# }

# .stTextInput > div > div > input {
#     background: rgba(255,255,255,0.05) !important;
#     border: 1px solid rgba(255,140,50,0.25) !important;
#     border-radius: 10px !important;
#     color: #f0ebe0 !important;
#     font-family: 'DM Sans', sans-serif !important;
#     font-size: 1rem !important;
#     padding: 0.75rem 1rem !important;
#     transition: border-color 0.2s, box-shadow 0.2s !important;
# }
# .stTextInput > div > div > input:focus {
#     border-color: #ff8c32 !important;
#     box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
# }
# .stTextInput > label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.72rem !important;
#     letter-spacing: 0.15em !important;
#     text-transform: uppercase !important;
#     color: #ff8c32 !important;
#     font-weight: 500 !important;
# }
# .stButton > button {
#     background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
#     color: #0a0a0f !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 700 !important;
#     font-size: 0.95rem !important;
#     letter-spacing: 0.04em !important;
#     border: none !important;
#     border-radius: 10px !important;
#     padding: 0.7rem 2.2rem !important;
#     cursor: pointer !important;
#     transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
#     box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
#     width: 100%;
# }
# .stButton > button:hover {
#     transform: translateY(-2px) !important;
#     box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
#     opacity: 0.95 !important;
# }
# .stButton > button:active { transform: translateY(0) !important; }

# .step-card {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 14px; padding: 1.5rem 1.8rem;
#     margin-bottom: 1.2rem; position: relative; overflow: hidden;
#     transition: border-color 0.3s;
# }
# .step-card.active { border-color: rgba(255,140,50,0.4); background: rgba(255,140,50,0.04); }
# .step-card.done   { border-color: rgba(80,200,120,0.3); background: rgba(80,200,120,0.03); }
# .step-card.skip   { border-color: rgba(255,255,255,0.04); opacity: 0.45; }
# .step-card::before {
#     content: ''; position: absolute; left: 0; top: 0; bottom: 0;
#     width: 3px; border-radius: 14px 0 0 14px;
#     background: rgba(255,255,255,0.05); transition: background 0.3s;
# }
# .step-card.active::before { background: #ff8c32; }
# .step-card.done::before   { background: #50c878; }

# .step-header { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.3rem; }
# .step-num { font-family: 'DM Mono', monospace; font-size: 0.68rem; font-weight: 500; letter-spacing: 0.15em; color: #ff8c32; opacity: 0.7; }
# .step-title { font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 700; color: #f0ebe0; }
# .step-status { margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em; }
# .status-waiting  { color: #555; }
# .status-running  { color: #ff8c32; }
# .status-done     { color: #50c878; }
# .status-skipped  { color: #404040; }

# .result-panel {
#     background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 14px; padding: 1.8rem 2rem; margin-top: 1rem; margin-bottom: 1.5rem;
# }
# .result-panel-title {
#     font-family: 'DM Mono', monospace; font-size: 0.7rem; font-weight: 500;
#     letter-spacing: 0.2em; text-transform: uppercase; color: #ff8c32;
#     margin-bottom: 1rem; padding-bottom: 0.7rem; border-bottom: 1px solid rgba(255,140,50,0.15);
# }
# .result-content {
#     font-size: 0.92rem; line-height: 1.8; color: #cdc8bf;
#     white-space: pre-wrap; font-family: 'DM Sans', sans-serif;
# }
# .report-panel {
#     background: rgba(255,255,255,0.025); border: 1px solid rgba(255,140,50,0.2);
#     border-radius: 16px; padding: 2rem 2.5rem; margin-top: 1rem;
# }
# .feedback-panel {
#     background: rgba(255,255,255,0.025); border: 1px solid rgba(80,200,120,0.2);
#     border-radius: 16px; padding: 2rem 2.5rem; margin-top: 1rem;
# }
# .panel-label {
#     font-family: 'DM Mono', monospace; font-size: 0.7rem;
#     letter-spacing: 0.2em; text-transform: uppercase;
#     margin-bottom: 1.2rem; padding-bottom: 0.7rem;
# }
# .panel-label.orange { color: #ff8c32; border-bottom: 1px solid rgba(255,140,50,0.15); }
# .panel-label.green  { color: #50c878; border-bottom: 1px solid rgba(80,200,120,0.15); }

# /* doc-mode banner */
# .doc-mode-banner {
#     background: rgba(255,140,50,0.08);
#     border: 1px solid rgba(255,140,50,0.25);
#     border-radius: 10px;
#     padding: 0.6rem 1rem;
#     margin-bottom: 1rem;
#     font-family: 'DM Mono', monospace;
#     font-size: 0.72rem;
#     color: #ff8c32;
#     letter-spacing: 0.08em;
#     display: flex;
#     align-items: center;
#     gap: 0.5rem;
# }

# .stSpinner > div { color: #ff8c32 !important; }
# details summary {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.75rem !important;
#     color: #a09890 !important;
#     letter-spacing: 0.1em !important;
#     cursor: pointer;
# }
# .section-heading {
#     font-family: 'Syne', sans-serif; font-size: 1.3rem;
#     font-weight: 700; color: #f0ebe0; margin: 2rem 0 1rem;
# }
# .notice {
#     font-family: 'DM Mono', monospace; font-size: 0.72rem;
#     color: #605850; text-align: center; margin-top: 3rem; letter-spacing: 0.08em;
# }
# </style>
# """, unsafe_allow_html=True)


# # ── Helper: render a step card ────────────────────────────────────────────────
# def step_card(num: str, title: str, state: str, desc: str = ""):
#     status_map = {
#         "waiting": ("WAITING",   "status-waiting"),
#         "running": ("● RUNNING", "status-running"),
#         "done":    ("✓ DONE",    "status-done"),
#         "skipped": ("— SKIP",    "status-skipped"),
#     }
#     label, cls = status_map.get(state, ("", ""))
#     card_cls = {"running": "active", "done": "done", "skipped": "skip"}.get(state, "")
#     st.markdown(f"""
#     <div class="step-card {card_cls}">
#         <div class="step-header">
#             <span class="step-num">{num}</span>
#             <span class="step-title">{title}</span>
#             <span class="step-status {cls}">{label}</span>
#         </div>
#         {"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
#     </div>
#     """, unsafe_allow_html=True)


# # ── Session state init ────────────────────────────────────────────────────────
# for key in ("results", "running", "done", "doc_content", "doc_name"):
#     if key not in st.session_state:
#         if key == "results":
#             st.session_state[key] = {}
#         elif key in ("doc_content", "doc_name"):
#             st.session_state[key] = ""
#         else:
#             st.session_state[key] = False


# # ── Hero ──────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="hero">
#     <div class="hero-eyebrow">Multi-Agent AI System</div>
#     <h1>Research<span>Mind</span></h1>
#     <p class="hero-sub">
#         Four specialized AI agents collaborate — searching, scraping, writing,
#         and critiquing — to deliver a polished research report on any topic.
#         Upload a document or image to analyse it directly.
#     </p>
# </div>
# <div class="divider"></div>
# """, unsafe_allow_html=True)


# # ── Layout ────────────────────────────────────────────────────────────────────
# col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

# with col_input:
#     st.markdown('<div class="input-card">', unsafe_allow_html=True)

#     # ── Text input ──
#     topic = st.text_input(
#         "Research Topic or Question",
#         placeholder="e.g. Summarise this document  ·  Quantum computing breakthroughs",
#         key="topic_input",
#         label_visibility="visible",
#     )

#     # ── File uploader (same card, below text input) ──
#     uploaded_file = st.file_uploader(
#         "Upload a file  (optional — PDF · image · TXT · CSV · MD)",
#         type=["pdf", "png", "jpg", "jpeg", "webp", "bmp", "tiff", "txt", "md", "csv"],
#         key="file_upload",
#         label_visibility="visible",
#         help="Upload a document or image and ask anything about it. "
#              "The agents will use your file as the primary research source.",
#     )

#     # Show badge when file is loaded
#     if uploaded_file is not None:
#         st.markdown(
#             f'<div class="file-badge">📎 {uploaded_file.name} '
#             f'({round(uploaded_file.size / 1024, 1)} KB) — ready</div>',
#             unsafe_allow_html=True,
#         )

#     st.markdown("<br>", unsafe_allow_html=True)
#     run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Example chips
#     st.markdown("""
#     <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
#         <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</span>
#     """, unsafe_allow_html=True)
#     for ex in ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]:
#         st.markdown(f"""
#         <span style="
#             background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
#             border-radius:6px; padding:0.25rem 0.7rem; font-size:0.75rem;
#             color:#a09890; font-family:'DM Sans',sans-serif; cursor:default;
#         ">{ex}</span>
#         """, unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

# with col_pipeline:
#     st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

#     r = st.session_state.results
#     has_doc = bool(st.session_state.doc_content)

#     def s(step):
#         if not r:
#             return "waiting"
#         steps = ["search", "reader", "writer", "critic"]
#         if step in r:
#             return "done"
#         # skip search + reader when a document was uploaded
#         if has_doc and step in ("search", "reader"):
#             return "skipped"
#         if st.session_state.running:
#             for k in steps:
#                 if k not in r:
#                     return "running" if k == step else "waiting"
#         return "waiting"

#     doc_active = bool(st.session_state.doc_content)

#     step_card("01", "Search Agent",  s("search"),
#               "Skipped — using uploaded document" if doc_active else "Gathers recent web information")
#     step_card("02", "Reader Agent",  s("reader"),
#               "Skipped — content already extracted" if doc_active else "Scrapes & extracts deep content")
#     step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report")
#     step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report")


# # ── Trigger pipeline ──────────────────────────────────────────────────────────
# if run_btn:
#     if not topic.strip() and uploaded_file is None:
#         st.warning("Please enter a topic or upload a file first.")
#     else:
#         # Extract file content NOW (before rerun loses the widget state)
#         if uploaded_file is not None:
#             with st.spinner("📂 Extracting file content…"):
#                 st.session_state.doc_content = extract_file_content(uploaded_file)
#                 st.session_state.doc_name    = uploaded_file.name
#         else:
#             st.session_state.doc_content = ""
#             st.session_state.doc_name    = ""

#         st.session_state.results = {}
#         st.session_state.running = True
#         st.session_state.done    = False
#         st.rerun()

# # ── Execute Pipeline ──────────────────────────────────────────────────────────
# if st.session_state.running and not st.session_state.done:

#     results   = {}
#     topic_val = st.session_state.topic_input
#     doc_text  = st.session_state.doc_content
#     doc_name  = st.session_state.doc_name

# # ── DOCUMENT MODE (RAG) ─────────────────────────────────────────────
#     if doc_text:

#         st.info(f"📎 Document mode — using **{doc_name}**")

#         results["search"] = (
#             f"[Document upload mode]\n"
#             f"File: {doc_name}"
#         )

#         results["reader"] = doc_text

#         # Create embeddings
#         with st.spinner("📚 Creating document embeddings..."):

#             vectorstore = create_vector_store(doc_text)

#         # Retrieve relevant chunks
#         with st.spinner("🔍 Retrieving relevant context..."):

#             relevant_context = retrieve_relevant_context(
#                 vectorstore,
#                 topic_val
#             )

#         # Generate answer
#         with st.spinner("✍️ Generating answer from document..."):

#             results["writer"] = rag_chain.invoke({

#                 "question": topic_val,

#                 "context": relevant_context

#             })


# # ── WEB RESEARCH MODE ─────────────────────────────────────────────
#     else:

#         # Step 1 → Search Agent
#         with st.spinner("🔍 Search Agent is working…"):

#             search_agent = build_search_agent()

#             sr = search_agent.invoke({

#                 "messages": [

#                     (
#                         "user",
#                         f"Find recent, reliable and detailed information about: {topic_val}"
#                     )

#                 ]
#             })

#             results["search"] = sr["messages"][-1][1]

# # ── Step 2: Reader Agent ──────────────────────────────

#         with st.spinner("📄 Reader Agent is scraping top resources…"):

#             search_text = results.get("search", "")

#             urls = re.findall(r'https?://[^\s]+', search_text)

#             if urls:

#                 top_url = urls[0]

#                 try:

#                     scraped_content = scrape_url.invoke(top_url)

#                     results["reader"] = scraped_content

#                 except Exception as e:

#                     results["reader"] = f"Error while scraping URL: {str(e)}"

#             else:

#                 results["reader"] = "No valid URL found."


# # ── Step 3 → Writer Agent ──────────────────────────────

#         with st.spinner("✍️ Writer is drafting the report…"):

#             research_combined = (

#                 f"TOPIC:\n{topic_val}\n\n"
#                 f"SEARCH RESULTS:\n{results.get('search', 'No search results available')}\n\n"
#                 f"SCRAPED CONTENT:\n{results.get('reader', 'No scraped content available')}"

#             )

#             results["writer"] = writer_chain.invoke({

#                 "topic": topic_val,

#                 "research": research_combined

#             })


# # ── Step 4 → Critic Agent ─────────────────────────────────────

#     with st.spinner("🧐 Critic is reviewing the report…"):

#         results["critic"] = critic_chain.invoke({

#             "report": results.get("writer", "No report generated")

#         })


#     st.session_state.results = dict(results)

#     st.session_state.running = False
#     st.session_state.done = True

#     st.rerun()




# # ── Results display ───────────────────────────────────────────────────────────
# r = st.session_state.results

# if r:
#     st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
#     st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

#     # Show doc-mode banner
#     if st.session_state.doc_content:
#         st.markdown(
#             f'<div class="doc-mode-banner">📎 Document mode · '
#             f'{st.session_state.doc_name} · '
#             f'{len(st.session_state.doc_content):,} chars extracted</div>',
#             unsafe_allow_html=True,
#         )

#     if "search" in r:
#         with st.expander("🔍 Search Results (raw)", expanded=False):
#             st.markdown(
#                 f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
#                 f'<div class="result-content">{r["search"]}</div></div>',
#                 unsafe_allow_html=True,
#             )

#     if "reader" in r:
#         label = "📄 Extracted Document Content (raw)" if st.session_state.doc_content else "📄 Scraped Content (raw)"
#         with st.expander(label, expanded=False):
#             st.markdown(
#                 f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
#                 f'<div class="result-content">{r["reader"][:3000]}{"…" if len(r["reader"]) > 3000 else ""}</div></div>',
#                 unsafe_allow_html=True,
#             )

#     if "writer" in r:
#         st.markdown("""
#         <div class="report-panel">
#             <div class="panel-label orange">📝 Final Research Report</div>
#         """, unsafe_allow_html=True)
#         st.markdown(r.get("writer", "No report available"))
#         st.markdown("</div>", unsafe_allow_html=True)

#         st.download_button(
#             label="⬇  Download Report (.md)",
#             data=r["writer"],
#             file_name=f"research_report_{int(time.time())}.md",
#             mime="text/markdown",
#         )

#     if "critic" in r:
#         feedback = r["critic"]
#         match = re.search(r"Score:\s*(\d+)/10", feedback)
#         if match:
#             score = int(match.group(1))
#             color      = "#50c878" if score >= 8 else "#ffb347" if score >= 6 else "#ff5a5a"
#             compliment = "Excellent Research" if score >= 8 else "Good Research" if score >= 6 else "Average Research"
#             feedback = re.sub(
#                 r"Score:\s*\d+/10",
#                 f'<div style="margin-bottom:1rem;">'
#                 f'<div style="font-size:1.2rem;font-weight:800;color:{color};">'
#                 f'⭐ Score: {score}/10 • {compliment}</div></div>',
#                 feedback,
#             )

#         st.markdown("""
#         <div class="feedback-panel">
#             <div class="panel-label green">🧐 Critic Feedback</div>
#         """, unsafe_allow_html=True)
#         st.markdown(feedback, unsafe_allow_html=True)
#         st.markdown("</div>", unsafe_allow_html=True)


# # ── Footer ────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="notice">
#     ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
# </div>
# """, unsafe_allow_html=True)


import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import re
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain, rag_chain
from tools import extract_file_content, scrape_url
from rag import create_vector_store, retrieve_relevant_context

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Master CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@200;300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
  --bg:          #05050a;
  --bg2:         #0c0c14;
  --surface:     rgba(255,255,255,0.035);
  --border:      rgba(255,255,255,0.07);
  --border2:     rgba(255,255,255,0.12);
  --accent:      #00e5ff;
  --accent2:     #7b61ff;
  --accent3:     #ff4d6d;
  --text:        #e8e6f0;
  --text2:       #8b8a9e;
  --text3:       #4a4a5e;
  --font-display: 'Bebas Neue', sans-serif;
  --font-body:    'Outfit', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
  --r-sm: 8px; --r-md: 14px; --r-lg: 20px; --r-xl: 28px;
  --glow-cyan:   0 0 40px rgba(0,229,255,0.15);
}

html, body, [class*="css"] { font-family: var(--font-body); color: var(--text); -webkit-font-smoothing: antialiased; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2.5rem 5rem !important; max-width: 1280px !important; }

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 90% 60% at 15% -5%,  rgba(0,229,255,0.07)  0%, transparent 55%),
        radial-gradient(ellipse 70% 50% at 85% 100%, rgba(123,97,255,0.08) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50%  50%, rgba(255,77,109,0.04) 0%, transparent 60%);
}
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.012'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/svg%3E");
    pointer-events: none; z-index: 0;
}

/* NAV */
.topbar { display:flex; align-items:center; justify-content:space-between; padding:1.4rem 0 1rem; border-bottom:1px solid var(--border); }
.topbar-logo { display:flex; align-items:baseline; gap:0.5rem; }
.topbar-logo-text { font-family:var(--font-display); font-size:2rem; letter-spacing:0.06em; color:var(--text); line-height:1; }
.topbar-logo-text span { color:var(--accent); }
.topbar-tag { font-family:var(--font-mono); font-size:0.6rem; letter-spacing:0.2em; color:var(--accent2); background:rgba(123,97,255,0.12); border:1px solid rgba(123,97,255,0.25); padding:0.2rem 0.6rem; border-radius:4px; text-transform:uppercase; }
.topbar-badges { display:flex; gap:0.5rem; align-items:center; }
.badge { font-family:var(--font-mono); font-size:0.58rem; letter-spacing:0.12em; text-transform:uppercase; padding:0.22rem 0.65rem; border-radius:4px; }
.badge-cyan   { color:var(--accent);  background:rgba(0,229,255,0.08);  border:1px solid rgba(0,229,255,0.2); }
.badge-purple { color:var(--accent2); background:rgba(123,97,255,0.08); border:1px solid rgba(123,97,255,0.2); }
.badge-red    { color:var(--accent3); background:rgba(255,77,109,0.08);  border:1px solid rgba(255,77,109,0.2); }

/* HERO */
.hero { padding:4rem 0 3rem; }
.hero-kicker { font-family:var(--font-mono); font-size:0.65rem; letter-spacing:0.3em; text-transform:uppercase; color:var(--accent); margin-bottom:1.2rem; display:flex; align-items:center; gap:0.7rem; }
.hero-kicker::before { content:''; display:inline-block; width:28px; height:1px; background:var(--accent); opacity:0.6; }
.hero-title { font-family:var(--font-display); font-size:clamp(4rem,9vw,8rem); line-height:0.92; letter-spacing:0.02em; color:var(--text); margin:0 0 1.5rem; }
.hero-title .line2 { color:transparent; -webkit-text-stroke:1px rgba(255,255,255,0.22); }
.hero-title .aw { color:var(--accent); }
.hero-desc { font-size:1rem; font-weight:300; color:var(--text2); line-height:1.75; max-width:480px; }
.hero-stats { display:flex; gap:2rem; margin-top:2.5rem; padding-top:2rem; border-top:1px solid var(--border); }
.stat-item { display:flex; flex-direction:column; gap:0.2rem; }
.stat-num { font-family:var(--font-display); font-size:2rem; letter-spacing:0.05em; color:var(--text); line-height:1; }
.stat-num span { color:var(--accent); }
.stat-label { font-family:var(--font-mono); font-size:0.58rem; letter-spacing:0.15em; text-transform:uppercase; color:var(--text3); }

/* SECTION EYEBROW */
.eyebrow { font-family:var(--font-mono); font-size:0.6rem; letter-spacing:0.25em; text-transform:uppercase; color:var(--text3); margin-bottom:1rem; display:flex; align-items:center; gap:0.6rem; }
.eyebrow::after { content:''; flex:1; height:1px; background:var(--border); }

/* INPUT CARD */
.input-card { background:var(--surface); border:1px solid var(--border2); border-radius:var(--r-xl); padding:2rem 2rem 1.5rem; position:relative; overflow:hidden; }
.input-card::before { content:''; position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,rgba(0,229,255,0.5) 30%,rgba(123,97,255,0.5) 70%,transparent); }
.input-card::after { content:''; position:absolute; top:-80px; right:-80px; width:200px; height:200px; background:radial-gradient(circle,rgba(0,229,255,0.06) 0%,transparent 70%); pointer-events:none; }

.stTextInput > label { font-family:var(--font-mono) !important; font-size:0.6rem !important; letter-spacing:0.2em !important; text-transform:uppercase !important; color:var(--accent) !important; font-weight:400 !important; margin-bottom:0.5rem !important; }
.stTextInput > div > div > input { background:rgba(0,0,0,0.3) !important; border:1px solid rgba(255,255,255,0.1) !important; border-radius:var(--r-md) !important; color:var(--text) !important; font-family:var(--font-body) !important; font-size:1.05rem !important; font-weight:300 !important; padding:0.85rem 1.1rem !important; transition:all 0.25s !important; }
.stTextInput > div > div > input::placeholder { color:var(--text3) !important; }
.stTextInput > div > div > input:focus { border-color:var(--accent) !important; box-shadow:0 0 0 3px rgba(0,229,255,0.1),var(--glow-cyan) !important; background:rgba(0,229,255,0.03) !important; }

[data-testid="stFileUploader"] label { font-family:var(--font-mono) !important; font-size:0.6rem !important; letter-spacing:0.2em !important; text-transform:uppercase !important; color:var(--accent2) !important; }
[data-testid="stFileUploader"] > div { background:rgba(123,97,255,0.04) !important; border:1px dashed rgba(123,97,255,0.3) !important; border-radius:var(--r-md) !important; transition:all 0.2s !important; }
[data-testid="stFileUploader"] > div:hover { border-color:rgba(123,97,255,0.6) !important; background:rgba(123,97,255,0.07) !important; }
[data-testid="stFileUploader"] button { background:rgba(123,97,255,0.15) !important; color:var(--accent2) !important; border:1px solid rgba(123,97,255,0.3) !important; border-radius:var(--r-sm) !important; font-family:var(--font-mono) !important; font-size:0.65rem !important; }

.stButton > button { background:linear-gradient(135deg,var(--accent) 0%,var(--accent2) 100%) !important; color:#05050a !important; font-family:var(--font-display) !important; font-size:1.15rem !important; letter-spacing:0.12em !important; border:none !important; border-radius:var(--r-md) !important; padding:0.8rem 2rem !important; cursor:pointer !important; transition:all 0.2s !important; box-shadow:0 4px 24px rgba(0,229,255,0.25) !important; width:100% !important; margin-top:0.5rem !important; }
.stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 32px rgba(0,229,255,0.35),0 0 60px rgba(0,229,255,0.1) !important; }
.stButton > button:active { transform:translateY(0) !important; }

.file-badge { display:inline-flex; align-items:center; gap:0.5rem; background:rgba(123,97,255,0.1); border:1px solid rgba(123,97,255,0.3); border-radius:var(--r-sm); padding:0.35rem 0.85rem; font-family:var(--font-mono); font-size:0.65rem; color:var(--accent2); margin-top:0.5rem; letter-spacing:0.05em; }
.file-badge-dot { width:6px; height:6px; background:var(--accent2); border-radius:50%; animation:pulse-dot 1.5s ease infinite; }
@keyframes pulse-dot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(0.7)} }

.chips-row { display:flex; gap:0.5rem; flex-wrap:wrap; margin-top:1.2rem; align-items:center; }
.chip-label { font-family:var(--font-mono); font-size:0.58rem; color:var(--text3); letter-spacing:0.12em; text-transform:uppercase; }
.chip { background:rgba(255,255,255,0.03); border:1px solid var(--border2); border-radius:6px; padding:0.25rem 0.7rem; font-family:var(--font-body); font-size:0.72rem; font-weight:400; color:var(--text2); cursor:default; }

/* PIPELINE */
.pipeline-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:1.2rem; }
.pipeline-title { font-family:var(--font-display); font-size:1.6rem; letter-spacing:0.06em; color:var(--text); }
.pipeline-subtitle { font-family:var(--font-mono); font-size:0.58rem; color:var(--text3); letter-spacing:0.12em; text-transform:uppercase; }

.step-card { position:relative; background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:var(--r-md); padding:1.1rem 1.3rem 1.1rem 1.6rem; margin-bottom:0.7rem; overflow:hidden; transition:all 0.3s; }
.step-card::before { content:''; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--border2); transition:background 0.3s,box-shadow 0.3s; }
.step-card.active { border-color:rgba(0,229,255,0.2); background:rgba(0,229,255,0.03); box-shadow:var(--glow-cyan); }
.step-card.active::before { background:var(--accent); box-shadow:0 0 12px var(--accent); }
.step-card.done { border-color:rgba(0,255,136,0.15); background:rgba(0,255,136,0.02); }
.step-card.done::before { background:#00ff88; }
.step-card.skip { opacity:0.3; }
.step-card.active::after { content:''; position:absolute; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,rgba(0,229,255,0.4),transparent); animation:scan 2s linear infinite; }
@keyframes scan { 0%{top:0} 100%{top:100%} }
.step-row { display:flex; align-items:center; gap:0.75rem; }
.step-index { font-family:var(--font-mono); font-size:0.58rem; color:var(--text3); letter-spacing:0.1em; min-width:22px; }
.step-icon { font-size:0.9rem; min-width:20px; text-align:center; }
.step-name { font-family:var(--font-body); font-size:0.88rem; font-weight:600; color:var(--text); flex:1; }
.step-desc { font-family:var(--font-body); font-size:0.72rem; font-weight:300; color:var(--text3); margin-top:0.2rem; padding-left:3.1rem; }
.step-status { font-family:var(--font-mono); font-size:0.58rem; letter-spacing:0.1em; text-transform:uppercase; padding:0.18rem 0.55rem; border-radius:4px; }
.st-wait { color:var(--text3); background:rgba(255,255,255,0.04); border:1px solid var(--border); }
.st-run  { color:var(--accent); background:rgba(0,229,255,0.1); border:1px solid rgba(0,229,255,0.3); animation:blink 1s ease infinite; }
.st-done { color:#00ff88; background:rgba(0,255,136,0.08); border:1px solid rgba(0,255,136,0.25); }
.st-skip { color:var(--text3); background:transparent; border:1px solid var(--border); }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.5} }

/* DIVIDER */
.h-divider { height:1px; background:linear-gradient(90deg,transparent,rgba(0,229,255,0.2) 25%,rgba(123,97,255,0.2) 75%,transparent); margin:2.5rem 0; }

/* RESULTS */
.results-heading { font-family:var(--font-display); font-size:3rem; letter-spacing:0.06em; color:var(--text); margin-bottom:0.3rem; }
.results-meta { font-family:var(--font-mono); font-size:0.6rem; color:var(--text3); letter-spacing:0.15em; text-transform:uppercase; margin-bottom:1.5rem; }
.doc-banner { display:flex; align-items:center; gap:0.8rem; background:linear-gradient(135deg,rgba(123,97,255,0.08),rgba(0,229,255,0.05)); border:1px solid rgba(123,97,255,0.25); border-radius:var(--r-md); padding:0.8rem 1.2rem; margin-bottom:1.5rem; font-family:var(--font-mono); font-size:0.65rem; color:var(--accent2); letter-spacing:0.07em; }

.raw-panel { background:rgba(0,0,0,0.25); border:1px solid var(--border); border-radius:var(--r-md); padding:1.5rem 1.8rem; margin-top:0.5rem; }
.raw-panel-title { font-family:var(--font-mono); font-size:0.6rem; letter-spacing:0.2em; text-transform:uppercase; color:var(--accent); margin-bottom:1rem; padding-bottom:0.6rem; border-bottom:1px solid var(--border); }
.raw-content { font-family:var(--font-mono); font-size:0.75rem; line-height:1.8; color:var(--text2); white-space:pre-wrap; word-break:break-word; }

.report-wrap { position:relative; background:var(--surface); border:1px solid rgba(0,229,255,0.15); border-radius:var(--r-xl); padding:2.5rem 2.8rem; margin-top:0.5rem; overflow:hidden; }
.report-wrap::before { content:''; position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,rgba(0,229,255,0.6) 40%,rgba(123,97,255,0.6) 60%,transparent); }
.report-wrap::after { content:'REPORT'; position:absolute; top:1.8rem; right:2rem; font-family:var(--font-display); font-size:0.65rem; letter-spacing:0.3em; color:rgba(0,229,255,0.12); }
.report-label { font-family:var(--font-mono); font-size:0.6rem; letter-spacing:0.22em; text-transform:uppercase; color:var(--accent); margin-bottom:1.5rem; padding-bottom:0.75rem; border-bottom:1px solid rgba(0,229,255,0.1); display:flex; align-items:center; gap:0.6rem; }
.report-label::before { content:''; display:inline-block; width:6px; height:6px; background:var(--accent); border-radius:50%; box-shadow:0 0 8px var(--accent); }
.report-wrap p { font-size:0.95rem; font-weight:300; line-height:1.85; color:var(--text2); margin-bottom:1rem; }
.report-wrap h1 { font-family:var(--font-display); font-size:2.2rem; letter-spacing:0.05em; color:var(--text); margin:1.5rem 0 0.5rem; }
.report-wrap h2 { font-family:var(--font-display); font-size:1.5rem; letter-spacing:0.04em; color:var(--text); margin:1.4rem 0 0.5rem; }
.report-wrap h3 { font-size:1rem; font-weight:600; color:var(--accent); margin:1.2rem 0 0.4rem; }
.report-wrap strong { color:var(--text); font-weight:600; }
.report-wrap ul { padding-left:1.2rem; }
.report-wrap li { font-size:0.92rem; color:var(--text2); line-height:1.75; margin-bottom:0.3rem; }
.report-wrap code { font-family:var(--font-mono); font-size:0.8rem; background:rgba(0,229,255,0.08); color:var(--accent); padding:0.1rem 0.4rem; border-radius:4px; }

.critic-wrap { background:var(--surface); border:1px solid rgba(0,255,136,0.12); border-radius:var(--r-xl); padding:2rem 2.5rem; margin-top:1.5rem; position:relative; overflow:hidden; }
.critic-wrap::before { content:''; position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,rgba(0,255,136,0.5),transparent); }
.critic-label { font-family:var(--font-mono); font-size:0.6rem; letter-spacing:0.22em; text-transform:uppercase; color:#00ff88; margin-bottom:1.2rem; padding-bottom:0.6rem; border-bottom:1px solid rgba(0,255,136,0.1); display:flex; align-items:center; gap:0.6rem; }
.critic-label::before { content:''; display:inline-block; width:6px; height:6px; background:#00ff88; border-radius:50%; box-shadow:0 0 8px #00ff88; }
.score-block { display:inline-flex; align-items:baseline; gap:0.4rem; margin-bottom:1.2rem; padding:0.6rem 1.2rem; border-radius:var(--r-md); border:1px solid rgba(255,255,255,0.07); background:rgba(0,0,0,0.2); }
.score-num { font-family:var(--font-display); font-size:2.8rem; line-height:1; letter-spacing:0.03em; }
.score-denom { font-family:var(--font-mono); font-size:0.9rem; opacity:0.5; }
.score-verdict { font-family:var(--font-mono); font-size:0.65rem; letter-spacing:0.12em; text-transform:uppercase; margin-left:0.5rem; }

[data-testid="stDownloadButton"] button { background:transparent !important; color:var(--accent) !important; border:1px solid rgba(0,229,255,0.3) !important; border-radius:var(--r-sm) !important; font-family:var(--font-mono) !important; font-size:0.65rem !important; letter-spacing:0.12em !important; padding:0.5rem 1.2rem !important; transition:all 0.2s !important; box-shadow:none !important; width:auto !important; }
[data-testid="stDownloadButton"] button:hover { background:rgba(0,229,255,0.07) !important; border-color:var(--accent) !important; transform:none !important; }

details > summary { font-family:var(--font-mono) !important; font-size:0.65rem !important; color:var(--text3) !important; letter-spacing:0.1em !important; cursor:pointer !important; padding:0.5rem 0 !important; text-transform:uppercase !important; }
.stSpinner > div { color:var(--accent) !important; }
.stAlert { background:rgba(0,229,255,0.05) !important; border:1px solid rgba(0,229,255,0.2) !important; border-radius:var(--r-md) !important; color:var(--text2) !important; font-family:var(--font-body) !important; font-size:0.85rem !important; }

.footer { text-align:center; padding:3rem 0 1rem; border-top:1px solid var(--border); margin-top:4rem; }
.footer-text { font-family:var(--font-mono); font-size:0.58rem; color:var(--text3); letter-spacing:0.15em; text-transform:uppercase; }
.footer-text span { color:var(--accent); }
</style>
""", unsafe_allow_html=True)


def step_card(num, icon, title, state, desc=""):
    icons_map    = {"waiting":icon,"running":icon,"done":"✓","skipped":"—"}
    status_map   = {"waiting":("IDLE","st-wait"),"running":("RUNNING","st-run"),"done":("DONE","st-done"),"skipped":("SKIP","st-skip")}
    lbl, cls     = status_map.get(state, ("",""))
    card_cls     = {"running":"active","done":"done","skipped":"skip"}.get(state,"")
    d_html       = f"<div class='step-desc'>{desc}</div>" if desc else ""
    st.markdown(f"""
    <div class="step-card {card_cls}">
      <div class="step-row">
        <span class="step-index">{num}</span>
        <span class="step-icon">{icons_map[state]}</span>
        <span class="step-name">{title}</span>
        <span class="step-status {cls}">{lbl}</span>
      </div>{d_html}
    </div>""", unsafe_allow_html=True)


for key in ("results","running","done","doc_content","doc_name"):
    if key not in st.session_state:
        st.session_state[key] = ({} if key=="results" else "" if key in ("doc_content","doc_name") else False)

# ── Top nav ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="topbar-logo">
    <span class="topbar-logo-text">RESEARCH<span>MIND</span></span>
    <span class="topbar-tag">v2.0</span>
  </div>
  <div class="topbar-badges">
    <span class="badge badge-cyan">4 Agents</span>
    <span class="badge badge-purple">RAG · Web</span>
    <span class="badge badge-red">Live</span>
  </div>
</div>
""", unsafe_allow_html=True)

col_left, col_gap, col_right = st.columns([6, 0.4, 4])

with col_left:
    st.markdown("""
    <div class="hero">
      <div class="hero-kicker">Multi-Agent AI Research System</div>
      <div class="hero-title">DEEP<br><span class="line2">RESEARCH</span><br><span class="aw">ENGINE</span></div>
      <p class="hero-desc">Four specialized agents orchestrate in real time — searching the web, scraping sources, synthesizing knowledge, and self-critiquing to produce verified research reports.</p>
      <div class="hero-stats">
        <div class="stat-item"><span class="stat-num">4<span>×</span></span><span class="stat-label">AI Agents</span></div>
        <div class="stat-item"><span class="stat-num">RAG</span><span class="stat-label">Doc Mode</span></div>
        <div class="stat-item"><span class="stat-num">∞</span><span class="stat-label">Topics</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">Query Interface</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic or Question",
        placeholder="e.g.  What are the latest breakthroughs in fusion energy?",
        key="topic_input",
    )
    uploaded_file = st.file_uploader(
        "Upload document  ·  PDF · Image · TXT · CSV · MD  (optional)",
        type=["pdf","png","jpg","jpeg","webp","bmp","tiff","txt","md","csv"],
        key="file_upload",
        help="Upload any document or image — agents will use it as the primary source.",
    )
    if uploaded_file is not None:
        st.markdown(
            f'<div class="file-badge"><span class="file-badge-dot"></span>'
            f'📎 &nbsp;{uploaded_file.name} &nbsp;·&nbsp; {round(uploaded_file.size/1024,1)} KB — ready</div>',
            unsafe_allow_html=True,
        )
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("⚡  LAUNCH RESEARCH PIPELINE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chips-row"><span class="chip-label">Try →</span>', unsafe_allow_html=True)
    for ex in ["LLM agents 2025","CRISPR gene editing","Fusion energy progress","Quantum computing"]:
        st.markdown(f'<span class="chip">{ex}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown("""
    <div class="pipeline-header" style="margin-top:2.5rem">
      <div><div class="pipeline-title">PIPELINE</div><div class="pipeline-subtitle">Agent execution flow</div></div>
    </div>""", unsafe_allow_html=True)

    r = st.session_state.results
    has_doc = bool(st.session_state.doc_content)

    def s(step):
        steps = ["search","reader","writer","critic"]
        if step in r: return "done"
        if has_doc and step in ("search","reader"): return "skipped"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    if has_doc and k in ("search","reader"): continue
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01","🔍","Search Agent", s("search"), "Skipped — document uploaded" if has_doc else "Discovers recent web sources")
    step_card("02","📄","Reader Agent", s("reader"), "Skipped — content extracted" if has_doc else "Scrapes & parses top URLs")
    step_card("03","✍️","Writer Chain", s("writer"), "Synthesises a structured report")
    step_card("04","🧐","Critic Chain", s("critic"), "Scores & reviews the report")

    running = st.session_state.running
    done    = st.session_state.done
    status_color = "#00ff88" if done else ("var(--accent)" if running else "var(--text3)")
    status_text  = "● COMPLETE" if done else ("● RUNNING" if running else "○ IDLE")
    st.markdown(f"""
    <div style="margin-top:1.2rem;padding:0.8rem 1rem;background:rgba(0,0,0,0.2);border:1px solid var(--border);border-radius:var(--r-md);display:flex;align-items:center;gap:0.7rem;">
      <span style="font-family:var(--font-mono);font-size:0.58rem;color:var(--text3);letter-spacing:0.1em;text-transform:uppercase;">Status</span>
      <span style="font-family:var(--font-mono);font-size:0.65rem;color:{status_color};">{status_text}</span>
    </div>""", unsafe_allow_html=True)


# ── Trigger ───────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip() and uploaded_file is None:
        st.warning("Please enter a topic or upload a file first.")
    else:
        if uploaded_file is not None:
            with st.spinner("📂 Extracting file content…"):
                st.session_state.doc_content = extract_file_content(uploaded_file)
                st.session_state.doc_name    = uploaded_file.name
        else:
            st.session_state.doc_content = ""
            st.session_state.doc_name    = ""
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done    = False
        st.rerun()


# ── Execute ───────────────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    results   = {}
    topic_val = st.session_state.topic_input
    doc_text  = st.session_state.doc_content
    doc_name  = st.session_state.doc_name

    if doc_text:
        st.info(f"📎 Document mode active — **{doc_name}**")
        results["search"] = f"[Document upload mode]\nFile: {doc_name}"
        results["reader"] = doc_text
        with st.spinner("📚 Building vector embeddings…"):
            vectorstore = create_vector_store(doc_text)
        with st.spinner("🔍 Retrieving relevant context…"):
            relevant_context = retrieve_relevant_context(vectorstore, topic_val)
        with st.spinner("✍️ Generating answer from document…"):
            results["writer"] = rag_chain.invoke({"question": topic_val, "context": relevant_context})
    else:
        with st.spinner("🔍 Search Agent scanning the web…"):
            search_agent = build_search_agent()
            sr = search_agent.invoke({"messages":[("user",f"Find recent, reliable and detailed information about: {topic_val}")]})
            results["search"] = sr["messages"][-1][1]
            st.session_state.results = dict(results)

        with st.spinner("📄 Reader Agent scraping sources…"):
            urls = re.findall(r'https?://[^\s]+', results.get("search",""))
            if urls:
                try:    results["reader"] = scrape_url.invoke(urls[0])
                except Exception as e: results["reader"] = f"Scrape error: {str(e)}"
            else: results["reader"] = "No valid URL found."
            st.session_state.results = dict(results)

        with st.spinner("✍️ Writer crafting the report…"):
            results["writer"] = writer_chain.invoke({
                "topic": topic_val,
                "research": f"TOPIC:\n{topic_val}\n\nSEARCH RESULTS:\n{results.get('search','')}\n\nSCRAPED CONTENT:\n{results.get('reader','')}",
            })
            st.session_state.results = dict(results)

    with st.spinner("🧐 Critic reviewing…"):
        results["critic"] = critic_chain.invoke({"report": results.get("writer","No report generated")})

    st.session_state.results = dict(results)
    st.session_state.running = False
    st.session_state.done    = True
    st.rerun()


# ── Results ───────────────────────────────────────────────────────────────────
r = st.session_state.results
if r:
    st.markdown('<div class="h-divider"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="results-heading">OUTPUT</div>
    <div class="results-meta">Generated · {time.strftime("%H:%M:%S")} · {len(r)} stages complete</div>
    """, unsafe_allow_html=True)

    if st.session_state.doc_content:
        st.markdown(
            f'<div class="doc-banner">📎 &nbsp; Document mode &nbsp;·&nbsp; {st.session_state.doc_name} &nbsp;·&nbsp; {len(st.session_state.doc_content):,} chars extracted</div>',
            unsafe_allow_html=True,
        )

    raw1, raw2 = st.columns(2)
    with raw1:
        if "search" in r:
            with st.expander("🔍 Search output (raw)"):
                st.markdown(f'<div class="raw-panel"><div class="raw-panel-title">Search Agent</div><div class="raw-content">{r["search"][:2000]}</div></div>', unsafe_allow_html=True)
    with raw2:
        if "reader" in r:
            lbl = "📎 Document content" if st.session_state.doc_content else "📄 Scraped content"
            with st.expander(f"{lbl} (raw)"):
                preview = r["reader"][:2000]
                ellipsis = "…" if len(r["reader"]) > 2000 else ""
                st.markdown(f'<div class="raw-panel"><div class="raw-panel-title">Reader Agent</div><div class="raw-content">{preview}{ellipsis}</div></div>', unsafe_allow_html=True)

    if "writer" in r:
        st.markdown('<div class="report-wrap"><div class="report-label">Final Research Report</div>', unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="⬇  DOWNLOAD REPORT (.md)",
            data=r["writer"],
            file_name=f"researchmind_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        feedback  = r["critic"]
        score_html = ""
        match = re.search(r"Score:\s*(\d+)/10", feedback)
        if match:
            score   = int(match.group(1))
            c       = "#00ff88" if score >= 8 else "#ffd166" if score >= 6 else "#ff4d6d"
            verdict = "Excellent" if score >= 8 else "Good" if score >= 6 else "Needs Work"
            score_html = (f'<div class="score-block"><span class="score-num" style="color:{c}">{score}</span>'
                          f'<span class="score-denom">/10</span>'
                          f'<span class="score-verdict" style="color:{c}">{verdict}</span></div>')
            feedback = re.sub(r"Score:\s*\d+/10", "", feedback)

        st.markdown(f'<div class="critic-wrap"><div class="critic-label">Critic Analysis</div>{score_html}', unsafe_allow_html=True)
        st.markdown(feedback)
        st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  <div class="footer-text">ResearchMind &nbsp;·&nbsp; <span>Multi-Agent AI</span> &nbsp;·&nbsp; LangChain · Streamlit · RAG</div>
</div>
""", unsafe_allow_html=True)
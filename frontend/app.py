import json
import datetime
from urllib.parse import urlparse

import requests
import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Seedling Labs — AI GitHub Issue Assistant",
    page_icon="🌱",
    layout="wide",
)

# -----------------------------
# GITHUB DARK MODE CSS
# -----------------------------
st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    background-color: #0d1117 !important;
    color: #c9d1d9 !important;
}

/* Typography */
h1, h2, h3, h4, h5, h6, div, p, span, label {
    color: #c9d1d9 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}

/* Gradient title */
.gradient-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #4ade80, #22d3ee);
    -webkit-background-clip: text;
    color: transparent !important;
}

/* INPUTS */
input, textarea, select,
.stTextInput > div > div > input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
    border-radius: 6px !important;
}

/* BUTTONS */
.stButton button {
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
    border-radius: 6px !important;
    padding: 6px 14px !important;
}
.stButton button:hover {
    background-color: #30363d !important;
    border-color: #8b949e !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton button {
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
}
.stDownloadButton button:hover {
    background-color: #30363d !important;
}

/* NUMBER INPUT SPINNERS */
.stNumberInput button {
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
}
.stNumberInput button:hover {
    background-color: #30363d !important;
}

/* CODE BLOCKS */
pre, code, .stCodeBlock {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #58a6ff !important;
    border-radius: 6px !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d !important;
}
[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}

/* SIDEBAR BUTTONS */
[data-testid="stSidebar"] button {
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
}
[data-testid="stSidebar"] button:hover {
    background-color: #30363d !important;
}

/* ALERT BANNERS */
.stAlert {
    background-color: #0d4429 !important;
    border: 1px solid #238636 !important;
}

/* Thick divider */
hr.thick {
    border: none;
    border-top: 3px solid #30363d !important;
    margin: 24px 0;
}

/* Label pills */
.pill {
    display:inline-block;
    padding:4px 10px;
    margin-right:6px;
    border-radius:20px;
    background-color:#21262d;
    border:1px solid #30363d;
    color:#c9d1d9;
    font-size:0.80rem;
}

/* Fade animation */
.fade-in {
    animation: fadeIn 0.35s ease-in-out;
}
@keyframes fadeIn {
    from {opacity:0; transform:translateY(6px);}
    to   {opacity:1; transform:translateY(0);}
}

/* Skeleton Loader */
.skeleton {
    background: linear-gradient(90deg,#30363d,#484f58,#30363d);
    background-size:200% 100%;
    animation: shimmer 1.3s infinite;
    border-radius: 6px;
}
@keyframes shimmer {
    0% {background-position:-200% 0;}
    100%{background-position:200% 0;}
}

/* Hide theme selector */
[data-testid="stSettingsDialog"] label[for="theme"],
[data-testid="stSettingsDialog"] select {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown("<h1 class='gradient-title'>🌱 Seedling Labs — AI GitHub Issue Assistant</h1>", unsafe_allow_html=True)
st.write("Enter a GitHub Issue → Get an LLM-powered structured analysis.")

# -----------------------------
# SESSION
# -----------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# -----------------------------
# HELPERS
# -----------------------------
def parse_owner_repo(url: str):
    try:
        parsed = urlparse(url)
        if parsed.netloc != "github.com":
            return None
        owner, repo = parsed.path.strip("/").split("/")[:2]
        return f"{owner}/{repo}"
    except Exception:
        return None

def priority_badge(score):
    score = str(score or "")
    digit = score[0] if score and score[0].isdigit() else "?"
    mapping = {
        "5": ("#dc2626", "🔥 Critical"),
        "4": ("#ea580c", "⚡ High"),
        "3": ("#ca8a04", "⬆ Medium"),
        "2": ("#16a34a", "⬇ Low"),
        "1": ("#2563eb", "ℹ Trivial"),
    }
    color, label = mapping.get(digit, ("#6b7280", "❔ Unknown"))
    return f"<span class='pill' style='border-color:{color};color:{color};'>{label} ({score})</span>"

def issue_type_badge(t):
    t = (t or "other").lower()
    mapping = {
        "bug": ("#ef4444", "❌ Bug"),
        "feature_request": ("#22c55e", "✨ Feature"),
        "documentation": ("#3b82f6", "📘 Docs"),
        "question": ("#a855f7", "❓ Question"),
    }
    color, label = mapping.get(t, ("#6b7280", "📦 Other"))
    return f"<span class='pill' style='border-color:{color};color:{color};'>{label}</span>"

def label_chip(l):
    return f"<span class='pill'>{l}</span>"

def detect_missing_info(body: str):
    text = (body or "").lower()
    out = []
    if "step" not in text and "repro" not in text:
        out.append("Missing reproduction steps.")
    if "expected" not in text or "actual" not in text:
        out.append("Missing expected/actual behavior.")
    if all(k not in text for k in ["env", "version", "os"]):
        out.append("Missing environment info.")
    if all(k not in text for k in ["log", "traceback", "error"]):
        out.append("Missing logs.")
    return out

def suggest_next_steps(t, p):
    t = (t or "").lower()
    out = []
    if t == "bug":
        out += ["Reproduce bug.", "Add failing tests.", "Identify minimal failing case."]
    elif t == "feature_request":
        out += ["Define acceptance criteria.", "Estimate effort."]
    elif t == "documentation":
        out += ["Update docs.", "Add examples."]
    elif t == "question":
        out += ["Provide explanation.", "Link documentation."]
    else:
        out.append("Request more details.")
    if str(p).startswith(("4", "5")):
        out.append("Escalate to core maintainer.")
    return out

def heuristic_confidence(prio, comments: int):
    base = 0.7
    if str(prio).startswith(("4", "5")):
        base += 0.1
    if comments >= 5:
        base += 0.05
    return min(base, 0.95)

# -----------------------------
# BACKEND API — HIDDEN HERE
# -----------------------------
BACKEND_URL = "http://localhost:8000"   # Hidden backend URL

# -----------------------------
# API CALLS
# -----------------------------
@st.cache_data(show_spinner=False)
def call_backend(repo, issue):
    r = requests.post(
        f"{BACKEND_URL}/analyze",
        json={"repo_url": repo, "issue_number": issue},
        timeout=60,
    )
    return r.status_code, r.text

@st.cache_data(show_spinner=False)
def fetch_metadata(repo, issue):
    owner = parse_owner_repo(repo)
    if not owner:
        return None
    r = requests.get(f"https://api.github.com/repos/{owner}/issues/{issue}")
    if r.status_code != 200:
        return None
    j = r.json()
    return {
        "state": j.get("state", ""),
        "comments": j.get("comments", 0),
        "user": j.get("user", {}).get("login", ""),
        "created_at": j.get("created_at", ""),
        "updated_at": j.get("updated_at", ""),
        "body": j.get("body", ""),
        "html_url": j.get("html_url", ""),
        "repo_html_url": f"https://github.com/{owner}",
    }

# -----------------------------
# SIDEBAR HISTORY
# -----------------------------
with st.sidebar:
    st.markdown("### 🕒 Recent Runs")
    if not st.session_state["history"]:
        st.caption("No recent runs.")
    else:
        for i, h in enumerate(reversed(st.session_state["history"][-8:])):
            label = f"{h['repo_short']} #{h['issue_number']}"
            if st.button(label, key=f"history_{i}"):
                st.session_state.update(
                    repo_url=h["repo_url"],
                    issue_number=h["issue_number"],
                )
                st.rerun()

# -----------------------------
# INPUT FORM (NO BACKEND FIELD)
# -----------------------------
st.markdown("<h3 class='gradient-title'>🛠 Issue Input</h3>", unsafe_allow_html=True)

repo_default = st.session_state.get("repo_url", "https://github.com/facebook/react")
issue_default = st.session_state.get("issue_number", 1)

with st.form("issue_form"):
    repo_url = st.text_input("Repository URL", repo_default)
    issue_number = st.number_input("Issue Number", min_value=1, value=int(issue_default))

    col1, col2 = st.columns(2)
    with col1:
        submitted = st.form_submit_button("🔍 Analyze")
    with col2:
        example = st.form_submit_button("✨ Load React Example")

if example:
    st.session_state["repo_url"] = "https://github.com/facebook/react"
    st.session_state["issue_number"] = 1
    st.rerun()

if not submitted:
    st.stop()

# -----------------------------
# SKELETON LOADER
# -----------------------------
loader = st.empty()
with loader.container():
    st.markdown("#### ⏳ Preparing analysis…")
    sk1, sk2 = st.columns([2, 1])
    with sk1:
        st.markdown("<div class='skeleton' style='height:18px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='skeleton' style='height:16px;width:70%;margin-top:6px;'></div>", unsafe_allow_html=True)
    with sk2:
        st.markdown("<div class='skeleton' style='height:60px;'></div>", unsafe_allow_html=True)

with st.spinner("Analyzing..."):
    status, raw = call_backend(repo_url, int(issue_number))

loader.empty()

if status != 200:
    st.error(f"Backend error {status}:\n{raw}")
    st.stop()

try:
    data = json.loads(raw)
except Exception:
    st.error("Invalid JSON returned by backend.")
    st.text(raw)
    st.stop()

meta = fetch_metadata(repo_url, issue_number) or {}
st.success("Analysis complete! 🎉")

owner_repo = parse_owner_repo(repo_url) or "unknown_repo"

st.session_state["history"].append(
    {
        "repo_url": repo_url,
        "repo_short": owner_repo,
        "issue_number": issue_number,
    }
)

# -----------------------------
# MAIN OUTPUT
# -----------------------------
st.markdown("<hr class='thick'>", unsafe_allow_html=True)
st.markdown("<h3 class='gradient-title'>📄 Issue Analysis</h3>", unsafe_allow_html=True)

# Summary
st.subheader("Summary")
st.write(data.get("summary", ""))

# Type / Priority / Labels
c1, c2, c3 = st.columns([1, 1.2, 2])
with c1:
    st.caption("Type")
    st.markdown(issue_type_badge(data.get("type", "")), unsafe_allow_html=True)
with c2:
    st.caption("Priority")
    st.markdown(priority_badge(data.get("priority_score", "")), unsafe_allow_html=True)
with c3:
    st.caption("Labels")
    chips = "".join(label_chip(l) for l in data.get("suggested_labels", []))
    st.markdown(chips, unsafe_allow_html=True)

# Impact
st.subheader("⚠ Potential Impact")
st.write(data.get("potential_impact", ""))

# --------------------------
# 📦 JSON Output
# --------------------------
st.subheader("📦 JSON Output")
pretty = json.dumps(data, indent=2)
st.code(pretty)

colA, colB = st.columns(2)

with colA:
    if st.button("📋 Copy JSON"):
        st.markdown(
            f"<script>navigator.clipboard.writeText(`{pretty}`)</script>",
            unsafe_allow_html=True,
        )
        st.info("Copied!")

with colB:
    st.download_button(
        "⬇ Download JSON",
        pretty,
        file_name=f"issue_{owner_repo.replace('/', '_')}.json",
        mime="application/json",
    )

# --------------------------
# ⭐ Detailed JSON Export
# --------------------------
detailed_output = {
    "issue": {
        "repo": owner_repo,
        "number": issue_number,
        "title": data.get("summary", ""),
        "body": meta.get("body", ""),
        "comments_count": meta.get("comments", 0),
        "created_at": meta.get("created_at", ""),
        "updated_at": meta.get("updated_at", ""),
        "state": meta.get("state", ""),
        "author": meta.get("user", ""),
    },
    "analysis": {
        "summary": data.get("summary", ""),
        "type": data.get("type", ""),
        "priority_score": data.get("priority_score", ""),
        "labels": data.get("suggested_labels", []),
        "impact": data.get("potential_impact", ""),
        "confidence": heuristic_confidence(
            data.get("priority_score", ""),
            meta.get("comments", 0),
        ),
        "missing_info": detect_missing_info(meta.get("body", "")),
        "next_steps": suggest_next_steps(
            data.get("type", ""),
            data.get("priority_score", ""),
        ),
    },
    "system": {
        "model_used": "gpt-4.1",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    },
}



with st.expander("📄 Show Detailed JSON Preview"):
    st.code(json.dumps(detailed_output, indent=2), language="json")

st.download_button(
    "⬇ Download Detailed JSON",
    json.dumps(detailed_output, indent=2),
    file_name=f"detailed_{owner_repo.replace('/', '_')}_issue_{issue_number}.json",
    mime="application/json",
)

st.markdown("<hr class='thick'>", unsafe_allow_html=True)

# -----------------------------
# ADDITIONAL INSIGHTS
# -----------------------------
st.markdown("<h3 class='gradient-title'>🔍 Additional Insights</h3>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("#### 🗂 Metadata")
    st.write(f"**State:** {meta.get('state','')}")
    st.write(f"**Author:** @{meta.get('user','')}")
    st.write(f"**Comments:** {meta.get('comments')}")
    st.write(f"**Created:** {meta.get('created_at')}")
    st.write(f"**Updated:** {meta.get('updated_at')}")

with col2:
    st.markdown("#### 🔗 GitHub Links")
    st.markdown(f"- [Open Issue]({meta.get('html_url')})")
    st.markdown(f"- [Repository]({meta.get('repo_html_url')})")
    st.markdown(f"- [All Issues]({meta.get('repo_html_url')}/issues)")

with col3:
    st.markdown("#### 🧠 Confidence")
    conf = heuristic_confidence(data.get("priority_score", ""), meta.get("comments", 0))
    st.metric("Estimated", f"{conf:.2f}")

with col4:
    st.markdown("#### ⚠ Missing Info")
    for m in detect_missing_info(meta.get("body", "")):
        st.write(f"- {m}")
    st.markdown("#### 🚀 Next Steps")
    for m in suggest_next_steps(data.get("type", ""), data.get("priority_score", "")):
        st.write(f"- {m}")

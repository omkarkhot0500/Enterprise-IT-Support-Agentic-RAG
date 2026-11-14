# Interview Intro of Project

One of my key projects is the Enterprise IT Support Agentic RAG, an AI-powered assistant that answers employees' IT questions using company documents.
I built it using Python, FastAPI, LangGraph, Pinecone, Groq, Hugging Face embeddings, and Tavily.
The main feature is that the agent first retrieves information from the private knowledge base and grades the information before generating an answer.
If the evidence is weak, it searches the web, rewrites the query, and retries if necessary. 
If it still cannot find reliable information, it returns an insufficient-evidence response.
I also implemented document ingestion using chunking and embeddings, a protected document-upload endpoint, and SQLite audit logging to record the agent's decisions.


# Read

One of my key projects is the Enterprise IT Support Agentic RAG Copilot, an AI-powered IT support assistant that helps employees find answers to their IT-related questions.

The problem I wanted to solve was that employees in a company often need to search through multiple documents or contact the IT support team to resolve common problems. I wanted to build an assistant that could answer their questions using the company's private IT documents instead of relying only on the LLM's existing knowledge.

I built it using Python, FastAPI, LangGraph, Pinecone, Hugging Face embeddings, Groq, and Tavily. I used FastAPI to build the backend APIs, LangGraph to manage the agent workflow, Pinecone to store and retrieve document embeddings, Groq to run the LLM, and Tavily for web search.

What makes this project interesting is that I didn't implement just a basic RAG pipeline. I built an agentic RAG workflow that can evaluate the retrieved evidence and decide what to do next.

When an employee asks a question, the agent first searches the private knowledge base. If the retrieved information is relevant, it generates an answer using that evidence. If the evidence is weak, it falls back to web search using Tavily. If the web evidence is also insufficient, it rewrites the query and retries the retrieval process. If it still cannot find reliable evidence, it returns an insufficient-evidence response instead of guessing.

For document ingestion, I implemented a pipeline that loads PDF, TXT, Markdown, and DOCX files, splits them into smaller chunks, generates embeddings, and stores them in Pinecone. I also added an admin-key-protected API for uploading documents.

For monitoring and debugging, I implemented SQLite audit logging, which records the user's question, the final source information, and the agent's decision trace.

The most important part of this project is the LangGraph state machine, where the workflow uses routing, evidence grading, conditional branching, and query rewriting to decide how to answer a question.

Overall, this project helped me gain practical experience with Agentic AI, RAG, LangGraph workflows, vector databases, embeddings, API development, document processing, and audit logging.


# All About the Agentic RAG Workflow
How the agent works in my project
In my project, I use LangGraph to control the entire question-answering workflow.
A normal RAG application generally retrieves relevant documents and passes them to an LLM to generate an answer. My application adds evidence grading, conditional routing, web fallback, and query rewriting.
When an employee asks a question, the router first decides whether it is an IT-related question that requires knowledge-base retrieval or a direct question such as a greeting.
If the question requires retrieval, the application searches Pinecone for the most relevant document chunks. The LLM then grades the retrieved evidence as either good or weak.
If the evidence is good, the agent generates an answer using the private knowledge base.
If the evidence is weak, the agent searches the web using Tavily and grades the web results. If the web evidence is good, it generates an answer from those results.
If both the private and web evidence are weak, the agent rewrites the query and retries the workflow. I configured max_retries = 1, so the agent allows one query rewrite and retry. If the evidence remains weak after that retry, it returns an insufficient-evidence response.
How the workflow works, step by step
1. route_question() classifies the user's question as kb or direct.
2. route_after_router() chooses the appropriate path.
3. retrieve_kb() retrieves up to four relevant chunks from Pinecone.
4. grade_kb() checks whether the private evidence is good or weak.
5. If the evidence is good, generate_from_kb() generates the answer.
6. If the evidence is weak, search_web() retrieves web results using Tavily.
7. grade_web() evaluates the web evidence.
8. If the web evidence is good, generate_from_web() generates the answer.
9. If the evidence is weak and a retry remains, rewrite_query() improves the query and sends the workflow back to knowledge-base retrieval.
10. If the evidence is still weak and no retry remains, insufficient() returns a safe response.
Interview answer
I implemented the agentic RAG workflow using LangGraph. The workflow contains nodes for routing, retrieval, evidence grading, web search, query rewriting, and answer generation. Conditional edges decide which node runs next based on the LLM's decisions. The system searches the private knowledge base first, falls back to web search if the evidence is weak, retries once with a rewritten query, and returns an insufficient-evidence response if it still cannot find reliable information.



# Q and A

Q1. Tell me about your Enterprise IT Support Agentic RAG project.

"I built an Enterprise IT Support Agentic RAG to help employees find accurate answers to internal IT-related questions using company documentation.

The problem I wanted to solve was that employees often create repetitive support tickets because they cannot find the correct information in internal documents. Traditional keyword search can return irrelevant results, and a basic LLM chatbot may generate answers that are not supported by the company's documentation.

To solve this, I used Retrieval-Augmented Generation, or RAG, with an agentic workflow built using LangGraph. I used Pinecone as the vector database, Hugging Face embeddings for semantic search, Groq to run the language model, Tavily for external web search when necessary, and FastAPI to expose the workflow through APIs.

The main feature is that the agent first retrieves information from the private knowledge base and grades the information before generating an answer.
If the evidence is weak, it searches the web, rewrites the query, and retries if necessary. 
If it still cannot find reliable information, it returns an insufficient-evidence response.
I also implemented document ingestion using chunking and embeddings, a protected document-upload endpoint, and SQLite audit logging to record the agent's decisions.


Q2. What is Agentic RAG, and how is it different from normal RAG?
Interview answer:

"Traditional RAG generally follows a predefined retrieval-and-generation pipeline: retrieve documents, pass them to the LLM, and generate an answer.

Agentic RAG adds decision-making to that workflow. Instead of always following one fixed path, the system evaluates intermediate results and decides what action to take next.


Q3. Why did you use LangGraph instead of a simple LangChain chain?
Interview answer:

"I chose LangGraph because my workflow has conditional branches and retry logic. A simple sequential chain is suitable when the steps always run in the same order, but my system needs to decide what to do based on retrieval quality.

For example, after retrieving private documents, the workflow grades the evidence. Depending on the result, it can generate an answer, use external search, or rewrite the query and retry. It also needs to stop when the retry limit is reached.

LangGraph lets me represent these operations as nodes, connect them with edges, and use conditional edges to control execution. Its shared state allows each node to read the current query, retrieved documents, evidence assessment, and retry information." 

Know these three terms for interviews:
- State: The data shared across the workflow, such as the question, documents, evidence grade, retry count, and final answer.
- Node: A function that performs a task, such as retrieval, grading, query rewriting, or answer generation.
- Edge: A connection that determines which node executes next. A conditional edge selects the next step based on the current state.


Q4. What is the difference between LangChain and LangGraph?
Interview answer:

"LangChain provides components for building LLM applications, such as model integrations, prompts, retrievers, and tool integrations. LangGraph focuses on orchestrating workflows that require state, conditional routing, and loops.

In my project, LangChain-compatible components can handle tasks such as calling the LLM or working with retrieval components, while LangGraph controls the overall flow of the application, including evidence grading, fallback routing, and retry logic."

The key distinction is that LangChain supplies useful building blocks, while LangGraph controls the stateful workflow. They can be used together.

Q5. How does the complete RAG pipeline work in your project?
Interview answer:

"My RAG system has two main pipelines: document ingestion and question answering.

During ingestion, I load the company documents, split them into smaller chunks using recursive text splitting, generate embeddings for those chunks, and index them in Pinecone.

During question answering, I take the user's question, generate its embedding using the compatible embedding model, and search Pinecone for semantically similar chunks. I then evaluate the retrieved evidence. If it is sufficient, the LLM generates a grounded answer. Otherwise, the workflow can try external search or query rewriting, subject to the retry limit."


Q5. What are embeddings, and why do you need them?
Interview answer:

"Embeddings are numerical vectors that represent the semantic meaning of text. Text with similar meanings tends to have vectors that are close to each other in the embedding space.

In my project, I use a Hugging Face embedding model to convert document chunks and user questions into vectors. Pinecone uses those vectors to find semantically relevant document chunks.

For example, a user might ask, 'I can't access the company network from home,' while the document says, 'Remote VPN connectivity troubleshooting.' The wording is different, but the meanings are related, so semantic retrieval can help find the relevant document."

Cross-question: Are embeddings generated by Groq?

Not in the architecture described in your resume. Hugging Face Embeddings handle vector generation, Pinecone handles vector search, and Groq provides access to the language model for reasoning and answer generation.

Cross-question: Do you need the exact same embedding model for documents and queries?

You generally need a compatible embedding model and configuration. The document chunks and user queries must be represented in the same compatible vector space, with matching dimensions and appropriate preprocessing.


Q6. What is recursive chunking, and why did you use it?
Interview answer:

"Recursive chunking splits a long document into smaller pieces while attempting to preserve meaningful text boundaries. Instead of blindly splitting text at an arbitrary character position, the splitter tries larger structural separators first and then falls back to smaller separators when necessary.

I used recursive chunking because company documents can contain multiple topics. If I store an entire document as one vector, retrieving it may provide too much irrelevant information. Smaller chunks help retrieve the specific section that answers a user's question."

For example, a document might contain sections about VPN setup, email configuration, and printer troubleshooting. Chunking makes it easier to retrieve only the relevant section.

Cross-question: What happens if chunks are too small?

They may lose important context. A chunk containing only "restart it" is not useful if the preceding text explains what "it" refers to.

Cross-question: What happens if chunks are too large?

They may include unrelated information, reduce retrieval precision, and consume more of the LLM's context window.

Cross-question: Why use chunk overlap?

Overlap preserves context around chunk boundaries. For example, if a troubleshooting instruction starts near the end of one chunk, the next chunk can retain part of that context. The exact chunk size and overlap should be tuned to your documents and evaluated rather than guessed.


Q10. What is Pinecone, and why did you choose it?
Interview answer:

"Pinecone is a managed vector database designed to store and search vector embeddings. I used it to index embeddings of company document chunks and retrieve the most semantically relevant chunks when a user asks a question.

It allows me to perform similarity searches without loading and comparing every document manually in my application code. I can also associate metadata with vectors to identify their source documents and apply supported filters where needed." 

Cross-question: Why not use MongoDB or SQLite for vector search?

MongoDB and SQLite are useful for application data, metadata, and structured records. Pinecone is specifically designed for vector retrieval and provides managed vector-search capabilities. Some other databases also support vector search, so Pinecone is a design choice rather than the only possible solution.

Cross-question: What happens if Pinecone returns irrelevant documents?

The evidence grader can identify that the retrieved material does not adequately support the question. The workflow can then use query rewriting or external search, within its configured limits. However, a grader is not perfect, so retrieval quality still needs testing and evaluation.



Q11. What does top_k mean in vector search?
Interview answer:

"top_k determines how many of the most similar vector matches are returned for a query. For example, if top_k is 5, the search returns up to five nearest matches, subject to the query and available data.

A very small value can miss relevant evidence. A very large value can introduce irrelevant content and increase prompt size and latency. I would tune top_k based on retrieval evaluation."

Cross-question: Does a high similarity score guarantee a correct answer?

No. Similarity indicates how closely the vectors match according to the retrieval metric; it does not prove that the document is factually correct or that it answers the question. That is why the project includes an evidence-grading stage.


Q12. What metadata would you store with each chunk?
Interview answer:

Meta data
{
    "id": "vpn_001_chunk_0",
    "values": [0.23, -0.17, 0.82, ...],
    "metadata": {
        "filename": "VPN_Guide.pdf",
        "document_id": "vpn_001",
        "chunk_index": 0,
        "text": "To connect to the company VPN, open Cisco AnyConnect..."
    }
}


Q13. What is evidence grading, and how does it work in your project?
Interview answer:

"Evidence grading is the step where the workflow evaluates whether the retrieved documents are relevant and sufficient to answer the user's question.

Retrieval alone does not guarantee that the correct information was found. Pinecone may return semantically similar content that does not actually answer the question.

In my project, the workflow uses an evaluation step to decide whether the retrieved evidence is strong enough to proceed with answer generation or whether it needs another retrieval strategy.

This makes the workflow more reliable than blindly passing the top search results to the LLM."

Example:

User asks: "What is the company's approved VPN client?"

Retrieved document: "Employees must connect through the company VPN when working remotely."

This document is related to VPN usage, but it does not identify the approved client. The evidence should be considered insufficient for that specific question.

Cross-question: Is evidence grading the same as checking the similarity score?

No. A similarity score measures vector similarity. Evidence grading evaluates whether the retrieved content is actually LLM call.



Q14. How do you prevent hallucinations in your project?
Interview answer:

"I designed the workflow to reduce hallucinations by grounding answers in retrieved evidence rather than relying only on the LLM's pretrained knowledge.

First, the system retrieves relevant private documents. Next, it evaluates the retrieved evidence before generating an answer. If the evidence is insufficient, it can try external web search or rewrite the query and retry retrieval. I also limit retries to avoid an endless loop.

If the available evidence is still insufficient, the system returns a controlled fallback response instead of pretending it knows the answer."

Cross-question: Can you guarantee zero hallucinations?

"No. An LLM-based system cannot guarantee zero hallucinations simply because it uses RAG. Retrieval can miss the correct document, the evidence grader can make mistakes, and the model can misinterpret its context.

My approach reduces the risk through retrieval, evidence evaluation, bounded retries, and fallback behavior. In a production system, I would also evaluate answer correctness, source support, and retrieval quality using a representative test dataset."



Q15. What happens when private documents don't contain the answer?
Interview answer:

"My workflow can fall back to Tavily for external web search when the internal evidence is insufficient. This gives the system another potential source of information instead of forcing it to answer from incomplete internal documentation.

The external results must still be evaluated before using them. If the available evidence remains insufficient after the retry logic, the system returns a controlled response indicating that it could not find enough information."

Cross-question: Why not always search the web first?

"Internal company documentation should generally be the preferred source for company-specific procedures because it represents the organization's own policies. External websites may describe generic practices that conflict with the company's approved process. I use web search as a fallback rather than treating it as automatically more authoritative."

Cross-question: What if an external website contradicts an internal document?

A sensible enterprise policy is to prefer the authoritative, current internal policy for company-specific procedures, flag the conflict when appropriate, and avoid silently replacing company policy with an external suggestion. External sources should be used only within the application's defined trust rules.


Q16. What is query rewriting, and why do you need it?
Interview answer:

"Query rewriting means transforming the user's original question into a clearer or more retrieval-friendly query without changing its intended meaning.

For example, a user may ask, 'VPN is not working from home. What should I do?' A rewritten query might be 'company remote VPN connection troubleshooting steps.'

The rewritten query can improve retrieval when the original wording doesn't closely match the language used in the documents. In my project, query rewriting is part of the recovery workflow when the existing evidence is insufficient."

Cross-question: Does rewriting always improve retrieval?

No. It can introduce assumptions or remove important details. A good implementation preserves the user's intent, and the revised query should be evaluated by retrieving and grading the resulting evidence.


Q17. Why do you need retry logic? How do you prevent an infinite loop?
Interview answer:

"Retry logic allows the workflow to recover when the first retrieval attempt doesn't produce sufficient evidence. Instead of immediately giving up, it can rewrite the query and attempt retrieval again.

However, retrying indefinitely would increase latency and API costs without guaranteeing a better result. I therefore use a bounded retry strategy. In my implementation, the retry limit is one additional attempt.

If the workflow still cannot obtain sufficient evidence, it stops retrying and returns the fallback response."

The important distinction is that retry logic is not a guarantee of correctness. It is a bounded attempt to improve the evidence.

Cross-question: Why not retry five or ten times?

Each attempt can involve embedding generation, vector search, LLM calls, and possibly external search. More attempts increase latency and cost. The retry limit should be chosen using evaluation results and the application's response-time requirements.









A. Architecture and Workflow
Q1. Complete RAG architecture — from query to answer?

"When a user hits /api/chat, FastAPI validates the request and calls ask(), which initializes an AgentState and invokes a compiled LangGraph. First, route_question decides — via an LLM with structured output — whether it's a casual message (direct answer) or an IT question needing retrieval. IT questions go to retrieve_kb, which embeds the query and pulls the top-4 chunks from Pinecone. grade_kb then has an LLM judge whether that evidence is sufficient — 'good' goes straight to generate_from_kb; 'weak' falls back to search_web using Tavily. Web results get graded too: 'good' generates an answer, 'weak' triggers rewrite_query, which rewords the question and loops back to KB retrieval — once max retries is hit, we return a fixed 'contact IT help desk' message instead of guessing. Finally we return the answer with source_used, a step-by-step trace, and citations, and we audit-log the question, route, and trace to SQLite." workflow.py:237-256 routes.py:25-43

Q2. What's in your LangGraph state?

"AgentState is a TypedDict with 11 fields. question is the original ask — never mutated, so graders always evaluate against user intent. current_query is what actually gets searched — rewrite_query updates it on retries. kb_docs and web_results hold the evidence each grader consumes. kb_grade and web_grade are the good/weak signals that drive conditional routing. retry_count bounds the loop, answer/source_used/citations are set by whichever terminal node ran, and trace is an append-only log every node writes to — that's what makes the whole decision path auditable. Each node returns a partial dict and LangGraph merges it, so nodes are decoupled." state.py:26-37 workflow.py:16-17

Q3. How does routing decide LLM-only vs. knowledge base?

"There's a dedicated route_question node that calls the LLM with structured output constrained to kb or direct. The prompt is explicit: 'direct' is only for greetings, thanks, casual chat; anything touching IT policy, VPN, passwords, MFA, troubleshooting goes 'kb'. Two deliberate design choices: first, structured output means the route is machine-readable, not free text to parse; second, on any exception we default to 'kb' — we fail toward grounded retrieval, never toward an ungrounded answer." workflow.py:62-77 workflow.py:81-82

Q4. Responsibilities of retrieval, grading, rewriting, generation nodes?

"They form a retrieve → evaluate → act loop. retrieve_kb runs current_query against the Pinecone retriever and stores chunks — importantly it uses current_query, not question, so rewrites actually take effect. grade_kb is an LLM-with-structured-output that reads every chunk and answers 'can this evidence answer the question confidently?' — binary good/weak. rewrite_query rephrases the question with better technical keywords and increments retry_count. The generation nodes — generate_from_kb, generate_from_web, direct_answer, insufficient — are the only ones that write answer, and they're all grounded: KB and web answers are prompted to use only the provided evidence and cite sources." workflow.py:86-88 workflow.py:163-173

B. Vector Search and Retrieval
Q5. Role of Pinecone, embedding, storage, retrieval?

"Pinecone is our managed vector store for the private KB. On ingestion, uploaded files — PDF, TXT, MD, DOCX — are loaded, chunked, and upserted through LangChain's PineconeVectorStore. Embeddings come from HuggingFace all-MiniLM-L6-v2, a 384-dim local model — so embedding is free and private. ensure_index creates a serverless cosine index on AWS if it doesn't exist. At query time, get_retriever wraps it with k=4 in namespace company-it-kb. One thing I'd change: ensure_index currently deletes and recreates the index if the embedding dimension doesn't match — fine in dev, dangerous in production." vectorstore.py:48-54 vectorstore.py:69-89 vectorstore.py:110-112

Q6. What is cosine similarity and why use it?

"It measures the angle between two embedding vectors — essentially normalized dot product — so it compares semantic direction regardless of document length. That's exactly what we want: 'can't connect to Wi-Fi' should match a network policy chunk even though the wording is completely different. Since embeddings encode meaning, small angle means same topic. We configure it on the index itself — metric='cosine' — so Pinecone ranks by it natively." vectorstore.py:82-86

Q7. Why chunk documents, and what if chunks are too small or large?

"Three reasons: embeddings average their content, so a whole document dilutes every topic into a mushy vector; graders and generators have prompt limits; and users want the relevant passage, not a 30-page PDF. We use RecursiveCharacterTextSplitter at 900 chars with 120 overlap — the overlap preserves context across boundaries like step lists. Too small and you slice procedures mid-step, so the grader sees fragments that look insufficient; too large and each vector covers multiple topics, similarity scores blur, and four huge chunks blow the prompt budget." ingestion.py:27-29

Q8. Five chunks retrieved but only two relevant — how handled?

"The grade_kb node reads all chunks and asks whether the set can answer confidently. If the two relevant chunks are enough, it grades 'good' and we answer — the noise is harmless since the generator is told to use only relevant evidence. If they're not enough, 'weak' triggers the web fallback. Honest caveat: the grader judges set-level sufficiency, not per-chunk relevance, and there's no similarity score threshold or reranker — adding a reranker like a cross-encoder would be my first improvement." workflow.py:92-107 workflow.py:111-112

C. Grading and Fallback Logic
Q9. How does grading decide sufficiency? What happens on weak?

"grade_kb formats each retrieved chunk with its source filename and asks the LLM — constrained by structured output to exactly 'good' or 'weak' — whether the evidence answers the question 'confidently and specifically.' Weak routes to search_web via after_kb. Two deliberate choices: it's a binary signal, which keeps the routing logic simple and deterministic, and any grader exception defaults to 'weak' — we fail toward gathering more evidence, not toward answering on thin ice." workflow.py:92-107

Q10. Why Tavily? When does web fallback trigger?

"Because private KBs are inherently incomplete — vendor outages, new software versions, issues with third-party tools nobody wrote internal docs for. The trigger is exactly one condition: kb_grade == 'weak'. Tavily returns up to 5 results plus a synthesized answer, and we format titles, URLs, and content into web_results while collecting citations — so web answers are always traceable and explicitly labeled as external info needing IT validation." workflow.py:116-133 workflow.py:196-202

Q11. Tavily returns unreliable results — then what?

"grade_web runs the same binary grading on the web results. If it's weak, after_web checks retry_count: under the limit, we go to rewrite_query — maybe the query's phrasing is the problem, not the data — and the loop re-runs KB retrieval, grading, and web search with the new query. Once retries are exhausted, insufficient returns a fixed 'contact the IT help desk' response. The key invariant: we never generate an answer from evidence that was graded weak." workflow.py:154-159 workflow.py:212-217

Q12. What is query rewriting and why does it help?

"It's rephrasing the user's question to match the vocabulary that actually appears in the corpus. Users write 'Outlook keeps dying'; docs say 'Outlook crash' or 'application error' — same meaning, different words, weaker embedding match. Our rewrite_query prompt preserves intent, adds technical keywords, returns only the query. The subtle design point: retrieval uses current_query but graders still evaluate against the original question, so rewriting improves recall without ever drifting from what the user actually asked." workflow.py:163-173 workflow.py:86-88

D. Retry Logic and LangGraph
Q13. How does retry_count prevent infinite loops?

"It starts at 0 in ask(), rewrite_query increments it on every pass, and after_web only routes back to rewrite_query while retry_count < max_retries — default 1. That's the loop's only exit condition, so termination is guaranteed by construction: the worst-case graph is bounded at compile-known maximums, roughly two full retrieval cycles. One asymmetry to note: the retry check happens after web grading, so a weak KB grade always buys one web search even on the last iteration." workflow.py:266-278 workflow.py:154-159

Q14. Everything fails — walk the exact path.

"Retrieve KB → grade_kb weak → search_web → grade_web weak → retry_count 0 < 1 → rewrite_query sets current_query, count becomes 1 → retrieve_kb again with the new query → grade_kb weak → search_web again → grade_web weak → retry_count 1 not < 1 → insufficient → fixed help-desk message → END. Every hop lands in trace, so the audit row reconstructs the entire decision path." workflow.py:154-159 workflow.py:212-217

Q15. Why bounded retries instead of search-until-success?

"Three reasons: each retry costs roughly four more LLM calls plus embedding and search API calls — real money and seconds of latency; returns diminish fast — if two query formulations failed, a third rarely succeeds; and a guaranteed-terminating system is far easier to reason about in production than an open-ended loop. The trade-off is a false negative: a user whose query was just badly worded twice gets an unnecessary 'insufficient.' And honestly, max_retries=1 is conservative — it's a config knob, so I'd tune it from real audit data." config.py:23

Q16. Why LangGraph over a simple chain?

"Because this workflow isn't a chain — it has three conditional branches, a three-way post-web decision, a cycle where rewrite_query feeds back into retrieve_kb, and shared mutable state. As function calls, that becomes nested if-else control flow with hand-rolled state passing and termination logic. LangGraph gives declarative nodes and edges, automatic state merging — each node returns a partial dict — and an inspectable graph structure. Extending it is cheap: adding a reranker node is literally add_node plus an edge. The graph definition is also self-documenting — I can show a stakeholder the exact flow." workflow.py:221-256

E. Reliability, Observability, and Deployment
Q17. How do you reduce hallucinations?

"Defense in depth, and I'd list the layers: grounded prompts — 'answer ONLY from the private KB, do not invent policy details'; temperature 0 on the LLM; an evidence grading gate before generation so weak evidence never reaches the generator; a fixed 'insufficient' response instead of guessing; citations on every generated answer for verification; and web answers explicitly labeled as external info needing IT validation. The honest gap: there's no post-generation faithfulness check — if the answer contradicts the evidence, nothing catches it today. My next step would be a verify node that checks answer claims against kb_docs, or at minimum sampling for that in offline eval." workflow.py:179-184 workflow.py:30-35 workflow.py:212-217

Q18. What do you log to understand a query's processing?

"Every request writes a query_audit row: timestamp, question, source_used, and the full trace as JSON. The trace captures every decision — router choice, how many chunks came back, both grades, the rewritten query, which generator ran — so 'why did it pick this route' is answerable from one row. What I'd add for production: per-node latency, token usage per LLM call, retrieved doc IDs with similarity scores, and retry_count — that turns the audit table from a decision log into a cost-and-quality dataset." audit.py:11-31 routes.py:30-31

Q19. Deployment challenges — API failures, env vars, credentials?

"Four areas. Credentials: four external secrets — Groq, Tavily, Pinecone, admin key — loaded via pydantic-settings from .env; in production that's a secrets manager, and the admin_api_key default of 'change-me' must never ship. Failure handling: missing keys raise lazily at first use; grading and routing already fail safe — 'weak' and 'kb' respectively — but a Pinecone or Tavily outage surfaces as a 500 through the generic handler; I'd map dependency failures to 503, add timeouts, and health-check them in /health. Cold start: the HuggingFace model downloads on first request, so I'd warm it at startup. And scale: SQLite audit is single-writer — fine for a demo, not for concurrent production load." config.py:10-30 routes.py:42-43

Q20. App is slow and burning API credits — how do you fix it?

"Diagnose before optimizing — add per-node timing to the trace, because the worst-case path is about 7 sequential LLM calls: route, KB grade, web grade, rewrite, then repeat, then generate. Then optimize in order of quality impact: first, eliminate calls — skip the router for obvious cases, skip grade_kb when similarity scores are clearly high; second, cache — answer cache keyed on normalized question, embedding cache for repeated queries; third, shrink prompts — fewer or trimmed chunks to graders; fourth, use a cheaper model for the router and graders — binary JSON judgments don't need the main model, and gpt-4o-mini is already sitting unused in config; fifth, run independent calls in parallel. None of this touches the retrieve → grade → generate safety structure, so quality impact is minimal." config.py:21 vectorstore.py:97-106
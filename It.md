# Project Intro
One of my key projects is the Enterprise IT Support Agentic RAG Copilot, an AI-powered IT support assistant that helps employees find answers to their IT-related questions.
The problem I wanted to solve was that employees in a company often need to search through multiple documents or contact the IT support team to resolve common problems. I wanted to build an assistant that could answer their questions using the company's private IT documents instead of relying only on the LLM's existing knowledge.
I built it using Python, FastAPI, LangGraph, Pinecone, Hugging Face embeddings, Groq, and Tavily. I used FastAPI to build the backend APIs, LangGraph to manage the agent workflow, Pinecone to store and retrieve document embeddings, Groq to run the LLM, and Tavily for web search.
What makes this project interesting is that I didn't implement just a basic RAG pipeline. I built an agentic RAG workflow that can evaluate the retrieved evidence and decide what to do next.
When an employee asks a question, the agent first searches the private knowledge base. If the retrieved information is relevant, it generates an answer using that evidence. If the evidence is weak, it falls back to web search using Tavily. If the web evidence is also insufficient, it rewrites the query and retries the retrieval process. If it still cannot find reliable evidence, it returns an insufficient-evidence response instead of guessing.
For document ingestion, I implemented a pipeline that loads PDF, TXT, Markdown, and DOCX files, splits them into smaller chunks, generates embeddings, and stores them in Pinecone. I also added an admin-key-protected API for uploading documents.
For monitoring and debugging, I implemented SQLite audit logging, which records the user's question, the final source information, and the agent's decision trace.
The most important part of this project is the LangGraph state machine, where the workflow uses routing, evidence grading, conditional branching, and query rewriting to decide how to answer a question.
Overall, this project helped me gain practical experience with Agentic AI, RAG, LangGraph workflows, vector databases, embeddings, API development, document processing, and audit logging.

# Interview Intro of Project
One of my key projects is the Enterprise IT Support Agentic RAG Copilot, an AI-powered assistant that answers employees' IT questions using company documents.
I built it using Python, FastAPI, LangGraph, Pinecone, Groq, Hugging Face embeddings, and Tavily.
The main feature is that the agent first retrieves information from the private knowledge base and grades the evidence before generating an answer. If the evidence is weak, it searches the web, rewrites the query, and retries if necessary. If it still cannot find reliable information, it returns an insufficient-evidence response.
I also implemented document ingestion using chunking and embeddings, a protected document-upload endpoint, and SQLite audit logging to record the agent's decisions.
Overall, this project helped me gain practical experience in Agentic RAG, LLM workflows, vector search, backend development, and evidence-based AI systems.

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


A. Architecture and Project Understanding
Q1. Can you explain the complete architecture of PromptVerse, from the moment a user interacts with the frontend until the request is processed by the backend and stored in the database?

Answer:
"PromptVerse is a monolithic Next.js app using the App Router. The frontend is React components like components/Feed.jsx, which call API routes under app/api/. Every request first passes through middleware.js, which applies Token Bucket rate limiting for sensitive routes using Redis. The API routes connect to MongoDB through a shared connectToDB() utility and use Mongoose models — User and Prompt. Redis (Upstash) sits in front of MongoDB purely as a cache for the homepage feed under the key feed:homepage with a 600-second TTL. Authentication is handled by NextAuth in app/api/auth/[...nextauth]/route.js with a JWT session strategy. So the flow is: client → middleware rate limiter → API route → Redis cache check → MongoDB on miss → response. MongoDB is the source of truth; Redis holds only ephemeral state like cache and rate-limit buckets."

Q2. You mentioned that PromptVerse is a product you've developed through multiple versions. What changes did you make based on feedback, and how did those changes improve the product?

Answer:
"Version 1 was basic prompt sharing — create, save, and share prompts, which I used with friends. In version 2, feedback showed users didn't want every prompt visible, so I added an isPrivate flag to the prompt schema. Version 3 focused on security, performance, and UX: I added Google OAuth via NextAuth, Redis-based Token Bucket rate limiting in middleware, Redis caching of the homepage feed, a trending feature driven by copy timestamps stored in recentCopyDates, and prompt expiry using an expiresAt field with a MongoDB TTL index for automatic cleanup. Each version was driven by a real user need or a scalability concern rather than features for their own sake."

Q3. Walk me through the complete Google OAuth authentication flow in PromptVerse. How do you identify an existing user, create a new user, and authenticate them?

Answer:
"The client calls signIn('google'), which redirects to Google's consent screen. Google calls back to /api/auth/callback/google with an authorization code, and the server exchanges the code plus clientSecret for tokens and the user profile. Then the signIn callback runs: it calls connectToDB() and does User.findOne({ email: profile.email }). If no user exists, it generates a unique username from the Google name via generateUniqueUsername and creates the user with email, username, and profile picture. Either way, the MongoDB _id and username are attached to the user object, which the jwt callback copies into the JWT token, and the session callback surfaces onto the session object. The session uses strategy: 'jwt' with a 1-hour maxAge, signed with NEXTAUTH_SECRET and stored in a cookie — so no server-side session store is needed."

Q4. Suppose you need to create an API that allows users to create, update, delete, and retrieve prompts. Which HTTP methods would you use, and how would you structure these endpoints?

Answer:
"I'd use REST semantics: nouns in the path, verbs in the method. POST /api/prompt/new to create, GET /api/prompt to list the public feed, GET /api/prompt/[id] to read one, PATCH /api/prompt/[id] for partial update, and DELETE /api/prompt/[id] to delete. I'd also have GET /api/users/[id]/posts for a user's own prompts and POST /api/prompt/[id]/copy as an action endpoint for copy tracking — which is exactly how the codebase is structured. Successful operations return 2xx, client errors like validation failures return 4xx, and I'd use 404 for missing resources rather than leaking whether a private prompt exists."

B. Redis and Rate Limiting
Q5. You use Redis to cache public prompts on the homepage. Walk me through what happens when a request arrives, the cache contains the data, and the cache does not contain the data.

Answer:
"In GET /api/prompt, the handler first calls redis.get('feed:homepage'). On a cache hit, it returns the cached JSON immediately — no database query at all. On a miss, it queries MongoDB for isPrivate: false prompts that aren't expired — handling three cases: expiresAt explicitly null, the field not existing for backward compatibility, or expiresAt in the future. It populates the creator reference, sorts by createdAt descending, then writes the result back with redis.set('feed:homepage', prompts, { ex: 600 }) — a 10-minute TTL. This is the classic cache-aside pattern: the application manages the cache, MongoDB remains the source of truth, and Redis errors are caught so a Redis failure just falls back to the database."

Q6. Suppose your homepage cache has a TTL of 10 minutes. A user creates a new public prompt, but it doesn't appear on the homepage immediately. Why might this happen, and how would you handle it?

Answer:
"This is the inherent staleness trade-off of cache-aside: the cached snapshot can lag up to the TTL, so a prompt created after the last cache write won't appear until the entry expires. The fix is active invalidation — calling redis.del('feed:homepage') inside the create, update, and delete routes, so the next request repopulates the cache with fresh data. TTL then becomes only a safety net, not the primary freshness mechanism. If stronger freshness were needed, options include shortening the TTL or using tag-based invalidation, but for a homepage feed a short staleness window plus write-time invalidation is the right balance between freshness and database load."

Q7. Explain how you implemented the Token Bucket rate-limiting algorithm. What information do you store in Redis, and how do you decide whether a request should be allowed or rejected?

Answer:
"In middleware.js, I configure per-route buckets — for example /api/prompt/new gets a bucketSize of 10 tokens refilling at 1 token per second. Each request builds a key like rate_limit:<email-or-sub-or-ip>:<pathname>. Redis stores an object { tokens, lastTime } per key. On each request I compute tokensToAdd = (now - lastTime) * refillRate, then tokens = min(bucketSize, tokens + tokensToAdd) — so the bucket refills continuously over time but never exceeds capacity. If tokens >= 1, I decrement, write back to Redis with a 1-hour expiry to keep Redis clean, and allow the request with X-RateLimit-Limit and X-RateLimit-Remaining headers. Otherwise I return 429 with a Retry-After header computed as (1 - tokens) / refillRate. The bucket design allows short bursts up to capacity while enforcing a sustainable average rate."

Q8. Suppose 100 requests from the same user arrive simultaneously. How would you ensure that your Redis-based rate limiter doesn't allow more requests than the configured limit?

Answer:
"Honestly, the current implementation is read-modify-write — a GET followed by a SET — so it's not atomic. If 100 requests arrive simultaneously, many could read the same token count before any writes back, and over-admit. The correct fix is to run the entire bucket logic inside a Lua script executed on Redis via EVAL/EVALSHA — Redis executes scripts atomically, so refills and decrements become a single operation. Alternatives are optimistic locking with WATCH/MULTI/EXEC or a distributed lock, but Lua is the standard approach — it's atomic, fast, and a single round trip. Upstash supports Lua scripts, so this is directly applicable to the current stack."

Q9. Imagine Redis becomes unavailable. Your application uses it for both caching and rate limiting. How should your backend behave in each case, and what trade-offs would you consider?

Answer:
"The codebase already handles both cases deliberately. For caching, the redis.get and redis.set calls are wrapped in try/catch — on failure the route logs the error and falls through to MongoDB, so reads just get slower but keep working. For rate limiting, the middleware's catch block returns NextResponse.next() — it fails open, allowing the request. The trade-off: fail-open keeps the site available but temporarily drops abuse protection; fail-closed protects the API but means a Redis outage takes down the whole application. For this product, availability wins, so fail-open is right — but for high-cost or abuse-sensitive endpoints I could add a conservative in-memory fallback limiter as a middle ground. The key point is the failure mode is a conscious choice, not an accident."

C. Database and Backend Engineering
Q10. How would you structure your MongoDB collections for users and prompts? How would you represent public and private prompts, and how would you associate prompts with their creators?

Answer:
"Two collections. User has email and username — both unique — plus image and timestamps. Prompt has creator as an ObjectId referencing User, a required prompt string, a required tag, isPrivate defaulting to false, expiresAt with a TTL index for automatic deletion, recentCopyDates as an array of Dates for trending, and an indexed createdAt. Public versus private is a flag on the same collection rather than separate collections — that keeps queries simple and lets a prompt toggle visibility with one update. Ownership is the creator reference, joined at read time with .populate('creator'). The schema evolved with product needs — isPrivate in v2, expiry and trending fields in v3 — which is easy with a document model."

Q11. Suppose a user tries to access another user's private prompt by changing the prompt ID in the API request. How would you prevent unauthorized access?

Answer:
"That's an IDOR vulnerability, and the rule is: never trust the ID in the URL alone. In GET, PATCH, and DELETE /api/prompt/[id], I get the authenticated session first — via getServerSession or getToken — then scope the query by ownership: Prompt.findOne({ _id: id, creator: session.user.id }) for any private-resource access. If the prompt isn't owned by the requester, return 404 — which also avoids leaking that a private prompt exists — or 403 if I want to distinguish 'exists but forbidden'. The general principle is to make authorization part of the query predicate rather than fetching first and checking ownership afterward, because a check after fetch is easy to forget and can leak data through error paths."

Q12. Your platform supports prompt categorization and search. How would you implement search and filtering efficiently as the number of prompts increases?

Answer:
"Three layers. First, indexes: tag should be indexed alongside the already-indexed isPrivate, createdAt, and expiresAt, and queries filter server-side — { isPrivate: false, tag } — instead of loading everything and filtering in Feed.jsx like the current client-side approach. Second, pagination: the feed route currently returns all public prompts, which won't scale — I'd use cursor-based pagination on createdAt/_id since it's stable under inserts, unlike offset pagination. Third, real search: for keyword matching add a MongoDB text index on prompt and tag, and for fuzzy or ranked search move to Atlas Search or Elasticsearch. The ordering matters — indexes and pagination solve 90% of the problem cheaply; a dedicated search engine only when relevance ranking becomes a real requirement."

Q13. Suppose a user submits an empty prompt, an invalid category, or a prompt ID that doesn't exist. How should your backend validate these requests and respond?

Answer:
"Each failure mode maps to a specific status code. Empty prompt or tag: Mongoose required validators catch it, but I'd validate explicitly in the route and return 400 { error: 'prompt is required' } rather than a generic 500. Invalid category: check against a whitelist and return 400. A prompt ID that doesn't exist: findById returns null, so return 404 — not 500, since it's a client error, not a server failure. A malformed ID like a non-ObjectId string throws a Mongoose CastError, which I'd catch and translate to 400. All errors use a consistent { error, message } shape — the same shape the 429 handler in middleware.js already returns. The principle: 4xx means the client can fix the request; 5xx is reserved for actual server faults."

D. Trending Logic and Product Decisions
Q14. Your trending system orders prompts by copy count, and the count resets monthly. Explain how this works and how you would handle a prompt that receives many copies near the end of the month.

Answer:
"The implementation actually uses a rolling window rather than a hard monthly reset — which I think is the better design. On each copy, POST /api/prompt/[id]/copy pushes the current timestamp into recentCopyDates and prunes entries older than 7 days. On feed load, Feed.jsx counts each prompt's array length — its copies in the last 7 days — sorts descending, and pins the top 3 to the front. The rolling window solves the end-of-month problem automatically: a prompt copied heavily near the boundary doesn't lose everything at once or get an unfair double-credit; old copies simply decay out of the window naturally. It also removes the need for a fragile scheduled reset job entirely — there's no cron to fail or run twice."

Q15. Suppose two prompts have the same copy count. How would you decide which one should appear first? What additional information could you use?

Answer:
"I'd tie-break on recency of the most recent copy — max(recentCopyDates) — favoring momentum over stale popularity. Next, createdAt with newer prompts first, to give fresh content exposure. A stronger signal would be unique copiers rather than raw count — ten copies by ten different users means more than ten copies by one user, and it resists single-user gaming. Whatever the secondary key, it must be deterministic: an unstable ordering between equal-count prompts would make the feed jitter between renders, which looks buggy to users."

Q16. How would you implement the monthly copy-count reset in a production application? What problems could occur if the reset process runs twice or fails midway?

Answer:
"First choice: avoid the reset entirely — the rolling-window design the codebase uses deletes stale timestamps on write, so there's no batch job to fail. If a reset job is required, I'd use a scheduled route like the existing app/api/cleanup/expired-prompts pattern, guarded by a distributed lock — SET lock NX EX in Redis — so only one instance runs it. To survive double-runs, the operation must be idempotent: deleting-by-predicate or setting a counter to zero is naturally idempotent; decrementing is not — running it twice corrupts data. For mid-job failure, process in batches with recorded progress or use a transaction, and prefer per-document updates — like $pull of old dates — over a global counter rewrite, so a crash leaves every document individually consistent."

E. Performance, Security, and Testing
Q17. Suppose the homepage becomes slow after the number of prompts grows significantly. How would you investigate the bottleneck and improve performance?

Answer:
"I'd investigate in order of likelihood. First, check the cache hit ratio — the feed route already logs cache hits and misses, so if misses dominate, something's wrong with the key or invalidation. Second, run explain() on the feed query — a missing compound index on { isPrivate, expiresAt, createdAt } would force a collection scan as data grows. Third, the biggest structural issue: the route returns all public prompts with no pagination, and Feed.jsx computes the trending sort client-side — so both payload size and client work grow linearly with prompt count. Fixes: cursor-based pagination, move trending computation server-side or precompute a trendingScore field on write, ensure the query is index-covered, and consider CDN or edge caching of the feed response since it's the same for all anonymous users."

Q18. How does your authentication system identify a user on subsequent requests? What would happen if a JWT expired, and how would you handle that in your current design?

Answer:
"After sign-in, the user's Mongo _id and username are embedded in a JWT signed with NEXTAUTH_SECRET and stored in an HttpOnly cookie, which the browser sends automatically. On the server, getToken({ req, secret }) in middleware and the session callback decrypt it — no database lookup needed per request, which is a scalability win. The session maxAge is one hour; on expiry the JWT won't decrypt and the user is treated as unauthenticated — protected routes redirect to sign-in. With the JWT strategy there's no refresh token, so the user re-authenticates through Google — it's a single click since Google usually has a live session. One operational caveat: rotating NEXTAUTH_SECRET invalidates every active JWT at once, so secret changes need a deploy strategy that tolerates mass re-login."

Q19. How would you test the Redis caching and Token Bucket rate limiter to ensure they behave correctly under normal and concurrent requests?

Answer:
"The repo already has tests/integration/middleware/rateLimit.test.js, which mocks @utils/redis and next-auth/jwt to cover: first request allowed with a fresh bucket, 429 returned when tokens: 0, Retry-After header present, and the fail-soft path when Redis throws. I'd extend that with refill correctness — mock lastTime in the past and assert tokens accrue at refillRate — and per-route isolation since limits are keyed by pathname. For concurrency, I'd script N parallel middleware calls against a real Redis — or ioredis-mock — sharing one key and assert total allowed never exceeds bucketSize. That test would actually expose the current non-atomic get/set race, which is a great interview talking point: the test exists to catch it, and the Lua-script fix makes it pass. For caching, mock redis.get returning data and assert Mongo is never called; mock it returning null and assert redis.set is called with ex: 600."

Q20. Suppose PromptVerse grows from 100 users to 100,000 users. Which parts of the application would you examine first for scalability problems, and what improvements would you prioritize?

Answer:
"Priority order by impact. First, the unbounded feed query — it returns all public prompts; I'd add cursor pagination and a compound index on { isPrivate, expiresAt, createdAt }. Second, the client-side trending sort — it requires fetching everything; move it to a Mongo aggregation or a precomputed trendingScore updated on copy. Third, rate-limiter atomicity — replace get/set with a Lua script before the race matters at real traffic. Fourth, infrastructure hygiene: ensure connectToDB connection caching for serverless, and confirm horizontal scaling is safe — which it is, since Redis holds shared state and JWT sessions need no server-side store, so any number of instances works. Fifth, caching strategy — the feed is identical for all users, so CDN/edge caching is nearly free scale. Mongo read replicas and Atlas Search come later if query load or search requirements justify them."
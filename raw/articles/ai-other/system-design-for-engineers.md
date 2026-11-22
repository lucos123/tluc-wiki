Hey there 👋,

It has been a while since our last post, so we wanted to come back with something really useful.

This one is about system design.

When you start learning it, there are so many terms. Load balancers, sharding, caching, queues, consistency models. You look up one, and it leads you to three more. It is easy to feel lost.

Over the last month, we shared a lot of system design resources on social media. Most of what you will find here is a compilation of those posts. Not everything will apply to you, but we wanted to have it all in one place.

This guide has **162 system design concepts**, in an order that builds up step by step. For each concept, you get two links:

- 📖 **One article**, when you want to read and understand the idea.
- 🎥 **One video**, when you want to see it explained.

Read one, watch the other, or both. You do not need to finish it in one go. Save it, and come back whenever a concept does not click.

> **System design is not about memorising answers. It is about understanding the pieces, so you can put them together.**

When we made our video on how an AI app grows from one user to 10,000 users, the model stayed the same. What changed was everything around it: how requests come in, how they wait, how they fail, and how the system grows. These are exactly the concepts you will find here.

They matter a lot in interviews too. The first diagram is usually the easy part. The follow-up questions are where these concepts really help, like “What happens if the payment service crashes?” or “What if two workers grab the same lock?”

---

**Prefer to learn visually first? Start with these three videos:**

🎥 **[AI System Design: 7 Patterns Explained in 17 Minutes](https://www.youtube.com/watch?v=0jCss9xfOiw)**  
Follow one AI application from one user to 10,000 users, and watch the gateway, rate limiting, caching, queues, circuit breakers, load balancing, and autoscaling get added one problem at a time.

🎥 **[How a Production AI Agent System Actually Works](https://www.youtube.com/watch?v=sKzL0wSN9vQ)**  
See how a simple demo becomes an application that works for real users, layer by layer.

🎥 **[AI Agent Memory: 7 Types Explained in 12 Minutes](https://www.youtube.com/watch?v=bK1clrG-boc)**  
Learn what an agent should remember, and where that memory lives.

---

## The map before the concepts

[![](https://substackcdn.com/image/fetch/$s_!XYaT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb01ce1d3-bc88-4981-a7f6-df82f099639e_2912x1942.png)](https://substackcdn.com/image/fetch/$s_!XYaT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb01ce1d3-bc88-4981-a7f6-df82f099639e_2912x1942.png)

You do not need to memorise all 162. It just helps to know where each one belongs.

Every system has to **take requests**, **store data**, let work **wait**, survive when things **fail**, and **scale** when more people use it. The 17 parts follow that path:

- **Think first (Part I):** requirements, trade-offs, and rough estimates.
- **Enter (Part II):** DNS, load balancers, and rate limits.
- **Store (Parts III, IV, V and VII):** databases, sharding, caching, and storage engines.
- **Wait (Part VIII):** queues, streams, and schedulers.
- **Fail (Parts VI and XIV):** consistency, consensus, and reliability.
- **Scale (Parts IX to XIII):** search, feeds, maps, and media.
- **AI in the system (Part XV):** what changes when there is an LLM.
- **Know your tools (Part XVI):** from PostgreSQL to Kubernetes.
- **Design X (Part XVII):** where every piece comes together.

> The goal is simply to have a map you can come back to. The next time someone says “just make the consumer idempotent”, you will know which part of the system they mean.

## How to use this guide

**⭐ Short on time? Start with these 15.** They come up again and again, and many other concepts build on them. You will find them marked with ⭐ in the list.

- **Think first:** #1 Approaching a problem, #2 Non-functional requirements, #3 Trade-offs, #4 Back-of-the-envelope estimation
- **Enter:** #12 Load balancers, #13 Retries, timeouts and idempotency, #15 Rate limiting
- **Store:** #21 Scaling relational databases, #24 Sharding, #25 Consistent hashing, #29 Caching layers
- **Fail:** #32 Consistency models, #38 Circuit breakers, #42 Keeping data in sync (the outbox pattern)
- **Wait:** #50 Distributed message queues

**Preparing for an interview?** Pick a “Design X” question from Part XVII. Try to sketch your own answer for 20 minutes first, then watch the walkthrough. If something surprises you, find that concept in this list and spend a little time there.

**Learning for your job?** Go one part at a time. And remember, the best way to learn is really by building. Write a tiny rate limiter. Put a cache in front of a slow API. Then break it on purpose and see what happens.

Do that a few times, and “Design X” stops feeling like a puzzle. It becomes a set of pieces you already understand.

---

## Part I: Foundations and the Interview Approach

**Why it matters:** The first five minutes decide the next forty. Clarify the requirements, name the trade-offs, and do the rough maths before you draw a single box.

**Interview signal:** “How many requests per second are we talking about?” Asking this yourself, before anyone prompts you, is already a good sign.

**⭐ 1. How to Approach a System Design Problem**

- 📖 Article: [Steps to solve a system design interview problem](https://www.geeksforgeeks.org/system-design/how-to-answer-a-system-design-interview-problem/)
- 🎥 Video: [How to answer system design questions (Exponent)](https://www.youtube.com/watch?v=L9TfZdODuFQ)

**⭐ 2. Non-Functional Requirements**

- 📖 Article: [Non-functional requirements in system design](https://www.geeksforgeeks.org/system-design/what-are-non-functional-requirements-in-system-design-examples-definition/)
- 🎥 Video: [Functional vs non-functional requirements (sudoCODE)](https://www.youtube.com/watch?v=xRdjEd-VQTU)

**⭐ 3. Thinking in Trade-offs**

- 📖 Article: [Trade-offs in system design](https://www.geeksforgeeks.org/system-design/tradeoffs-in-system-design/)
- 🎥 Video: [System design trade-offs (ByteByteGo)](https://www.youtube.com/watch?v=1nENigGr-a0)

**⭐ 4. Back-of-the-Envelope Estimation**

- 📖 Article: [Back-of-the-envelope estimation in system design](https://www.geeksforgeeks.org/system-design/back-of-the-envelope-estimation-in-system-design/)
- 🎥 Video: [Back-of-the-envelope estimation (ByteByteGo)](https://www.youtube.com/watch?v=UC5xf8FbdJc)

**5\. How a Server Handles Many Requests**

- 📖 Article: [Thread pools vs event loops](https://rohith-gandhi.com/blog/thread-pools-vs-event-loops)
- 🎥 Video: [How NGINX handles millions of requests (ByteMonk)](https://www.youtube.com/watch?v=I6dpN0geIb4)

**6\. Monolith vs Microservices**

- 📖 Article: [Monolithic vs microservices architecture](https://www.geeksforgeeks.org/software-engineering/monolithic-vs-microservices-architecture/)
- 🎥 Video: [Monolith vs microservices: which and when (Alex Hyett)](https://www.youtube.com/watch?v=NdeTGlZ__Do)

**7\. Core Abstractions (RPC)**

- 📖 Article: [RPC mechanism in distributed systems](https://www.geeksforgeeks.org/computer-networks/what-is-rpc-mechanism-in-distributed-system/)
- 🎥 Video: [What is RPC? (ByteByteGo)](https://www.youtube.com/watch?v=gnchfOojMk4)

---

## Part II: Networking, APIs and Traffic

**Why it matters:** This is how requests enter. Every request passes through DNS, a load balancer, and usually a gateway before it reaches your code. It is also where you decide what to slow down, retry, or reject.

**Interview signal:** “Walk me through what happens when a user presses send.” Start at DNS, not at the database.

**8\. DNS**

- 📖 Article: [What is DNS? (Cloudflare)](https://www.cloudflare.com/learning/dns/what-is-dns/)
- 🎥 Video: [How a DNS server works (PowerCert)](https://www.youtube.com/watch?v=mpQZVYPuDGU)

**9\. TCP vs UDP**

- 📖 Article: [TCP vs UDP](https://www.geeksforgeeks.org/computer-networks/differences-between-tcp-and-udp/)
- 🎥 Video: [TCP vs UDP comparison (PowerCert)](https://www.youtube.com/watch?v=uwoD5YsGACg)

**10\. HTTP, REST and gRPC**

- 📖 Article: [gRPC vs REST (AWS)](https://aws.amazon.com/compare/the-difference-between-grpc-and-rest/)
- 🎥 Video: [REST vs gRPC in microservices (ByteMonk)](https://www.youtube.com/watch?v=AMNWLz_f6qM)

**11\. Service-to-Service Communication**

- 📖 Article: [Synchronous vs asynchronous communication](https://www.geeksforgeeks.org/system-design/synchronous-vs-asynchronous-communication-system-design/)
- 🎥 Video: [Sync and async communication between microservices (Arpit Bhayani)](https://www.youtube.com/watch?v=ewUw0sUxHI4)

**⭐ 12. Load Balancers**

- 📖 Article: [What are load balancers? (AlgoMaster)](https://algomaster.io/learn/system-design/load-balancers)
- 🎥 Video: [What is a load balancer? (IBM)](https://www.youtube.com/watch?v=sCR3SAVdyCc)

**⭐ 13. Retries, Timeouts and Idempotency**

- 📖 Article: [Timeouts, retries and backoff with jitter (AWS Builders’ Library)](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- 🎥 Video: [Exponential backoff and jitter explained (CodeLucky)](https://www.youtube.com/watch?v=NByH-cau97A)

**14\. Protecting Systems Under Load**

- 📖 Article: [Backpressure and load shedding](https://www.techdiagrams.net/blog/backpressure-and-load-shedding/)
- 🎥 Video: [Backpressure simply explained (Software Developer Diaries)](https://www.youtube.com/watch?v=3DTSIlj72Qs)

**⭐ 15. Rate Limiting**

- 📖 Article: [Rate limiting algorithms](https://www.geeksforgeeks.org/system-design/rate-limiting-algorithms-system-design/)
- 🎥 Video: [Design a distributed rate limiter (Hello Interview)](https://www.youtube.com/watch?v=MIJFyUPG4Z4)

**16\. Content Delivery Networks (CDN)**

- 📖 Article: [What is a CDN? (Cloudflare)](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/)
- 🎥 Video: [What is a CDN? (ByteByteGo)](https://www.youtube.com/watch?v=RI9np1LWzqw)

---

## Part III: Relational Databases and Data Modeling

**Why it matters:** Most systems are still a relational database with good indexes. Knowing how indexes, transactions, and the write-ahead log work tells you why a query is slow, and when the database really is the bottleneck.

**Interview signal:** “This query got slow as the table grew. How would you fix it without adding new infrastructure?”

**17\. Relational Database Design**

- 📖 Article: [What is database normalization? (IBM)](https://www.ibm.com/think/topics/database-normalization)
- 🎥 Video: [Database normalization 1NF to 5NF (Decomplexify)](https://www.youtube.com/watch?v=GFQaEYEc8_8)

**18\. Indexing and B-Trees**

- 📖 Article: [How database B-tree indexing works (Built In)](https://builtin.com/data-science/b-tree-index)
- 🎥 Video: [Understanding B-trees (Spanning Tree)](https://www.youtube.com/watch?v=K1a2Bk8NrYQ)

**19\. Transactions: Locking, Isolation and MVCC**

- 📖 Article: [Transaction isolation levels](https://www.geeksforgeeks.org/dbms/transaction-isolation-levels-dbms/)
- 🎥 Video: [Isolation levels in DBMS (Edredo)](https://www.youtube.com/watch?v=-gxyut1VLcs)

**20\. Write-Ahead Log and Crash Recovery**

- 📖 Article: [Write-ahead logging (PostgreSQL docs)](https://www.postgresql.org/docs/current/wal-intro.html)
- 🎥 Video: [Write-ahead logs (Ben Dicken)](https://www.youtube.com/watch?v=s3hKYMOpp3E)

**⭐ 21. Scaling Relational Databases**

- 📖 Article: [Sharding, partitioning and read replicas compared](https://westpoint.io/insights/scaling-relational-databases-sharding-partitioning-and-read-replicas-compared)
- 🎥 Video: [7 strategies to scale your database (ByteByteGo)](https://www.youtube.com/watch?v=_1IKwnbscQU)

**22\. Living with Schemas (Pagination)**

- 📖 Article: [Keyset vs offset pagination (Leapcell)](https://leapcell.io/blog/efficient-data-pagination-keyset-vs-offset)
- 🎥 Video: [Offset vs cursor pagination (PlanetScale)](https://www.youtube.com/watch?v=zwDIN04lIpc)

---

## Part IV: NoSQL, Partitioning and IDs

**Why it matters:** Once one machine is not enough, you have to split the data. How you split it decides which queries stay cheap and which ones have to touch every shard.

**Interview signal:** “One very popular account is melting a single shard. What do you do?”

**23\. Choosing NoSQL**

- 📖 Article: [SQL vs NoSQL (IBM)](https://www.ibm.com/think/topics/sql-vs-nosql)
- 🎥 Video: [SQL vs NoSQL (IBM)](https://www.youtube.com/watch?v=Q5aTUc7c4jg)

**⭐ 24. Sharding and Partitioning**

- 📖 Article: [What is database sharding? (AWS)](https://aws.amazon.com/what-is/database-sharding/)
- 🎥 Video: [What is database sharding? (Gaurav Sen)](https://www.youtube.com/watch?v=5faMjKuB9bc)

**⭐ 25. Consistent Hashing**

- 📖 Article: [Consistent hashing explained (AlgoMaster)](https://blog.algomaster.io/p/consistent-hashing-explained)
- 🎥 Video: [Consistent hashing (ByteByteGo)](https://www.youtube.com/watch?v=UF9Iqmg94tk)

**26\. Distributed ID Generation**

- 📖 Article: [Snowflake ID (Wikipedia)](https://en.wikipedia.org/wiki/Snowflake_ID)
- 🎥 Video: [Design a unique ID generator (Nikhil Lohia)](https://www.youtube.com/watch?v=ogOKDhOa_cs)

**27\. Bloom Filters**

- 📖 Article: [Bloom filters (AlgoMaster)](https://algomaster.io/learn/system-design/bloom-filters)
- 🎥 Video: [Bloom filters (ByteByteGo)](https://www.youtube.com/watch?v=V3pzxngeLqw)

**28\. Hot and Cold Storage**

- 📖 Article: [Cold, warm and hot storage (CTERA)](https://www.ctera.com/blog/differences-hot-warm-cold-file-storage/)
- 🎥 Video: [Hot storage vs cold storage (Telusko)](https://www.youtube.com/watch?v=90EBp9wkoYM)

---

## Part V: Caching

**Why it matters:** Caching is often the cheapest speed-up you have, and also the easiest way to serve stale data. Know where each cache sits and how it gets invalidated.

**Interview signal:** “What happens to your cache when the underlying data changes?”

**⭐ 29. Caching Layers**

- 📖 Article: [Cache-aside, read-through, write-through, write-back](https://system-design.space/en/chapter/caching-strategies/)
- 🎥 Video: [5 caching strategies (SoftwareDude)](https://www.youtube.com/watch?v=2zIFUqTx_TU)

**30\. Designing a Distributed Cache**

- 📖 Article: [Design a distributed cache](https://www.geeksforgeeks.org/system-design/design-distributed-cache-system-design/)
- 🎥 Video: [Distributed cache system design interview](https://www.youtube.com/watch?v=iuqZvajTOyA)

---

## Part VI: Distributed Systems Core

**Why it matters:** This is where things fail. Networks drop messages, clocks drift, and two machines can believe different things at the same time. Most of the hardest follow-up questions live here.

**Interview signal:** “The payment service crashed after charging the card, but before saving the order. What now?”

**31\. Distributed Systems Foundations**

- 📖 Article: [Fallacies of distributed computing (Wikipedia)](https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing)
- 🎥 Video: [Why distributed systems are hard (InfoQ)](https://www.youtube.com/watch?v=w9GP7MNbaRc)

**⭐ 32. Consistency Models**

- 📖 Article: [Consistency models: linearizability to eventual](https://systemdesigntutorial.com/m22-consistency-models)
- 🎥 Video: [Data consistency and trade-offs (Gaurav Sen)](https://www.youtube.com/watch?v=m4q7VkgDWrM)

**33\. Replication**

- 📖 Article: [Single-leader, multi-leader, leaderless replication](https://systemdesigntutorial.com/m25-replication-patterns.html)
- 🎥 Video: [Database replication explained (Exponent)](https://www.youtube.com/watch?v=bI8Ry6GhMSE)

**34\. CAP and PACELC**

- 📖 Article: [PACELC theorem](https://www.geeksforgeeks.org/operating-systems/pacelc-theorem/)
- 🎥 Video: [CAP theorem and PACELC (SoftwareDude)](https://www.youtube.com/watch?v=BaKtC-VIYrM)

**35\. Clocks and Ordering**

- 📖 Article: [Lamport clocks and vector clocks](https://systemdesigntutorial.com/m23-time-order-clocks.html)
- 🎥 Video: [Logical time (Martin Kleppmann)](https://www.youtube.com/watch?v=x-D8iFU1d-o)

**36\. Consensus and Leader Election**

- 📖 Article: [Raft consensus algorithm (official site)](https://raft.github.io/)
- 🎥 Video: [Understand Raft without breaking your brain](https://www.youtube.com/watch?v=IujMVjKvWP4)

**37\. Distributed Locks and Leases**

- 📖 Article: [How to do distributed locking (Martin Kleppmann)](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)
- 🎥 Video: [How distributed locks work with Redis (ByteMonk)](https://www.youtube.com/watch?v=qY4MfWv01pI)

**⭐ 38. Circuit Breakers**

- 📖 Article: [Circuit breaker (Martin Fowler)](https://martinfowler.com/bliki/CircuitBreaker.html)
- 🎥 Video: [Circuit breaker pattern (Defog Tech)](https://www.youtube.com/watch?v=ADHcBxEXvFA)

**39\. Gossip, Membership and Failure Detection**

- 📖 Article: [Gossip protocol explained (High Scalability)](https://highscalability.com/gossip-protocol-explained/)
- 🎥 Video: [Gossip protocol system design (Piyush Garg)](https://www.youtube.com/watch?v=TUc_hPtxyf8)

**40\. Designing a Key-Value Store**

- 📖 Article: [Dynamo: design of a key-value store](https://medium.com/@nvedansh/dynamo-design-of-a-key-value-store-6c55eb905160)
- 🎥 Video: [Distributed key-value store design (TechPrep)](https://www.youtube.com/watch?v=Uqk7IQFS-Eo)

**41\. Distributed Transactions**

- 📖 Article: [Distributed transactions: 2PC vs saga](https://luminhkhuong.dev/technical-knowledge/system-design/distributed-transactions/)
- 🎥 Video: [2PC vs saga pattern (Hello Interview)](https://www.youtube.com/watch?v=DOFflggE_0Q)

**⭐ 42. Keeping Data in Sync**

- 📖 Article: [Transactional outbox pattern (AWS)](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)
- 🎥 Video: [What is the transactional outbox pattern? (Confluent)](https://www.youtube.com/watch?v=5YLpjPmsPCA)

**43\. Exactly-Once Processing and Deduplication**

- 📖 Article: [Exactly-once semantics in Kafka (Confluent)](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)
- 🎥 Video: [Kafka delivery semantics (Irtiza Hafiz)](https://www.youtube.com/watch?v=V0c0qAP7sWk)

---

## Part VII: Storage Engines and Blob Storage

**Why it matters:** Under every database there is a storage engine trading fast writes against fast reads. And large files belong in object storage, not in your database.

**Interview signal:** “Where do the uploaded images go, and what do you store in the database instead?”

**44\. Storage Engine Fundamentals**

- 📖 Article: [LSM tree vs B-tree storage engines](https://www.vetoralabs.com/system-design/concepts/storage/engines/lsm-vs-btree)
- 🎥 Video: [Data storage engines: 5 must-know components (Ben Dicken)](https://www.youtube.com/watch?v=K4YMuDzbu_E)

**45\. Log-Structured Storage (Bitcask)**

- 📖 Article: [Bitcask, a log-structured KV store (Arpit Bhayani)](https://arpitbhayani.me/blogs/bitcask/)
- 🎥 Video: [Bitcask explained (Arpit Bhayani)](https://www.youtube.com/watch?v=0WI_tJRUMqM)

**46\. LSM Trees**

- 📖 Article: [Introduction to LSM trees](https://www.geeksforgeeks.org/dsa/introduction-to-log-structured-merge-lsm-tree/)
- 🎥 Video: [LSM tree, the secret sauce behind NoSQL (ByteByteGo)](https://www.youtube.com/watch?v=I6jB0nM9SKU)

**47\. Object Storage vs Databases**

- 📖 Article: [Database vs blob storage for files](https://engineeringatscale.substack.com/p/when-to-use-blob-storage-vs-database)
- 🎥 Video: [Object storage (blobs) explained (Hayk Simonyan)](https://www.youtube.com/watch?v=dEcQK4-pqiw)

**48\. Designing a Blob Store (S3)**

- 📖 Article: [S3 architecture (System Design Newsletter)](https://newsletter.systemdesign.one/p/s3-architecture)
- 🎥 Video: [Object storage in system design (Hello Interview)](https://www.youtube.com/watch?v=RvaMHMxHjp4)

---

## Part VIII: Async Work, Queues and Streams

**Why it matters:** Not every request needs an answer right away. You can think of a queue like the order tickets in a restaurant kitchen: the waiter takes the order, and the kitchen works through the tickets at its own pace. This is how work waits safely.

**Interview signal:** “You need to process 50,000 documents. How would you architect it?”

**49\. Delegation and Async Work**

- 📖 Article: [Choosing between message queues and event streams](https://thenewstack.io/choosing-between-message-queues-and-event-streams/)
- 🎥 Video: [Stream, event bus or queue? (James Eastham)](https://www.youtube.com/watch?v=e_ldsz7xzmY)

**⭐ 50. Distributed Message Queue**

- 📖 Article: [Message queue system design](https://www.systemdesignhandbook.com/guides/message-queue-system-design/)
- 🎥 Video: [Distributed message queue design](https://www.youtube.com/watch?v=iJLL-KPqBpM)

**51\. Pub-Sub Systems**

- 📖 Article: [Publisher-subscriber pattern (Azure)](https://learn.microsoft.com/en-us/azure/architecture/patterns/publisher-subscriber)
- 🎥 Video: [What is the publisher-subscriber model? (Gaurav Sen)](https://www.youtube.com/watch?v=FMhbR_kQeHw)

**52\. Kafka-Style Log**

- 📖 Article: [Kafka architecture](https://www.geeksforgeeks.org/apache-kafka/kafka-architecture/)
- 🎥 Video: [Kafka tutorial for beginners (TechWorld with Nana)](https://www.youtube.com/watch?v=QkdkLdMBuL0)

**53\. Distributed Task Scheduler**

- 📖 Article: [Design a distributed job scheduler (AlgoMaster)](https://blog.algomaster.io/p/design-a-distributed-job-scheduler)
- 🎥 Video: [Distributed job scheduler (Jordan has no life)](https://www.youtube.com/watch?v=pzDwYHRzEnk)

**54\. Workflow Orchestration**

- 📖 Article: [DAGs (Apache Airflow docs)](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- 🎥 Video: [Learn Apache Airflow in 10 minutes](https://www.youtube.com/watch?v=5peQThvQmQk)

**55\. Fanout Patterns**

- 📖 Article: [Fan-out on read vs fan-out on write](https://dev.to/na2axl/fan-out-on-read-vs-fan-out-on-write-choosing-the-right-trade-off-for-a-dynamic-feed-1a8a)
- 🎥 Video: [Fanout on read vs fanout on write (Kartikeya Sharma)](https://www.youtube.com/watch?v=SeeKlGMxyBQ)

**56\. Flash Sale Inventory Locking**

- 📖 Article: [Design a flash sale (AlgoMaster)](https://algomaster.io/learn/system-design-interviews/design-flash-sale)
- 🎥 Video: [Flash sale system design (TechPrep)](https://www.youtube.com/watch?v=U2Acfwcah80)

---

## Part IX: Search and Retrieval

**Why it matters:** Search is an indexing problem before it is a ranking problem. If you build RAG systems, you already use half of this part: BM25, vector search, and hybrid retrieval.

**Interview signal:** “How would you combine keyword search and vector search?”

**57\. How Search Engines Work**

- 📖 Article: [Inverted index](https://www.geeksforgeeks.org/dbms/inverted-index/)
- 🎥 Video: [Inverted index (Arpit Bhayani)](https://www.youtube.com/watch?v=iHHqnyThrqE)

**58\. Relevance Ranking**

- 📖 Article: [Okapi BM25 (Wikipedia)](https://en.wikipedia.org/wiki/Okapi_BM25)
- 🎥 Video: [BM25 explained (ritvikmath)](https://www.youtube.com/watch?v=ruBm9WywevM)

**59\. Query Understanding and Search Quality**

- 📖 Article: [Evaluation metrics for search and recommendation (Weaviate)](https://weaviate.io/blog/retrieval-evaluation-metrics)
- 🎥 Video: [Ranking metrics: MRR, MAP, NDCG (ritvikmath)](https://www.youtube.com/watch?v=2XegvMul_mE)

**60\. Scaling Search**

- 📖 Article: [Elasticsearch shards and replicas (Elastic)](https://www.elastic.co/search-labs/blog/elasticsearch-shards-and-replicas-guide)
- 🎥 Video: [What are Elasticsearch shards?](https://www.youtube.com/watch?v=NxpZyQVO0K4)

**61\. Designing a Web Crawler**

- 📖 Article: [Design a web crawler (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/web-crawler)
- 🎥 Video: [Design a web crawler (Hello Interview)](https://www.youtube.com/watch?v=krsuaUp__pM)

**62\. Vector Search and Hybrid Retrieval**

- 📖 Article: [Hybrid search explained (Redis)](https://redis.io/blog/hybrid-search-explained/)
- 🎥 Video: [What is a vector database? (IBM)](https://www.youtube.com/watch?v=gl1r1XV0SLw)

**63\. Typeahead and Autocomplete**

- 📖 Article: [Typeahead system design (System Design School)](https://systemdesignschool.io/problems/typeahead/solution)
- 🎥 Video: [Design autocomplete for Google search (Tushar Roy)](https://www.youtube.com/watch?v=us0qySiUsGU)

---

## Part X: Analytics and Probabilistic Data Structures

**Why it matters:** At very large scale, exact answers get expensive. These data structures trade a small, known error for a huge saving in memory.

**Interview signal:** “How do you count unique visitors across billions of events?”

**64\. Counting at Scale**

- 📖 Article: [Distributed counter system design](https://systemdesign.one/distributed-counter-system-design/)
- 🎥 Video: [Sharded counters (Arpit Vaish)](https://www.youtube.com/watch?v=Z-HZ7vysEj0)

**65\. HyperLogLog**

- 📖 Article: [HyperLogLog in system design](https://www.geeksforgeeks.org/system-design/hyperloglog-algorithm-in-system-design/)
- 🎥 Video: [HyperLogLog: counting distinct elements (Gaurav Sen)](https://www.youtube.com/watch?v=eV1haPUt0NU)

**66\. Count-Min Sketch and Top-K**

- 📖 Article: [Count-min sketch explained (Vivek Bansal)](https://vivekbansal.substack.com/p/count-min-sketch)
- 🎥 Video: [Count-min sketch (Tech Dummies)](https://www.youtube.com/watch?v=ibxXO-b14j4)

**67\. Sampling and Percentiles**

- 📖 Article: [Reservoir sampling](https://www.geeksforgeeks.org/dsa/reservoir-sampling/)
- 🎥 Video: [Reservoir sampling (Eric Laber)](https://www.youtube.com/watch?v=A1iwzSew5QY)

**68\. Time-Window Aggregation**

- 📖 Article: [Windowing in stream processing (RisingWave)](https://risingwave.com/blog/windowing-stream-processing-tumbling-sliding-session/)
- 🎥 Video: [Tumbling, sliding and session windows (Ease With Data)](https://www.youtube.com/watch?v=yq_gOzSQQY4)

**69\. Live Reactions at High Throughput**

- 📖 Article: [Design Facebook live comments (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/fb-live-comments)
- 🎥 Video: [Design live comments (Hello Interview)](https://www.youtube.com/watch?v=LjLx0fCd1k8)

---

## Part XI: Realtime, Social and Feeds

**Why it matters:** Feeds and chat are fan-out problems: one write and many readers, or many writes and one reader. Your choice decides where the cost lands.

**Interview signal:** “Do you build the feed when someone posts, or when someone opens the app?”

**70\. Realtime Communication**

- 📖 Article: [WebSockets vs SSE vs long polling (RxDB)](https://rxdb.info/articles/websockets-sse-polling-webrtc-webtransport.html)
- 🎥 Video: [WebSockets vs polling vs SSE (Piyush Garg)](https://www.youtube.com/watch?v=WS352jTTkPU)

**71\. Modeling a Social Graph**

- 📖 Article: [TAO: the power of the graph (Meta Engineering)](https://engineering.fb.com/2013/06/25/core-infra/tao-the-power-of-the-graph/)
- 🎥 Video: [TAO: Facebook’s social graph store (Gaurav Sen)](https://www.youtube.com/watch?v=Dg07kVN4U28)

**72\. Feed Generation**

- 📖 Article: [Feed system: pull, push and hybrid fanout](https://blog.rajpoot.dev/system-design/design-feed-system-2026/)
- 🎥 Video: [Design FB news feed (Hello Interview)](https://www.youtube.com/watch?v=Qj4-GruzyDU)

**73\. Unread Indicators and Live Commentary**

- 📖 Article: [Slack channel fan-out and unread counts](https://scalablesystem.dev/system-design/build-slacks-channel-message-fan-out-and-unread-counts)
- 🎥 Video: [Live streaming events like ESPN and Hotstar (Gaurav Sen)](https://www.youtube.com/watch?v=yKgWAHqmAwk)

---

## Part XII: Geospatial and Matching

**Why it matters:** “Nearby” is not a normal database query. Geospatial indexes turn a location on a map into something you can search quickly.

**Interview signal:** “How do you find the drivers closest to a rider?”

**74\. Geospatial Indexing**

- 📖 Article: [Geohashing and quadtrees](https://www.geeksforgeeks.org/system-design/geohashing-and-quadtrees-for-location-based-services/)
- 🎥 Video: [QuadTrees and Hilbert curves (Gaurav Sen)](https://www.youtube.com/watch?v=OcUKFIjhKu0)

**75\. Geofencing**

- 📖 Article: [Point in polygon (Wikipedia)](https://en.wikipedia.org/wiki/Point_in_polygon)
- 🎥 Video: [Ray casting algorithm (Inside code)](https://www.youtube.com/watch?v=RSXM9bgqxJM)

**76\. Matching and Recommendations**

- 📖 Article: [Candidate generation overview (Google)](https://developers.google.com/machine-learning/recommendation/overview/candidate-generation)
- 🎥 Video: [Recommendation system infra basics (Hello Interview)](https://www.youtube.com/watch?v=GncgOIiMII8)

**77\. Routing and ETA Computation**

- 📖 Article: [Traffic prediction with graph neural networks (DeepMind)](https://deepmind.google/blog/traffic-prediction-with-advanced-graph-neural-networks/)
- 🎥 Video: [Google Maps is unreasonably fast (Veritasium)](https://www.youtube.com/watch?v=kS-CGkiPetQ)

---

## Part XIII: Media, Files and Video

**Why it matters:** Large files change the design. Uploads go straight to object storage, and a video is processed into many versions before anyone watches it.

**Interview signal:** “A user uploads a 2 GB video on a slow connection. What happens?”

**78\. Direct-to-Object-Storage Uploads**

- 📖 Article: [Large uploads with S3 multipart upload (AWS)](https://aws.amazon.com/blogs/compute/uploading-large-objects-to-amazon-s3-using-multipart-upload-and-transfer-acceleration/)
- 🎥 Video: [S3 multipart upload with pre-signed URLs (Chandan Maurya)](https://www.youtube.com/watch?v=dfxXEQxJPzI)

**79\. Image Delivery**

- 📖 Article: [Resizing images with CloudFront and Lambda@Edge (AWS)](https://aws.amazon.com/blogs/networking-and-content-delivery/resizing-images-with-amazon-cloudfront-lambdaedge-aws-cdn-blog/)
- 🎥 Video: [How apps store images (Irtiza Hafiz)](https://www.youtube.com/watch?v=mVmIJ4hvTss)

**80\. Video Pipeline**

- 📖 Article: [Adaptive bitrate streaming explained (Mux)](https://www.mux.com/articles/adaptive-bitrate-streaming-guide)
- 🎥 Video: [HLS adaptive bitrate streaming (Piyush Garg)](https://www.youtube.com/watch?v=6JTV4PwisoQ)

**81\. Live Streaming**

- 📖 Article: [How WebRTC works (Cloudflare)](https://www.cloudflare.com/learning/video/how-webrtc-works/)
- 🎥 Video: [WebRTC in 100 seconds (Fireship)](https://www.youtube.com/watch?v=WmR9IMUD_CY)

**82\. File Sync**

- 📖 Article: [How Dropbox sync works](https://akshayghalme.com/blogs/how-dropbox-delta-sync-works/)
- 🎥 Video: [Block-level deduplication explained (MGDecodes)](https://www.youtube.com/watch?v=GXPpxBk_djA)

---

## Part XIV: Reliability and Operations

**Why it matters:** This is where your design meets reality. Observability, SLOs, safe deployments, and incident response are how you keep a system alive after launch.

**Interview signal:** “How would you know this system is broken before your users tell you?”

**83\. Observability**

- 📖 Article: [Three pillars of observability (IBM)](https://www.ibm.com/think/insights/observability-pillars)
- 🎥 Video: [Metrics, logs and traces (Tech Upskill)](https://www.youtube.com/watch?v=aJpzr8648XE)

**84\. SLOs and Error Budgets**

- 📖 Article: [Service level objectives (Google SRE book)](https://sre.google/sre-book/service-level-objectives/)
- 🎥 Video: [SLO vs SLI vs SLA vs error budget](https://www.youtube.com/watch?v=Akri1BlGp10)

**85\. Incident Response**

- 📖 Article: [Managing incidents (Google SRE book)](https://sre.google/sre-book/managing-incidents/)
- 🎥 Video: [Incident management in SRE](https://www.youtube.com/watch?v=NUmOZ3nnS7I)

**86\. Safe Deployments and Migrations**

- 📖 Article: [Blue-green, canary and rolling deployments (Harness)](https://www.harness.io/blog/blue-green-canary-deployment-strategies)
- 🎥 Video: [Top 5 deployment strategies (ByteByteGo)](https://www.youtube.com/watch?v=AWVTKBUnoIg)

**87\. Backups and Disaster Recovery**

- 📖 Article: [RTO vs RPO in system design](https://www.geeksforgeeks.org/system-design/recovery-time-objective-rto-vs-recovery-point-objective-rpo-in-system-design/)
- 🎥 Video: [RPO and RTO explained (AWS)](https://www.youtube.com/watch?v=rD3nBaS3OG4)

**88\. Multi-Region Architecture**

- 📖 Article: [Active-active vs active-passive multi-region design](https://www.designgurus.io/blog/active-active-vs-active-passive-architecture)
- 🎥 Video: [Active-active vs active-passive (Hussein Nasser)](https://www.youtube.com/watch?v=d-Bfi5qywFo)

**89\. Data Retention, Deletion and Privacy**

- 📖 Article: [Right to erasure: what to delete and when (ICO)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/)
- 🎥 Video: [Developing a data retention policy (AIIM)](https://www.youtube.com/watch?v=kVeSL0YR_ys)

**90\. Security and Abuse Prevention**

- 📖 Article: [OWASP Top 10](https://owasp.org/projects/top-ten)
- 🎥 Video: [OWASP Top 10 security risks (Telusko)](https://www.youtube.com/watch?v=wUaeKEl1RCw)

**91\. Multi-Tenant Design**

- 📖 Article: [SaaS and multitenant architecture (Azure)](https://learn.microsoft.com/en-us/azure/architecture/guide/saas-multitenant-solution-architecture/)
- 🎥 Video: [Multitenancy explained (IBM)](https://www.youtube.com/watch?v=60ccSmOxpMw)

**92\. Lessons from System Failures**

- 📖 Article: [How Facebook disappeared from the internet (Cloudflare)](https://blog.cloudflare.com/october-2021-facebook-outage/)
- 🎥 Video: [Why was Facebook down for five hours? (Ben Eater)](https://www.youtube.com/watch?v=-wMU8vmfaYo)

---

## Part XV: AI-Era System Design

**Why it matters:** An LLM adds new costs and new failure modes: expensive requests, very different response times, and answers that can be wrong while every dashboard looks healthy. The classic patterns still apply. The numbers change. For the seven patterns that come up most in AI interviews, read our earlier post, [System Design for AI Engineers](https://jamwithai.substack.com/p/system-design-for-ai-engineers-7).

**Interview signal:** “How would you protect your inference API from a sudden traffic spike?”

**93\. How AI Is Changing System Design**

- 📖 Article: [System design interviews in the age of AI](https://medium.com/@itlearningai/how-to-prepare-for-system-design-interviews-in-the-age-of-ai-2026-update-cae43717c1da)
- 🎥 Video: [What do they ask in an AI system design interview?](https://www.youtube.com/watch?v=icd5KdbtwxM)

**94\. Designing a ChatGPT-Like System**

- 📖 Article: [How ChatGPT system design works (Educative)](https://www.educative.io/blog/how-chatgpt-system-design-works)
- 🎥 Video: [System design of ChatGPT (sudoCODE)](https://www.youtube.com/watch?v=H9Qdm8_JBAs)

**95\. Data Infrastructure for AI/ML**

- 📖 Article: [What is a feature store? (Databricks)](https://www.databricks.com/blog/what-feature-store-complete-guide-ml-feature-engineering)
- 🎥 Video: [What is a feature store? (Hopsworks)](https://www.youtube.com/watch?v=DESBDukN9gw)

**96\. LLM-Powered Customer Support Bot**

- 📖 Article: [RAG-powered customer support chatbot](https://dev.to/pallavi_sharma_10c1a6f1da/how-to-build-a-rag-powered-customer-support-chatbot-with-python-and-llms-2ebd)
- 🎥 Video: [AI chatbot architecture: MVP to enterprise](https://www.youtube.com/watch?v=o7uMZkuegEE)

**97\. AI-Powered Code Assistant**

- 📖 Article: [How does GitHub Copilot work? (Educative)](https://www.educative.io/blog/how-does-github-copilot-work)
- 🎥 Video: [Under the hood of GitHub Copilot (Microsoft)](https://www.youtube.com/watch?v=EzP2HTD6wRM)

---

## Part XVI: Technology Deep Dives

**Why it matters:** Interviewers often ask you to name a technology and defend it. Know what each one is good at and, more importantly, what it is bad at.

**Interview signal:** “Why RabbitMQ here, and not Kafka?”

**98\. PostgreSQL**

- 📖 Article: [PostgreSQL architectural fundamentals (docs)](https://www.postgresql.org/docs/current/tutorial-arch.html)
- 🎥 Video: [PostgreSQL internal architecture (Hussein Nasser)](https://www.youtube.com/watch?v=Q56kljmIN14)

**99\. MySQL**

- 📖 Article: [InnoDB architecture (MySQL docs)](https://dev.mysql.com/doc/refman/8.4/en/innodb-architecture.html)
- 🎥 Video: [MySQL architecture (Code with Lucian)](https://www.youtube.com/watch?v=aKOaQfpW7to)

**100\. MongoDB**

- 📖 Article: [MongoDB architecture (MongoDB)](https://www.mongodb.com/resources/products/fundamentals/mongodb-architecture)
- 🎥 Video: [MongoDB in 100 seconds (Fireship)](https://www.youtube.com/watch?v=-bt_y4Loofg)

**101\. Redis**

- 📖 Article: [Redis explained (Architecture Notes)](https://architecturenotes.co/p/redis)
- 🎥 Video: [Redis in 100 seconds (Fireship)](https://www.youtube.com/watch?v=G1rOthIU-uo)

**102\. Memcached**

- 📖 Article: [What is Memcached?](https://www.geeksforgeeks.org/system-design/what-is-memcached/)
- 🎥 Video: [Memcached (Udacity)](https://www.youtube.com/watch?v=1MAgt0bFdwM)

**103\. DynamoDB**

- 📖 Article: [How DynamoDB works (AWS docs)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.html)
- 🎥 Video: [DynamoDB deep dive (Hello Interview)](https://www.youtube.com/watch?v=2X2SO3Y-af8)

**104\. Cassandra**

- 📖 Article: [Cassandra architecture (Apache docs)](https://cassandra.apache.org/doc/latest/cassandra/architecture/index.html)
- 🎥 Video: [Cassandra deep dive (Hello Interview)](https://www.youtube.com/watch?v=TD3-INhm60Q)

**105\. Elasticsearch**

- 📖 Article: [Elasticsearch architecture](https://www.geeksforgeeks.org/elasticsearch/elasticsearch-architecture/)
- 🎥 Video: [What is Elasticsearch? (IBM)](https://www.youtube.com/watch?v=ZP0NmfyfsoM)

**106\. RabbitMQ**

- 📖 Article: [AMQP 0-9-1 model explained (RabbitMQ docs)](https://www.rabbitmq.com/tutorials/amqp-concepts)
- 🎥 Video: [What is RabbitMQ? (IBM)](https://www.youtube.com/watch?v=7rkeORD4jSw)

**107\. Amazon SQS**

- 📖 Article: [Amazon SQS queue types (AWS docs)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-queue-types.html)
- 🎥 Video: [AWS SQS overview for beginners (Be A Better Dev)](https://www.youtube.com/watch?v=CyYZ3adwboc)

**108\. Apache Flink**

- 📖 Article: [What is Apache Flink? (AWS)](https://aws.amazon.com/what-is/apache-flink/)
- 🎥 Video: [What is Apache Flink? (Confluent)](https://www.youtube.com/watch?v=PVoc5tRr6to)

**109\. Apache Spark**

- 📖 Article: [Apache Spark architecture (InterviewBit)](https://www.interviewbit.com/blog/apache-spark-architecture/)
- 🎥 Video: [Learn Apache Spark in 10 minutes (Darshil Parmar)](https://www.youtube.com/watch?v=v_uodKAywXA)

**110\. AWS Lambda**

- 📖 Article: [How Lambda works (AWS docs)](https://docs.aws.amazon.com/lambda/latest/dg/concepts-basics.html)
- 🎥 Video: [Introduction to AWS Lambda (AWS)](https://www.youtube.com/watch?v=eOBq__h4OJ4)

**111\. Nginx**

- 📖 Article: [NGINX architecture (NGINX blog)](https://blog.nginx.org/nginx-architecture)
- 🎥 Video: [NGINX explained (TechWorld with Nana)](https://www.youtube.com/watch?v=iInUBOVeBCc)

**112\. ZooKeeper**

- 📖 Article: [What is Apache ZooKeeper?](https://www.geeksforgeeks.org/java/what-is-apache-zookeeper/)
- 🎥 Video: [ZooKeeper explained in 5 minutes (TechPrep)](https://www.youtube.com/watch?v=iHrsHqSAe18)

**113\. Docker**

- 📖 Article: [What is a container? (Docker)](https://www.docker.com/resources/what-container/)
- 🎥 Video: [Docker in 100 seconds (Fireship)](https://www.youtube.com/watch?v=Gjnup-PuquQ)

**114\. Kubernetes**

- 📖 Article: [Kubernetes components (docs)](https://kubernetes.io/docs/concepts/overview/components/)
- 🎥 Video: [Kubernetes explained in 6 minutes (ByteByteGo)](https://www.youtube.com/watch?v=TlHvYWVUZyc)

**115\. Prometheus**

- 📖 Article: [Prometheus overview (docs)](https://prometheus.io/docs/introduction/overview/)
- 🎥 Video: [How Prometheus monitoring works (TechWorld with Nana)](https://www.youtube.com/watch?v=h4Sl21AKiDg)

---

## Part XVII: “Design X” Walkthroughs

**Why it matters:** This is where everything comes together. Try each design yourself first, then watch the walkthrough and compare. You will learn more from the difference than from the video.

**Interview signal:** Every question in this part. Pick one a day and talk it through out loud, the way you would in the real interview.

**116\. URL Shortener**

- 📖 Article: [URL shortener system design](https://www.geeksforgeeks.org/system-design/system-design-url-shortening-service/)
- 🎥 Video: [Design a URL shortener (NeetCodeIO)](https://www.youtube.com/watch?v=qSJAvd5Mgio)

**117\. Product Listing / E-commerce (Amazon)**

- 📖 Article: [E-commerce system design](https://www.geeksforgeeks.org/system-design/e-commerce-architecture-system-design-for-e-commerce-website/)
- 🎥 Video: [E-commerce platform design (TechPrep)](https://www.youtube.com/watch?v=2811UT5r5Jk)

**118\. Notification System**

- 📖 Article: [Design a notification system](https://www.systemdesignhandbook.com/guides/design-a-notification-system/)
- 🎥 Video: [Notification service design (codeKarle)](https://www.youtube.com/watch?v=CUwt9_l0DOg)

**119\. Ticket Booking**

- 📖 Article: [Design Ticketmaster (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster)
- 🎥 Video: [Design Ticketmaster (Hello Interview)](https://www.youtube.com/watch?v=fhdPyoO6aXI)

**120\. Payment System**

- 📖 Article: [Design a payment system](https://www.systemdesignhandbook.com/guides/design-a-payment-system/)
- 🎥 Video: [Design a payment system (Code with Lucian)](https://www.youtube.com/watch?v=olfaBgJrUBI)

**121\. Search Service**

- 📖 Article: [Search engine system design (Educative)](https://www.educative.io/blog/search-engine-system-design)
- 🎥 Video: [Design a basic search engine (Interview Pen)](https://www.youtube.com/watch?v=0LTXCcVRQi0)

**122\. Recommendation System**

- 📖 Article: [System design for recommendations and search (Eugene Yan)](https://eugeneyan.com/writing/system-design-for-discovery/)
- 🎥 Video: [Design an ML recommendation engine (Interview Pen)](https://www.youtube.com/watch?v=FoSCaue3lcg)

**123\. Chat and Messaging**

- 📖 Article: [Design WhatsApp (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/whatsapp)
- 🎥 Video: [WhatsApp system design (Gaurav Sen)](https://www.youtube.com/watch?v=vvhC64hQZMk)

**124\. Social Feed (Twitter)**

- 📖 Article: [Designing Twitter](https://www.geeksforgeeks.org/interview-experiences/design-twitter-a-system-design-interview-question/)
- 🎥 Video: [Design Twitter (NeetCode)](https://www.youtube.com/watch?v=o5n85GRKuzk)

**125\. Q&A Platform (Quora)**

- 📖 Article: [System design: Quora (Educative)](https://www.educative.io/courses/grokking-the-system-design-interview/system-design-quora)
- 🎥 Video: [Design Quora mock interview (SDE Skills)](https://www.youtube.com/watch?v=LPO9rttyeNU)

**126\. Nearby Search (Yelp)**

- 📖 Article: [Design Yelp (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/yelp)
- 🎥 Video: [Design a location-based service (ByteByteGo)](https://www.youtube.com/watch?v=M4lR_Va97cQ)

**127\. Ride Matching (Uber)**

- 📖 Article: [Design Uber (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/uber)
- 🎥 Video: [Design Uber (Hello Interview)](https://www.youtube.com/watch?v=lsKU38RKQSo)

**128\. Google Maps**

- 📖 Article: [Designing Google Maps](https://www.geeksforgeeks.org/system-design/designing-google-maps-system-design/)
- 🎥 Video: [Google Maps system design (codeKarle)](https://www.youtube.com/watch?v=jk3yvVfNvds)

**129\. Video Platform (YouTube)**

- 📖 Article: [Design YouTube (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/youtube)
- 🎥 Video: [Design YouTube (NeetCode)](https://www.youtube.com/watch?v=jPKTo1iGQiE)

**130\. Photo Sharing (Instagram)**

- 📖 Article: [Design Instagram (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/instagram)
- 🎥 Video: [Designing Instagram (Gaurav Sen)](https://www.youtube.com/watch?v=QmX2NPkJTKg)

**131\. File Sync (Dropbox)**

- 📖 Article: [Design Dropbox (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/dropbox)
- 🎥 Video: [Design Dropbox or Google Drive (Hello Interview)](https://www.youtube.com/watch?v=_UZ1ngy-kOI)

**132\. Collaborative Editor (Google Docs)**

- 📖 Article: [Google Docs system design](https://www.systemdesignhandbook.com/guides/google-docs-system-design/)
- 🎥 Video: [Google Docs: operational transformation (Tech Dummies)](https://www.youtube.com/watch?v=2auwirNBvGg)

**133\. Online Judge (LeetCode)**

- 📖 Article: [Design LeetCode (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/leetcode)
- 🎥 Video: [Design LeetCode (Hello Interview)](https://www.youtube.com/watch?v=1xHADtekTNg)

**134\. Observability Platform**

- 📖 Article: [Metrics monitoring and alerting system](https://www.systemdesignsandbox.com/learn/design-metrics-monitoring)
- 🎥 Video: [Metrics monitoring and alerting design (TechPrep)](https://www.youtube.com/watch?v=T-8DgGQ7wUo)

**135\. Database Migration**

- 📖 Article: [Zero-downtime migrations: expand-contract pattern](https://drcodes.com/posts/zero-downtime-database-migrations-master-the-expand-contract-pattern)
- 🎥 Video: [Expand-contract pattern (Software Developer Diaries)](https://www.youtube.com/watch?v=ONSCQWLD9d0)

**136\. Pastebin**

- 📖 Article: [Design Pastebin](https://www.systemdesignhandbook.com/guides/design-pastebin/)
- 🎥 Video: [Design Pastebin (Jordan has no life)](https://www.youtube.com/watch?v=V_yOcipUqUE)

**137\. Team Chat (Slack)**

- 📖 Article: [Slack architecture (System Design One)](https://systemdesign.one/slack-architecture/)
- 🎥 Video: [Design a Slack-like chat app (ShowOffer)](https://www.youtube.com/watch?v=Zw36jSyMlZI)

**138\. Video Conferencing (Zoom)**

- 📖 Article: [Designing Zoom](https://www.geeksforgeeks.org/system-design/designing-zoom-system-design/)
- 🎥 Video: [WebRTC vs SFU vs MCU for video calls (Piyush Garg)](https://www.youtube.com/watch?v=Zaz6hYVm-WE)

**139\. Reddit**

- 📖 Article: [Design Reddit](https://www.geeksforgeeks.org/system-design/design-reddit-system-design/)
- 🎥 Video: [Design Reddit mock interview (Exponent)](https://www.youtube.com/watch?v=KYExYE_9nIY)

**140\. Dating App (Tinder)**

- 📖 Article: [Design Tinder (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/tinder)
- 🎥 Video: [Design Tinder (Hello Interview)](https://www.youtube.com/watch?v=18Fg5Akhkqw)

**141\. Music Streaming (Spotify)**

- 📖 Article: [Design Spotify (AlgoMaster)](https://blog.algomaster.io/p/design-spotify-system-design-interview)
- 🎥 Video: [Design Spotify (IGotAnOffer)](https://www.youtube.com/watch?v=_K-eupuDVEc)

**142\. Netflix**

- 📖 Article: [Netflix system design](https://www.geeksforgeeks.org/system-design/system-design-netflix-a-complete-architecture/)
- 🎥 Video: [Netflix system design (Tech Dummies)](https://www.youtube.com/watch?v=psQzyFfsUGU)

**143\. Live Streaming (Twitch)**

- 📖 Article: [Design a live streaming app like Twitch](https://www.geeksforgeeks.org/system-design/design-a-live-streaming-app-like-twitch-system-design/)
- 🎥 Video: [How live streaming platforms work (ByteByteGo)](https://www.youtube.com/watch?v=7AMRfNKwuYo)

**144\. Email Service (Gmail)**

- 📖 Article: [Distributed email service (book notes)](https://books.dwf.dev/docs/system-design/c24)
- 🎥 Video: [Email system design: SMTP, IMAP, POP3 (ByteMonk)](https://www.youtube.com/watch?v=aria5gmElSc)

**145\. Hotel Booking (Airbnb)**

- 📖 Article: [System design of Airbnb](https://www.geeksforgeeks.org/system-design/system-design-of-airbnb-hotel-reservation-system/)
- 🎥 Video: [Hotel booking system design (Scaler)](https://www.youtube.com/watch?v=ctDvzgZj6vw)

**146\. Food Delivery (DoorDash)**

- 📖 Article: [Design DoorDash](https://pushkarkumar-dev.github.io/system-design/doordash/)
- 🎥 Video: [System design of DoorDash (Gaurav Sen)](https://www.youtube.com/watch?v=iRhSAR3ldTw)

**147\. News Aggregator (Google News)**

- 📖 Article: [Design Google News (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/google-news)
- 🎥 Video: [News aggregator system design](https://www.youtube.com/watch?v=xRBLqs6Gij4)

**148\. Ad Click Aggregator**

- 📖 Article: [Design an ad click aggregator (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/ad-click-aggregator)
- 🎥 Video: [Design an ad click aggregator (Hello Interview)](https://www.youtube.com/watch?v=Zcv_899yqhI)

**149\. Multi-Tenant E-commerce (Shopify)**

- 📖 Article: [Multi-tenant architecture (Shopify)](https://www.shopify.com/blog/multi-tenant-architecture)
- 🎥 Video: [Shopify e-commerce system design (Success in Tech)](https://www.youtube.com/watch?v=lEL4F_0J3l8)

**150\. Online Auction (eBay)**

- 📖 Article: [Design an online auction](https://www.systemdesignhandbook.com/guides/design-online-auction/)
- 🎥 Video: [Bidding platform (Jordan has no life)](https://www.youtube.com/watch?v=3aX-lC5_P1M)

**151\. Digital Wallet**

- 📖 Article: [Design a digital wallet (Brijesh Patel)](https://brijesh.work/system-design/digital-wallet/)
- 🎥 Video: [Digital wallet design with saga (System Design Pal)](https://www.youtube.com/watch?v=8ByEyCd-MEM)

**152\. Stock Exchange**

- 📖 Article: [Design a stock exchange (ByteByteGo)](https://bytebytego.com/guides/design-stock-exchange/)
- 🎥 Video: [High-throughput stock exchange (Jordan has no life)](https://www.youtube.com/watch?v=dGYfpO3WJ1o)

**153\. Load Balancer**

- 📖 Article: [Load balancer: types, algorithms, examples](https://softwaresystemdesign.com/high-level-design/load-balancer/)
- 🎥 Video: [Load balancing the right way (Jordan has no life)](https://www.youtube.com/watch?v=PERKHUJYotM)

**154\. API Gateway**

- 📖 Article: [API gateways (AlgoMaster)](https://algomaster.io/learn/system-design/api-gateways)
- 🎥 Video: [API gateways in system design (Hello Interview)](https://www.youtube.com/watch?v=7-6F3b14baA)

**155\. Time-Series Database**

- 📖 Article: [What is a time series database? (AWS)](https://aws.amazon.com/what-is/time-series-database/)
- 🎥 Video: [How time series databases work (Hello Interview)](https://www.youtube.com/watch?v=Qd76ZmfRs_Q)

**156\. Distributed Lock Service (Chubby)**

- 📖 Article: [The Chubby lock service (Google paper)](https://static.googleusercontent.com/media/research.google.com/en//archive/chubby-osdi06.pdf)
- 🎥 Video: [The Chubby distributed lock service (Nabadeep Das)](https://www.youtube.com/watch?v=2YIDaTKwW4Q)

**157\. Likes Counting System**

- 📖 Article: [Designing a scalable likes counting system (AlgoMaster)](https://blog.algomaster.io/p/designing-a-scalable-likes-counting-system)
- 🎥 Video: [How Facebook and YouTube handle billions of likes (ByteMonk)](https://www.youtube.com/watch?v=LGOnP9Udffo)

**158\. Leaderboard**

- 📖 Article: [Leaderboard system design (System Design One)](https://systemdesign.one/leaderboard-system-design/)
- 🎥 Video: [Redis sorted sets explained (Redis)](https://www.youtube.com/watch?v=MUKlxdBQZ7g)

**159\. Top-K / Trending**

- 📖 Article: [Top K problem: heavy hitters](https://serhatgiydiren.com/system-design-interview-top-k-problem-heavy-hitters/)
- 🎥 Video: [Top K problem (heavy hitters)](https://www.youtube.com/watch?v=kx-XDoPjoHw)

**160\. CI/CD Pipeline**

- 📖 Article: [CI/CD pipeline system design](https://www.geeksforgeeks.org/system-design/cicd-pipeline-system-design/)
- 🎥 Video: [Design a CI/CD system (ShowOffer)](https://www.youtube.com/watch?v=y32PywFi7Ek)

**161\. Calendar System**

- 📖 Article: [Design Google Calendar](https://www.geeksforgeeks.org/system-design/system-design-design-google-calendar/)
- 🎥 Video: [Design Google Calendar (ShowOffer)](https://www.youtube.com/watch?v=b_gpaGfS9H8)

**162\. Online Chess**

- 📖 Article: [Design an online chess platform (Hello Interview)](https://www.hellointerview.com/learn/system-design/problem-breakdowns/online-chess)
- 🎥 Video: [Design online chess (ShowOffer)](https://www.youtube.com/watch?v=A7ISCoZab2I)

---

That’s the full guide. 162 concepts, from DNS to stock exchanges.

## When the follow-up question catches you

Here are some follow-up questions that tend to catch people, and where to look in this list:

- **“The payment service crashed after charging the card, but before saving the order.”** → Distributed transactions and the outbox pattern (#41, #42)
- **“Two workers grabbed the same lock.”** → Distributed locks, leases, and fencing tokens (#37)
- **“One celebrity account is melting a single shard.”** → Sharding, hot partitions, and fan-out (#24, #55, #72)
- **“Our retries made the outage worse.”** → Backoff with jitter, backpressure, and circuit breakers (#13, #14, #38)
- **“Users still see old data after an update.”** → Caching, consistency models, and replication (#29, #32, #33)
- **“The same message was processed twice.”** → Idempotency and exactly-once processing (#13, #43)
- **“A user asked us to delete all of their data.”** → Data retention, deletion, and privacy (#89)
- **“Our inference API slowed down during a traffic spike.”** → Protecting systems under load, rate limiting, and AI-era design (#14, #15, #93)

> **The larger lesson:** “Design X” is not a puzzle you memorise. It is a combination of pieces you already understand. The model, the database, the queue: each one is simple on its own. The system is how they behave together when 10,000 users show up.

Know a better article or video for any topic? Drop it in the comments and help the next engineer who comes looking.

If this guide helped you, share it with a friend who is preparing for system design interviews.

**For the next step, explore:**

- [System Design for AI Engineers: 7 patterns you should know in your interviews](https://jamwithai.substack.com/p/system-design-for-ai-engineers-7)
- [20 AI Engineering Concepts Explained](https://jamwithai.substack.com/p/20-ai-engineering-concepts-explained)
- [All GPU related concepts simply explained](https://jamwithai.substack.com/p/all-gpu-related-concepts-simply-explained)
- [LLM Inference 101](https://jamwithai.substack.com/p/llm-inference-101)

We hope this guide helps you with your system design preparation, and best of luck!

Until next time ❤️

---

**Want to learn to build a production RAG system?**

Do check out our **[Agentic RAG System Course](https://jamwithai.com/courses/rag/)**.
Hey there 👋,

We wanted to address some technical terms around GPUs. Imagine, you get a new GPU to run your AI model. You think it will be fast, but it is still slow.

So you add a second GPU. It does not help much.

**The GPU is working. So why is your model still slow?**

Sometimes the model needs more memory. Sometimes the GPU has to wait for data. And sometimes two GPUs spend too much time sending data to each other.

> A better GPU does not fix every problem. First, you need to know what is slowing the model down.

You may have seen words like **VRAM, BF16, and NVLink**. They look hard at first. But each one tells you something about how an AI model runs.

This guide explains **55+ GPU ideas** with simple words and clear pictures. You will learn what these words mean and why they are useful.

We will start with the basics. You can read the whole guide or save it and come back when you see a word you do not know.

---

You can also learn with these three videos:

🎥 **How a Production AI Agent System Actually Works**

See how a simple AI demo becomes an app that works well for real users.

![](https://www.youtube.com/watch?v=sKzL0wSN9vQ)

🎥 **AI Agent Memory: 7 Types Explained in 12 Minutes**

Learn the seven types of AI agent memory with one clear example.

![](https://www.youtube.com/watch?v=bK1clrG-boc)

🎥 **AI System Design: 7 Patterns Explained in 17 Minutes**

Learn important AI system design patterns used in AI applications in production.

![](https://www.youtube.com/watch?v=0jCss9xfOiw)

---

## The map before the terms

[![All GPU Concepts: an overview of GPU fundamentals, memory, compute, GPU generations, training and inference, multi-GPU, interconnects, and scaling.](https://substackcdn.com/image/fetch/$s_!CJe-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff198a93-b175-4fe7-949c-7d93d305b3c7_1586x992.png)](https://substackcdn.com/image/fetch/$s_!CJe-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff198a93-b175-4fe7-949c-7d93d305b3c7_1586x992.png)

All GPU Concepts: an overview of GPU fundamentals, memory, compute, GPU generations, training and inference, multi-GPU, interconnects, and scaling.

The terms are grouped into eight areas:

1. **GPU fundamentals:** CPU, GPU, CUDA Cores, Tensor Cores, threads, warps, and kernels.
2. **Memory:** VRAM, HBM, memory bandwidth, caches, model weights, activations, and KV cache.
3. **Compute:** FLOPS, FP32, BF16, FP16, FP8, FP4, INT8, INT4, mixed precision, and quantization.
4. **GPU generations:** V100, A100, H100, H200, B100, B200, and the architectures behind them.
5. **Training and inference:** LLM training, inference, batch size, GPU utilization, and common workload limits.
6. **Multi-GPU:** Model sharding, Data Parallelism, Tensor Parallelism, Pipeline Parallelism, and communication overhead.
7. **Interconnects:** PCIe, NVLink, NVSwitch, NCCL, AllReduce, and inter-GPU bandwidth.
8. **Scaling:** Single-GPU, multi-GPU, distributed training, GPU clusters, bottlenecks, and scaling efficiency.

You do not need to memorize all of them.

> The goal is simply to have a reference you can return to when you encounter terms like **HBM, FP8, NVLink, Tensor Parallelism, or NCCL** and think:
> 
> *“Wait, what does that mean again?”*

---

### Meet me at NVIDIA GTC Berlin

![Official NVIDIA GTC Berlin event artwork](https://substackcdn.com/image/fetch/$s_!lLTs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe50e4de0-ab02-4153-a332-b2a014eb7710_960x540.jpeg)

Official NVIDIA GTC Berlin event artwork

Since we are talking about NVIDIA GPUs, here is a date to keep in mind: **NVIDIA GTC is coming to Berlin on October 20–22, 2026.**

Over the coming weeks and during GTC, I’ll share what I find, session by session.

Can’t make it in person? [Jensen Huang’s keynote on October 21](https://www.nvidia.com/en-eu/gtc/keynote/) will stream for free. You do not need to register to watch it online.

**[Register here for GTC Berlin](https://nvda.ws/3RLDajN)**

If you’re coming to GTC Berlin, let’s connect 😇  
Drop a comment or send me a DM.

---

## 1\. GPU Fundamentals

Before talking about H100s, CUDA, or Tensor Cores, we need to understand why GPUs became so important for AI in the first place.

### 1.1 CPU

A **CPU (Central Processing Unit)** is designed to handle many different kinds of tasks.

Your operating system, browser, database, Python program, and API server all depend heavily on CPUs.

CPUs have a relatively small number of powerful cores. They are very good at workloads where instructions need to happen one after another.

Think of a CPU as having a few highly skilled workers who can each handle complicated jobs.

[![CPU diagram](https://substackcdn.com/image/fetch/$s_!rVfA!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F181cd74c-6876-4d92-9be5-fefaa080ca7b_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!rVfA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F181cd74c-6876-4d92-9be5-fefaa080ca7b_2400x1160.png)

CPU diagram

---

### 1.2 GPU

A **GPU (Graphics Processing Unit)** takes a different approach.

Instead of having a few powerful cores, a GPU contains many smaller processing units that can perform large numbers of calculations at the same time.

Originally, this was useful for graphics. Rendering an image requires calculating millions of pixels, and many of those calculations can happen independently.

AI happens to have a similar property.

Neural networks perform huge numbers of mathematical operations that can often run in parallel.

[![GPU diagram](https://substackcdn.com/image/fetch/$s_!d5yr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88ffb948-2ee0-469f-b4ad-eb31d63ee513_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!d5yr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F88ffb948-2ee0-469f-b4ad-eb31d63ee513_2400x1160.png)

GPU diagram

---

### 1.3 Parallel Computing

Suppose you need to perform 10,000 similar calculations.

A CPU might process a smaller number of them at once.  
A GPU can process a much larger number simultaneously.

This is **parallel computing**.

It is one of the main reasons GPUs are so effective for neural networks.

[![Parallel Computing diagram](https://substackcdn.com/image/fetch/$s_!WDRz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F383f2dd9-d0bb-4d62-937e-1bf8cab7a42a_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!WDRz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F383f2dd9-d0bb-4d62-937e-1bf8cab7a42a_2400x1160.png)

Parallel Computing diagram

---

### 1.4 Matrix and Tensor Operations

Most neural network computation eventually becomes operations on large collections of numbers.

A **matrix** is a two-dimensional grid of numbers.  
A **tensor** is a more general structure that can have one, two, three, or many dimensions.

Model weights, activations, embeddings, and input batches are all commonly represented using tensors.

When an LLM runs, it repeatedly transforms input tensors through matrix multiplication, activations, and further matrix operations to produce an output.

GPUs are extremely good at performing these operations in parallel.

That is the fundamental reason GPUs became the main compute engine behind modern AI.

[![Matrix and Tensor Operations diagram](https://substackcdn.com/image/fetch/$s_!v_eP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e86ce9e-03b1-4c1c-ae12-4b75b233397d_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!v_eP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e86ce9e-03b1-4c1c-ae12-4b75b233397d_2400x1160.png)

Matrix and Tensor Operations diagram

---

### 1.5 Streaming Multiprocessor (SM)

An NVIDIA GPU is divided into groups called **Streaming Multiprocessors**, usually shortened to **SMs**.

You can think of an SM as one major execution unit inside the GPU.

Each SM contains resources for running many calculations simultaneously, including CUDA Cores, Tensor Cores, registers, and cache.

A GPU contains many SMs, allowing large amounts of work to happen in parallel.

[![Streaming Multiprocessor (SM) diagram](https://substackcdn.com/image/fetch/$s_!FNW1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94e6ee11-bc49-4111-889c-1dc4bbed6915_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!FNW1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F94e6ee11-bc49-4111-889c-1dc4bbed6915_2400x1160.png)

Streaming Multiprocessor (SM) diagram

---

### 1.6 CUDA Cores

**CUDA Cores** are arithmetic units inside NVIDIA GPUs.

They perform operations such as addition and multiplication.

Large numbers of these operations can run simultaneously across the GPU.

But modern AI workloads have an even more specialized piece of hardware.

[![CUDA Cores diagram](https://substackcdn.com/image/fetch/$s_!4igs!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f37afbf-7db8-469e-a91d-6eb6d14c6da6_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!4igs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f37afbf-7db8-469e-a91d-6eb6d14c6da6_2400x1160.png)

CUDA Cores diagram

---

### 1.7 Tensor Cores

**Tensor Cores** are specialized units designed to accelerate matrix operations.

And matrix multiplication is everywhere in deep learning.

For example, Tensor Cores accelerate the large matrix multiplications inside LLM layers.

Tensor Cores are particularly important for lower-precision formats such as FP16, BF16, FP8, and newer formats supported by recent GPU generations.

[![Tensor Cores diagram](https://substackcdn.com/image/fetch/$s_!CNiu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77c71de4-295c-41eb-99ad-a7e8a8aa75ab_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!CNiu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77c71de4-295c-41eb-99ad-a7e8a8aa75ab_2400x1160.png)

Tensor Cores diagram

---

### 1.8 Threads

A **thread** is one small unit of work executed by the GPU.

Instead of asking the GPU to perform one huge calculation sequentially, a workload can create many threads.

This is how the GPU turns a large problem into many smaller pieces of work.

[![Threads diagram](https://substackcdn.com/image/fetch/$s_!SdGv!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8e799c7-2936-40e4-b2b5-80edfd1243a1_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!SdGv!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb8e799c7-2936-40e4-b2b5-80edfd1243a1_2400x1160.png)

Threads diagram

---

### 1.9 Warps

NVIDIA GPUs do not normally execute every thread completely independently.

Threads are organized into groups called **warps**.

A warp contains **32 threads** that execute instructions together.

You do not need to manage warps manually when simply running PyTorch or serving an LLM, but the concept helps explain how NVIDIA GPUs organize parallel execution.

[![Warps diagram](https://substackcdn.com/image/fetch/$s_!9kCr!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6109996-4e62-4986-aefd-adc30f4e4aa9_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!9kCr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6109996-4e62-4986-aefd-adc30f4e4aa9_2400x1160.png)

Warps diagram

---

### 1.10 CUDA Kernels

A **CUDA kernel** is a function that runs on the GPU.

For example, an operation such as matrix multiplication may launch a CUDA kernel across many GPU threads.

The flow starts in Python or PyTorch: a GPU operation is requested, a CUDA kernel launches across many threads, and the operation returns a result.

Most AI engineers do not write CUDA kernels themselves.

Frameworks and libraries such as PyTorch and CUDA libraries handle much of this work.

The useful mental model is:

**GPU → SMs → CUDA/Tensor Cores → threads and warps executing CUDA kernels.**

[![CUDA Kernels diagram](https://substackcdn.com/image/fetch/$s_!-ekp!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98a609b3-0660-4ebc-84c5-85d17c888f46_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!-ekp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98a609b3-0660-4ebc-84c5-85d17c888f46_2400x1160.png)

CUDA Kernels diagram

---

## 2\. GPU Memory

Compute is only half of the GPU story.

The other half is memory.

You can have an extremely fast GPU and still be unable to run a model because the workload does not fit into GPU memory.

---

### 2.1 VRAM

**VRAM** is the memory available to the GPU.

When you load an LLM onto a GPU, its model weights need to be stored somewhere.

That somewhere is GPU memory, commonly referred to as VRAM.

If the workload requires more memory than your GPU provides, you may encounter:

```markup
CUDA out of memory
```

This is commonly called a **CUDA OOM** error.

[![VRAM diagram](https://substackcdn.com/image/fetch/$s_!vMjP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f103dec-ec0d-4873-8e47-d0773af5b01a_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!vMjP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2f103dec-ec0d-4873-8e47-d0773af5b01a_2400x1160.png)

VRAM diagram

---

### 2.2 HBM

High-end AI GPUs commonly use **HBM: High Bandwidth Memory**.

HBM is designed to move very large amounts of data quickly between GPU memory and the compute units.

This matters because AI workloads constantly need to read and write large tensors.

[![HBM diagram](https://substackcdn.com/image/fetch/$s_!_fjH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65b98a4d-afc6-4260-b1c7-7264851695ed_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!_fjH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F65b98a4d-afc6-4260-b1c7-7264851695ed_2400x1160.png)

HBM diagram

---

### 2.3 Memory Bandwidth

**Memory bandwidth** tells us how quickly data can move between GPU memory and the compute units.

Memory capacity and memory bandwidth are different.

Imagine a warehouse.

**Capacity** tells you how many boxes the warehouse can hold.

**Bandwidth** tells you how quickly those boxes can move in and out.

AI workloads care about both.

A GPU might have enough memory to hold a model but still spend significant time waiting for data to reach its compute units.

[![Memory Bandwidth diagram](https://substackcdn.com/image/fetch/$s_!hmWH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0b9aecb-ebbe-43f6-aacb-ea1264ab086f_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!hmWH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff0b9aecb-ebbe-43f6-aacb-ea1264ab086f_2400x1160.png)

Memory Bandwidth diagram

---

### 2.4 GPU Memory Hierarchy

Not all GPU memory is equally fast.

A simplified **memory hierarchy** moves from registers to L1 cache, L2 cache, and finally HBM / VRAM.

[![GPU Memory Hierarchy diagram](https://substackcdn.com/image/fetch/$s_!KgLT!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d565eaa-3d50-43d2-bd22-9a61bbd57efa_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!KgLT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5d565eaa-3d50-43d2-bd22-9a61bbd57efa_2400x1160.png)

GPU Memory Hierarchy diagram

---

#### Registers

**Registers** are extremely fast storage located very close to the GPU’s compute units.

They are small, but data stored there can be accessed very quickly.

[![Registers diagram](https://substackcdn.com/image/fetch/$s_!bNGR!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa8323c0-0512-439c-bda9-db7e0599a975_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!bNGR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa8323c0-0512-439c-bda9-db7e0599a975_2400x1160.png)

Registers diagram

---

#### L1 Cache

**L1 cache** is small, fast memory associated closely with the SMs.

It helps avoid repeatedly fetching frequently needed data from slower memory.

[![L1 Cache diagram](https://substackcdn.com/image/fetch/$s_!YZc_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd74c03db-be04-4b67-b739-d65ff1c81f25_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!YZc_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd74c03db-be04-4b67-b739-d65ff1c81f25_2400x1160.png)

L1 Cache diagram

---

#### L2 Cache

**L2 cache** is larger and shared more broadly across the GPU.

It sits between the SM-level caches and the GPU’s main memory.

[![L2 Cache diagram](https://substackcdn.com/image/fetch/$s_!yiom!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3f964b7-b87f-4967-b43a-3ca37c7a5bfa_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!yiom!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3f964b7-b87f-4967-b43a-3ca37c7a5bfa_2400x1160.png)

L2 Cache diagram

---

#### HBM / VRAM

HBM provides much greater capacity than registers and caches, but accessing it is slower.

The general idea is simple:

**Closer memory → smaller and faster**

**Farther memory → larger and slower**

[![HBM / VRAM diagram](https://substackcdn.com/image/fetch/$s_!qtHb!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdf609c7-4db6-4310-a736-b0d5160ec089_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!qtHb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdf609c7-4db6-4310-a736-b0d5160ec089_2400x1160.png)

HBM / VRAM diagram

---

### 2.5 Model Weights

**Model weights** are the learned parameters of the neural network.

When you hear:

```markup
7B model
70B model
405B model
```

the “B” refers to billions of parameters.

Those parameters consume GPU memory.

For example, a 7-billion-parameter model using FP16 requires roughly:

```markup
7 billion parameters
×
2 bytes per parameter
≈
14 GB
```

just for the model weights.

That does not include all the additional memory required while running or training the model.

[![Model Weights diagram](https://substackcdn.com/image/fetch/$s_!Zs3G!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F706f1146-bf51-49a5-9a81-c274d1ac1504_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!Zs3G!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F706f1146-bf51-49a5-9a81-c274d1ac1504_2400x1160.png)

Model Weights diagram

---

### 2.6 Activations

**Activations** are intermediate values created as data moves through the neural network.

During training, activations can consume substantial GPU memory because many of them need to be retained for the backward pass.

This is one reason training usually requires much more memory than simply storing model weights.

[![Activations diagram](https://substackcdn.com/image/fetch/$s_!-xEd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2f7561c-c7b2-4ad9-9c5c-179d9e3fd51e_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!-xEd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe2f7561c-c7b2-4ad9-9c5c-179d9e3fd51e_2400x1160.png)

Activations diagram

---

### 2.7 KV Cache

During LLM inference, another important consumer of memory is the **KV cache**.

When an LLM generates tokens, it needs information from previously processed tokens.

Instead of recomputing everything for every new token, the model stores useful intermediate values in the KV cache.

This makes generation faster.

But the KV cache grows as:

- context length increases
- batch size increases
- more requests are served simultaneously

So an inference server can run out of GPU memory even when the model weights fit comfortably.

The important distinction is:

**Model size determines part of your memory requirement. Your workload determines the rest.**

[![KV Cache diagram](https://substackcdn.com/image/fetch/$s_!Eg7I!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c126f7b-3757-41ce-a3e2-dc0fd5fa99e0_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!Eg7I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c126f7b-3757-41ce-a3e2-dc0fd5fa99e0_2400x1160.png)

KV Cache diagram

---

## 3\. GPU Compute and Numerical Precision

When GPUs perform calculations, numbers must be represented using some numerical format.

Common formats include:

```markup
FP32
TF32
BF16
FP16
FP8
FP4
INT8
INT4
```

Generally, fewer bits mean less memory per value and potentially faster computation on hardware that supports that format.

---

### 3.1 FP32

**FP32** uses 32 bits to represent a floating-point number.

It provides relatively high numerical precision but requires more memory than smaller formats.

Historically, FP32 was common for neural-network training.

Modern AI workloads increasingly use lower precision where possible.

[![FP32 diagram](https://substackcdn.com/image/fetch/$s_!KkMd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa97f2c2c-2807-4241-b299-c7ce81562121_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!KkMd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa97f2c2c-2807-4241-b299-c7ce81562121_2400x1160.png)

FP32 diagram

---

### 3.2 TF32

**TF32, or TensorFloat-32**, is an NVIDIA format designed to accelerate certain deep-learning calculations on Tensor Cores while keeping a numerical range similar to FP32.

For beginners, the important idea is that TF32 helps existing FP32-style workloads take advantage of faster Tensor Core computation.

TF32 speeds up supported matrix calculations while values remain stored as FP32, so enabling TF32 does not halve model memory.

[![TF32 diagram](https://substackcdn.com/image/fetch/$s_!IIdz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e9ff3c3-99bf-4d46-877e-431881fd595c_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!IIdz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e9ff3c3-99bf-4d46-877e-431881fd595c_2400x1160.png)

TF32 diagram

---

### 3.3 FP16 and BF16

**FP16** and **BF16** both use 16 bits.

That means values require roughly half the storage of FP32 values.

BF16 has become particularly common in modern LLM training because its numerical range makes it convenient for large neural networks.

[![FP16 and BF16 diagram](https://substackcdn.com/image/fetch/$s_!DAkq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04476f9f-ac77-4611-ba39-151b7b5e9677_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!DAkq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04476f9f-ac77-4611-ba39-151b7b5e9677_2400x1160.png)

FP16 and BF16 diagram

---

### 3.4 FP8

Newer GPUs increasingly support **FP8** computation.

Using 8 bits reduces memory requirements further and allows supported hardware to perform more operations.

FP8 can therefore improve both memory efficiency and compute throughput for suitable AI workloads.

[![FP8 diagram](https://substackcdn.com/image/fetch/$s_!CuU1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd605ebf5-7b24-438d-b36b-14f09cfb6edb_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!CuU1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd605ebf5-7b24-438d-b36b-14f09cfb6edb_2400x1160.png)

FP8 diagram

---

### 3.5 FP4, INT8 and INT4

Even lower precision can be useful, especially during inference.

**INT8** uses 8-bit integers.  
**INT4** uses 4-bit integers.  
**FP4** represents floating-point values using only 4 bits.

Lower precision can dramatically reduce the memory required to store and process a model.

But reducing precision too aggressively can affect model quality.

[![FP4, INT8 and INT4 diagram](https://substackcdn.com/image/fetch/$s_!hh8Z!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3943d9d8-a35f-4786-a482-ad64fffc8fe6_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!hh8Z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3943d9d8-a35f-4786-a482-ad64fffc8fe6_2400x1160.png)

FP4, INT8 and INT4 diagram

---

### 3.6 Mixed Precision

Modern AI systems often use **mixed precision**.

Instead of forcing every calculation to use the same numerical format, different parts of the workload can use different precisions.

For example, some operations might use BF16 while others retain FP32 where additional precision is useful.

The goal is:

**Use lower precision where it is safe, while keeping higher precision where it is needed.**

[![Mixed Precision diagram](https://substackcdn.com/image/fetch/$s_!XQLM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd06457d-ebc8-48d8-abd4-15493e409387_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!XQLM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd06457d-ebc8-48d8-abd4-15493e409387_2400x1160.png)

Mixed Precision diagram

---

### 3.7 Quantization

**Quantization** reduces the precision used to represent model values.

For example, a model stored in FP16 can be quantized to INT8 or INT4.

This can significantly reduce memory requirements.

A model that previously needed multiple GPUs may sometimes fit on fewer GPUs after quantization.

The trade-off is that aggressive quantization can affect model quality.

[![Quantization diagram](https://substackcdn.com/image/fetch/$s_!gYTq!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfaf671e-9764-429b-a2bc-32cf972385e2_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!gYTq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdfaf671e-9764-429b-a2bc-32cf972385e2_2400x1160.png)

Quantization diagram

---

### 3.8 FLOPS

GPU compute performance is often described using **FLOPS: Floating Point Operations Per Second**.

Higher FLOPS means the hardware can theoretically perform more floating-point operations every second.

But FLOPS alone does not tell you how fast an LLM will run.

Performance can also be limited by:

- memory bandwidth
- GPU communication
- model architecture
- batch size
- software efficiency

So theoretical GPU compute and real LLM performance are not the same thing.

[![FLOPS diagram](https://substackcdn.com/image/fetch/$s_!kgdk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa405b1cd-e606-4c25-b3cf-7b0d9df366ad_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!kgdk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa405b1cd-e606-4c25-b3cf-7b0d9df366ad_2400x1160.png)

FLOPS diagram

---

## 4\. NVIDIA GPU Generations

You will frequently see names such as:

```markup
V100
A100
H100
H200
B100
B200
```

Instead of memorizing specifications for every GPU, it is more useful to understand the major generations.

---

### 4.1 Volta: V100

**Volta** is the NVIDIA architecture behind the **V100**.

One of Volta’s most important contributions to AI was the introduction of Tensor Cores.

This marked a major shift toward GPU hardware specifically optimized for neural-network computation.

[![Volta: V100 diagram](https://substackcdn.com/image/fetch/$s_!OSmL!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a1019c0-31c6-4f9f-b1b2-94d1d194b85c_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!OSmL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a1019c0-31c6-4f9f-b1b2-94d1d194b85c_2400x1160.png)

Volta: V100 diagram

---

### 4.2 Ampere: A100

The **A100** belongs to NVIDIA’s **Ampere** generation.

It became one of the most widely used GPUs for large-scale AI training and inference.

Ampere improved Tensor Core performance and support for lower-precision AI computation.

For several years, A100 clusters became a common reference point for large AI workloads.

[![Ampere: A100 diagram](https://substackcdn.com/image/fetch/$s_!dcV1!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40af37f6-9f9e-4d2e-9ca5-2bdee27b773c_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!dcV1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F40af37f6-9f9e-4d2e-9ca5-2bdee27b773c_2400x1160.png)

Ampere: A100 diagram

---

### 4.3 Hopper: H100 and H200

The **H100** belongs to NVIDIA’s **Hopper** generation.

Hopper introduced improvements designed specifically for transformer workloads, including the Transformer Engine and strong FP8 support.

The **H200** builds on Hopper while providing more HBM capacity and bandwidth than H100 variants.

That additional memory is particularly useful for large models.

[![Hopper: H100 and H200 diagram](https://substackcdn.com/image/fetch/$s_!xJ9G!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03fd608a-5689-465c-8981-88241f1df14c_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!xJ9G!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F03fd608a-5689-465c-8981-88241f1df14c_2400x1160.png)

Hopper: H100 and H200 diagram

---

### 4.4 Blackwell: B100 and B200

**Blackwell** followed Hopper.

The **B100** and **B200** continue the trend toward higher AI throughput, more memory capability, faster communication, and stronger support for low-precision computation.

The exact specifications change with each generation.

The broader pattern combines more compute, more GPU memory, more memory bandwidth, faster interconnects, and better low-precision support.

That is the direction modern AI GPUs continue to move.

[![Blackwell: B100 and B200 diagram](https://substackcdn.com/image/fetch/$s_!Ivj9!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F32c62a62-3684-495f-a282-9fc28f5851ca_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!Ivj9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F32c62a62-3684-495f-a282-9fc28f5851ca_2400x1160.png)

Blackwell: B100 and B200 diagram

---

## 5\. LLM Training and Inference

We often say a GPU is being used “for an LLM.”

But **LLM training** and **LLM inference** place very different demands on the GPU.

---

### 5.1 LLM Training

During **LLM training**, the model learns its parameters.

A training step runs a forward pass on the input, calculates the loss, runs a backward pass to calculate gradients, and updates the weights.

Training therefore needs memory for much more than model weights.

Depending on the training method, GPU memory may contain:

- model weights
- activations
- gradients
- optimizer states

That is why training a large model can require many GPUs even when its weights alone could fit on fewer GPUs.

[![LLM Training diagram](https://substackcdn.com/image/fetch/$s_!s6-n!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55e92939-4bb8-4fd9-928b-34a5e1a3e120_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!s6-n!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55e92939-4bb8-4fd9-928b-34a5e1a3e120_2400x1160.png)

LLM Training diagram

---

### 5.2 LLM Inference

**LLM inference** happens after the model has been trained.

You provide a prompt and ask the model to generate tokens.

Inference does not need the same gradient and optimizer storage required by full training.

But it introduces other challenges, especially KV-cache memory and serving many users simultaneously.

[![LLM Inference diagram](https://substackcdn.com/image/fetch/$s_!hvSX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4708927-09a8-4c79-b966-175e719bf88f_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!hvSX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4708927-09a8-4c79-b966-175e719bf88f_2400x1160.png)

LLM Inference diagram

---

### 5.3 Batch Size

**Batch size** describes how many inputs are processed together.

Larger batches can improve GPU utilization because the GPU receives more parallel work.

But larger batches also consume more memory.

Finding the right batch size is therefore often a trade-off between throughput and available memory.

[![Batch Size diagram](https://substackcdn.com/image/fetch/$s_!69MC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31afb699-7247-47e2-b9eb-0b0674871237_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!69MC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F31afb699-7247-47e2-b9eb-0b0674871237_2400x1160.png)

Batch Size diagram

---

### 5.4 GPU Utilization

**GPU utilization** is a measure of how busy the GPU is. In common tools such as `nvidia-smi`, it reports the percentage of time the GPU was running at least one kernel. A reading of 100% does not necessarily mean it is using all its computing capacity.

Buying a powerful GPU does not guarantee high performance.

If your application cannot feed work to the GPU quickly enough, much of that expensive hardware can sit idle.

[![GPU Utilization diagram](https://substackcdn.com/image/fetch/$s_!uOuC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95bbee4c-80da-4c55-bb79-cbc319ec162b_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!uOuC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F95bbee4c-80da-4c55-bb79-cbc319ec162b_2400x1160.png)

GPU Utilization diagram

---

### 5.5 Compute-Bound Workloads

A workload is **compute-bound** when performance is mainly limited by how quickly the GPU can perform calculations.

In this situation, additional compute capability can improve performance.

[![Compute-Bound Workloads diagram](https://substackcdn.com/image/fetch/$s_!q288!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F449d2cc2-6b25-4698-8941-c0ba93865371_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!q288!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F449d2cc2-6b25-4698-8941-c0ba93865371_2400x1160.png)

Compute-Bound Workloads diagram

---

### 5.6 Memory-Bound Workloads

A workload is **memory-bound** when performance is mainly limited by how quickly data can move between GPU memory and the compute units.

In that situation, adding more theoretical FLOPS may not help much.

This is why GPU specifications need to be considered together:

**Compute tells us how quickly calculations can happen. Memory bandwidth tells us how quickly we can feed data into those calculations.**

[![Memory-Bound Workloads diagram](https://substackcdn.com/image/fetch/$s_!kAIY!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4b362c1-f8ec-4590-b991-ee91733089fa_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!kAIY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4b362c1-f8ec-4590-b991-ee91733089fa_2400x1160.png)

Memory-Bound Workloads diagram

---

## 6\. From One GPU to Multiple GPUs

Eventually, a model or workload may become too large for one GPU.

Suppose your workload needs 120 GB of GPU memory but each GPU provides only 80 GB.

One solution is to use multiple GPUs.

But that introduces a new question:

**How do we divide the work between them?**

---

### 6.1 Model Sharding

**Model sharding** means splitting a model across multiple GPUs.

Each GPU stores part of the model, rather than the entire model.

Different parallelism techniques determine how this work is divided.

[![Model Sharding diagram](https://substackcdn.com/image/fetch/$s_!FACu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96d263c9-23cb-4678-aa6e-b02a24f77999_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!FACu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F96d263c9-23cb-4678-aa6e-b02a24f77999_2400x1160.png)

Model Sharding diagram

---

### 6.2 Data Parallelism

With **Data Parallelism (DP)**, multiple GPUs hold copies of the model but process different batches of training data.

During training, the GPUs combine their gradients so each model copy receives a consistent update.

Data Parallelism is useful when the model fits on each GPU but you want to process more training data simultaneously.

[![Data Parallelism diagram](https://substackcdn.com/image/fetch/$s_!cF8Q!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2347e3d-dbd9-4b64-9282-fed2676c76df_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!cF8Q!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb2347e3d-dbd9-4b64-9282-fed2676c76df_2400x1160.png)

Data Parallelism diagram

---

### 6.3 Tensor Parallelism

With **Tensor Parallelism (TP)**, individual tensor operations are divided across GPUs.

Imagine a very large matrix multiplication.

Multiple GPUs perform parts of that operation and combine or exchange their results.

This allows one model operation to use the compute and memory resources of multiple GPUs.

The downside is that the GPUs frequently need to exchange intermediate results.

[![Tensor Parallelism diagram](https://substackcdn.com/image/fetch/$s_!tdEC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F607a062e-fb64-45b1-9387-177afbae081c_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!tdEC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F607a062e-fb64-45b1-9387-177afbae081c_2400x1160.png)

Tensor Parallelism diagram

---

### 6.4 Pipeline Parallelism

With **Pipeline Parallelism (PP)**, different groups of model layers run on different GPUs.

For example, one GPU might hold layers 1–20, a second layers 21–40, and a third layers 41–60.

The output from one GPU becomes the input to the next.

You can think of this as an assembly line for model layers.

[![Pipeline Parallelism diagram](https://substackcdn.com/image/fetch/$s_!DuRu!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73915035-fb99-475a-9dba-c79a025ffd03_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!DuRu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73915035-fb99-475a-9dba-c79a025ffd03_2400x1160.png)

Pipeline Parallelism diagram

---

### 6.5 Model Parallelism

**Model parallelism** is the broader idea of distributing one model across multiple GPUs.

Tensor Parallelism and Pipeline Parallelism are two ways of doing this.

Large training systems often combine **Data Parallelism, Tensor Parallelism, and Pipeline Parallelism**.

This allows very large models to use hundreds or thousands of GPUs.

[![Model Parallelism diagram](https://substackcdn.com/image/fetch/$s_!uFyZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac5d4b50-35ef-4a59-bdc2-7d60e01bee4e_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!uFyZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac5d4b50-35ef-4a59-bdc2-7d60e01bee4e_2400x1160.png)

Model Parallelism diagram

---

### 6.6 Communication Overhead

Multiple GPUs introduce **communication overhead**.

If GPU 1 calculates something that GPU 2 needs, that result has to move between the GPUs.

The more frequently GPUs need to communicate, the more time can be spent moving data instead of performing useful computation.

More GPUs bring both more compute and more communication.

This is why doubling the number of GPUs does not automatically double performance.

[![Communication Overhead diagram](https://substackcdn.com/image/fetch/$s_!hNn5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6dfcac1-2403-4164-b74f-fa9dc863b279_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!hNn5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc6dfcac1-2403-4164-b74f-fa9dc863b279_2400x1160.png)

Communication Overhead diagram

---

## 7\. GPU Interconnects and Communication

Once multiple GPUs work together, the connections between them become part of the performance equation.

---

### 7.1 PCIe

**PCIe** is a standard interface used to connect GPUs and many other devices inside computers and servers.

GPUs can communicate through PCIe.

For many workloads, this works perfectly well.

But large distributed AI workloads can require much more GPU-to-GPU bandwidth.

[![PCIe diagram](https://substackcdn.com/image/fetch/$s_!NgyF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04a27de3-256c-45ec-a358-2681ce3580cf_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!NgyF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F04a27de3-256c-45ec-a358-2681ce3580cf_2400x1160.png)

PCIe diagram

---

### 7.2 NVLink

**NVLink** is NVIDIA’s high-speed interconnect technology.

It provides high-bandwidth communication between supported GPUs.

Think of PCIe and NVLink as roads available for moving data.

When GPUs constantly exchange large tensors, having a wider and faster road can significantly affect performance.

This becomes especially important for techniques such as Tensor Parallelism.

[![NVLink diagram](https://substackcdn.com/image/fetch/$s_!gIqX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea185a0e-6486-4b76-9c6a-242cd78fbe4b_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!gIqX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fea185a0e-6486-4b76-9c6a-242cd78fbe4b_2400x1160.png)

NVLink diagram

---

### 7.3 NVSwitch

When many GPUs need fast communication with one another, some NVIDIA systems use **NVSwitch**.

NVSwitch connects groups of GPUs using high-bandwidth NVLink connectivity.

Instead of focusing only on individual GPU-to-GPU links, NVSwitch helps provide high-bandwidth connectivity across a larger group of GPUs.

[![NVSwitch diagram](https://substackcdn.com/image/fetch/$s_!nQOU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a8b0517-37c4-4e6f-b0c8-327200383f25_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!nQOU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a8b0517-37c4-4e6f-b0c8-327200383f25_2400x1160.png)

NVSwitch diagram

---

### 7.4 Inter-GPU Bandwidth

**Inter-GPU bandwidth** tells us how much data GPUs can exchange over a connection in a given amount of time.

Higher inter-GPU bandwidth matters when large tensors need to move frequently between GPUs.

If the GPUs calculate results faster than they can exchange them, communication becomes the bottleneck.

[![Inter-GPU Bandwidth diagram](https://substackcdn.com/image/fetch/$s_!OtmD!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e289f04-ed5c-4605-b166-2410bfa2c34b_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!OtmD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e289f04-ed5c-4605-b166-2410bfa2c34b_2400x1160.png)

Inter-GPU Bandwidth diagram

---

### 7.5 NCCL

**NCCL: NVIDIA Collective Communications Library** provides optimized communication operations for NVIDIA GPUs.

Distributed frameworks such as PyTorch can use NCCL underneath their distributed workloads.

Instead of every developer manually implementing GPU communication, NCCL provides optimized primitives for common communication patterns.

[![NCCL diagram](https://substackcdn.com/image/fetch/$s_!U-pJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F190f5a5b-c96d-4223-a250-d3915f933d07_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!U-pJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F190f5a5b-c96d-4223-a250-d3915f933d07_2400x1160.png)

NCCL diagram

---

### 7.6 AllReduce

One important collective communication operation is **AllReduce**.

Imagine four GPUs independently calculating gradients during distributed training.

Those gradients need to be combined so the GPUs can continue training using synchronized information.

Conceptually, AllReduce combines values contributed by the GPUs and sends the same combined result to every GPU.

That is the basic idea behind **AllReduce**.

As the number of GPUs increases, operations like AllReduce can consume significant time.

The important lesson is:

**Adding more GPUs also adds more communication.**

[![AllReduce diagram](https://substackcdn.com/image/fetch/$s_!vbLo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ba1524d-7a03-473c-ba94-43e421b51965_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!vbLo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9ba1524d-7a03-473c-ba94-43e421b51965_2400x1160.png)

AllReduce diagram

---

## 8\. Scaling LLMs Across GPUs

We can now connect everything we have learned.

### 8.1 Single-GPU

The simplest setup is **single-GPU inference**: one GPU holds the model and runs inference.

If the model fits into GPU memory and one GPU provides enough performance, this is usually the simplest architecture.

There is no reason to introduce distributed complexity when a single GPU already solves the problem.

[![Single-GPU diagram](https://substackcdn.com/image/fetch/$s_!S3A4!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e51958f-533a-40ec-abfb-b59f02cba5a9_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!S3A4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e51958f-533a-40ec-abfb-b59f02cba5a9_2400x1160.png)

Single-GPU diagram

---

### 8.2 Multi-GPU

If the model cannot fit on one GPU, or one GPU cannot provide enough performance, we can use a **multi-GPU** setup.

Model sharding, Tensor Parallelism, Pipeline Parallelism, or other techniques can distribute the workload across GPUs.

Now we gain additional memory and compute.

But we also introduce communication overhead.

[![Multi-GPU diagram](https://substackcdn.com/image/fetch/$s_!zzq_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F165cd422-0aa8-4e8e-9075-c3dfd54d33e3_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!zzq_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F165cd422-0aa8-4e8e-9075-c3dfd54d33e3_2400x1160.png)

Multi-GPU diagram

---

### 8.3 Distributed Training

When many GPUs work together to train a model, especially across multiple machines, we enter **distributed training**.

A distributed training system might combine **Data Parallelism, Tensor Parallelism, and Pipeline Parallelism**.

The exact combination depends on:

- model size
- GPU memory
- number of GPUs
- workload
- communication bandwidth

Scaling therefore becomes both a compute problem and a communication problem.

[![Distributed Training diagram](https://substackcdn.com/image/fetch/$s_!dlrC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10cd4ee4-56bf-4ac0-b3e7-76b40962f7a8_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!dlrC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F10cd4ee4-56bf-4ac0-b3e7-76b40962f7a8_2400x1160.png)

Distributed Training diagram

---

### 8.4 GPU Cluster

A **GPU cluster** is a collection of GPU-equipped machines working together.

Conceptually, scaling progresses from one GPU to multiple GPUs, multiple GPU servers, and a GPU cluster.

Large AI training jobs can use hundreds or thousands of GPUs from these clusters.

The challenge is making all of those GPUs cooperate efficiently.

[![GPU Cluster diagram](https://substackcdn.com/image/fetch/$s_!0loX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F008e7af5-e381-4adb-a244-85a19817d2da_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!0loX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F008e7af5-e381-4adb-a244-85a19817d2da_2400x1160.png)

GPU Cluster diagram

---

### 8.5 Memory Bottleneck

A **memory bottleneck** occurs when memory capacity or memory bandwidth limits the workload.

Examples include:

- model does not fit in VRAM
- KV cache consumes available memory
- GPU waits for data from HBM
- batch size cannot be increased because memory is full

Adding more raw compute does not necessarily solve these problems.

[![Memory Bottleneck diagram](https://substackcdn.com/image/fetch/$s_!7ZUa!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F715752a0-904f-4882-85be-f0ddd1a09bbd_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!7ZUa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F715752a0-904f-4882-85be-f0ddd1a09bbd_2400x1160.png)

Memory Bottleneck diagram

---

### 8.6 Compute Bottleneck

A **compute bottleneck** occurs when the GPU’s arithmetic units are already heavily utilized and the workload simply requires more calculations than the available hardware can perform quickly.

More compute capability can help here.

[![Compute Bottleneck diagram](https://substackcdn.com/image/fetch/$s_!8E8V!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f11df1f-08a1-4248-8429-9c0b2590cd81_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!8E8V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f11df1f-08a1-4248-8429-9c0b2590cd81_2400x1160.png)

Compute Bottleneck diagram

---

### 8.7 Communication Bottleneck

A **communication bottleneck** appears when GPUs spend too much time waiting for data from other GPUs.

For example, a GPU may finish a calculation, wait for a tensor from another GPU, resume computing, and then have to wait again.

At that point, adding another GPU may provide surprisingly little improvement.

This is particularly important in workloads that require frequent synchronization or tensor exchange.

[![Communication Bottleneck diagram](https://substackcdn.com/image/fetch/$s_!SKBx!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F219defd1-4eee-44ff-b422-4389c53aba6e_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!SKBx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F219defd1-4eee-44ff-b422-4389c53aba6e_2400x1160.png)

Communication Bottleneck diagram

---

### 8.8 Scaling Efficiency

**Scaling efficiency** describes how effectively additional GPUs improve performance.

Imagine one GPU processes a workload in 100 seconds.

Ideally:

```markup
1 GPU → 100 sec
2 GPUs → 50 sec
4 GPUs → 25 sec
8 GPUs → 12.5 sec
```

That would be close to perfect scaling.

Real systems rarely behave that way.

You may instead see:

```markup
1 GPU → 100 sec
2 GPUs → 58 sec
4 GPUs → 36 sec
8 GPUs → 29 sec
```

Why?

Because additional GPUs also introduce:

- communication
- synchronization
- tensor transfers
- coordination
- idle time while waiting for other GPUs

This gives us the larger lesson behind GPU scaling:

**A faster AI system is not simply a system with more GPUs.**

Performance depends on how well **compute, memory, parallelism, and GPU communication** work together.

[![Scaling Efficiency diagram](https://substackcdn.com/image/fetch/$s_!Hy_G!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec87e50f-a853-4788-80d3-c1ccf7a4d657_2400x1160.png)](https://substackcdn.com/image/fetch/$s_!Hy_G!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec87e50f-a853-4788-80d3-c1ccf7a4d657_2400x1160.png)

Scaling Efficiency diagram

---

## The GPU vocabulary starts making more sense once the pieces connect

You do not need to remember every term in this article.

What matters is knowing roughly **where each term belongs**.

If someone mentions **HBM or CUDA OOM**, they are probably talking about memory.

If they mention **BF16, FP8, or INT4**, they are talking about numerical precision.

If the conversation moves to **Tensor Parallelism or Pipeline Parallelism**, the model is being split across GPUs.

And when terms like **NVLink, NCCL, or AllReduce** appear, the problem has moved from individual GPUs to communication between them.

That basic map is often enough to make GPU discussions much easier to follow.

> **GPU performance is not just about having a faster GPU. Compute, memory, precision, parallelism, and communication all play a part.**

You do not need to become a GPU hardware expert to work with AI systems. But understanding this vocabulary makes it much easier to read model requirements, compare GPUs, understand infrastructure decisions, and follow conversations about training and inference.

Keep this post around as a reference.

The next time you see **H100 + BF16 + TP=4 + NVLink** in a configuration, hopefully it looks a little less like alphabet soup.

---

For the next step, explore:

- [20 AI Engineering Concepts Explained](https://jamwithai.substack.com/p/20-ai-engineering-concepts-explained)
- [Agent Memory: the 7 types you should know](https://jamwithai.substack.com/p/agent-memory-the-7-types-you-should).
- [LLM Inference 101](https://jamwithai.substack.com/p/llm-inference-101)

If this guide helped, share it with someone who is learning to work with GPUs.

Until next time ❤️
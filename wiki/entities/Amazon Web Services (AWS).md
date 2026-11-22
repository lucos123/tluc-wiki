---
title: "Amazon Web Services (AWS)"
date: 2026-11-18
tags:
  - entity
  - organization
  - cloud-platform
  - aws
---

# Amazon Web Services (AWS)

**Amazon Web Services (AWS)** is Amazon's cloud computing platform providing foundational global infrastructure (Regions, Availability Zones, Edge Locations) alongside managed services spanning compute, storage, networking, relational/NoSQL databases, containers, asynchronous messaging, observability, and cryptographic security.

## Core Service Architecture Covered in Second Brain

Based on [AWS Core Services Notes](../sources/AWS%20Core%20Services%20Notes.md), core AWS primitives cluster into three engineering pillars:

1. **Global Infrastructure, Identity, Networking & Compute** — [AWS Foundation, Networking and Compute](../concepts/AWS%20Foundation%2C%20Networking%20and%20Compute.md):
   - **Infrastructure & Identity**: AWS Regions & Availability Zones (`AZ`), `IAM` (Users, Groups, Roles, Policies).
   - **Networking & Traffic**: `VPC` (Public/Private Subnets, IGW, NAT Gateway, Route Tables, Security Groups, NACLs), `ELB/ALB/NLB`, `Route 53`.
   - **Compute & Storage**: `EC2`, `EBS` (`gp3`, `io2`, `st1`, `sc1`).
2. **Managed Data, Containers & Decoupled Messaging** — [AWS Databases, Containers and Messaging](../concepts/AWS%20Databases%2C%20Containers%20and%20Messaging.md):
   - **Databases**: Amazon `RDS` (`Multi-AZ`, PostgreSQL/MySQL/Aurora) & `DynamoDB` (serverless key-value/document NoSQL).
   - **Queues & Containers**: Amazon `SQS` (Standard vs. FIFO queues), `ECR`, `ECS` (`EC2` / `Fargate`), `EKS` (managed Kubernetes).
3. **Observability, Auditing & Cryptographic Controls** — [AWS Observability and Cryptographic Security](../concepts/AWS%20Observability%20and%20Cryptographic%20Security.md):
   - **Observability & Compliance**: Amazon `CloudWatch` & AWS `CloudTrail` (`Management` vs. `Data` events).
   - **Secrets & Keys**: `AWS Secrets Manager` & `AWS KMS` (FIPS 140-2 Level 3 HSMs).

## Ingested Sources
- [AWS Core Services Notes](../sources/AWS%20Core%20Services%20Notes.md) (`2026-11-16`): 18-page Vietnamese visual handbook by [Viet Nguyen AI](Viet%20Nguyen%20AI.md) summarizing 17 core AWS services with architecture diagrams, comparison tables, CLI snippets, and operational best practices.

## Related Concepts
- [AWS Foundation, Networking and Compute](../concepts/AWS%20Foundation%2C%20Networking%20and%20Compute.md)
- [AWS Databases, Containers and Messaging](../concepts/AWS%20Databases%2C%20Containers%20and%20Messaging.md)
- [AWS Observability and Cryptographic Security](../concepts/AWS%20Observability%20and%20Cryptographic%20Security.md)
- [Inference Serving and Deployment Patterns](../concepts/Inference%20Serving%20and%20Deployment%20Patterns.md)
- [AI Deployment Lifecycle and Environments](../concepts/AI%20Deployment%20Lifecycle%20and%20Environments.md)

# Kubernetes Mastery Lab — A-to-Z Hands-On Curriculum

> **Owner:** Anas Khan
> **Purpose:** A single source-of-truth learning plan any AI agent (Claude, or otherwise) can pick up and continue teaching from — with zero context loss between agent switches.
> **Environment:** Azure VM (`Standard_D8s_v5`, 8 vCPU / 32 GB, **Standard** security type) → nested VMs via **Multipass** → real multi-node cluster via **kubeadm**.
> **Pinned Kubernetes version:** `v1.35` (supported until Feb 2027). Note: `v1.37` releases ~26 Aug 2026 — always verify the current stable before starting.

> **LIVE ENVIRONMENT FACTS (VM is provisioned):**
> - **Public IP:** `74.162.152.114`
> - **Domain (DuckDNS):** `azureproofk8s.duckdns.org` → `74.162.152.114`
> - Use this domain for all Gateway API host-based routing + TLS (Module 12). Wildcard/sub-hosts (e.g. `api.azureproofk8s.duckdns.org`, `blue.`/`green.`) resolve to the same IP via DuckDNS.
> - **Azure NSG — ONLY these inbound ports are open:** `22` (SSH), `80` (HTTP), `443` (HTTPS). Nothing else.
>   - The NodePort range (30000–32767) is **NOT** reachable from the internet. Do not expose services via NodePort for external access.
>   - All external app traffic must arrive on **80/443** through the Gateway API / ingress path (or MetalLB IP fronted onto 80/443 by the host).
>   - For anything else during learning, use `kubectl port-forward` over the existing SSH session (port 22) — do not ask to open new NSG ports unless Anas explicitly agrees.

---

## ⛔ SECTION 0 — MANDATORY AGENT PROTOCOL (READ BEFORE ANYTHING)

**Any agent using this file MUST follow every rule below. This is not optional.**

### 0.0 — GOLDEN RULES (read these first, never break them)

**RULE 1 — Go slow. One thing at a time. STOP and wait for EXPLICIT approval.**
- Teach **step by step, explaining each thing before doing it.** Do ONE concept / ONE object, explain what it is and why, run it, show the result — then **STOP.**
- **HARD GATE:** after every step, do NOT move to the next step until Anas **explicitly says he understood** (e.g. "samajh aa gaya", "ho gaya", "next", "aage chalo"). Silence, a thumbs-up emoji, or a vague reply is NOT approval — if unsure, ask "samajh aaya? aage badhun?" and wait.
- Anas being an absolute beginner may need a concept re-explained 2-3 times. That is fine and expected. Re-explain differently, more simply — never rush him past it or make him feel slow.
- **NEVER** blast through a whole module (or multiple modules) and finish everything in one go. That defeats the purpose — Anas is here to learn, not to watch an AI complete the lab.
- No "here's the entire setup, run all of this." Small, digestible steps, each followed by a pause + wait-for-approval.
- Proceeding without Anas's explicit go-ahead is a rule violation. When in doubt, wait.

**RULE 2 — Log to `PROGRESS.md` after EVERY step (strict, for multi-AI use).**
- Anas uses **multiple AIs**. Any AI, after doing *anything* following an Anas message, **MUST append what it just did to `PROGRESS.md`** — the command, the result, what broke, the next step.
- This is per-step, not per-module. If you did something, it goes in the log — immediately.
- This is what lets Anas switch between AIs freely: the next AI reads `PROGRESS.md` and knows the exact state. If you skip logging, you break the whole system.

**RULE 3 — Every file/config you create MUST be commented.**
- Every YAML / config / script file **must start with a `#` comment block** at the top explaining: what this file is, what it does, and how it fits the lab.
- **Every meaningful line/section inside** must have a `#` comment explaining what it does and why — so Anas learns by reading, and any AI understands the file later.
- No uncommented files, ever. A file without comments = incomplete work.
- Example header every file must have:
  ```yaml
  # ============================================================
  # FILE: postgres-deployment.yaml
  # WHAT: Deploys a single PostgreSQL pod for the k8s-revision app
  # WHY:  App's user data store; Service name here must match app's DB_HOST
  # PART OF: Module 9 (Storage) / manual-first build
  # ============================================================
  apiVersion: apps/v1
  kind: Deployment          # a Deployment manages the Postgres pod + restarts it if it dies
  metadata:
    name: postgres          # this name is referenced by the Postgres Service selector
  ...
  ```

**RULE 4 — Anas is an ABSOLUTE BEGINNER. Start from ZERO.**
- Anas has **no prior Kubernetes knowledge.** Assume nothing. Teach from the ground up.
- Explain **every term the first time it appears** — pod, node, container, cluster, kubectl, YAML, etc. — in plain language with an analogy before the technical definition.
- Do not skip "obvious" basics or assume he knows Docker/Linux/networking concepts unless `PROGRESS.md` shows he's already covered them.
- If a step needs background knowledge he hasn't learned yet, **teach that background first**, in small pieces.
- Never make him feel behind. Slow, patient, zero-to-hero. When in doubt, explain more simply, not less.
- Check understanding before moving on ("samajh aaya? koi sawal?") rather than assuming.

---

### 0.1 — Progress logging (the most important rule)
There is a sibling file called **`PROGRESS.md`** in the same folder as this file.

- **Before teaching:** open and read `PROGRESS.md` fully. It tells you exactly where Anas left off and what already works. Never re-teach a completed module unless asked.
- **After every working step (not just every module):** append a new entry to `PROGRESS.md` using the template in Section 0.6. Log what was done, the exact commands that worked, what broke, and the next step.
- **If `PROGRESS.md` does not exist yet:** create it using the template in 0.6, then start from Module 1.
- The goal: Anas can switch AIs anytime and the new AI knows the full state instantly. **No progress lives only in chat — it must be written to `PROGRESS.md`.**

### 0.2 — Always use latest docs (freshness rule)
- This file is written as of **August 2026**. Kubernetes moves fast.
- **Before teaching any tool or version-specific step, web-search the official/latest 2026 docs** and confirm the current stable version, package repo path, and any deprecations.
- State the **version and freshness** explicitly to Anas ("verified against v1.35 docs, Aug 2026").
- Pin exact versions in commands. Never use `latest` blindly for cluster components.

### 0.3 — Always include best practices
- For each module, teach the **production best practice**, not just the minimum to make it work.
- Flag anti-patterns and deprecated approaches clearly (e.g. legacy `apt.kubernetes.io` repos are dead — use `pkgs.k8s.io`).
- Where a tool is retired/insecure, say so and teach the modern replacement (see Section 0.5).

### 0.4 — Teaching style (match Anas's preferences)
- **Format:** analogy first → concept → practical copy-paste commands → a **Case → Action** table at the end.
- **Short and direct.** No long lectures or dense walls of text. He will redirect if it drags.
- **Language:** casual Roman Urdu + English code-switch is fine for normal teaching. For **interview / speaking-practice** contexts, output **pure English**, full topic coverage in one message, ending with a Case→Action table.
- Give commands he can **copy and run directly**. Explain *after* the command, briefly.
- When an approach is exhausted, **say so** and change tactic — don't recycle the same failed suggestion.

### 0.5 — Known 2026 facts to respect (do not teach dead tech as primary)
- **`ingress-nginx` (community `kubernetes/ingress-nginx`) is RETIRED (March 2026)** — repo read-only, no security patches (killed partly by CVE-2025-1974 "IngressNightmare"). Its planned successor **InGate also died**.
  - Teach the legacy Ingress API **only** to explain the concept. The real prod-grade target is **Gateway API** (GA since Oct 2023, mature at v1.4+).
  - Note: F5/NGINX Inc's separate `nginxinc/kubernetes-ingress` + **NGINX Gateway Fabric** is still maintained.
- **Observability preference:** Anas does NOT want Prometheus/Grafana. Use **SigNoz, Coroot (eBPF), Netdata, OpenTelemetry Collector** instead.
- **Nested virtualization:** Azure Dv5/Dsv5 (and Ev5, Dasv5) support it, but ONLY with **Standard** security type — Trusted Launch blocks it. First check: `ls -la /dev/kvm`.

### 0.6 — `PROGRESS.md` entry template
```markdown
## [YYYY-MM-DD HH:MM] Module X.Y — <title>
- **Status:** DONE | IN-PROGRESS | BLOCKED
- **Docs verified against:** <version + date, e.g. k8s v1.35, Aug 2026>
- **What we did:** <1-3 lines>
- **Commands that worked:**
  ```bash
  <exact commands>
  ```
- **What broke / gotchas:** <errors + how fixed, or "none">
- **Best practice noted:** <the pro tip from this module>
- **Next step:** <exact next module or action>
```

### 0.7 — First-run bootstrap (agent does this once)
If `PROGRESS.md` is missing, create it with this header, then begin Module 0:
```markdown
# PROGRESS LOG — Kubernetes Mastery Lab
> Append newest entries at the BOTTOM. Never delete history.
> Current position: Module 0 (not started)
---
```

### 0.8 — Reference test application: `k8s-revision` (Anas's own Node.js app)
All deployment practice (routing, scaling, canary/blue-green, error-reproduction, GitOps) uses **Anas's own repo** as the target app.

- **Repo:** https://github.com/anasdev0ps/k8s-revision  *(private — clone as `nodejs-docker`)*
- **Why it fits:** small, clean Node.js API with exactly Postgres + Redis — simple enough to deploy every object by hand and actually understand it.
- **What the app is:** a Node.js/Express REST API (Sequelize ORM → Postgres). No separate frontend — it's an API, tested via `curl`/Postman.
  - `GET  /`        → `Hello World!`
  - `POST /users`   → body `{ "name": "...", "age": 25 }` → creates a user
  - `GET  /users`   → list of users
  - Listens on **port 3000**.
- **Stack → what to deploy as separate Kubernetes objects:**
  - **backend/API** → the Node.js app (Deployment + Service, port 3000)
  - **PostgreSQL** → user data store (Deployment + Service + PVC + Secret; later convert to StatefulSet)
  - **Redis** → cache/connection as wired in the app (Deployment + Service)
- **Agent MUST read these two files from the repo first** to get the exact wiring (do not guess):
  - `.env.example` → real env var names (DB host/user/pass/name/port, Redis host/port, app port). These become the **ConfigMap** (non-secret) + **Secret** (passwords).
  - `docker-compose.yml` → shows service names, ports, and how the app currently reaches `postgres` and `redis`. In Kubernetes those hostnames become **Service names** (e.g. app's `DB_HOST` must equal the Postgres Service name, `REDIS_HOST` the Redis Service name).
- **Local sanity check before k8s (optional):** `docker-compose up --build` → `curl localhost:3000` → confirm the app + DB + Redis work, then rebuild the same understanding as k8s objects.
- **Key wiring gotcha (log in PROGRESS.md when hit):** in Kubernetes the app finds Postgres/Redis by **Service name**, not `localhost`. If `DB_HOST`/`REDIS_HOST` still point to `localhost` or a compose service name that doesn't match your k8s Service, you'll get connection-refused / `CrashLoopBackOff` — this is a deliberate teaching moment (ties to Module 2 Services + Module 17 errors).

### 0.9 — MANUAL-FIRST RULE (do NOT hand Anas shortcuts)
Anas is here to **learn by building**, not to run `kubectl apply -f` on someone else's ready files and watch magic happen.

- **Do NOT** use any ready Helm chart or pre-made bundle in the early phases.
- Instead, deploy each tier **by hand, one object at a time**, writing the YAML together and explaining every field: build Postgres (Deployment + Service + PVC + Secret) → Redis (Deployment + Service) → Node API (Deployment + Service, env wired to the Postgres/Redis Service names via ConfigMap + Secret). Test with `curl`/port-forward after each stage.
- Prefer **imperative → declarative** progression: show the imperative command, then the equivalent YAML, then explain why declarative wins.
- After every object: `kubectl describe`, `kubectl logs`, `kubectl get <obj> -o yaml` to see what actually happened.
- **Ready Helm chart / GitOps bundles are unlocked only at Module 14 (Helm) and Module 18 (ArgoCD)** — by then the manual foundation exists, so the abstraction teaches something instead of hiding everything.
- If Anas asks for a one-line `apply` shortcut before the concept is built, gently redirect to the manual build.

### 0.10 — Container registry: GitLab (Docker registry ONLY)
Anas uses **GitLab Container Registry** strictly as a **Docker image registry** — `docker build` / `docker push` / `docker pull` and nothing else.

- **Do NOT** pull him into GitLab CI/CD pipelines, GitLab Runners, GitLab Auto DevOps, or GitLab's Fleet/Agent GitOps. GitOps in this lab = **ArgoCD** (Module 18), not GitLab.
- Registry use = only: build an image locally → push to GitLab registry → reference it in Kubernetes manifests → cluster pulls it.
- **imagePullSecret is required** for private GitLab registry: teach creating a `docker-registry` type Secret and referencing it in the pod spec / ServiceAccount. This ties directly into Module 4 (Secrets) and the `ImagePullBackOff` error in Module 17.
- Typical flow to teach:
  ```bash
  # 1. login (use a GitLab Personal/Deploy Token, not account password)
  docker login registry.gitlab.com -u <username> -p <token>
  # 2. build + tag
  docker build -t registry.gitlab.com/<group>/<project>/nodejs-app:v1 .
  # 3. push
  docker push registry.gitlab.com/<group>/<project>/nodejs-app:v1
  # 4. k8s pull secret (referenced by Deployments)
  kubectl create secret docker-registry gitlab-registry \
    --docker-server=registry.gitlab.com \
    --docker-username=<username> \
    --docker-password=<token>
  # 5. in the Deployment: spec.imagePullSecrets: [{ name: gitlab-registry }]
  ```
- **Security:** always use a scoped GitLab token (Deploy Token with `read_registry`/`write_registry`), never the account password; never commit the token into Git manifests — it lives in the Secret only.

---

## 🗺️ CURRICULUM MAP (learning order)

| Phase | Modules | Theme |
|---|---|---|
| **A. Foundation** | 0–4 | Cluster up, core objects, config |
| **B. Reliability** | 5–8 | Probes, scheduling, resources, autoscaling |
| **C. Storage & Workloads** | 9–10 | Volumes, StatefulSets, Jobs, DaemonSets |
| **D. Networking** | 11–13 | Services, MetalLB, Gateway API routing, NetworkPolicy |
| **E. Packaging & Security** | 14–15 | Helm, RBAC/security |
| **F. Observability & Errors** | 16–17 | Monitoring (SigNoz/Netdata), error-reproduction lab |
| **G. Delivery** | 18–21 | GitOps (ArgoCD), Rollouts (blue-green/canary), Kargo, Rancher |
| **H. Operations** | 22–23 | Upgrades, backup, troubleshooting |
| **I. Wrap** | 24 | Best-practices + interview prep |

Each module below has: **Analogy · Concept · Hands-on · Errors to break+fix · Best practice · Done-check.**

> ### ⚠️ STRICT ORDER — do modules in sequence, no jumping ahead
> The order is deliberately built so each module only uses concepts already taught. **Do NOT teach a later module before the earlier ones are done and approved.** Every module assumes the previous ones are complete (verify via `PROGRESS.md`).
>
> Prerequisite chain (so nothing is taught "out of nowhere"):
> - **Pods → ReplicaSet → Deployment** (M1) before anything that runs a workload.
> - **Services** (M2) before MetalLB (M11), Gateway API (M12), StatefulSet headless service (M10).
> - **ConfigMap/Secret** (M4) before wiring the app to DB/Redis and before imagePullSecret.
> - **Requests/limits** (M7) before HPA (M8) — autoscaling needs requests set.
> - **Volumes/PV/PVC/StorageClass** (M9) before StatefulSet (M10) — stateful pods need storage.
> - **MetalLB** (M11) before Gateway API (M12) — the gateway needs an external IP.
> - **All core objects built manually** (M0–M13) before Helm (M14) and ArgoCD (M18) — manual-first rule.
> - **Gateway API traffic-split** (M12) + **HPA** (M8) before Argo Rollouts canary (M19).
> - **ArgoCD** (M18) + **Helm** (M14) before Kargo (M20).
> - **Error-reproduction lab** (M17) after the concepts it breaks (probes, resources, storage, networking, RBAC) are taught.
>
> If Anas ever asks to jump ahead (e.g. "abhi volumes karwa do" before pods are done), explain the prerequisite briefly and offer to do the missing foundation first — don't skip the chain.

---

## PHASE A — FOUNDATION

### Module 0 — Environment & multi-node cluster
- **Analogy:** Host VM = building; Multipass = builds mini-flats (VMs); each flat = a k8s node; kubeadm = wiring them into one cluster.
- **Concept:** nested virtualization → Multipass VMs → kubeadm control-plane + workers → CNI for pod networking.
- **Hands-on:**
  1. `ls -la /dev/kvm` (must exist). Install: `sudo snap install multipass`.
  2. Launch: 1 `master` (2 vCPU/2G), 2 workers (1 vCPU/2G), Ubuntu 24.04.
  3. On every node: swap off, `br_netfilter`+`overlay` modules, sysctl bridge/forward, install `containerd` (SystemdCgroup=true), install `kubelet kubeadm kubectl` from `pkgs.k8s.io/core:/stable:/v1.35/deb/`.
  4. `kubeadm init --pod-network-cidr=10.244.0.0/16` on master → set kubeconfig → apply **Flannel** CNI.
  5. `kubeadm token create --print-join-command` → run on both workers.
  6. Verify: `kubectl get nodes -o wide` → all `Ready`.
- **Errors to break+fix:** wrong CIDR clash; `containerd` cgroup mismatch (nodes NotReady); swap-on init failure.
- **Best practice:** pin exact k8s version + `apt-mark hold`; use separate node roles; snapshot working state before experiments.
- **Done-check:** 3 nodes Ready, a test `nginx` pod runs and is reachable via a Service.

### Module 1 — Pods, ReplicaSets, Deployments
- **Analogy:** Pod = one worker; ReplicaSet = HR keeping N workers alive; Deployment = manager doing rolling version changes.
- **Concept:** Pod (smallest unit) → ReplicaSet (count) → Deployment (rollout/rollback). Labels & selectors tie everything.
- **Hands-on:** create a Deployment (nginx), scale it, `kubectl rollout` update image, `rollout undo`, inspect with `describe`/`get -o yaml`.
- **Errors to break+fix:** selector/label mismatch (0 pods); bad image tag → `ImagePullBackOff`.
- **Best practice:** never create bare Pods in prod; always Deployments; declarative YAML in Git, not imperative `kubectl run`.
- **Done-check:** rolling update + rollback demonstrated.

### Module 2 — Services & basic networking
- **Analogy:** Pods have changing phone numbers (IPs); a Service is a fixed reception desk that always forwards to a live worker.
- **Concept:** `ClusterIP` (internal), `NodePort` (node:port), `LoadBalancer` (external — needs a provider), Endpoints, kube-proxy, CoreDNS name resolution.
- **Hands-on:** expose a Deployment as each type; curl ClusterIP from another pod; resolve `svc.namespace.svc.cluster.local`.
- **Errors to break+fix:** selector mismatch → empty Endpoints → connection refused; wrong `targetPort`.
- **Best practice:** prefer ClusterIP + Ingress/Gateway over NodePort; name your ports.
- **Done-check:** pod-to-service and DNS resolution working.

### Module 3 — Namespaces, labels, annotations
- **Concept:** namespaces = logical isolation; labels = selectable metadata; annotations = non-selectable metadata.
- **Hands-on:** create namespaces (dev/stage/prod), scope resources, `kubectl -n`, set context default namespace.
- **Best practice:** one namespace per env/team; consistent label schema (`app`, `env`, `version`).
- **Done-check:** resources cleanly separated by namespace.

### Module 4 — ConfigMaps & Secrets
- **Analogy:** ConfigMap = settings sticky-note; Secret = the same but in a locked drawer (base64, ideally encrypted at rest).
- **Concept:** inject config as env vars or mounted files; Secrets for credentials; `stringData` vs base64.
- **Hands-on:** mount a ConfigMap as a file + as env; create a Secret and consume it; rotate a value and restart.
- **Errors to break+fix:** missing key → pod crash; secret not mounted → app 500s.
- **Best practice:** never commit plaintext Secrets to Git; use Sealed Secrets / external secret store; enable etcd encryption-at-rest.
- **Done-check:** app reads config + secret correctly.

---

## PHASE B — RELIABILITY

### Module 5 — Health probes (liveness / readiness / startup)
- **Analogy:** Readiness = "are you ready to take calls?" (traffic gate); Liveness = "are you still alive or stuck?" (restart trigger); Startup = "give slow starters extra time before we judge them."
- **Concept:** readiness controls Service traffic; liveness restarts a hung container; startup protects slow-boot apps from premature liveness kills. Probe types: httpGet, tcpSocket, exec, grpc.
- **Hands-on:** add all three probes; make readiness fail → watch pod drop from Endpoints; make liveness fail → watch restarts climb.
- **Errors to break+fix:** wrong probe path/port → `CrashLoopBackOff` from liveness; too-tight `initialDelaySeconds`.
- **Best practice:** readiness on a real dependency check; liveness lightweight; always set startupProbe for slow apps; never make liveness depend on external services.
- **Done-check:** traffic stops to a not-ready pod without killing it.

### Module 6 — Scheduling: affinity, anti-affinity, taints, tolerations
- **Analogy:** nodeSelector = "must sit at this table"; affinity = "prefer to sit near friends"; anti-affinity = "don't seat two of us together"; taint = "this table is reserved — only those with a pass (toleration) may sit."
- **Concept:** `nodeSelector`, node affinity (required/preferred), pod affinity/anti-affinity, taints & tolerations, topology spread constraints, `nodeName`.
- **Hands-on:**
  1. Label a node, force a pod there via nodeSelector + node affinity.
  2. Pod anti-affinity: spread replicas across nodes.
  3. Taint a node (`kubectl taint nodes worker1 key=val:NoSchedule`) → prove pods avoid it → add toleration to allow.
  4. Topology spread across nodes for HA.
- **Errors to break+fix:** over-constrained pod → `Pending` (no node fits); taint with no toleration → unschedulable.
- **Best practice:** use anti-affinity/topology spread for HA; taint dedicated nodes (GPU/system); prefer `preferred` over `required` unless truly mandatory.
- **Done-check:** replicas provably spread; tainted node respected.

### Module 7 — Resources: requests, limits, QoS, quotas
- **Analogy:** request = the seat you reserve; limit = the max you're allowed to eat before you're cut off (CPU throttled / memory OOMKilled).
- **Concept:** requests (scheduling) vs limits (enforcement); QoS classes (Guaranteed/Burstable/BestEffort); `LimitRange`; `ResourceQuota`.
- **Hands-on:** set requests/limits; force `OOMKilled` with a tiny memory limit; observe CPU throttling; apply a namespace ResourceQuota and hit it.
- **Errors to break+fix:** `OOMKilled`; `Pending` because requests exceed capacity; quota-exceeded rejections.
- **Best practice:** always set requests/limits; aim for Guaranteed on critical workloads; use LimitRange defaults + ResourceQuota per namespace.
- **Done-check:** QoS class visible; OOM reproduced and understood.

### Module 8 — Autoscaling (HPA, VPA, Cluster Autoscaler, KEDA)
- **Analogy:** HPA = hire/fire waiters based on how busy the restaurant is.
- **Concept:** `metrics-server` → HPA (scale pods on CPU/mem/custom); VPA (right-size a pod); Cluster Autoscaler (add nodes — concept only in lab); KEDA (event-driven scaling — mention).
- **Hands-on:** install metrics-server; create HPA on CPU; generate load (e.g. `hey`/busy loop) → watch pods scale up then down.
- **Errors to break+fix:** HPA `unknown` targets → metrics-server missing/misconfigured (fix TLS flag in nested VMs).
- **Best practice:** HPA needs sane requests set; combine with PodDisruptionBudget; don't mix HPA + VPA on same metric.
- **Done-check:** pods auto scale under load and back down.

---

## PHASE C — STORAGE & WORKLOADS

### Module 9 — Storage: Volumes, PV, PVC, StorageClass
- **Analogy:** PVC = "I need a locker of size X"; PV = the actual locker; StorageClass = the locker vendor that makes them on demand.
- **Concept:** ephemeral volumes vs persistent; PV/PVC binding; StorageClass + dynamic provisioning; access modes; reclaim policy. In lab use `local-path` provisioner (Rancher) or hostPath.
- **Hands-on:** install local-path provisioner; PVC → PV bound; mount into a pod; write data, delete pod, prove data persists.
- **Errors to break+fix:** PVC stuck `Pending` (no matching PV/StorageClass); access-mode mismatch.
- **Best practice:** always use StorageClass/dynamic provisioning; set correct reclaim policy; never rely on hostPath in prod.
- **Done-check:** data survives pod recreation.

### Module 10 — Workload types: StatefulSet, DaemonSet, Job, CronJob
- **Concept:** Deployment (stateless) vs **StatefulSet** (stable identity + storage, e.g. DB) vs **DaemonSet** (one pod per node, e.g. log agent) vs **Job** (run-to-completion) vs **CronJob** (scheduled).
- **Hands-on:** StatefulSet with per-pod PVC (stable `pod-0/1/2` names); DaemonSet on all nodes; a Job that completes; a CronJob every minute.
- **Errors to break+fix:** StatefulSet stuck on PVC; Job backoff on failure.
- **Best practice:** StatefulSet for ordered/identity workloads only; DaemonSet tolerations for tainted nodes; set Job `backoffLimit` + `ttlSecondsAfterFinished`.
- **Done-check:** each workload type behaves as expected.

---

## PHASE D — NETWORKING (prod-grade routing)

### Module 11 — Load balancing with MetalLB
- **Concept:** in bare-metal/nested clusters, `type: LoadBalancer` needs MetalLB to hand out external IPs from a pool.
- **Hands-on:** install MetalLB, define an IP address pool on the Multipass subnet, expose a Service as LoadBalancer, get a real external IP.
- **Errors to break+fix:** IP pool overlaps node range; L2 advertisement missing → EXTERNAL-IP `<pending>`.
- **Best practice:** dedicate a non-conflicting IP range; use L2 mode for lab.
- **Done-check:** Service gets an external IP reachable from host.

### Module 12 — Gateway API routing (the modern, prod-grade path)
> ingress-nginx is retired — this is the real target.
- **Analogy:** GatewayClass = the type of gate; Gateway = the actual gate/door; HTTPRoute = the sign that says "which hallway this visitor goes down."
- **Concept:** install a Gateway API implementation (**Traefik** or **Envoy Gateway** or **NGINX Gateway Fabric**). Objects: `GatewayClass`, `Gateway` (listeners/ports/TLS), `HTTPRoute` (rules).
- **Hands-on — every routing type:**
  - **Path-based:** `/app1` → svcA, `/app2` → svcB.
  - **Host-based:** route by hostname → `blue.azureproofk8s.duckdns.org` vs `green.azureproofk8s.duckdns.org` (two versions of the same API; both resolve to `74.162.152.114`). This doubles as prep for blue-green in Module 19.
  - **Header/query-based** routing.
  - **Weighted / traffic split** (90/10 — foundation for canary).
  - **Rewrite / redirect** (path strip, HTTPS redirect).
  - **TLS termination** via cert-manager + Let's Encrypt (real domain).
- **Also cover (for legacy awareness only):** the classic Ingress object once, to understand what teams are migrating *from*.
- **Errors to break+fix:** `502/503` (backend down / wrong port); wrong `parentRef`; cert not ready.
- **Best practice:** Gateway API over Ingress for new work; separate Gateway (platform team) from HTTPRoute (app team); automate certs with cert-manager.
- **Done-check:** all routing types + HTTPS working on the real domain.

### Module 13 — Network policies & DNS internals
- **Analogy:** default k8s = open-plan office (everyone talks to everyone). NetworkPolicy = adding doors and keycards.
- **Concept:** default allow-all → deny-by-default + explicit allows; ingress/egress rules; requires a policy-capable CNI (Calico). CoreDNS internals.
- **Hands-on:** switch/augment CNI with Calico; apply default-deny; allow only specific pod-to-pod; break DNS and diagnose.
- **Errors to break+fix:** policy too strict → app can't reach DB; DNS failures.
- **Best practice:** default-deny then allow explicitly; label-based policy targeting; test policies before prod.
- **Done-check:** traffic blocked/allowed exactly as intended.

---

## PHASE E — PACKAGING & SECURITY

### Module 14 — Helm (A-to-Z)
- **Analogy:** Helm = an app installer (like apt) for Kubernetes; a Chart = the installable package; values = the config knobs.
- **Concept:** charts, `values.yaml`, templating (`{{ }}`), releases, `install/upgrade/rollback`, repos, dependencies, `helm template`/`--dry-run`.
- **Hands-on:** install a public chart with custom values; `helm upgrade` + `helm rollback`; **write your own chart** for one of your apps; add a dependency; lint + template.
- **Errors to break+fix:** template render errors; failed upgrade → rollback; values not overriding.
- **Best practice:** version charts; keep values per-env; `--atomic` upgrades; never `helm install` untrusted charts blindly.
- **Done-check:** own chart installs, upgrades, rolls back cleanly.

### Module 15 — Security: RBAC, ServiceAccounts, SecurityContext, Pod Security
- **Analogy:** RBAC = who has which keys to which rooms.
- **Concept:** `Role`/`ClusterRole` + `RoleBinding`/`ClusterRoleBinding`; ServiceAccounts; `SecurityContext` (runAsNonRoot, drop caps, readOnlyRootFS); Pod Security Standards (privileged/baseline/restricted); image/supply-chain basics.
- **Hands-on:** create a limited ServiceAccount + Role (read pods in one ns only); test `kubectl auth can-i`; run a pod as non-root with dropped capabilities; enforce a restricted namespace label.
- **Errors to break+fix:** `Forbidden` from missing RBAC; pod rejected by Pod Security admission.
- **Best practice:** least privilege; no `cluster-admin` for apps; runAsNonRoot + read-only rootfs; scan images.
- **Done-check:** least-privilege SA works; privileged pod rejected.

---

## PHASE F — OBSERVABILITY & ERROR LAB

### Module 16 — Observability (Anas's stack: NO Prometheus/Grafana)
- **Concept:** metrics + logs + traces. Use **metrics-server** (HPA), **SigNoz** or **Netdata** for dashboards, **Coroot** (eBPF, auto service map), **OpenTelemetry Collector** for pipelines.
- **Hands-on:** deploy Netdata or SigNoz; instrument an app with OTel; read golden signals (latency/traffic/errors/saturation); use `kubectl top`, `logs`, `events`, `kubectl debug` (ephemeral containers).
- **Best practice:** structured logs; OTel as the vendor-neutral standard; alert on symptoms (SLOs) not causes.
- **Done-check:** live dashboard + trace of a request end-to-end.

### Module 17 — Production error-reproduction lab (break everything on purpose)
Deliberately cause each, then diagnose with `describe` / `logs` / `events` / `get -o yaml`:

| Error | How to trigger | Skill learned |
|---|---|---|
| `CrashLoopBackOff` | bad command / failing liveness | restart policy + logs |
| `ImagePullBackOff` / `ErrImagePull` | wrong tag / private registry no secret | images + imagePullSecrets |
| `OOMKilled` | memory limit too low | resource limits |
| `Pending` (unschedulable) | requests > capacity / taint | scheduling + events |
| `502 / 503` | backend down / wrong port | Gateway↔Service↔Pod chain |
| Readiness never ready | wrong probe path | probes |
| Service unreachable | selector mismatch → empty Endpoints | labels/endpoints |
| DNS resolution fail | wrong svc name / CoreDNS down | cluster DNS |
| PVC `Pending` | no StorageClass | storage |
| TLS/cert error | expired/missing cert | cert-manager |
| HPA `unknown` | metrics-server missing | autoscaling |
| `Forbidden` | missing RBAC | RBAC |
| NetworkPolicy blackhole | over-strict policy | network policy |
| Node `NotReady` | kubelet/containerd/CNI down | node troubleshooting |

- **Best practice:** learn a fixed triage order — `get pods` → `describe` → `logs` (+ `--previous`) → `get events --sort-by=.lastTimestamp` → `get -o yaml`.
- **Done-check:** every row reproduced and fixed once.

---

## PHASE G — DELIVERY (GitOps & progressive)

### Module 18 — GitOps with ArgoCD
- **Analogy:** Git = the single source of truth; ArgoCD = a robot that constantly makes the cluster match Git and heals drift.
- **Concept:** declarative GitOps; Application CRD; sync, self-heal, prune, drift detection; app-of-apps; sync waves.
- **Hands-on:** install ArgoCD; connect a Git repo of manifests/Helm; auto-sync; manually edit cluster → watch ArgoCD revert it (self-heal); app-of-apps pattern.
- **Errors to break+fix:** OutOfSync loops; sync-wave ordering; failed hooks.
- **Best practice:** Git is the only way to change prod; enable self-heal + prune carefully; separate config repo from code repo.
- **Done-check:** cluster state provably driven by Git.

### Module 19 — Progressive delivery with Argo Rollouts (blue-green + canary)
- **Analogy:** blue-green = two identical stages, flip the spotlight instantly; canary = let a few audience members in first, watch, then let the rest.
- **Concept:** `Rollout` CRD replaces Deployment; **blue-green** (preview + active service, instant switch); **canary** (stepped weight shifts) with **analysis** (auto-promote/rollback on metrics); integrates with Gateway API traffic splitting.
- **Hands-on:**
  1. Convert a Deployment to a Rollout.
  2. **Blue-green:** deploy v2 to preview, verify, promote (instant cutover), then rollback.
  3. **Canary:** 10% → 30% → 60% → 100% with pauses; wire AnalysisTemplate to auto-rollback on error rate.
- **Errors to break+fix:** stuck rollout on failed analysis; traffic not splitting (Gateway/route misconfig).
- **Best practice:** always define analysis + auto-rollback; short bake times per step; combine with HPA + PDB.
- **Done-check:** both strategies + an automatic rollback demonstrated.

### Module 20 — Kargo (multi-stage promotion)
- **Analogy:** an assembly line that moves a verified artifact dev → stage → prod automatically, with gates.
- **Concept:** Kargo sits above GitOps; models **Stages**, **Freight** (a versioned bundle), and **promotion** flows with verification gates. Built for promoting the same artifact across environments.
- **Hands-on:** install Kargo; define a Warehouse (image source) + Stages (dev→stage→prod); promote Freight through stages with verification; wire to ArgoCD Applications.
- **Errors to break+fix:** promotion blocked by failed verification; credentials/registry access.
- **Best practice:** immutable Freight promoted unchanged across stages; automated gates before prod; audit trail in Git.
- **Done-check:** one artifact promoted through all stages with gates.

### Module 21 — Rancher (multi-cluster management UI)
- **Analogy:** a single control-tower dashboard for all your clusters, apps, and users.
- **Concept:** Rancher = cluster management + app catalog + RBAC + monitoring UI; can import your kubeadm cluster; provides Fleet (its own GitOps) and easy Helm app deploys.
- **Hands-on:** install Rancher; import the kubeadm cluster; deploy an app from the catalog; manage RBAC + view workloads/monitoring from the UI.
- **Note:** Rancher is memory-heavy — this is why the VM is 32 GB. Do this module last so it doesn't starve earlier experiments.
- **Best practice:** use Rancher for visibility/governance; keep Git/ArgoCD as source of truth, not click-ops.
- **Done-check:** cluster + apps manageable from Rancher UI.

---

## PHASE H — OPERATIONS

### Module 22 — Cluster upgrades (kubeadm)
- **Concept:** version skew policy (N-2); upgrade order: control-plane `kubeadm upgrade apply` → drain node → upgrade kubelet/kubectl → uncordon → repeat per node.
- **Hands-on:** upgrade the cluster one minor version (e.g. 1.35 → 1.36) following the drain/upgrade/uncordon cycle.
- **Errors to break+fix:** skew violations; forgetting to switch the `pkgs.k8s.io` repo minor version; PodDisruptionBudget blocking drain.
- **Best practice:** always drain first; upgrade one minor at a time; back up etcd before upgrading; read release notes for removed APIs.
- **Done-check:** cluster upgraded, all nodes on new version, workloads intact.

### Module 23 — Backup & disaster recovery
- **Concept:** etcd is the cluster's brain — back it up. **Velero** for namespaced resource + PV backup/restore.
- **Hands-on:** take an etcd snapshot; install Velero; back up a namespace; delete it; restore from backup.
- **Best practice:** scheduled etcd snapshots off-node; test restores regularly (a backup you can't restore is useless).
- **Done-check:** namespace restored successfully from backup.

---

## PHASE I — WRAP

### Module 24 — Best-practices consolidation + interview prep
- Review the running best-practice notes gathered in `PROGRESS.md`.
- **Interview mode (pure English):** for each major topic, deliver full coverage in one message ending with a **Case → Action** table, e.g.:

| Case | Action |
|---|---|
| Pod stuck `Pending` | check `describe` events → resources/taints/PVC |
| App gets no traffic | check readiness probe + Service Endpoints |
| Need zero-downtime release | blue-green (instant) or canary (gradual) via Rollouts |
| Config changed but pod stale | rollout restart / checksum annotation |
| Prod change must be auditable | GitOps via ArgoCD, no manual kubectl |
| Same artifact across envs | promote Freight via Kargo, don't rebuild |
| External IP `<pending>` (bare metal) | MetalLB pool + L2 advertisement |
| ingress-nginx in use | migrate to Gateway API (retired March 2026) |

---

## APPENDIX — Quick reference

**Triage order for ANY broken pod:**
```bash
kubectl get pods -A
kubectl describe pod <pod> -n <ns>
kubectl logs <pod> -n <ns> [--previous]
kubectl get events -n <ns> --sort-by=.lastTimestamp
kubectl get <pod> -o yaml
```

**Snapshot working cluster state before experiments:** `multipass stop <all>` then note it in `PROGRESS.md`, or `multipass` clone if needed.

**Version check before each session:** web-search "latest stable Kubernetes version" + confirm `pkgs.k8s.io/core:/stable:/vX.Y/deb/` path.

---

## ✅ MASTER COMPONENT CHECKLIST — cover EVERYTHING, skip nothing

> Anas's rule: **not a single component may be left out.** Any AI must ensure every item below is taught hands-on and ticked in `PROGRESS.md`. If an item isn't in a numbered module above, teach it in the most relevant module. Tick `[x]` in `PROGRESS.md` as each is done.

**Cluster & nodes**
- [ ] Nodes (control-plane vs worker), kubelet, kube-proxy, container runtime (containerd)
- [ ] Control-plane parts: kube-apiserver, etcd, scheduler, controller-manager
- [ ] Namespaces, contexts, kubeconfig
- [ ] CRDs (Custom Resource Definitions) + operators (concept — you'll meet them via ArgoCD/Rollouts/Kargo)

**Workloads**
- [ ] Pod (single + multi-container)
- [ ] Init containers
- [ ] Sidecar containers (native sidecar / multi-container patterns)
- [ ] ReplicaSet
- [ ] Deployment (rolling update, rollback, strategies)
- [ ] StatefulSet
- [ ] DaemonSet
- [ ] Job
- [ ] CronJob
- [ ] Static pods (concept)

**Config & data**
- [ ] ConfigMap (env + mounted file)
- [ ] Secret (env + mounted, docker-registry type)
- [ ] Environment variables + `envFrom`
- [ ] Downward API (expose pod metadata to the app)

**Storage / Volumes**
- [ ] Volumes (emptyDir, hostPath)
- [ ] PersistentVolume (PV)
- [ ] PersistentVolumeClaim (PVC)
- [ ] StorageClass + dynamic provisioning
- [ ] Access modes + reclaim policy
- [ ] Volume mounts vs volume claims in StatefulSet

**Scheduling & placement**
- [ ] nodeSelector
- [ ] Node affinity / anti-affinity (required + preferred)
- [ ] Pod affinity / anti-affinity
- [ ] Taints & tolerations
- [ ] Topology spread constraints
- [ ] nodeName / manual scheduling (concept)
- [ ] Priority & preemption (PriorityClass)

**Reliability & resources**
- [ ] Liveness / Readiness / Startup probes (httpGet, tcpSocket, exec, grpc)
- [ ] Requests & limits
- [ ] QoS classes (Guaranteed / Burstable / BestEffort)
- [ ] LimitRange
- [ ] ResourceQuota
- [ ] PodDisruptionBudget (PDB)
- [ ] Horizontal Pod Autoscaler (HPA)
- [ ] Vertical Pod Autoscaler (VPA)
- [ ] Cluster Autoscaler (concept in single-host lab)
- [ ] KEDA (event-driven autoscaling)

**Networking**
- [ ] Service: ClusterIP
- [ ] Service: NodePort
- [ ] Service: LoadBalancer (via MetalLB)
- [ ] Service: ExternalName / headless (for StatefulSet)
- [ ] Endpoints / EndpointSlices
- [ ] kube-proxy modes (concept)
- [ ] CoreDNS / cluster DNS resolution
- [ ] CNI (Flannel; Calico for policy)
- [ ] Ingress (legacy — concept only, ingress-nginx retired)
- [ ] Gateway API: GatewayClass, Gateway, HTTPRoute
- [ ] Routing: path / host / header / weighted / rewrite / redirect / TLS
- [ ] NetworkPolicy (default-deny + explicit allow, ingress + egress)

**Security**
- [ ] ServiceAccounts
- [ ] RBAC: Role, ClusterRole, RoleBinding, ClusterRoleBinding
- [ ] `kubectl auth can-i`
- [ ] SecurityContext (runAsNonRoot, drop capabilities, readOnlyRootFilesystem)
- [ ] Pod Security Standards / admission (privileged / baseline / restricted)
- [ ] imagePullSecrets (GitLab registry)
- [ ] etcd encryption-at-rest (concept)

**Observability (NO Prometheus/Grafana — use SigNoz/Netdata/Coroot/OTel)**
- [ ] metrics-server
- [ ] `kubectl top`, logs, events, describe
- [ ] `kubectl debug` / ephemeral containers
- [ ] SigNoz or Netdata dashboard
- [ ] Coroot (eBPF auto service map)
- [ ] OpenTelemetry Collector + app instrumentation

**Packaging & delivery**
- [ ] Helm: charts, values, templating, install/upgrade/rollback, own chart, dependencies
- [ ] GitOps: ArgoCD (sync, self-heal, prune, drift, app-of-apps, sync waves)
- [ ] Progressive delivery: Argo Rollouts — blue-green
- [ ] Progressive delivery: Argo Rollouts — canary + AnalysisTemplate (auto-rollback)
- [ ] Kargo: Stages, Freight, multi-stage promotion + gates
- [ ] Rancher: import cluster, catalog apps, UI management

**Operations**
- [ ] kubeadm cluster upgrade (drain / upgrade / uncordon, version skew)
- [ ] Node maintenance: cordon / drain / uncordon
- [ ] etcd snapshot backup + restore
- [ ] Velero backup/restore of namespace + PV
- [ ] Full troubleshooting triage (the 14-error lab, Module 17)

**Rule:** if an AI reaches the end and any box above is unchecked in `PROGRESS.md`, the lab is **not complete** — go back and cover it. Nothing is skipped.

---

*End of curriculum. Remember Section 0: read `PROGRESS.md`, log every step, verify against latest 2026 docs, teach best practices, and leave NO component from the Master Checklist uncovered.*
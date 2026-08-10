# 📊 Kubernetes Mastery Lab - Progress Tracker

> **Note:** This checklist tracks all mandatory components required by the lab. Checked items `[x]` are covered in the modules. Unchecked items `[ ]` were missed and need dedicated modules.

## **Cluster & nodes**
- [x] Nodes (control-plane vs worker), kubelet, kube-proxy, container runtime (containerd)
- [x] Control-plane parts: kube-apiserver, etcd, scheduler, controller-manager
- [x] Namespaces, contexts, kubeconfig
- [x] CRDs (Custom Resource Definitions) + operators (concept)

## **Workloads**
- [x] Pod (single + multi-container)
- [ ] Init containers
- [ ] Sidecar containers (native sidecar / multi-container patterns)
- [x] ReplicaSet
- [x] Deployment (rolling update, rollback, strategies)
- [x] StatefulSet
- [x] DaemonSet
- [x] Job
- [x] CronJob
- [ ] Static pods (concept)

## **Config & data**
- [x] ConfigMap (env + mounted file)
- [x] Secret (env + mounted, docker-registry type)
- [x] Environment variables + `envFrom`
- [ ] Downward API (expose pod metadata to the app)

## **Storage / Volumes**
- [x] Volumes (emptyDir, hostPath)
- [x] PersistentVolume (PV)
- [x] PersistentVolumeClaim (PVC)
- [x] StorageClass + dynamic provisioning
- [x] Access modes + reclaim policy
- [x] Volume mounts vs volume claims in StatefulSet

## **Scheduling & placement**
- [x] nodeSelector
- [x] Node affinity / anti-affinity (required + preferred)
- [x] Pod affinity / anti-affinity
- [x] Taints & tolerations
- [x] Topology spread constraints
- [x] nodeName / manual scheduling (concept)
- [ ] Priority & preemption (PriorityClass)

## **Reliability & resources**
- [x] Liveness / Readiness / Startup probes (httpGet, tcpSocket, exec, grpc)
- [x] Requests & limits
- [x] QoS classes (Guaranteed / Burstable / BestEffort)
- [x] LimitRange
- [x] ResourceQuota
- [x] PodDisruptionBudget (PDB)
- [x] Horizontal Pod Autoscaler (HPA)
- [x] Vertical Pod Autoscaler (VPA)
- [x] Cluster Autoscaler (concept in single-host lab)
- [x] KEDA (event-driven autoscaling)

## **Networking**
- [x] Service: ClusterIP
- [x] Service: NodePort
- [x] Service: LoadBalancer (via MetalLB)
- [x] Service: ExternalName / headless (for StatefulSet)
- [ ] Endpoints / EndpointSlices
- [x] kube-proxy modes (concept)
- [x] CoreDNS / cluster DNS resolution
- [x] CNI (Flannel; Calico for policy)
- [x] Ingress (legacy — concept only, ingress-nginx retired)
- [x] Gateway API: GatewayClass, Gateway, HTTPRoute
- [x] Routing: path / host / header / weighted / rewrite / redirect / TLS
- [x] NetworkPolicy (default-deny + explicit allow, ingress + egress)

## **Security**
- [ ] ServiceAccounts
- [ ] RBAC: Role, ClusterRole, RoleBinding, ClusterRoleBinding
- [ ] `kubectl auth can-i`
- [ ] SecurityContext (runAsNonRoot, drop capabilities, readOnlyRootFilesystem)
- [ ] Pod Security Standards / admission (privileged / baseline / restricted)
- [ ] imagePullSecrets (GitLab registry)
- [x] etcd encryption-at-rest (concept)

## **Observability**
- [x] metrics-server
- [x] `kubectl top`, logs, events, describe
- [x] `kubectl debug` / ephemeral containers
- [x] SigNoz or Netdata dashboard
- [x] Coroot (eBPF auto service map)
- [x] OpenTelemetry Collector + app instrumentation

## **Packaging & delivery**
- [x] Helm: charts, values, templating, install/upgrade/rollback, own chart, dependencies
- [x] GitOps: ArgoCD (sync, self-heal, prune, drift, app-of-apps, sync waves)
- [x] Progressive delivery: Argo Rollouts — blue-green
- [x] Progressive delivery: Argo Rollouts — canary + AnalysisTemplate (auto-rollback)
- [x] Kargo: Stages, Freight, multi-stage promotion + gates
- [x] Rancher: import cluster, catalog apps, UI management

## **Operations**
- [x] kubeadm cluster upgrade (drain / upgrade / uncordon, version skew)
- [x] Node maintenance: cordon / drain / uncordon
- [x] etcd snapshot backup + restore
- [x] Velero backup/restore of namespace + PV
- [x] Full troubleshooting triage (the 14-error lab, Module 17)

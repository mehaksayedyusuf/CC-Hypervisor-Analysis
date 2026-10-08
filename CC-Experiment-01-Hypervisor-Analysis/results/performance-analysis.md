# Performance Analysis: Type-1 (Proxmox VE) vs Type-2 (VMware Workstation)

## 1. Primary Benchmark Metrics

| Performance Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Delta | Percentage Change | Advantage |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Execution Time** | 10.0005 s | 10.0004 s | +0.0001 s | — | — |
| **Total Events** | 15,877 | 14,410 | +1,467 | +10.18% | **Proxmox VE** |
| **Events / sec** | 1,587.47 | 1,440.80 | +146.67 | +10.18% | **Proxmox VE** |
| **Min Latency (ms)** | 0.59 | 0.65 | -0.06 | -9.23% | **Proxmox VE** |
| **Avg Latency (ms)** | 0.63 | 0.69 | -0.06 | -8.70% | **Proxmox VE** |
| **95th Percentile (ms)** | 0.65 | 0.90 | -0.25 | -27.78% | **Proxmox VE** |
| **Max Latency (ms)** | 1.34 | 1.89 | -0.55 | -29.10% | **Proxmox VE** |

---

## 2. Resource Specifications Summary

| Resource Parameter | Proxmox VE (Type-1) | VMware Workstation (Type-2) |
| :--- | :--- | :--- |
| **Hypervisor Type** | Bare-Metal | Hosted |
| **Guest Operating System** | Ubuntu 22.04.5 LTS (x86_64) | Ubuntu 22.04.5 LTS (x86_64) |
| **Virtual CPU (vCPU)** | 2 vCPU (1 socket, 2 cores) | 2 vCPU (1 processor, 2 cores) |
| **CPU Model** | QEMU Virtual CPU 2.5+ | 13th Gen Intel Core i5-13450HX |
| **Memory Allocation** | 2048 MiB (2.0 GB) | 2048 MB (~2.0 GB) |
| **Virtual Storage** | 20 GB Virtual Disk | 20 GB Virtual Disk |
| **Network Mode** | Linux Bridge (`vmbr0`) | NAT (`VMnet8`) |
| **Virtualization Mode** | KVM / Full Virtualization | VMware / Full Virtualization |

---

## 3. Mathematical Calculations

1. **Throughput Delta ($\Delta\text{EPS}$):**
   $$\Delta\text{EPS} = 1587.47 - 1440.80 = +146.67\text{ events/sec}$$
   $$\text{Percentage Improvement} = \left(\frac{1587.47 - 1440.80}{1440.80}\right) \times 100\% = +10.18\%$$

2. **Average Latency Delta:**
   $$\Delta\text{Latency} = 0.69\text{ ms} - 0.63\text{ ms} = 0.06\text{ ms}$$
   $$\text{Reduction} = \left(\frac{0.69 - 0.63}{0.69}\right) \times 100\% = 8.70\%$$

3. **95th Percentile Latency Reduction:**
   $$\text{Tail Latency Reduction} = \left(\frac{0.90 - 0.65}{0.90}\right) \times 100\% = 27.78\%$$

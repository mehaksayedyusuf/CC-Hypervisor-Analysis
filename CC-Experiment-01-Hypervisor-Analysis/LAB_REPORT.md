# Academic Laboratory Report
## Performance Analysis of Type-1 and Type-2 Hypervisors

**Course:** Cloud Computing Laboratory  
**Experiment Number:** 01  
**Study Title:** Empirical Performance Benchmarking of Bare-Metal (Proxmox VE) and Hosted (VMware Workstation) Hypervisors  

---

### Student Identification

| Attribute | Value |
| :--- | :--- |
| **Name** | Mehak Sayed Yusuf |
| **USN** | 01FE24BCI012 |
| **Division** | B |
| **Roll Number** | 202 |

---

## 1. Experiment Aim & Objectives

The primary aim of this experiment is to evaluate and compare the CPU compute performance, execution throughput, and latency characteristics of two fundamental hypervisor architectures:
1. **Type-1 (Bare-Metal) Hypervisor:** Proxmox Virtual Environment (PVE) backed by KVM.
2. **Type-2 (Hosted) Hypervisor:** VMware Workstation running over a desktop host operating system.

### Key Objectives:
- Provision identical Ubuntu 22.04 LTS guest virtual machines across both virtualization platforms.
- Verify hardware configuration, resource allocations, and host/guest status using standard Linux diagnostics.
- Execute standardized Sysbench prime computation tests (`--cpu-max-prime=20000 run`).
- Measure, compute, and contrast throughput (events per second) and latency statistics.
- Analyze the underlying architectural trade-offs between direct hardware execution and host-mediated virtualization.

---

## 2. Theoretical Background

### 2.1 Type-1 Virtualization Architecture (Bare-Metal)
In Type-1 hypervisors, the hypervisor software is installed directly onto bare-metal physical hardware, functioning as the operating platform.
- **Implementation:** Proxmox VE utilizes the Linux Kernel-based Virtual Machine (KVM) module.
- **Hardware Interaction:** Virtual machines utilize processor hardware virtualization extensions (Intel VT-x / AMD-V) to execute guest code in VMX non-root mode.
- **Resource Dispatch:** Virtual CPUs (vCPUs) map directly to host kernel POSIX threads, scheduled via the Completely Fair Scheduler (CFS) without user-space host intervention.

### 2.2 Type-2 Virtualization Architecture (Hosted)
In Type-2 hypervisors, the hypervisor operates as a user-level application on top of a general-purpose host operating system (e.g., Windows 11).
- **Implementation:** VMware Workstation Pro.
- **Hardware Interaction:** The hypervisor interfaces with the host OS kernel and device drivers to request resources.
- **Resource Dispatch:** Virtual machine operations require context switching between the guest OS, the hypervisor virtual machine monitor (VMM), and the host OS kernel. This additional translation layer introduces compute latency and scheduling contention.

---

## 3. Testbed Specifications & Experimental Parameters

Both guest virtual machines were provisioned with matched resource parameters to guarantee valid comparative results:

| Parameter | Proxmox VE (Type-1) | VMware Workstation (Type-2) |
| :--- | :--- | :--- |
| **Guest Operating System** | Ubuntu 22.04.5 LTS (x86_64) | Ubuntu 22.04.5 LTS (x86_64) |
| **Virtual CPU Count** | 2 vCPUs (1 socket, 2 cores) | 2 vCPUs (1 processor, 2 cores) |
| **Exposed CPU Model** | QEMU Virtual CPU version 2.5+ | 13th Gen Intel Core i5-13450HX |
| **Allocated System RAM** | 2048 MiB (2 GB) | 2048 MB (~2 GB) |
| **Virtual Disk Allocation** | 20 GB | 20 GB |
| **Network Interface Mode** | Bridged (`vmbr0`) | NAT (`VMnet8`) |
| **Virtualization Mode** | KVM / Full Virtualization | VMware / Full Virtualization |

---

## 4. Experimental Procedure

### 4.1 Type-1 Hypervisor Setup (Proxmox VE)
1. Sign in to the Proxmox VE web management dashboard.
2. Create a new virtual machine (`VM 109: vm01-type01`) with 2 vCPUs, 2048 MiB RAM, and a 20 GB virtual disk.
3. Attach the Ubuntu 22.04.5 LTS ISO to the virtual optical drive and configure network bridging via `vmbr0`.
4. Power on the VM, complete the OS installation, reboot, and log in.
5. Inspect and verify allocated resources:
   ```bash
   hostnamectl
   lscpu
   free -h
   df -h
   top
   ```
6. Install and execute the Sysbench CPU benchmark:
   ```bash
   sudo apt update && sudo apt install sysbench -y
   sysbench --version
   sysbench cpu --cpu-max-prime=20000 run
   ```
7. Review host-level telemetry graphs on the Proxmox dashboard and shut down the machine cleanly using `sudo poweroff`.

### 4.2 Type-2 Hypervisor Setup (VMware Workstation)
1. Launch VMware Workstation on the host system.
2. Select **Create a New Virtual Machine** with the *Typical* wizard.
3. Specify the Ubuntu 22.04.5 LTS ISO image, set VM storage to 20 GB, and allocate 2 vCPUs and 2 GB RAM.
4. Set the network adapter mode to NAT.
5. Power on the virtual machine, complete installation, and verify system metrics (`hostnamectl`, `lscpu`, `free -h`, `df -h`, `top`).
6. Install Sysbench:
   ```bash
   sudo apt update && sudo apt install sysbench -y
   sysbench --version
   ```
7. Execute the benchmark:
   ```bash
   sysbench cpu --cpu-max-prime=20000 run
   ```
8. Record the benchmark metrics and cleanly power off the VM.

---

## 5. Recorded Benchmark Outputs

### 5.1 Proxmox VE Benchmark Terminal Output
```text
Running the test with following options:
Number of threads: 1
Initializing random number generator from current time

Prime numbers limit: 20000
Initializing worker threads...
Threads started!

CPU speed:
    events per second:  1587.47

General statistics:
    total time:                          10.0005s
    total number of events:              15877

Latency (ms):
         min:                                    0.59
         avg:                                    0.63
         max:                                    1.34
         95th percentile:                        0.65
         sum:                                 9996.82

Threads fairness:
    events (avg/stddev):           15877.0000/0.00
    execution time (avg/stddev):   9.9968/0.00
```

### 5.2 VMware Workstation Benchmark Terminal Output
```text
Running the test with following options:
Number of threads: 1
Initializing random number generator from current time

Prime numbers limit: 20000
Initializing worker threads...
Threads started!

CPU speed:
    events per second:  1440.80

General statistics:
    total time:                          10.0004s
    total number of events:              14410

Latency (ms):
         min:                                    0.65
         avg:                                    0.69
         max:                                    1.89
         95th percentile:                        0.90
         sum:                                 9994.20

Threads fairness:
    events (avg/stddev):           14410.0000/0.00
    execution time (avg/stddev):   9.9942/0.00
```

---

## 6. Quantitative Analysis & Comparison

| Parameter | Proxmox VE (Type-1) | VMware Workstation (Type-2) | Difference | Analysis |
| :--- | :---: | :---: | :---: | :--- |
| **Total Benchmark Time** | 10.0005 s | 10.0004 s | 0.0001 s | Standard test window |
| **Total Events Processed** | **15,877** | 14,410 | **+1,467 events** | Proxmox VE processed +10.18% more cycles |
| **Throughput (EPS)** | **1,587.47** | 1,440.80 | **+146.67 eps** | Proxmox VE is **10.18% faster** |
| **Minimum Latency** | **0.59 ms** | 0.65 ms | -0.06 ms | 9.23% lower latency on Type-1 |
| **Mean / Average Latency** | **0.63 ms** | 0.69 ms | -0.06 ms | 8.70% lower latency on Type-1 |
| **95th Percentile Latency**| **0.65 ms** | 0.90 ms | -0.25 ms | **27.78% tighter tail consistency** |
| **Peak / Maximum Latency** | **1.34 ms** | 1.89 ms | -0.55 ms | **29.10% lower peak latency spikes** |

### Mathematical Calculations

1. **Throughput Delta ($\Delta \text{EPS}$):**
   $$\Delta \text{EPS} = 1587.47 - 1440.80 = +146.67\text{ events/sec}$$
   $$\text{Improvement} = \left(\frac{1587.47 - 1440.80}{1440.80}\right) \times 100\% = +10.18\%$$

2. **Average Latency Reduction ($\Delta \text{Latency}$):**
   $$\Delta \text{Latency} = 0.69\text{ ms} - 0.63\text{ ms} = 0.06\text{ ms}$$
   $$\text{Reduction} = \left(\frac{0.69 - 0.63}{0.69}\right) \times 100\% = 8.70\%$$

3. **Tail Latency Improvement (95th Percentile):**
   $$\text{Tail Reduction} = \left(\frac{0.90 - 0.65}{0.90}\right) \times 100\% = 27.78\%$$

---

## 7. Visual Data Representations

### Figure 1: Events Per Second Comparison
![Throughput](images/events_per_second_comparison.png)

### Figure 2: Latency Distribution Profile
![Latency](images/latency_comparison.png)

### Figure 3: Total Events Processed
![Total Events](images/total_events_comparison.png)

### Figure 4: Multi-Metric Evaluation Dashboard
![Dashboard](images/overall_performance_dashboard.png)

---

## 8. Technical Discussion

The quantitative observations demonstrate a distinct performance advantage for Type-1 virtualization in computational workloads:

1. **Hardware-Assisted Direct Execution:**  
   Proxmox VE runs on bare-metal hardware. Guest CPU instructions execute directly through processor VMX root/non-root modes. In contrast, VMware Workstation must mediate instructions through the host operating system, causing context-switching delays.
2. **Scheduling Contention & Tail Latency:**  
   The 95th percentile latency of VMware Workstation (0.90 ms) is significantly higher than that of Proxmox VE (0.65 ms). This divergence stems from the Windows host OS scheduler periodically preempting the hypervisor process to service background system threads.
3. **Memory Address Translation:**  
   Proxmox VE benefits from direct nested page table (EPT) translation without host OS virtual memory management intervention, lowering overall memory access latency.

---

## 9. Conclusion

1. The experiment verified that **Type-1 hypervisors (Proxmox VE)** provide superior compute throughput (+10.18%) and lower average latency (8.70% reduction) compared to **Type-2 hypervisors (VMware Workstation)** under matched hardware configurations.
2. Type-1 hypervisors exhibit significantly lower latency variability and fewer peak spikes (1.34 ms vs 1.89 ms), making them indispensable for production cloud environments and mission-critical enterprise workloads.
3. Type-2 hypervisors remain highly valuable for rapid software testing, desktop sandboxing, and educational use cases where host desktop integration and ease of deployment are prioritized.

---

**Student Name:** Mehak Sayed Yusuf  
**USN:** 01FE24BCI012 | **Division:** B | **Roll No:** 202  
**Date:** September 24, 2026  

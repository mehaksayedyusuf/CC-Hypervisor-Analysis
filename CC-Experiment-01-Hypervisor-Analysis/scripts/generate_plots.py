import matplotlib.pyplot as plt
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath(os.path.join(script_dir, '..', 'screenshots', 'comparison'))
os.makedirs(output_dir, exist_ok=True)

# Styling configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig_dpi = 300

# Distinct refined color palette
c_type1 = '#1d4ed8'  # Deep Blue (Proxmox VE)
c_type2 = '#d97706'  # Amber / Warm Bronze (VMware Workstation)

hypervisors = ['Proxmox VE\n(Type-1 Bare-Metal)', 'VMware Workstation\n(Type-2 Hosted)']
eps_values = [1587.47, 1440.80]
events_values = [15877, 14410]
metrics = ['Minimum Latency', 'Average Latency', '95th Percentile', 'Maximum Latency']
proxmox_lat = [0.59, 0.63, 0.65, 1.34]
vmware_lat = [0.65, 0.69, 0.90, 1.89]

pct_eps_diff = ((1587.47 - 1440.80) / 1440.80) * 100
diff_events = 15877 - 14410

# -------------------------------------------------------------------------
# Chart 1: CPU Processing Throughput (Events per Second)
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=fig_dpi)
bars = ax.bar(hypervisors, eps_values, color=[c_type1, c_type2], width=0.42, edgecolor='#1e293b', linewidth=1.1)

ax.set_ylabel('Events per Second (Throughput)', fontsize=11, fontweight='600')
ax.set_title('CPU Benchmark Throughput (Sysbench Prime Computation)', fontsize=13, fontweight='bold', pad=14)
ax.set_ylim(0, 1950)

for bar in bars:
    h = bar.get_height()
    ax.annotate(f'{h:,.2f} EPS',
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 6),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=10.5, fontweight='bold')

ax.text(0.5, 0.86, f'Proxmox VE (Type-1) delivers +{pct_eps_diff:.2f}%\nhigher processing throughput', 
        transform=ax.transAxes, fontsize=11, fontweight='600', ha='center',
        bbox=dict(boxstyle="round,pad=0.55", facecolor='#eff6ff', edgecolor='#93c5fd', alpha=0.95))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'events_per_second_comparison.png'))
plt.close()

# -------------------------------------------------------------------------
# Chart 2: Latency Distribution Profile
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.5, 5.5), dpi=fig_dpi)
x = np.arange(len(metrics))
width = 0.32

rects1 = ax.bar(x - width/2, proxmox_lat, width, label='Proxmox VE (Type-1)', color=c_type1, edgecolor='#1e293b', linewidth=1)
rects2 = ax.bar(x + width/2, vmware_lat, width, label='VMware Workstation (Type-2)', color=c_type2, edgecolor='#1e293b', linewidth=1)

ax.set_ylabel('Latency (milliseconds)', fontsize=11, fontweight='600')
ax.set_title('Sysbench CPU Latency Profile (Lower is Better)', fontsize=13, fontweight='bold', pad=14)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=10.5, fontweight='600')
ax.legend(fontsize=10.5, loc='upper left', frameon=True)
ax.set_ylim(0, 2.4)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.2f} ms', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 4),
                textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='600', color='#1e3a8a')

for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.2f} ms', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 4),
                textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='600', color='#7c2d12')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'latency_comparison.png'))
plt.close()

# -------------------------------------------------------------------------
# Chart 3: Total Computation Events
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=fig_dpi)
bars = ax.bar(hypervisors, events_values, color=[c_type1, c_type2], width=0.42, edgecolor='#1e293b', linewidth=1.1)

ax.set_ylabel('Total Events Executed (10s Window)', fontsize=11, fontweight='600')
ax.set_title('Total Computational Workload Executed', fontsize=13, fontweight='bold', pad=14)
ax.set_ylim(0, 19000)

for bar in bars:
    h = bar.get_height()
    ax.annotate(f'{h:,} events',
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 6),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=10.5, fontweight='bold')

ax.text(0.5, 0.86, f'Proxmox VE completed +{diff_events:,} more events\n({pct_eps_diff:.2f}% additional compute capacity)', 
        transform=ax.transAxes, fontsize=11, fontweight='600', ha='center',
        bbox=dict(boxstyle="round,pad=0.55", facecolor='#eff6ff', edgecolor='#93c5fd', alpha=0.95))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'total_events_comparison.png'))
plt.close()

# -------------------------------------------------------------------------
# Chart 4: Multi-Metric Performance Overview
# -------------------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(13, 9.5), dpi=fig_dpi)
fig.suptitle('Comparative Hypervisor Performance: Proxmox VE vs VMware Workstation', 
             fontsize=15, fontweight='bold', y=0.98)

# Panel 1: Throughput
axs[0, 0].bar(hypervisors, eps_values, color=[c_type1, c_type2], width=0.38, edgecolor='#1e293b')
axs[0, 0].set_title('Throughput (EPS) - Higher is Better', fontsize=11.5, fontweight='bold')
axs[0, 0].set_ylabel('EPS', fontsize=10)
for bar in axs[0, 0].patches:
    axs[0, 0].annotate(f'{bar.get_height():,.2f}', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9.5)

# Panel 2: Total Events
axs[0, 1].bar(hypervisors, events_values, color=[c_type1, c_type2], width=0.38, edgecolor='#1e293b')
axs[0, 1].set_title('Total Events (10s) - Higher is Better', fontsize=11.5, fontweight='bold')
axs[0, 1].set_ylabel('Events Count', fontsize=10)
for bar in axs[0, 1].patches:
    axs[0, 1].annotate(f'{int(bar.get_height()):,}', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9.5)

# Panel 3: Mean Latency
avg_lats = [0.63, 0.69]
axs[1, 0].bar(hypervisors, avg_lats, color=[c_type1, c_type2], width=0.38, edgecolor='#1e293b')
axs[1, 0].set_title('Average Latency - Lower is Better', fontsize=11.5, fontweight='bold')
axs[1, 0].set_ylabel('ms', fontsize=10)
axs[1, 0].set_ylim(0, 0.95)
for bar in axs[1, 0].patches:
    axs[1, 0].annotate(f'{bar.get_height():.2f} ms', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9.5)

# Panel 4: 95th Percentile Latency
p95_lats = [0.65, 0.90]
axs[1, 1].bar(hypervisors, p95_lats, color=[c_type1, c_type2], width=0.38, edgecolor='#1e293b')
axs[1, 1].set_title('95th Percentile Latency - Lower is Better', fontsize=11.5, fontweight='bold')
axs[1, 1].set_ylabel('ms', fontsize=10)
axs[1, 1].set_ylim(0, 1.2)
for bar in axs[1, 1].patches:
    axs[1, 1].annotate(f'{bar.get_height():.2f} ms', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold', fontsize=9.5)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(output_dir, 'overall_performance_dashboard.png'))
plt.close()

print('Refined plots saved directly to screenshots/comparison/')

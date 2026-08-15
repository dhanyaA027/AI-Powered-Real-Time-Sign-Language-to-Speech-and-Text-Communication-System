
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# Pipeline definition: (stage title, owner, data handed to the NEXT stage)
# ---------------------------------------------------------------------------

STAGES = [
    ("Webcam Feed", "Hardware", "raw BGR frame"),
    ("Image Preprocessing\n(OpenCV: clean / resize / normalize)", "Ananya HA", "cleaned frame"),
    ("Hand Detection & Landmark Tracking\n(MediaPipe: 21 landmarks/hand)", "Dhanya Shree A", "landmark coords"),
    ("Sign-Logic Engine\n(smoothing, confidence gating, debounce)", "S. V. Nayana", "sign + confidence"),
    ("Gesture-to-Text Integration\n(sign stream -> text/sentence)", "S. V. Nayana", "text/sentence"),
    ("Text-to-Speech (TTS)", "Vidhya Shree R", "audio waveform"),
    ("AI Avatar + Lip-Sync", "Vidhya Shree R", "lip-synced frames"),
    ("GUI Dashboard\n(PyQt5 / Tkinter, live display + alerts)", "All Members", None),
]

OWNER_COLORS = {
    "Hardware":       "#5C6B73",
    "Ananya HA":      "#8E8E93",
    "Dhanya Shree A": "#8E8E93",
    "S. V. Nayana":   "#2E86AB",
    "Vidhya Shree R": "#8E8E93",
    "All Members":    "#4C9A6A",
}
NAYANA_HIGHLIGHT = "#2E86AB"
ARROW_COLOR = "#3A3A3A"
BG_COLOR = "#F7F8FA"


def build_diagram(output_path: str) -> None:
    n = len(STAGES)
    box_w, box_h = 5.4, 1.15
    gap = 0.75
    total_h = n * (box_h + gap) - gap

    fig_w, fig_h = 9.5, total_h * 0.62 + 2.2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.axis("off")

    x0 = 1.4
    y = total_h
    centers = []

    for i, (title, owner, data_label) in enumerate(STAGES):
        color = OWNER_COLORS.get(owner, "#8E8E93")
        is_nayana = owner == "S. V. Nayana"

        shadow = FancyBboxPatch(
            (x0 + 0.07, y - 0.07), box_w, box_h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=0, facecolor="black", alpha=0.12, zorder=1,
        )
        ax.add_patch(shadow)

        edge_color = "#1B4F72" if is_nayana else "#4A4A4A"
        box = FancyBboxPatch(
            (x0, y), box_w, box_h,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            linewidth=2.4 if is_nayana else 1.2,
            edgecolor=edge_color, facecolor=color, alpha=0.95, zorder=2,
        )
        ax.add_patch(box)

        badge_r = 0.22
        badge_cx, badge_cy = x0 - 0.05, y + box_h - 0.05
        ax.add_patch(patches.Circle((badge_cx, badge_cy), badge_r,
                                     facecolor="white", edgecolor=edge_color,
                                     linewidth=1.5, zorder=3))
        ax.text(badge_cx, badge_cy, str(i + 1), ha="center", va="center",
                fontsize=10, fontweight="bold", color=edge_color, zorder=4)

        ax.text(x0 + box_w / 2, y + box_h * 0.62, title, ha="center", va="center",
                fontsize=9.3, fontweight="bold", color="white", zorder=4,
                linespacing=1.4)
        ax.text(x0 + box_w / 2, y + box_h * 0.20, f"Owner: {owner}", ha="center",
                va="center", fontsize=8.2, color="white", alpha=0.95, zorder=4,
                style="italic")

        centers.append((x0 + box_w / 2, y, y + box_h))
        y -= (box_h + gap)

    for i in range(n - 1):
        cx_i, bottom_i, top_i = centers[i]
        cx_ip1, bottom_ip1, top_ip1 = centers[i + 1]

        arrow = FancyArrowPatch(
            (cx_i, bottom_i - 0.03), (cx_ip1, top_ip1 + 0.03),
            arrowstyle="-|>", mutation_scale=16, linewidth=1.8,
            color=ARROW_COLOR, zorder=2,
        )
        ax.add_patch(arrow)

        data_label = STAGES[i][2]
        if data_label:
            mid_y = (bottom_i + top_ip1) / 2
            ax.text(cx_i + box_w / 2 + 0.15, mid_y, data_label,
                    ha="left", va="center", fontsize=7.6, color="#2A2A2A",
                    style="italic",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                              edgecolor="#CCCCCC", linewidth=0.6, alpha=0.9))

    ax.text(x0 + box_w / 2, total_h + box_h + 0.55,
            "System Architecture", ha="center", va="bottom",
            fontsize=16, fontweight="bold", color="#1B1B1B")
    ax.text(x0 + box_w / 2, total_h + box_h + 0.20,
            "AI-Powered Real-Time Sign Language to Speech & Text Communication System",
            ha="center", va="bottom", fontsize=9.5, color="#555555")

    legend_elements = [
        Line2D([0], [0], marker='s', color='w', label='S. V. Nayana (this package)',
               markerfacecolor=NAYANA_HIGHLIGHT, markersize=14),
        Line2D([0], [0], marker='s', color='w', label='Other individual owners',
               markerfacecolor="#8E8E93", markersize=14),
        Line2D([0], [0], marker='s', color='w', label='Joint deliverable (All Members)',
               markerfacecolor="#4C9A6A", markersize=14),
        Line2D([0], [0], marker='s', color='w', label='Hardware / input',
               markerfacecolor="#5C6B73", markersize=14),
    ]
    y_top = total_h + box_h + 1.1
    y_bottom = centers[-1][1] - 1.15
    ax.set_xlim(0, x0 * 2 + box_w + 2.6)
    ax.set_ylim(y_bottom, y_top)

    legend = ax.legend(handles=legend_elements, loc="lower center",
                        bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False,
                        fontsize=8.3, handletextpad=0.6, columnspacing=1.2)
    for text in legend.get_texts():
        text.set_color("#333333")
    fig.tight_layout()
    fig.savefig(output_path, dpi=220, facecolor=BG_COLOR)
    print(f"Diagram saved to {output_path}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    build_diagram(os.path.join(out_dir, "system_architecture_diagram.png"))
import os

from bertopic import BERTopic


# ==================================================
# Configuration
# ==================================================

MODEL_PATH = "models/topic_model"

RESULTS_PATH = "results/topic_info.csv"

VISUALIZATION_PATH = "visualizations"


# ==================================================
# Create visualization directory
# ==================================================

os.makedirs(
    VISUALIZATION_PATH,
    exist_ok=True
)


# ==================================================
# Load trained BERTopic model
# ==================================================

print("Loading BERTopic model...")

topic_model = BERTopic.load(
    MODEL_PATH
)

print("BERTopic model loaded successfully.")


# ==================================================
# Get topic information
# ==================================================

print("\nGetting topic information...")

topic_info = topic_model.get_topic_info()

print(
    f"Total topic entries: "
    f"{len(topic_info)}"
)


# ==================================================
# Save topic information
# ==================================================

print("\nSaving topic information...")

topic_info.to_csv(
    RESULTS_PATH,
    index=False
)

print(
    f"Topic information saved to: "
    f"{RESULTS_PATH}"
)


# ==================================================
# Visualization 1
# Topic Overview
# ==================================================

print("\nCreating topic overview...")

fig = topic_model.visualize_topics()

topic_overview_path = os.path.join(
    VISUALIZATION_PATH,
    "topic_visualization.html"
)

fig.write_html(
    topic_overview_path
)

print(
    f"Saved: {topic_overview_path}"
)


# ==================================================
# Visualization 2
# Topic Bar Chart
# ==================================================

print("\nCreating topic bar chart...")

fig = topic_model.visualize_barchart(
    top_n_topics=20,
    n_words=8
)

topic_barchart_path = os.path.join(
    VISUALIZATION_PATH,
    "topic_barchart.html"
)

fig.write_html(
    topic_barchart_path
)

print(
    f"Saved: {topic_barchart_path}"
)


# ==================================================
# Visualization 3
# Topic Hierarchy
# ==================================================

print("\nCreating topic hierarchy...")

fig = topic_model.visualize_hierarchy()

topic_hierarchy_path = os.path.join(
    VISUALIZATION_PATH,
    "topic_hierarchy.html"
)

fig.write_html(
    topic_hierarchy_path
)

print(
    f"Saved: {topic_hierarchy_path}"
)


# ==================================================
# Final summary
# ==================================================

print("\n===================================")
print("VISUALIZATION COMPLETE")
print("===================================")

print("\nCreated files:")

print(
    "1. visualizations/topic_visualization.html"
)

print(
    "2. visualizations/topic_barchart.html"
)

print(
    "3. visualizations/topic_hierarchy.html"
)

print("\nStep 3 completed successfully.")
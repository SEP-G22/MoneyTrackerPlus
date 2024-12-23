"""
test file testing get_category.py and TrasactionCategory class

Get all the predefined categories and show their icons.
"""

from utils import get_categories
import matplotlib.pyplot as plt
from matplotlib.image import imread
import os

if __name__ == '__main__':
    gc = get_categories.getCategories()
    categories = gc.setUp()  # list[TrasactionCategory]

    # Calculate the number of rows and columns for the subplot grid
    num_categories = len(categories)
    num_cols = 5  # You can adjust this value to change the number of columns
    num_rows = (num_categories + num_cols - 1) // num_cols

    # Create a figure with subplots
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 3 * num_rows))
    fig.suptitle("Category Icons", fontsize=16)

    # Flatten the axes array for easier indexing
    axes = axes.flatten()

    for i, category in enumerate(categories):
        print(category.category)

        # Load and display the image
        icon_path = os.path.join(f'images/{category.category}.png')
        if os.path.exists(icon_path):
            img = imread(icon_path)
            axes[i].imshow(img)
            axes[i].axis('off')
            axes[i].set_title(category.category)
        else:
            axes[i].text(0.5, 0.5, f"No icon for\n{category.category}", ha='center', va='center')
            axes[i].axis('off')

    # Remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
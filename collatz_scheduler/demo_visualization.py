"""
Kaitian - Collatz Convergence Visualization
Version 0.1.0

Visualizes the convergence path of the Collatz scheduler.
Generates a plot showing how task complexity shrinks/expands until reaching 1.
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for script execution

from scheduler import CollatzScheduler


def visualize_convergence(
    complexities: list[int],
    title: str = "Collatz Convergence Paths",
    save_path: str = "collatz_convergence.png"
):
    """
    Generate a convergence visualization for multiple starting complexities.
    
    Args:
        complexities: List of starting complexity values to simulate.
        title: Plot title.
        save_path: Output file path.
    """
    fig, axes = plt.subplots(
        len(complexities), 1,
        figsize=(10, 2.5 * len(complexities)),
        squeeze=False
    )

    for idx, start_complexity in enumerate(complexities):
        ax = axes[idx][0]

        # Simulate pure Collatz sequence
        n = start_complexity
        path = [n]
        while n != 1 and len(path) < 1000:
            if n % 2 == 0:
                n = n // 2
            else:
                n = n * 3 + 1
            path.append(n)

        steps = range(len(path))
        ax.plot(steps, path, 'b-o', markersize=4, linewidth=1.5, label=f'Start: {start_complexity}')
        ax.axhline(y=1, color='green', linestyle='--', alpha=0.5, label='Convergence (1)')
        ax.set_ylabel('Complexity')
        ax.set_xlabel('Step')
        ax.set_title(f'Start = {start_complexity} → Converged in {len(path)-1} steps')
        ax.legend()
        ax.grid(True, alpha=0.3)

    fig.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Visualization saved to: {save_path}")


def demo_with_scheduler():
    """
    Full demo: use the actual CollatzScheduler with mock tasks,
    then visualize the convergence paths.
    """
    scheduler = CollatzScheduler()

    tasks = [
        ("Parse Ruby project", 120),
        ("Validate AST nodes", 75),
        ("Generate Python code", 180),
    ]
    scheduler.decompose(tasks)

    import random
    random.seed(123)

    def executor(description: str, complexity: int) -> bool:
        prob = max(0.1, 1.0 - complexity / 400)
        return random.random() < prob

    results = scheduler.run(executor)

    # Collect convergence paths
    for subtask in results:
        path = scheduler.get_convergence_path(subtask.id)
        # Add starting complexity at the beginning
        start_map = {0: 120, 1: 75, 2: 180}
        full_path = [start_map[subtask.id]] + path
        print(f"Subtask '{subtask.description}': {full_path} "
              f"→ Status: {subtask.status.value}")


if __name__ == "__main__":
    # Pure Collatz math demo — no task semantics, just numbers
    visualize_convergence(
        complexities=[27, 100, 500, 1000, 5000],
        title="Collatz Convergence - Pure Mathematical Paths",
        save_path="collatz_convergence.png"
    )
    print("\n" + "=" * 40)
    demo_with_scheduler()

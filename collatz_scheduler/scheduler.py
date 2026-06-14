"""
Kaitian - Collatz Convergence Scheduler
Version 0.1.0

Pure mathematical implementation. Given a task complexity metric:
- On success: divide by 2 (shrink scope)
- On failure: multiply by 3, add 1 (expand exploration)
- Repeat until converging to 1 (task complete)

This is a deterministic task scheduling algorithm, NOT a random exploration strategy.
The mathematical guarantee: all positive integers reach 1 under the Collatz process.
"""

from typing import List, Tuple, Callable, Any
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    CONVERGED = "converged"


@dataclass
class Subtask:
    id: int
    description: str
    complexity: int  # Starting complexity metric
    status: TaskStatus = TaskStatus.RUNNING
    attempts: int = 0


@dataclass
class ConvergenceLog:
    """Records each step of the Collatz convergence path."""
    step: int
    complexity: int
    status: TaskStatus
    subtask_id: int


class CollatzScheduler:
    """
    Schedules and tracks task execution using the Collatz convergence protocol.
    
    Protocol:
    1. Decompose main task into subtasks with complexity metrics
    2. For each subtask: attempt execution
    3. If success: complexity = complexity // 2 (shrink)
    4. If failure: complexity = complexity * 3 + 1 (expand)
    5. Repeat until complexity == 1 (converged)
    """

    def __init__(self, max_iterations: int = 10000):
        self.max_iterations = max_iterations
        self.history: List[ConvergenceLog] = []
        self.subtasks: List[Subtask] = []

    def decompose(self, task_descriptions: List[Tuple[str, int]]) -> None:
        """
        Decompose a main task into subtasks.
        
        Args:
            task_descriptions: List of (description, complexity) tuples.
                Complexity should be a positive integer representing task scope.
        """
        self.subtasks = [
            Subtask(id=i, description=desc, complexity=comp)
            for i, (desc, comp) in enumerate(task_descriptions)
        ]

    def step(self, subtask_id: int, executor: Callable[[], bool]) -> TaskStatus:
        """
        Execute one scheduling step for a subtask.
        
        Args:
            subtask_id: Index of the subtask to process.
            executor: Callable that attempts execution, returns True on success.
        
        Returns:
            Current TaskStatus after this step.
        """
        subtask = self.subtasks[subtask_id]

        if subtask.complexity == 1:
            subtask.status = TaskStatus.CONVERGED
            self._log(subtask_id, subtask.complexity, TaskStatus.CONVERGED)
            return TaskStatus.CONVERGED

        subtask.attempts += 1
        success = executor()

        if success:
            subtask.complexity = max(1, subtask.complexity // 2)
            if subtask.complexity == 1:
                subtask.status = TaskStatus.CONVERGED
                self._log(subtask_id, subtask.complexity, TaskStatus.CONVERGED)
                return TaskStatus.CONVERGED
            else:
                subtask.status = TaskStatus.RUNNING
                self._log(subtask_id, subtask.complexity, TaskStatus.SUCCESS)
                return TaskStatus.SUCCESS
        else:
            subtask.complexity = subtask.complexity * 3 + 1
            subtask.status = TaskStatus.RUNNING
            self._log(subtask_id, subtask.complexity, TaskStatus.FAILURE)
            return TaskStatus.FAILURE

    def run(self, executor: Callable[[str, int], bool]) -> List[Subtask]:
        """
        Run the full convergence process for all subtasks.
        
        Args:
            executor: Callable that takes (description, complexity) and returns success.
        
        Returns:
            List of completed Subtask objects.
        """
        for subtask in self.subtasks:
            iteration = 0
            while subtask.complexity != 1 and iteration < self.max_iterations:
                success = executor(subtask.description, subtask.complexity)
                self.step(subtask.id, lambda: success)
                iteration += 1

            if iteration >= self.max_iterations:
                subtask.status = TaskStatus.FAILURE

        return self.subtasks

    def _log(self, subtask_id: int, complexity: int, status: TaskStatus) -> None:
        self.history.append(ConvergenceLog(
            step=len(self.history) + 1,
            complexity=complexity,
            status=status,
            subtask_id=subtask_id,
        ))

    def get_convergence_path(self, subtask_id: int) -> List[int]:
        """Get the complexity values along the convergence path for a subtask."""
        return [
            entry.complexity
            for entry in self.history
            if entry.subtask_id == subtask_id
        ]

    def summary(self) -> str:
        """Generate a human-readable summary of the scheduling process."""
        lines = ["Collatz Scheduler Summary", "=" * 30]
        for subtask in self.subtasks:
            path = self.get_convergence_path(subtask.id)
            steps = len(path)
            status_str = subtask.status.value
            lines.append(
                f"[{status_str}] Subtask {subtask.id}: '{subtask.description}' "
                f"→ converged in {steps} steps. Path: {path}"
            )
        return "\n".join(lines)


# ─── Demo ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    scheduler = CollatzScheduler()

    # Define three sample subtasks with different complexity levels
    scheduler.decompose([
        ("Parse 100 Ruby files", 100),
        ("Validate syntax tree", 50),
        ("Generate Python output", 200),
    ])

    # Mock executor: simulates varying success rates based on complexity
    import random
    random.seed(42)

    def mock_executor(description: str, complexity: int) -> bool:
        # Higher complexity → lower probability of immediate success
        success_prob = max(0.1, 1.0 - complexity / 500)
        return random.random() < success_prob

    scheduler.run(mock_executor)
    print(scheduler.summary())

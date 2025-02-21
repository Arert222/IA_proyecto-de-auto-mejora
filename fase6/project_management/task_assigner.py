from collections import defaultdict

class TaskAssigner:
    def __init__(self, team_skills: dict):
        self.team = team_skills
    
    def assign_tasks(self, tasks: list) -> dict:
        """Asigna tareas óptimamente"""
        assignments = defaultdict(list)
        for task in sorted(tasks, key=lambda x: x['complexity'], reverse=True):
            best_dev = min(self.team, key=lambda d: self.team[d]['workload'])
            assignments[best_dev].append(task)
            self.team[best_dev]['workload'] += task['complexity']
        return assignments
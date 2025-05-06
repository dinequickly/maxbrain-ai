class ResearchAgent:
    def __init__(self):
        self.research_data = {}
    
    def run(self):
        # Implementation for research phase
        print("Running research phase...")
        # Collect data, analyze information, etc.
        self.research_data = {"findings": "Sample research findings"}
    
    def review(self):
        # Review research results
        print("Reviewing research results...")
        return self.research_data

class DesignAgent:
    def __init__(self):
        self.design_specs = {}
    
    def run(self):
        # Implementation for design phase
        print("Running design phase...")
        # Create design specifications, mockups, etc.
        self.design_specs = {"specs": "Sample design specifications"}
    
    def review(self):
        # Review design results
        print("Reviewing design results...")
        return self.design_specs

class ExecutionAgent:
    def __init__(self):
        self.execution_results = {}
    
    def run(self):
        # Implementation for execution phase
        print("Running execution phase...")
        # Execute tasks, implement solutions, etc.
        self.execution_results = {"results": "Sample execution results"}
    
    def review(self):
        # Review execution results
        print("Reviewing execution results...")
        return self.execution_results

class ProjectAgent:
    def __init__(self, goal):
        self.goal = goal
        self.phases = {
            'research': ResearchAgent(),
            'design': DesignAgent(),
            'execute': ExecutionAgent()
        }
        self.results = {}

    def execute_chain(self):
        for phase_name, phase in self.phases.items():
            print(f"Starting {phase_name} phase...")
            phase.run()
            self.results[phase_name] = phase.review()
        
        return self.results
    
    def get_status(self):
        return {
            "goal": self.goal,
            "completed_phases": list(self.results.keys()),
            "pending_phases": [phase for phase in self.phases.keys() if phase not in self.results]
        }
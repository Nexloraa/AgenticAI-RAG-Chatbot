from crewai import Crew

from src.agents_src.agents.quest_ans_agent import qa_agent
from src.agents_src.tasks.quest_ans_task import qa_task


qa_crew = Crew(
    agents=[qa_agent],
    tasks=[qa_task],
    verbose=True,
)
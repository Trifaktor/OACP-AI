"""
Defines the three core agents used in the OACP investment workflow.

Each agent encapsulates a role-specific system prompt which provides
context, mandate and tone. These prompts live in the `prompts/`
directory so that they can be easily modified without touching code.

The `Agent` class comes from CrewAI and requires a role, goal,
backstory (i.e. the system prompt) and whether delegation to other
agents is allowed. See run_crew.py for usage.
"""

import os
from crewai import Agent

HERE = os.path.dirname(__file__)

# Load system prompts for each role
with open(os.path.join(HERE, 'prompts', 'athena.md'), encoding='utf-8') as f:
    ATHENA_SYS = f.read()
with open(os.path.join(HERE, 'prompts', 'baobab.md'), encoding='utf-8') as f:
    BAOBAB_SYS = f.read()
with open(os.path.join(HERE, 'prompts', 'imbokodo.md'), encoding='utf-8') as f:
    IMBOKODO_SYS = f.read()

# Define the agents
Athena = Agent(
    role='Investment Principal',
    goal='Produce IC-ready strategic outputs and exit scenarios.',
    backstory=ATHENA_SYS,
    allow_delegation=True,
)

Baobab = Agent(
    role='Investment Associate',
    goal='Turn research into diligence packs and monitoring updates.',
    backstory=BAOBAB_SYS,
    allow_delegation=True,
)

Imbokodo = Agent(
    role='Investment Analyst',
    goal='Generate research briefs, models, and ESG scorecards.',
    backstory=IMBOKODO_SYS,
    allow_delegation=False,
)